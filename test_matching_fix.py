#!/usr/bin/env python3
"""
Test script to verify proper noun matching fix
"""
from market_matcher import MarketMatcher

matcher = MarketMatcher()

# Test cases: (kalshi_title, poly_question, expected_behavior)
test_cases = [
    # FALSE MATCHES - Generic vs Specific (should be 0.0)
    {
        "kalshi": "Who will be the next Prime Minister of Israel?",
        "poly": "Will Yair Golan be the next Prime Minister of Israel?",
        "expected": "0.0 (generic vs specific person)",
    },
    {
        "kalshi": "Who will be the next Prime Minister of the Netherlands?",
        "poly": "Will Dick Schoof be the next Prime Minister of the Netherlands?",
        "expected": "0.0 (generic vs specific person)",
    },
    {
        "kalshi": "Who will win the next presidential election?",
        "poly": "Will JB Pritzker win the next presidential election?",
        "expected": "0.0 (generic vs specific person)",
    },
    {
        "kalshi": "Who will win the next presidential election?",
        "poly": "Will Tulsi Gabbard win the next presidential election?",
        "expected": "0.0 (generic vs specific person)",
    },

    # TRUE MATCHES - Same person (should be high score >= 0.7)
    {
        "kalshi": "Will Donald Trump win the election?",
        "poly": "Will Trump win the election?",
        "expected": ">= 0.7 (same person)",
    },
    {
        "kalshi": "Will Joe Biden be president?",
        "poly": "Will Biden be president?",
        "expected": ">= 0.7 (same person)",
    },

    # TRUE MATCHES - Sports (should be high score >= 0.9)
    {
        "kalshi": "Barry vs Seidel tennis match",
        "poly": "Monique Barry vs Ella Seidel tennis match",
        "expected": ">= 0.9 (sports match)",
    },
    {
        "kalshi": "BARRY vs SEIDEL",
        "poly": "Barry vs Seidel",
        "expected": ">= 0.9 (sports match)",
    },
]

print("=" * 80)
print("TESTING PROPER NOUN MATCHING FIX")
print("=" * 80)

passed = 0
failed = 0

for i, test in enumerate(test_cases, 1):
    k_market = {"title": test["kalshi"]}
    p_market = {"question": test["poly"]}

    score = matcher.compute_similarity(k_market, p_market)

    # Determine pass/fail
    expected = test["expected"]
    if "0.0" in expected:
        # Should be 0.0 or very close
        is_pass = score < 0.3
    elif ">= 0.9" in expected:
        is_pass = score >= 0.9
    elif ">= 0.7" in expected:
        is_pass = score >= 0.7
    else:
        is_pass = False

    status = "✅ PASS" if is_pass else "❌ FAIL"

    if is_pass:
        passed += 1
    else:
        failed += 1

    print(f"\nTest {i}: {status}")
    print(f"  Kalshi:   {test['kalshi'][:70]}")
    print(f"  Poly:     {test['poly'][:70]}")
    print(f"  Score:    {score:.2f}")
    print(f"  Expected: {expected}")

print("\n" + "=" * 80)
print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
print("=" * 80)
