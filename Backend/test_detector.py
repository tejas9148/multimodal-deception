#!/usr/bin/env python3
"""
Quick test script for the deception detector
Tests with fake and real statements to verify scoring is working
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.deception_detector import DeceptionDetector

# Test statements
test_statements = [
    # REAL/AUTHENTIC (should be LOW score)
    ("The Earth orbits around the Sun", "REAL"),
    ("Water boils at 100 degrees Celsius at sea level", "REAL"),
    ("Paris is the capital of France", "REAL"),
    ("The human body has 206 bones in adults", "REAL"),
    
    # FAKE/DECEPTIVE (should be HIGH score)
    ("The moon is made of cheese", "FAKE"),
    ("Humans only use 10% of their brain", "FAKE"),
    ("Lightning never strikes the same place twice", "FAKE"),
    ("Sugar makes children hyperactive", "FAKE"),
    
    # FAKE NEWS (should be HIGH score)
    ("Breaking: New policy passed eliminating Social Security starting next year", "FAKE_NEWS"),
    ("The new vaccine contains tracking devices that monitor all citizens", "FAKE_NEWS"),
    ("Drinking bleach kills COVID-19 virus and boosts immunity", "FAKE_NEWS"),
    ("Scientists discovered that gravity doesn't actually exist, it was a hoax", "FAKE_NEWS"),
    
    # CLICKBAIT/SUSPICIOUS (should be MEDIUM-HIGH score)
    ("This One Trick Will CHANGE YOUR LIFE!!! Click here NOW!!!", "CLICKBAIT"),
    ("You won't BELIEVE what this celebrity did next!?!?", "CLICKBAIT"),
    ("Doctors HATE this miracle cure for cancer!!!", "CLICKBAIT"),
]

def main():
    print("=" * 80)
    print("DECEPTION DETECTOR TEST SUITE")
    print("=" * 80)
    
    detector = DeceptionDetector()
    
    for statement, category in test_statements:
        print(f"\n[{category}] {statement[:60]}...")
        
        result = detector.analyze(text=statement)
        
        risk_score = result['riskScore']
        verdict = result['verdict']
        text_score = result['textScore']
        reasons = result['reasons']
        
        print(f"  Score: {risk_score}% | Verdict: {verdict} (Text: {text_score}%)")
        print(f"  Reasons: {reasons[0] if reasons else 'No specific reasons'}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)
    print("\nExpected Results Guide:")
    print("  REAL statements: 15-35% risk")
    print("  FAKE statements: 55-85% risk")
    print("  FAKE_NEWS: 70-95% risk")
    print("  CLICKBAIT: 65-85% risk")

if __name__ == '__main__':
    main()
