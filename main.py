import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label

def check_conjunction_effects(planets_data):
    """
    planets_data = {
       "Sun": {"deg": 142.5, "is_retro": False, "sign": "Virgo"},
       "Moon": {"deg": 142.8, "is_retro": False, "sign": "Virgo"},
       ...
    }
    """
    if not os.path.exists("conjunction_rules.json"):
        return ["Rules file not found!"]

    with open("conjunction_rules.json", "r") as f:
        rules = json.load(f)

    active_effects = []
    planets = list(planets_data.keys())

    # 1 डिग्री की रेंज में युति (Conjunction) चेक करें
    for i in range(len(planets)):
        for j in range(i + 1, len(planets)):
            p1, p2 = planets[i], planets[j]
            d1 = planets_data[p1]["deg"]
            d2 = planets_data[p2]["deg"]

            diff = abs(d1 - d2)
            if diff > 180:
                diff = 360 - diff

            # अगर दोनों ग्रहों का डिफ़रेंस <= 1° है
            if diff <= 1.0:
                matched = False
                for rule in rules:
                    r1, r2 = rule["planet1"], rule["planet2"]
                    if (p1 == r1 and p2 == r2) or (p1 == r2 and p2 == r1):
                        matched = True
                        
                        # वक्री (Retrograde) कंडीशन चेक
                        if rule.get("condition") == "jupiter_retrograde":
                            jup_retro = planets_data.get("Jupiter", {}).get("is_retro", False)
                            effect = rule["effect_if_true"] if jup_retro else rule["effect_if_false"]
                        
                        # राशि (Sign) कंडीशन चेक
                        elif rule.get("condition") == "sign_type":
                            sign = planets_data.get(p1, {}).get("sign", "")
                            is_bearish = sign in ["Cancer", "Scorpio", "Pisces"]
                            effect = rule["effect_bearish"] if is_bearish else rule["effect_bullish"]
                        
                        else:
                            effect = rule.get("effect", "Active Conjunction")

                        active_effects.append(f"[CONJUNCTION] {p1} + {p2}\nEffect: {effect}")

                if not matched:
                    active_effects.append(f"[CONJUNCTION] {p1} + {p2}\nEffect: Active Conjunction")

    return active_effects
