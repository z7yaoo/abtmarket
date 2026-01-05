#!/usr/bin/env python3
"""
Test the bad matches found in the app
"""
from market_matcher import MarketMatcher

matcher = MarketMatcher()

# Test the actual bad matches from the app
test_cases = [
    {
        "kalshi": "Will Trump recognize Somaliland?",
        "poly": "Will Trump deport less than 250,000?",
        "expected": "0.0 - recognize vs deport (different actions)",
    },
    {
        "kalshi": "Will Trump go on SNL during his second term?",
        "poly": "Will Trump deport 2,000,000 or more people?",
        "expected": "0.0 - SNL appearance vs deportation",
    },
    {
        "kalshi": "Will Trump halve the trade deficit?",
        "poly": "Will Trump & Elon reduce the deficit in 2025?",
        "expected": "0.0 - trade deficit vs budget deficit",
    },
    {
        "kalshi": "Will Trump buy Greenland?",
        "poly": "Will Trump deport 500,000-750,000- people?",
        "expected": "0.0 - buy Greenland vs deportation",
    },
    {
        "kalshi": "Will the Portland Trailblazers be bought and become the Seattle SuperSonics?",
        "poly": "Will the Seattle Seahawks win Super Bowl 2026?",
        "expected": "0.0 - NBA vs NFL, different teams",
    },
    {
        "kalshi": "Will OpenAI or Anthropic IPO first?",
        "poly": "Will OpenAI launch a new consumer hardware product by March 31, 2026?",
        "expected": "0.0 - IPO vs product launch",
    },
    {
        "kalshi": "Will Harris Dickinson be the next James Bond?",
        "poly": "Will Kamala Harris win the 2028 US Presidential Election?",
        "expected": "0.0 - different Harris (actor vs politician)",
    },
    {
        "kalshi": "Will Kenneth Lee become the next Justice on the Supreme Court?",
        "poly": "Will Kenneth Walker be the 2025-2026 NFL Comeback Player of the Year?",
        "expected": "0.0 - different Kenneth (judge vs NFL player)",
    },
]

print("=" * 100)
print("TESTING BAD MATCHES FROM APP")
print("=" * 100)

passed = 0
failed = 0

for i, test in enumerate(test_cases, 1):
    k_market = {"title": test["kalshi"]}
    p_market = {"question": test["poly"]}

    score = matcher.compute_similarity(k_market, p_market)

    # Should be < 0.5 to not match
    is_pass = score < 0.5

    status = "✅ PASS" if is_pass else "❌ FAIL"

    if is_pass:
        passed += 1
    else:
        failed += 1

    print(f"\n{status} Test {i}: Score = {score:.2f}")
    print(f"  Kalshi:   {test['kalshi'][:80]}")
    print(f"  Poly:     {test['poly'][:80]}")
    print(f"  Expected: {test['expected']}")

print("\n" + "=" * 100)
print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
if failed == 0:
    print("✅ All bad matches correctly blocked!")
else:
    print(f"⚠️  {failed} bad matches still getting through!")
print("=" * 100)
