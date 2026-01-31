
import sys
import os

# Add aceit_backend to path
sys.path.append(os.path.join(os.getcwd(), 'aceit_backend'))

print("Importing database...")
from database import progress_data

print(f"Initial progress_data id: {id(progress_data)}")
print(f"Initial len: {len(progress_data)}")

print("Importing analytics_service...")
from services.analytics_service import AnalyticsService

# Check if analytics service sees the same list
# (I need to inspect how it imports it. Since I modified it to import at func level or top level, let's see)

# Simulate adding data like the route does
print("Adding data to progress_data...")
progress_data.append({"module": "resume", "user_id": "test_user", "timestamp": "2023-01-01"})

print(f"Current len: {len(progress_data)}")

# Now run analytics
class MockDB:
    def query(self, *args): return self
    def filter(self, *args): return self
    def order_by(self, *args): return self
    def limit(self, *args): return self
    def all(self): return []
    def join(self, *args): return self
    def count(self): return 0

print("Running generate_user_analytics...")
try:
    result = AnalyticsService.generate_user_analytics(MockDB(), "test_user")
    print(f"Result recent_activity count: {len(result.get('recent_activity', []))}")
    
    # Check if Resume module has items
    resume_module = next((m for m in result['recent_activity'] if m['module'] == 'Resume'), None)
    if resume_module and len(resume_module['items']) > 0:
        print("SUCCESS: Resume data found in analytics!")
    else:
        print("FAILURE: Resume data NOT found in analytics.")
        print(f"Resume module: {resume_module}")
except Exception as e:
    print(f"Error: {e}")
