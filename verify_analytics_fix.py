import sys
import os
from datetime import datetime, timedelta

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'd:\\AceIt\\aceit_backend'))

def test_streak_calculation():
    from services.unified_analytics_service import UnifiedAnalyticsService
    
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    two_days_ago = today - timedelta(days=2)
    three_days_ago = today - timedelta(days=3)
    five_days_ago = today - timedelta(days=5)
    
    # Test 1: 3 consecutive days including today
    dates1 = [today, yesterday, two_days_ago]
    streak1 = UnifiedAnalyticsService._calculate_streak(dates1)
    print(f"Test 1 (Today, Yesterday, 2 days ago): Expected 3, Got {streak1}")
    assert streak1 == 3
    
    # Test 2: 2 consecutive days including yesterday (last practiced)
    dates2 = [yesterday, two_days_ago]
    streak2 = UnifiedAnalyticsService._calculate_streak(dates2)
    print(f"Test 2 (Yesterday, 2 days ago): Expected 2, Got {streak2}")
    assert streak2 == 2
    
    # Test 3: Gap in practice
    dates3 = [today, yesterday, three_days_ago]
    streak3 = UnifiedAnalyticsService._calculate_streak(dates3)
    print(f"Test 3 (Today, Yesterday, 3 days ago): Expected 2, Got {streak3}")
    assert streak3 == 2
    
    # Test 4: Not practiced recently
    dates4 = [two_days_ago, three_days_ago]
    streak4 = UnifiedAnalyticsService._calculate_streak(dates4)
    print(f"Test 4 (2 days ago, 3 days ago): Expected 0, Got {streak4}")
    assert streak4 == 0
    
    # Test 5: Empty dates
    streak5 = UnifiedAnalyticsService._calculate_streak([])
    print(f"Test 5 (Empty): Expected 0, Got {streak5}")
    assert streak5 == 0
    
    # Test 6: Duplicate dates
    dates6 = [today, today, yesterday, yesterday]
    streak6 = UnifiedAnalyticsService._calculate_streak(dates6)
    print(f"Test 6 (Duplicates): Expected 2, Got {streak6}")
    assert streak6 == 2

    print("\nAll streak calculation tests passed!")

if __name__ == "__main__":
    try:
        test_streak_calculation()
    except Exception as e:
        print(f"Verification failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
