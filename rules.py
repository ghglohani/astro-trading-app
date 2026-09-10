# इमेजेस के आधार पर ग्रहों की युति (Conjunctions) के ट्रेडिंग इफ़ेक्ट
CONJUNCTION_RULES = {
    ("Moon", "Mars"): "General Positive Momentum",
    ("Moon", "Mercury"): "Sometimes Positive and Sometimes Negative Momentum",
    ("Moon", "Jupiter"): "Sometimes Positive and Sometimes Negative Momentum",
    ("Moon", "Venus"): "Majority times Negative Momentum",
    ("Moon", "Saturn"): "Sometimes Positive and Sometimes Negative Momentum",
    ("Moon", "Rahu"): "Negative Momentum",
    ("Moon", "Ketu"): "Sometimes Positive and Sometimes Negative Momentum",
    ("Moon", "Uranus"): "General Positive Momentum",
    ("Moon", "Neptune"): "Before Conjunction Positive, Post Conjunction Negative Momentum",
    ("Moon", "Pluto"): "General Positive Momentum",

    ("Mars", "Mercury"): "General Positive (If Mercury Retrograde/Combust -> Major Positive)",
    ("Mars", "Jupiter"): "General Negative (If Jupiter Fast Moving -> Positive)",
    ("Mars", "Venus"): "General Positive Momentum",
    ("Mars", "Saturn"): "Negative Momentum (If Saturn Retrograde -> Dual Trend/Minor Positive)",
    ("Mars", "Rahu"): "General Positive Momentum",
    ("Mars", "Ketu"): "Sometimes Positive and Sometimes Negative Momentum",
    ("Mars", "Uranus"): "Positive Momentum",
    ("Mars", "Neptune"): "Before Conjunction Positive, Post Conjunction Negative Momentum",
    ("Mars", "Pluto"): "General Positive Momentum",

    ("Mercury", "Jupiter"): "General Positive Momentum",
    ("Mercury", "Venus"): "Negative Momentum (If Mercury Combust/Retrograde -> Positive)",
    ("Mercury", "Saturn"): "Volatile Trend in both sides",
    ("Mercury", "Rahu"): "No Major Effect on Market",
    ("Mercury", "Ketu"): "No Major Effect on Market",
    ("Mercury", "Uranus"): "Positive Momentum",
    ("Mercury", "Neptune"): "Before Conjunction Positive, Post Conjunction Negative Momentum",
    ("Mercury", "Pluto"): "Positive Momentum",

    ("Jupiter", "Venus"): "Positive in Bullish Signs, Negative in Bearish Signs (If Retrograde -> Negative)",
    ("Jupiter", "Saturn"): "Positive Momentum (If Retrograde -> Negative)",
    ("Jupiter", "Rahu"): "Positive Momentum (If Jupiter Retrograde -> Negative)",
    ("Jupiter", "Ketu"): "Positive Momentum (If Jupiter Retrograde -> Negative)",
    ("Jupiter", "Uranus"): "Major Positive Momentum",
    ("Jupiter", "Neptune"): "Before Conjunction Positive, Post Conjunction Negative Momentum",
    ("Jupiter", "Pluto"): "Positive Momentum",

    ("Saturn", "Rahu"): "Major Negative in Bearish Sign, General in Bullish Sign",
    ("Saturn", "Ketu"): "General Negative Momentum",
    ("Saturn", "Uranus"): "Major Negative in Bearish Sign, General in Bullish Sign",
    ("Saturn", "Neptune"): "Major Negative in Bearish Sign, General in Bullish Sign",
    ("Saturn", "Pluto"): "No Effect Found",

    ("Rahu", "Uranus"): "Major Negative in Bearish Sign, General Negative in Bullish Sign",
    ("Ketu", "Uranus"): "Major Negative in Bearish Sign, General Negative in Bullish Sign",
    ("Rahu", "Neptune"): "General Positive (If Neptune Retro/Combust -> Negative)",
    ("Ketu", "Neptune"): "General Positive (If Neptune Retro/Combust -> Negative)",
    ("Rahu", "Pluto"): "No Effect Found",
    ("Ketu", "Pluto"): "No Effect Found",

    ("Uranus", "Neptune"): "Major Negative Momentum",
    ("Uranus", "Pluto"): "No Effect Found"
}

def get_conjunction_effect(p1, p2):
    return CONJUNCTION_RULES.get((p1, p2)) or CONJUNCTION_RULES.get((p2, p1)) or "No Specific Rule Set"
