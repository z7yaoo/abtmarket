#!/usr/bin/env python3
"""
Test the final 7 matches
"""
from market_matcher import MarketMatcher

matcher = MarketMatcher()

test_cases = [
    {
        "kalshi": "Will Trump win his lawsuit against New York for its sanctuary cities law?",
        "poly": "Will Donald Trump win the 2028 US Presidential Election?",
        "expected": "0.0 - lawsuit vs election",
    },
    {
        "kalshi": "Will the Democratic party win the governorship in Delaware",
        "poly": "Will Stephen A. Smith win the 2028 Democratic presidential nomination?",
        "expected": "0.0 - governorship vs presidential",
    },
    {
        "kalshi": "Will Trump balance the budget?",
        "poly": "Will Trump & Elon reduce the deficit in 2025?",
        "expected": ">= 0.5 - both about reducing deficit (might be okay)",
    },
]

print("=" * 100)
print("TESTING FINAL MATCHES")
print("=" * 100)

for i, test in enumerate(test_cases, 1):
    k_market = {"title": test["kalshi"]}
    p_market = {"question": test["poly"]}

    score = matcher.compute_similarity(k_market, p_market)

    print(f"\nTest {i}: Score = {score:.2f}")
    print(f"  Kalshi:   {test['kalshi'][:80]}")
    print(f"  Poly:     {test['poly'][:80]}")
    print(f"  Expected: {test['expected']}")
