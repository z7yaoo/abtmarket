#!/usr/bin/env python3
"""
Test pardon vs election matches
"""
from market_matcher import MarketMatcher

matcher = MarketMatcher()

# Test pardon vs election
test_cases = [
    {
        "kalshi": "Will Hunter Biden receive a presidential pardon before Jan 21, 2029?",
        "poly": "Will Hunter Biden win the 2028 Democratic presidential nomination?",
        "expected": "0.0 - pardon vs election",
    },
    {
        "kalshi": "Will Pete Rose receive a presidential pardon before Jan 21, 2029?",
        "poly": "Will Pete Buttigieg win the 2028 US Presidential Election?",
        "expected": "0.0 - different Pete (Rose vs Buttigieg)",
    },
    {
        "kalshi": "Will Trump balance the budget?",
        "poly": "Will Trump & Elon reduce the deficit in 2025?",
        "expected": ">= 0.5 - both about reducing government deficit (might be okay)",
    },
]

print("=" * 100)
print("TESTING PARDON VS ELECTION")
print("=" * 100)

for i, test in enumerate(test_cases, 1):
    k_market = {"title": test["kalshi"]}
    p_market = {"question": test["poly"]}

    score = matcher.compute_similarity(k_market, p_market)

    print(f"\nTest {i}: Score = {score:.2f}")
    print(f"  Kalshi:   {test['kalshi'][:80]}")
    print(f"  Poly:     {test['poly'][:80]}")
    print(f"  Expected: {test['expected']}")
