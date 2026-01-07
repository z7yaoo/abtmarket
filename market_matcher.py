"""
Market Matching Algorithm Module
Intelligently matches similar markets across Kalshi and Polymarket
"""
import re
from typing import List, Dict, Tuple, Set


class MarketMatcher:
    """Matches similar prediction markets across platforms using keyword and semantic analysis"""

    def __init__(self):
        # Specific keywords that identify unique markets
        self.important_keywords = [
            # Politics - People
            'trump', 'biden', 'harris', 'desantis', 'obama', 'clinton',
            'mcconnell', 'pelosi', 'pence', 'vivek', 'haley',
            # Politics - Events
            'president', 'election', 'senate', 'congress', 'republican', 'democrat',
            'gop', 'primary', 'impeach', 'nomination',
            # Crypto - Specific coins
            'bitcoin', 'btc', 'ethereum', 'eth', 'solana', 'sol',
            'dogecoin', 'doge', 'matic', 'polygon', 'usdc', 'usdt',
            'cardano', 'ada', 'polkadot', 'dot', 'avalanche', 'avax',
            # Sports - Leagues & Events
            'nfl', 'nba', 'mlb', 'nhl', 'super', 'bowl', 'championship', 'mvp',
            'playoffs', 'series', 'finals', 'cup', 'olympics',
            # Sports - Teams (examples)
            'lakers', 'warriors', 'celtics', 'yankees', 'dodgers', 'cowboys',
            'patriots', 'chiefs', 'ravens', 'texans',
            # Companies & Tech
            'apple', 'google', 'amazon', 'microsoft', 'tesla', 'meta', 'nvidia',
            'spacex', 'openai', 'anthropic',
            # People - Tech/Business
            'elon', 'musk', 'bezos', 'zuckerberg', 'gates', 'buffett',
            # Economics - Specific
            'gdp', 'inflation', 'recession', 'fed', 'unemployment', 'cpi',
            # Countries/Places
            'china', 'russia', 'ukraine', 'taiwan', 'israel', 'iran',
            'california', 'texas', 'florida', 'mars',
        ]

        # Topic keywords - markets must share at least one topic to match
        # These represent the SUBJECT or ACTION of the market
        self.topic_keywords = {
            # Election/Political
            'presidential_election': ['presidential election', 'president', 'nominee', 'nomination'],
            'governorship': ['governorship', 'governor'],
            'impeachment': ['impeach', 'impeachment', 'remove', 'resign', 'resignation'],
            'pardon': ['pardon', 'pardoned', 'clemency'],

            # Economics/Finance
            'trade_deficit': ['trade deficit', 'trade balance', 'exports', 'imports'],
            'budget_deficit': ['budget', 'deficit', 'surplus', 'debt', 'spending', 'fiscal', 'reduce the deficit'],
            'gdp': ['gdp', 'growth', 'economy', 'economic', 'recession'],
            'inflation': ['inflation', 'cpi', 'prices', 'deflation'],
            'wealth': ['trillionaire', 'billionaire', 'millionaire', 'net worth', 'richest', 'wealth'],

            # Immigration
            'deportation': ['deport', 'deportation', 'deported'],
            'immigration': ['immigration', 'border', 'visa', 'green card'],

            # Healthcare
            'healthcare': ['ivf', 'healthcare', 'hospital', 'medical', 'insurance', 'obamacare'],

            # Meetings/Events
            'meeting': ['meeting', 'meet', 'summit', 'visit', 'conference'],

            # Crypto/Markets
            'price': ['price', 'reach', 'above', 'below', 'hit', 'trade'],

            # Sports
            'sports_match': ['vs', 'versus', 'game', 'match', 'play'],

            # Specific Actions
            'recognize': ['recognize', 'recognition', 'acknowledge'],
            'buy_acquire': ['buy', 'purchase', 'acquire', 'acquisition', 'take', 'takeover'],
            'ipo': ['ipo', 'public offering', 'go public'],
            'product_launch': ['launch', 'release', 'announce', 'unveil', 'product'],
            'lawsuit': ['lawsuit', 'sue', 'litigation', 'legal action', 'win his lawsuit'],
            'supreme_court': ['supreme court', 'justice', 'scotus'],
            'bond_actor': ['james bond', '007', 'bond actor'],
            'nfl': ['nfl', 'super bowl', 'football'],
            'nba': ['nba', 'basketball'],
            'cabinet': ['cabinet'],
        }

    def extract_keywords(self, text: str) -> Set[str]:
        """
        Extract important keywords from market title

        Args:
            text: Market title or description

        Returns:
            Set of extracted keywords
        """
        if not text:
            return set()

        text_lower = text.lower()
        keywords = set()

        # Extract predefined important keywords
        for keyword in self.important_keywords:
            if keyword in text_lower:
                keywords.add(keyword)

        # Extract years (2024, 2025, etc.)
        years = re.findall(r'\b(20\d{2})\b', text)
        keywords.update(years)

        # Extract dollar amounts ($100k, $50000, etc.)
        dollar_amounts = re.findall(r'\$\s*(\d+(?:,\d{3})*(?:\.\d+)?)\s*([kmb])?', text_lower)
        for amount, suffix in dollar_amounts:
            normalized = amount.replace(',', '')
            if suffix == 'k':
                normalized = str(int(float(normalized) * 1000))
            elif suffix == 'm':
                normalized = str(int(float(normalized) * 1000000))
            elif suffix == 'b':
                normalized = str(int(float(normalized) * 1000000000))
            keywords.add(f"${normalized}")

        # Extract percentages
        percentages = re.findall(r'(\d+(?:\.\d+)?)\s*%', text)
        keywords.update([f"{p}%" for p in percentages])

        # Extract numbers that might be thresholds
        numbers = re.findall(r'\b(\d+(?:,\d{3})+)\b', text)
        keywords.update([n.replace(',', '') for n in numbers])

        return keywords

    def extract_topics(self, text: str) -> Set[str]:
        """
        Extract topic categories from market title

        Args:
            text: Market title or description

        Returns:
            Set of topic categories (e.g., 'election', 'budget', 'deportation')
        """
        if not text:
            return set()

        text_lower = text.lower()
        topics = set()

        # Check each topic category
        for topic_name, keywords in self.topic_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    topics.add(topic_name)
                    break  # Found this topic, move to next

        return topics

    def extract_polarity(self, text: str) -> str:
        """
        Extract positive/negative polarity from market title

        Args:
            text: Market title

        Returns:
            'positive', 'negative', or 'neutral'
        """
        if not text:
            return 'neutral'

        text_lower = text.lower()

        # Negative indicators
        negative_words = [
            'negative', 'below', 'less than', 'under', 'decrease', 'decline',
            'fall', 'drop', 'lose', 'fail', 'not', "won't", 'resign', 'remove'
        ]

        # Positive indicators
        positive_words = [
            'positive', 'above', 'more than', 'over', 'increase', 'rise',
            'reach', 'exceed', 'win', 'achieve', 'success'
        ]

        # Count indicators
        neg_count = sum(1 for word in negative_words if word in text_lower)
        pos_count = sum(1 for word in positive_words if word in text_lower)

        if neg_count > pos_count:
            return 'negative'
        elif pos_count > neg_count:
            return 'positive'
        else:
            return 'neutral'

    def extract_match_participants(self, text: str) -> Set[str]:
        """
        Extract participant names from sports match titles (e.g., "Team A vs Team B")

        Args:
            text: Market title

        Returns:
            Set of normalized participant names
        """
        participants = set()

        # Pattern: "A vs B", "A v B", "A vs. B" (case-insensitive)
        vs_patterns = [
            # Match multi-word names: "John Smith vs Jane Doe"
            r'([A-Za-z]+(?:\s+[A-Za-z]+)*)\s+(?:vs?\.?|versus)\s+([A-Za-z]+(?:\s+[A-Za-z]+)*)',
        ]

        for pattern in vs_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # Add both participants, normalized to lowercase and trimmed
                name1 = match[0].lower().strip()
                name2 = match[1].lower().strip()

                # Only add if names are meaningful (not common words)
                if len(name1) > 2 and len(name2) > 2:
                    participants.add(name1)
                    participants.add(name2)

        return participants

    def compute_similarity(self, market1: Dict, market2: Dict) -> float:
        """
        Compute similarity score between two markets (0-1)

        Args:
            market1: First market dictionary (Kalshi)
            market2: Second market dictionary (Polymarket)

        Returns:
            Similarity score from 0.0 to 1.0
        """
        # Get titles
        title1 = market1.get("title", "")
        title2 = market2.get("question", market2.get("title", ""))

        if not title1 or not title2:
            return 0.0

        # Normalize titles
        title1_lower = title1.lower()
        title2_lower = title2.lower()

        # CRITICAL CHECK #1: Extract topics - markets must share at least one topic
        topics1 = self.extract_topics(title1)
        topics2 = self.extract_topics(title2)

        # STRICT: If both have topics but none overlap, they're about different things
        if topics1 and topics2:
            if not (topics1 & topics2):
                # Different topics entirely (e.g., election vs deportation vs budget)
                return 0.0

            # EXTRA CHECKS: Certain topics should NOT match with each other
            incompatible_pairs = [
                ('trade_deficit', 'budget_deficit'),  # Trade vs budget deficit
                ('pardon', 'presidential_election'),  # Pardon vs election
                ('pardon', 'governorship'),  # Pardon vs governorship
                ('pardon', 'impeachment'),  # Pardon vs impeachment
                ('ipo', 'product_launch'),  # IPO vs product launch
                ('nfl', 'nba'),  # Different sports leagues
                ('supreme_court', 'presidential_election'),  # Court appointment vs election
                ('governorship', 'presidential_election'),  # State vs federal election
                ('lawsuit', 'presidential_election'),  # Lawsuit vs election
                ('cabinet', 'presidential_election'),  # Cabinet appointment vs election
            ]

            for topic_a, topic_b in incompatible_pairs:
                if (topic_a in topics1 and topic_b in topics2) or \
                   (topic_b in topics1 and topic_a in topics2):
                    return 0.0

        # STRICT: If NO topics found for either market, require very high word similarity
        # This prevents matching unrelated events with the same person name
        if not topics1 or not topics2:
            # Continue to compute similarity but will require higher threshold later
            pass

        # CRITICAL CHECK #1b: If same topic, check polarity (positive vs negative)
        if topics1 and topics2 and (topics1 & topics2):
            polarity1 = self.extract_polarity(title1)
            polarity2 = self.extract_polarity(title2)

            # If one is positive and other is negative, they're opposite questions
            if (polarity1 == 'positive' and polarity2 == 'negative') or \
               (polarity1 == 'negative' and polarity2 == 'positive'):
                return 0.0

        # CRITICAL CHECK #2: Extract proper nouns (names, places, entities)
        # Skip sentence-initial words and common words
        words_to_skip = {'will', 'would', 'could', 'should', 'can', 'may', 'might'}

        # Words that are NOT person names (places, titles, generic terms)
        non_person_words = {
            # Titles/Positions
            'president', 'prime', 'minister', 'senator', 'governor', 'mayor',
            'secretary', 'director', 'chairman', 'leader', 'chief', 'king', 'queen',
            # Countries
            'america', 'usa', 'china', 'russia', 'israel', 'iran', 'ukraine',
            'taiwan', 'india', 'japan', 'korea', 'france', 'germany', 'italy',
            'spain', 'brazil', 'mexico', 'canada', 'australia', 'britain', 'england',
            'netherlands',
            # Places
            'california', 'texas', 'florida', 'york', 'washington', 'chicago',
            'mars', 'earth', 'house', 'senate', 'congress', 'court',
            # Organizations
            'democratic', 'republican', 'gop', 'nato', 'olympics',
            # Other
            'super', 'bowl', 'world', 'cup', 'final', 'championship',
            'january', 'february', 'march', 'april', 'may', 'june', 'july',
            'august', 'september', 'october', 'november', 'december',
            'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'
        }

        # Extract individual capitalized words (not at sentence start)
        def extract_proper_nouns(text):
            words = text.split()
            proper = set()
            for i, word in enumerate(words):
                # Remove punctuation
                clean_word = re.sub(r'[^\w\s]', '', word)
                # Skip if first word or in skip list
                if i > 0 and clean_word and clean_word[0].isupper():
                    lower_word = clean_word.lower()
                    if lower_word not in words_to_skip:
                        proper.add(lower_word)
            return proper

        # Extract person names specifically (filter out non-person words)
        def extract_person_names(text):
            proper = extract_proper_nouns(text)
            # Filter out places, titles, generic terms
            person_names = {word for word in proper if word not in non_person_words}
            return person_names

        proper_nouns1 = extract_proper_nouns(title1)
        proper_nouns2 = extract_proper_nouns(title2)

        person_names1 = extract_person_names(title1)
        person_names2 = extract_person_names(title2)

        # Check if proper nouns overlap or if one is substring of another
        # Example: "Trump" should match "Donald Trump"
        def has_proper_noun_overlap(set1, set2):
            if not set1 or not set2:
                return False

            # Check exact overlap
            if set1 & set2:
                return True

            # Check if any noun from set1 is in any noun from set2 (fuzzy match)
            for n1 in set1:
                for n2 in set2:
                    if n1 in n2 or n2 in n1:
                        return True

            return False

        # CRITICAL: Check person names specifically, not just any proper nouns
        # If one has person names but they don't overlap, they're different markets
        if person_names1 and person_names2:
            if not has_proper_noun_overlap(person_names1, person_names2):
                # Different people
                return 0.0
        elif person_names2 and not person_names1:
            # Polymarket has specific person, Kalshi is generic "who"
            return 0.0
        elif person_names1 and not person_names2:
            # Kalshi has specific person, Polymarket doesn't
            return 0.0

        # Extract keywords from both
        keywords1 = self.extract_keywords(title1)
        keywords2 = self.extract_keywords(title2)

        # Extract all meaningful words (filter out common stop words)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                      'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'be', 'been',
                      'will', 'would', 'could', 'should', 'has', 'have', 'had', 'do', 'does',
                      'did', 'this', 'that', 'these', 'those', 'what', 'which', 'who', 'when',
                      'where', 'why', 'how', 'their', 'there', 'than', 'then'}

        words1 = set(w for w in re.findall(r'\w+', title1_lower) if len(w) > 2 and w not in stop_words)
        words2 = set(w for w in re.findall(r'\w+', title2_lower) if len(w) > 2 and w not in stop_words)

        if not words1 or not words2:
            return 0.0

        # Extract match participants (for sports: "A vs B")
        participants1 = self.extract_match_participants(title1)
        participants2 = self.extract_match_participants(title2)

        # If both have participants, check if they match
        if participants1 and participants2:
            # Check exact overlap first
            participant_overlap = len(participants1 & participants2)

            # Also check if names are substrings of each other (e.g., "barry" in "monique barry")
            fuzzy_matches = 0
            for p1 in participants1:
                for p2 in participants2:
                    # Check if one is substring of the other
                    if p1 in p2 or p2 in p1:
                        fuzzy_matches += 1
                        break

            # If 2+ participants match (exact or fuzzy), this is likely the same match
            if participant_overlap >= 2 or fuzzy_matches >= 2:
                # Very high score for matching sports events
                return 0.95

        # Extract keywords from both
        keyword_overlap = len(keywords1 & keywords2)
        keyword_union = len(keywords1 | keywords2)

        # CRITICAL: Must have at least 2 specific keywords in common
        # If less than 2 keywords overlap, they're likely different markets
        if keyword_overlap < 2:
            # Check if they share significant proper nouns
            # Extract capitalized words (proper nouns)
            proper_nouns1 = set(w for w in re.findall(r'\b[A-Z][a-z]+', title1))
            proper_nouns2 = set(w for w in re.findall(r'\b[A-Z][a-z]+', title2))

            proper_overlap = len(proper_nouns1 & proper_nouns2)

            # If less than 2 proper nouns overlap, score very low
            if proper_overlap < 2:
                # Only check general word similarity as fallback
                word_overlap = len(words1 & words2)
                word_union = len(words1 | words2)

                # Even with word overlap, max score is 0.4 if no keyword/proper noun match
                if word_union > 0:
                    return min(0.4, (word_overlap / word_union) * 0.5)
                return 0.0

        # Calculate keyword similarity (Jaccard)
        keyword_similarity = keyword_overlap / keyword_union if keyword_union > 0 else 0.0

        # Calculate word overlap (Jaccard similarity)
        word_overlap = len(words1 & words2)
        word_union = len(words1 | words2)
        word_similarity = word_overlap / word_union if word_union > 0 else 0.0

        # Weighted combination: keywords matter much more than general words
        base_score = (keyword_similarity * 0.85) + (word_similarity * 0.15)

        # Boost score if proper nouns match (names, entities)
        proper_boost = 0.0
        if proper_nouns1 and proper_nouns2 and has_proper_noun_overlap(proper_nouns1, proper_nouns2):
            proper_boost = 0.3  # Significant boost for matching entities

        # Boost score if same category
        cat1 = market1.get("category", "").lower()
        cat2 = market2.get("category", "").lower()
        category_boost = 0.1 if cat1 and cat2 and cat1 == cat2 else 0.0

        # Combine scores
        final_score = min(1.0, base_score + proper_boost + category_boost)

        # PENALTY: If no topics found, apply moderate penalty unless score is very high
        # This prevents "Trump does X" from matching "Trump does Y"
        if not topics1 or not topics2:
            # Without topics, require high match (75%+ word overlap)
            if final_score < 0.75:
                final_score = final_score * 0.6  # Moderate penalty (was 0.3)

        return final_score

    def search_polymarket_for_kalshi(self, kalshi_market: Dict, poly_markets: List[Dict]) -> Tuple[Dict, float]:
        """
        Search for the best Polymarket match for a single Kalshi market

        Args:
            kalshi_market: Single Kalshi market to search for
            poly_markets: List of all Polymarket markets to search in

        Returns:
            Tuple of (best_poly_market, similarity_score) or (None, 0.0)
        """
        k_title = kalshi_market.get("title", "")
        if not k_title:
            return None, 0.0

        best_match = None
        best_score = 0.0

        # Score all Polymarket markets
        for p_market in poly_markets:
            score = self.compute_similarity(kalshi_market, p_market)

            if score > best_score:
                best_score = score
                best_match = p_market

        return best_match, best_score

    def find_matches(
        self,
        kalshi_markets: List[Dict],
        poly_markets: List[Dict],
        threshold: float = 0.5
    ) -> List[Tuple[Dict, Dict, float]]:
        """
        Find matching markets by searching Kalshi for each Polymarket market

        Strategy:
        1. Use Polymarket as source (has specific, non-duplicate markets)
        2. For each Polymarket market, search all Kalshi markets
        3. Find best match based on full title similarity
        4. Only match if score >= threshold

        Args:
            kalshi_markets: List of Kalshi markets (search pool)
            poly_markets: List of Polymarket markets (source)
            threshold: Minimum similarity score to consider a match (0-1)

        Returns:
            List of tuples: (kalshi_market, poly_market, similarity_score)
        """
        matches = []
        used_kalshi_indices = set()

        print(f"🔍 Searching {len(kalshi_markets)} Kalshi markets for {len(poly_markets)} Polymarket markets...")

        for idx, p_market in enumerate(poly_markets):
            # Search for best Kalshi match
            best_match = None
            best_score = 0.0
            best_index = -1

            for i, k_market in enumerate(kalshi_markets):
                # Skip if already matched
                if i in used_kalshi_indices:
                    continue

                score = self.compute_similarity(k_market, p_market)

                if score > best_score:
                    best_score = score
                    best_match = k_market
                    best_index = i

            # Add match only if score meets threshold
            if best_match and best_score >= threshold and best_index >= 0:
                matches.append((best_match, p_market, best_score))
                used_kalshi_indices.add(best_index)

                # Log high-quality matches
                if best_score >= 0.8:
                    p_title = p_market.get("question", p_market.get("title", ""))[:50]
                    k_title = best_match.get("title", "")[:50]
                    print(f"  ✓ Match {len(matches)}: {p_title}... = {k_title}... (score: {best_score:.2f})")

        # Sort by similarity score (highest first)
        matches.sort(key=lambda x: x[2], reverse=True)

        print(f"✓ Found {len(matches)} matched markets from {len(poly_markets)} Polymarket markets (threshold: {threshold})")

        return matches

    def filter_by_category(self, markets: List[Dict], categories: List[str]) -> List[Dict]:
        """
        Filter markets by category

        Args:
            markets: List of markets
            categories: List of category names to include

        Returns:
            Filtered list of markets
        """
        if not categories:
            return markets

        categories_lower = [c.lower() for c in categories]
        filtered = []

        for market in markets:
            market_cat = market.get("category", "").lower()
            market_title = market.get("title", market.get("question", "")).lower()

            # Check if category matches or if title contains category keyword
            if market_cat in categories_lower or any(cat in market_title for cat in categories_lower):
                filtered.append(market)

        return filtered
