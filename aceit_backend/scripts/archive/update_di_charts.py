"""
Update Data Interpretation Charts Script

Regenerates all Data Interpretation question charts with:
- Precise probability distribution formatting
- Percentage labels on each data point
- Angle measurements for pie charts
- Clear axis labels with units
"""

import os
import sys
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from services.chart_generator import ChartGenerator, DIDataGenerator
from models.aptitude_sql import AptitudeQuestion

load_dotenv()

def update_di_charts():
    print("🎨 Starting Data Interpretation Chart Update...")
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("❌ DATABASE_URL not found!")
        return

    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Fetch all DI questions
        di_questions = session.query(AptitudeQuestion).filter(
            AptitudeQuestion.category == "Data Interpretation"
        ).all()
        
        total = len(di_questions)
        print(f"📊 Found {total} Data Interpretation questions to update.")
        
        updated_count = 0
        batch_size = 100
        
        for i, q in enumerate(di_questions):
            topic = q.topic
            
            # Generate new chart based on topic
            if topic == "Bar Graph":
                data = DIDataGenerator.generate_bar_question_data()
                new_url = data["chart_url"]
                
                # Update question text with new data if needed (optional)
                # For now, just update the chart URL
                
            elif topic == "Line Graph":
                data = DIDataGenerator.generate_line_question_data()
                new_url = data["chart_url"]
                
            elif topic == "Pie Chart":
                data = DIDataGenerator.generate_pie_question_data()
                new_url = data["chart_url"]
                
            else:
                print(f"⚠️ Unknown DI topic: {topic} for question {q.id}")
                continue
            
            # Update the image URL
            q.image_url = new_url
            updated_count += 1
            
            # Batch commit
            if (i + 1) % batch_size == 0:
                session.commit()
                progress = ((i + 1) / total) * 100
                print(f"   ✓ Updated {i + 1}/{total} ({progress:.1f}%)")
        
        # Final commit
        session.commit()
        print(f"\n✅ Successfully updated {updated_count} DI question charts!")
        
        # Show sample
        print("\n📷 Sample updated charts:")
        samples = session.query(AptitudeQuestion).filter(
            AptitudeQuestion.category == "Data Interpretation"
        ).limit(3).all()
        
        for s in samples:
            print(f"  Topic: {s.topic}")
            print(f"  URL: {s.image_url[:80]}...")
            print()
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()


if __name__ == "__main__":
    update_di_charts()
