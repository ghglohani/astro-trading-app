import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

# स्क्रीन का बैकग्राउंड डार्क रखने के लिए
Window.clearcolor = (0.1, 0.1, 0.12, 1)

# --- 1. CONJUNCTION LOGIC FUNCTION ---
def check_conjunction_effects(planets_data):
    """
    planets_data structure example:
    {
       "Moon": {"deg": 120.5, "is_retro": False, "sign": "Leo"},
       "Mars": {"deg": 121.2, "is_retro": False, "sign": "Leo"},
       "Jupiter": {"deg": 45.0, "is_retro": True, "sign": "Taurus"}
    }
    """
    json_path = "conjunction_rules.json"
    if not os.path.exists(json_path):
        return ["[ERROR] conjunction_rules.json file missing!"]

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            rules = json.load(f)
    except Exception as e:
        return [f"[ERROR] JSON read failed: {str(e)}"]

    active_effects = []
    planets = list(planets_data.keys())

    # हर दो ग्रहों के बीच 1 डिग्री युति (Conjunction) चेक करें
    for i in range(len(planets)):
        for j in range(i + 1, len(planets)):
            p1, p2 = planets[i], planets[j]
            d1 = planets_data[p1].get("deg", 0.0)
            d2 = planets_data[p2].get("deg", 0.0)

            diff = abs(d1 - d2)
            if diff > 180:
                diff = 360 - diff

            # Orb Difference <= 1.0 Degree
            if diff <= 1.0:
                matched = False
                for rule in rules:
                    r1, r2 = rule.get("planet1"), rule.get("planet2")
                    if (p1 == r1 and p2 == r2) or (p1 == r2 and p2 == r1):
                        matched = True
                        
                        # Condition: Retrograde Check
                        if rule.get("condition") == "jupiter_retrograde":
                            jup_retro = planets_data.get("Jupiter", {}).get("is_retro", False)
                            effect = rule.get("effect_if_true") if jup_retro else rule.get("effect_if_false")
                        
                        # Condition: Bullish / Bearish Sign Check
                        elif rule.get("condition") == "sign_type":
                            sign = planets_data.get(p1, {}).get("sign", "")
                            is_bearish = sign in ["Cancer", "Scorpio", "Pisces"]
                            effect = rule.get("effect_bearish") if is_bearish else rule.get("effect_bullish")
                        
                        else:
                            effect = rule.get("effect", "Active Conjunction")

                        active_effects.append(f"[b]• {p1} + {p2}[/b]\n  [color=00ffcc]Effect:[/color] {effect}")

                if not matched:
                    active_effects.append(f"[b]• {p1} + {p2}[/b]\n  [color=00ffcc]Effect:[/color] General Conjunction Active")

    return active_effects


# --- 2. DAILY SCREEN WITH SCROLLVIEW ---
class DailyTransitScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Main Layout
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # Heading Label
        heading = Label(
            text="[b]Daily Astro Conjunctions[/b]",
            font_size='22sp',
            size_hint_y=None,
            height=40,
            markup=True,
            color=(1, 0.8, 0.2, 1)
        )
        layout.add_widget(heading)

        # ScrollView Layout
        scroll = ScrollView(size_hint=(1, 1))
        
        self.content_label = Label(
            text="Loading Transits...",
            font_size='17sp',
            size_hint_y=None,
            markup=True,
            halign='left',
            valign='top',
            color=(1, 1, 1, 1)
        )
        
        # Auto height binding for ScrollView text
        self.content_label.bind(
            width=lambda instance, value: setattr(instance, 'text_size', (value, None)),
            texture_size=lambda instance, value: setattr(instance, 'height', value[1])
        )
        
        scroll.add_widget(self.content_label)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def on_enter(self):
        # यहाँ अपना Swiss Ephemeris / Real Planets Data जोड़ें
        # Sample Planet Data (Degree Differences <= 1.0 Check)
        sample_planets_data = {
            "Moon": {"deg": 142.5, "is_retro": False, "sign": "Leo"},
            "Mars": {"deg": 143.1, "is_retro": False, "sign": "Leo"},
            "Jupiter": {"deg": 88.0, "is_retro": True, "sign": "Gemini"},
            "Rahu": {"deg": 88.5, "is_retro": True, "sign": "Gemini"},
            "Saturn": {"deg": 320.0, "is_retro": False, "sign": "Aquarius"}
        }

        # Check Conjunctions
        effects = check_conjunction_effects(sample_planets_data)

        if effects:
            self.content_label.text = "\n\n".join(effects)
        else:
            self.content_label.text = "No Active Conjunctions Found Today."


# --- 3. KIVY MAIN APP CLASS ---
class AstroTradingApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(DailyTransitScreen(name='daily'))
        return sm

if __name__ == '__main__':
    AstroTradingApp().run()
