#!/usr/bin/env python3
"""
Test the specific matches visible in the app to verify quality
"""
from market_matcher import MarketMatcher

matcher = MarketMatcher()

# Test cases from the visible matches in the app
test_cases = [
    {
        "kalshi": "Where will Trump and Putin's first meeting after their planned August 15, 2025 meeting in Alaska occur?",
        "poly": "Will Trump & Elon reduce the deficit in 2025?",
        "expected": "Should be 0.0 - completely different events",
    },
    {
        "kalshi": "Where will Trump and Putin's first meeting after their planned August 15, 2025 meeting in Alaska occur?",
        "poly": "Will Trump deport 750,000 or more people in 2025?",
        "expected": "Should be 0.0 - completely different events",
    },
    {
        "kalshi": "Will Elon Musk be a trillionaire before 2028?",
        "poly": "Will Elon Musk win the 2028 US Presidential Election?",
        "expected": "Should be 0.0 - one is about wealth, other is about election",
    },
    {
        "kalshi": "Will quarterly GDP be above 5% in any quarter in Q1 2025 to Q4 2028?",
        "poly": "Negative GDP growth in 2025?",
        "expected": "Should be 0.0 - opposite questions (positive vs negative GDP)",
    },
    {
        "kalshi": "Will Trump balance the budget?",
        "poly": "Will Trump deport less than 250,000?",
        "expected": "Should be 0.0 - budget vs deportation are different",
    },
    {
        "kalshi": "Will Trump make IVF free?",
        "poly": "Will Trump deport 2,000,000 or more people?",
        "expected": "Should be 0.0 - IVF vs deportation are different",
    },
    {
        "kalshi": "Will President Trump resign before his term is up?",
        "poly": "Will Donald Trump win the 2028 US Presidential Election?",
        "expected": "Should be 0.0 - resignation vs future election are different",
    },
    {
        "kalshi": "Will Donald Trump Jr. receive a presidential pardon before Jan 21, 2029?",
        "poly": "Will Donald Trump Jr. win the 2028 US Presidential Election?",
        "expected": "Should be 0.0 - pardon vs election are different",
    },
]

print("=" * 100)
print("TESTING VISIBLE MATCHES FROM APP")
print("=" * 100)

issues = 0

for i, test in enumerate(test_cases, 1):
    k_market = {"title": test["kalshi"]}
    p_market = {"question": test["poly"]}

    score = matcher.compute_similarity(k_market, p_market)

    # These should all be 0.0 or very low
    is_issue = score >= 0.5

    status = "❌ BAD MATCH" if is_issue else "✅ Correct"

    if is_issue:
        issues += 1

    print(f"\n{status} Test {i}: Score = {score:.2f}")
    print(f"  Kalshi:   {test['kalshi'][:90]}")
    print(f"  Poly:     {test['poly'][:90]}")
    print(f"  Expected: {test['expected']}")

print("\n" + "=" * 100)
print(f"RESULT: {issues} issues found out of {len(test_cases)} tests")
if issues > 0:
    print("⚠️  The matching algorithm is producing false positives!")
else:
    print("✅ All matches are correct!")
print("=" * 100)
