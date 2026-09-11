import os
import json
import datetime
import swisseph as swe

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.resources import resource_find

# ऐप बैकग्राउंड
Window.clearcolor = (0.1, 0.1, 0.12, 1)

# -------------------------------------------------------------
# 1. FILE PATH HANDLER (Android Safe Path)
# -------------------------------------------------------------
def get_rules_filepath(filename="conjunction_rules.json"):
    # Kivy resource check
    found = resource_find(filename)
    if found and os.path.exists(found):
        return found
    
    # Absolute local path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    local_path = os.path.join(base_dir, filename)
    return local_path if os.path.exists(local_path) else None

# -------------------------------------------------------------
# 2. SWISS EPHEMERIS CORE ENGINE
# -------------------------------------------------------------
PLANET_IDS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
    "Rahu": swe.MEAN_NODE
}

ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", 
    "Leo", "Virgo", "Libra", "Scorpio", 
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

def calculate_swiss_ephemeris_positions():
    """शुद्ध Swiss Ephemeris से सभी 9+ ग्रहों की सटीक डिग्री प्राप्त करें"""
    now = datetime.datetime.utcnow()
    # UTC Julian Day Berechnung
    julian_day = swe.julday(now.year, now.month, now.day, now.hour + now.minute / 60.0)

    calculated_planets = {}

    for name, p_id in PLANET_IDS.items():
        try:
            # Swiss Ephemeris UT calculation
            res, flags = swe.calc_ut(julian_day, p_id)
            long_deg = res[0]
            speed = res[3]
            
            sign_idx = int(long_deg // 30)
            sign_name = ZODIAC_SIGNS[sign_idx] if 0 <= sign_idx < 12 else "Unknown"
            is_retro = speed < 0  # Negative Speed = Retrograde

            calculated_planets[name] = {
                "deg": long_deg,
                "speed": speed,
                "sign": sign_name,
                "is_retro": is_retro
            }
        except Exception as e:
            continue

    # Ketu Calculation (Rahu + 180 Degrees)
    if "Rahu" in calculated_planets:
        rahu_deg = calculated_planets["Rahu"]["deg"]
        ketu_deg = (rahu_deg + 180.0) % 360.0
        ketu_sign_idx = int(ketu_deg // 30)
        calculated_planets["Ketu"] = {
            "deg": ketu_deg,
            "speed": calculated_planets["Rahu"]["speed"],
            "sign": ZODIAC_SIGNS[ketu_sign_idx],
            "is_retro": True
        }

    return calculated_planets

# -------------------------------------------------------------
# 3. RULES MATCHING ENGINE
# -------------------------------------------------------------
def evaluate_conjunctions():
    # 1. Swiss Ephemeris data fetch
    planets_data = calculate_swiss_ephemeris_positions()
    
    # 2. JSON Rules load
    json_path = get_rules_filepath("conjunction_rules.json")
    if not json_path:
        return ["[ERROR] 'conjunction_rules.json' missing from APK bundle!"]

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            rules = json.load(f)
    except Exception as e:
        return [f"[ERROR] Rules JSON parse failed: {str(e)}"]

    active_effects = []
    planets = list(planets_data.keys())

    # 3. Check Degree Differences (Orb <= 1.0°)
    for i in range(len(planets)):
        for j in range(i + 1, len(planets)):
            p1, p2 = planets[i], planets[j]
            d1 = planets_data[p1]["deg"]
            d2 = planets_data[p2]["deg"]

            diff = abs(d1 - d2)
            if diff > 180:
                diff = 360 - diff

            # Orb Difference Check
            if diff <= 1.0:
                matched = False
                for rule in rules:
                    r1, r2 = rule.get("planet1"), rule.get("planet2")
                    if (p1 == r1 and p2 == r2) or (p1 == r2 and p2 == r1):
                        matched = True
                        
                        # Retrograde Check
                        if rule.get("condition") == "jupiter_retrograde":
                            jup_retro = planets_data.get("Jupiter", {}).get("is_retro", False)
                            effect = rule.get("effect_if_true") if jup_retro else rule.get("effect_if_false")
                        
                        # Sign Type Check
                        elif rule.get("condition") == "sign_type":
                            sign = planets_data.get(p1, {}).get("sign", "")
                            is_bearish = sign in ["Cancer", "Scorpio", "Pisces"]
                            effect = rule.get("effect_bearish") if is_bearish else rule.get("effect_bullish")
                        
                        else:
                            effect = rule.get("effect", "Active Conjunction")

                        r_tag1 = " (R)" if planets_data[p1]["is_retro"] else ""
                        r_tag2 = " (R)" if planets_data[p2]["is_retro"] else ""
                        
                        active_effects.append(
                            f"[b]• {p1}{r_tag1} + {p2}{r_tag2}[/b]\n"
                            f"  [color=00ffcc]Effect:[/color] {effect}\n"
                            f"  [color=888888]Orb Diff: {diff:.2f}° | Sign: {planets_data[p1]['sign']}[/color]"
                        )

                if not matched:
                    active_effects.append(
                        f"[b]• {p1} + {p2}[/b]\n"
                        f"  [color=00ffcc]Effect:[/color] Active Conjunction\n"
                        f"  [color=888888]Orb Diff: {diff:.2f}°[/color]"
                    )

    return active_effects

# -------------------------------------------------------------
# 4. KIVY SCREEN UI
# -------------------------------------------------------------
class DailyTransitScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        heading = Label(
            text="[b]Swiss Ephemeris Conjunctions[/b]",
            font_size='20sp',
            size_hint_y=None,
            height=40,
            markup=True,
            color=(1, 0.8, 0.2, 1)
        )
        layout.add_widget(heading)

        scroll = ScrollView(size_hint=(1, 1))
        
        self.content_label = Label(
            text="Calculating live Swiss Ephemeris transits...",
            font_size='16sp',
            size_hint_y=None,
            markup=True,
            halign='left',
            valign='top',
            color=(1, 1, 1, 1)
        )
        
        self.content_label.bind(
            width=lambda instance, value: setattr(instance, 'text_size', (value, None)),
            texture_size=lambda instance, value: setattr(instance, 'height', value[1])
        )
        
        scroll.add_widget(self.content_label)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def on_enter(self):
        try:
            effects = evaluate_conjunctions()
            if effects:
                self.content_label.text = "\n\n".join(effects)
            else:
                self.content_label.text = "[color=aaaaaa]No Active Planetary Conjunctions (<= 1.0°) Today.[/color]"
        except Exception as e:
            self.content_label.text = f"[color=ff3333][CRASH PREVENTED] Error: {str(e)}[/color]"

# -------------------------------------------------------------
# 5. APP BUILDER
# -------------------------------------------------------------
class AstroTradingApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(DailyTransitScreen(name='daily'))
        return sm

if __name__ == '__main__':
    AstroTradingApp().run()
