#!/usr/bin/env python3
"""Test detector with categorized statements"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.deception_detector import DeceptionDetector

# Test statements organized by expected category
test_statements = [
    # ✅ AUTHENTIC (expected: 10-30)
    ("The server maintenance is scheduled for March 2nd, and services may be unavailable for one hour.", "AUTHENTIC", "A1"),
    ("A recent study found that network latency improves by 12% after protocol optimization.", "AUTHENTIC", "A2"),
    ("Your meeting has been confirmed and the calendar entry is updated.", "AUTHENTIC", "A3"),
    ("Your profile information was updated successfully. No further action is required.", "AUTHENTIC", "A4"),
    ("The research team published the analysis results along with supporting data charts.", "AUTHENTIC", "A5"),
    ("Payment for invoice #4921 has been processed and the receipt is available in your account.", "AUTHENTIC", "A6"),
    ("Your package has arrived at the local facility and will be delivered tomorrow.", "AUTHENTIC", "A7"),
    ("We received your request and our support team will respond within 24 hours.", "AUTHENTIC", "A8"),
    
    # 🟡 SUSPICIOUS (expected: 31-70)
    ("Don't miss this limited time update! Please review your account details.", "SUSPICIOUS", "S1"),
    ("This is a shocking update about your package status. Please check your dashboard.", "SUSPICIOUS", "S2"),
    ("URGENT update: your order requires immediate verification to avoid delays.", "SUSPICIOUS", "S3"),
    ("Please confirm your details to avoid potential issues with your login.", "SUSPICIOUS", "S4"),
    ("Your device might have security concerns. Check the system report now?", "SUSPICIOUS", "S5"),
    ("Limited time update! Access your benefits before they expire soon.", "SUSPICIOUS", "S6"),
    ("Some unusual login attempts were detected. It is recommended to verify the session.", "SUSPICIOUS", "S7"),
    ("We noticed irregular activity on your profile… review and update if needed.", "SUSPICIOUS", "S8"),
    
    # ❌ DECEPTIVE (expected: 71-100)
    ("BREAKING NEWS!! Your account WILL BE TERMINATED!!! Click here NOW to avoid PERMANENT LOSS [URGENT]", "DECEPTIVE", "D1"),
    ("This unbelievable trick FINALLY REVEALED… Doctors HATE this secret formula!!!", "DECEPTIVE", "D2"),
    ("URGENT ALERT: Your BANK ACCOUNT is BLOCKED due to a CATASTROPHIC security breach!!! VERIFY IMMEDIATELY!!", "DECEPTIVE", "D3"),
    ("ALERT!!! Your account is permanently SUSPENDED! Restore access IMMEDIATELY: http://secure-restore-now.biz", "DECEPTIVE", "D4"),
    ("This SECRET METHOD is GUARANTEED to make you thousands — unbelievable results revealed today!!", "DECEPTIVE", "D5"),
    ("DISASTER EXPLOSION JUST HAPPENED!!! Millions DEAD — share this before it gets DELETED!!", "DECEPTIVE", "D6"),
    ("Your tax refund is on hold. Enter your ATM PIN and CVV to release the payment instantly.", "DECEPTIVE", "D7"),
    ("URGENT BREAKING NEWS: Government finally EXPOSED the shocking truth they HID for years!!!", "DECEPTIVE", "D8"),
    
    # ⭐ MIXED STRESS TEST
    ("Your verification attempt failed. Try updating your details again to avoid disruption.", "SUSPICIOUS", "M1"),
    ("LAST CHANCE!!! Claim your FREE rewards before your eligibility EXPIRES FOREVER!!", "DECEPTIVE", "M2"),
    ("Your subscription will renew next month unless cancelled.", "AUTHENTIC", "M3"),
    ("Review this update now — you might be eligible for a special program.", "SUSPICIOUS", "M4"),
    ("Congratulations! You're selected for an EXCLUSIVE offer. Click the link to receive your reward instantly!", "DECEPTIVE", "M5"),
]

def main():
    print("=" * 100)
    print("DECEPTION DETECTOR - COMPREHENSIVE TEST SUITE")
    print("=" * 100)
    
    detector = DeceptionDetector()
    
    results = {"AUTHENTIC": [], "SUSPICIOUS": [], "DECEPTIVE": []}
    
    for statement, expected_category, test_id in test_statements:
        result = detector.analyze(text=statement)
        
        risk_score = result['riskScore']
        verdict = result['verdict']
        reasons = result['reasons'][0] if result['reasons'] else 'No reasons'
        
        # Determine if score is in expected range
        if expected_category == "AUTHENTIC":
            expected_range = "10-30"
            in_range = 10 <= risk_score <= 30
        elif expected_category == "SUSPICIOUS":
            expected_range = "31-70"
            in_range = 31 <= risk_score <= 70
        else:  # DECEPTIVE
            expected_range = "71-100"
            in_range = 71 <= risk_score <= 100
        
        status = "[PASS]" if in_range else "[FAIL]"
        results[expected_category].append((test_id, risk_score, verdict, in_range))
        
        print(f"\n[{test_id}] {status} Expected: {expected_category} ({expected_range})")
        print(f"     Statement: {statement[:75]}{'...' if len(statement) > 75 else ''}")
        print(f"     Score: {risk_score}% | Verdict: {verdict}")
    
    # Summary
    print("\n" + "=" * 100)
    print("TEST SUMMARY")
    print("=" * 100)
    
    total_passed = 0
    total_tests = 0
    
    for category in ["AUTHENTIC", "SUSPICIOUS", "DECEPTIVE"]:
        tests = results[category]
        passed = sum(1 for _, _, _, in_range in tests if in_range)
        total = len(tests)
        total_passed += passed
        total_tests += total
        
        status = "[OK]" if passed == total else "[ISSUES]"
        print(f"\n{status} {category} ({len([t for t in test_statements if t[1] == category])} tests):")
        for test_id, score, verdict, in_range in tests:
            result_status = "[PASS]" if in_range else "[FAIL]"
            print(f"     {test_id}: {score:3d}% ({verdict:10s}) - {result_status}")
        print(f"     Result: {passed}/{total} passed")
    
    print("\n" + "=" * 100)
    print(f"OVERALL: {total_passed}/{total_tests} tests passed ({int(100*total_passed/total_tests)}%)")
    print("=" * 100)

if __name__ == '__main__':
    main()
