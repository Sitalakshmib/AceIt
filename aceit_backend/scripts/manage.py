import argparse
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.aptitude_sql import AptitudeQuestion
from models.user_sql import User
from passlib.context import CryptContext

load_dotenv()

def get_session():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("❌ DATABASE_URL not found!")
        sys.exit(1)
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session(), engine

def check_connection(args):
    print("🔌 Checking Database Connection...")
    session, engine = get_session()
    try:
        session.execute(text("SELECT 1"))
        print("✅ Connection successful!")
        
        user_count = session.query(User).count()
        print(f"👥 Users found: {user_count}")
        
        q_count = session.query(AptitudeQuestion).count()
        print(f"📚 Questions found: {q_count}")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
    finally:
        session.close()

def count_questions(args):
    session, _ = get_session()
    try:
        query = session.query(AptitudeQuestion)
        
        if args.topic:
            query = query.filter(AptitudeQuestion.topic == args.topic)
            print(f"🔍 Filtering by Topic: {args.topic}")
        
        if args.category:
            query = query.filter(AptitudeQuestion.category == args.category)
            print(f"🔍 Filtering by Category: {args.category}")
            
        count = query.count()
        print(f"📊 Total Questions: {count}")
        
        # Breakdown
        if not args.topic and not args.category:
            print("\n--- Breakdown by Category ---")
            cats = session.query(AptitudeQuestion.category, text("count(*)")).group_by(AptitudeQuestion.category).all()
            for cat, c in cats:
                print(f"  {cat}: {c}")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        session.close()

def delete_questions(args):
    if not args.topic and not args.category:
        print("❌ You must specify --topic or --category to delete.")
        return

    confirm = input(f"⚠️  Are you sure you want to DELETE questions matching (Topic={args.topic}, Category={args.category})? [y/N] ")
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        return

    session, _ = get_session()
    try:
        # Build query to get IDs first for constraint handling
        query = session.query(AptitudeQuestion.id)
        if args.topic:
            query = query.filter(AptitudeQuestion.topic == args.topic)
        if args.category:
            query = query.filter(AptitudeQuestion.category == args.category)
            
        ids = [str(q[0]) for q in query.all()]
        count = len(ids)
        print(f"Targeting {count} questions for deletion...")
        
        if count > 0:
            # Delete dependent question_attempts
            if ids:
                ids_tuple = tuple(ids)
                if len(ids_tuple) == 1:
                     ids_tuple = f"('{ids_tuple[0]}')"
                else:
                     ids_tuple = str(ids_tuple)
                
                # Try deleting attempts
                try:
                    sql = text(f"DELETE FROM question_attempts WHERE question_id IN {ids_tuple}")
                    res = session.execute(sql)
                    print(f"🗑️  Deleted {res.rowcount} dependent user attempts.")
                except Exception as ex:
                    print(f"⚠️  Warning deleting attempts (might not exist): {ex}")
            
            # Delete questions
            q_del = session.query(AptitudeQuestion)
            if args.topic:
                q_del = q_del.filter(AptitudeQuestion.topic == args.topic)
            if args.category:
                q_del = q_del.filter(AptitudeQuestion.category == args.category)
                
            deleted = q_del.delete(synchronize_session=False)
            session.commit()
            print(f"✅ Successfully deleted {deleted} questions.")
        else:
            print("Nothing to delete.")

    except Exception as e:
        print(f"❌ Error during deletion: {e}")
        session.rollback()
    finally:
        session.close()

def reset_password(args):
    if not args.email or not args.password:
        print("❌ You must specify --email and --password.")
        return

    print(f"🔐 Resetting password for {args.email}...")
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    session, _ = get_session()
    try:
        user = session.query(User).filter(User.email == args.email).first()
        if user:
            # Bcrypt has a 72-byte limit
            if isinstance(args.password, str):
                if len(args.password.encode('utf-8')) > 72:
                    args.password = args.password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
            hashed = pwd_context.hash(args.password)
            user.password = hashed
            session.commit()
            print(f"✅ Password reset successfully for {args.email}")
        else:
            print(f"⚠️  User {args.email} not found.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        session.close()

def main():
    parser = argparse.ArgumentParser(description="AceIt Database Management Tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Check
    subparsers.add_parser("check", help="Check database connection")
    
    # Count
    count_parser = subparsers.add_parser("count", help="Count questions")
    count_parser.add_argument("--topic", help="Filter by topic")
    count_parser.add_argument("--category", help="Filter by category")
    
    # Delete
    del_parser = subparsers.add_parser("delete", help="Delete questions")
    del_parser.add_argument("--topic", help="Filter by topic")
    del_parser.add_argument("--category", help="Filter by category")

    # Reset Password
    reset_parser = subparsers.add_parser("reset-password", help="Reset user password")
    reset_parser.add_argument("--email", required=True, help="User email")
    reset_parser.add_argument("--password", required=True, help="New password")

    args = parser.parse_args()
    
    if args.command == "check":
        check_connection(args)
    elif args.command == "count":
        count_questions(args)
    elif args.command == "delete":
        delete_questions(args)
    elif args.command == "reset-password":
        reset_password(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
