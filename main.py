from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
import datetime
import swisseph as swe

# Swiss Ephemeris Lahiri Ayanamsa Setup
swe.set_sid_mode(swe.SIDM_LAHIRI)

# Planet IDs
PLANETS = {
    'Moon': swe.MOON,
    'Sun': swe.SUN,
    'Mercury': swe.MERCURY,
    'Venus': swe.VENUS,
    'Mars': swe.MARS,
    'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN,
    'Rahu': swe.MEAN_NODE,
    'Uranus': swe.URANUS,
    'Neptune': swe.NEPTUNE,
    'Pluto': swe.PLUTO
}

# 27 Nakshatras
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", 
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", 
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", 
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

# Image Rules Engine
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

def get_planet_pos(date_obj, planet_id):
    julian_day = swe.julday(date_obj.year, date_obj.month, date_obj.day, 5.5)
    res, _ = swe.calc_ut(julian_day, planet_id, swe.FLG_SIDEREAL)
    longitude = res[0]
    nak_num = int(longitude / (360 / 27))
    pada = int((longitude % (360 / 27)) / (360 / 108)) + 1
    return longitude, NAKSHATRAS[nak_num], pada

class AstroTradingApp(App):
    def build(self):
        self.title = "Astro Trading Dashboard"
        panel = TabbedPanel(do_default_tab=False)

        # Tab 1: Daily View
        t1 = TabbedPanelHeader(text="Daily")
        t1.content = self.create_daily_view()
        panel.add_widget(t1)

        # Tab 2: Weekly View
        t2 = TabbedPanelHeader(text="Weekly")
        t2.content = self.create_weekly_view()
        panel.add_widget(t2)

        # Tab 3: Monthly View & Search
        t3 = TabbedPanelHeader(text="Monthly/Search")
        t3.content = self.create_monthly_view()
        panel.add_widget(t3)

        # Tab 4: Nakshatra View
        t4 = TabbedPanelHeader(text="Nakshatra")
        t4.content = self.create_nakshatra_view()
        panel.add_widget(t4)

        return panel

    def create_daily_view(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        today = datetime.date.today()
        layout.add_widget(Label(text=f"Daily Transit Impact ({today})", font_size=18, bold=True, size_hint_y=None, height=40))
        
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        content.bind(minimum_height=content.setter('height'))

        p_positions = {p: get_planet_pos(today, p_id)[0] for p, p_id in PLANETS.items()}
        
        p_keys = list(PLANETS.keys())
        found = False
        for i in range(len(p_keys)):
            for j in range(i+1, len(p_keys)):
                p1, p2 = p_keys[i], p_keys[j]
                diff = abs(p_positions[p1] - p_positions[p2])
                if diff <= 6.0:
                    found = True
                    effect = get_conjunction_effect(p1, p2)
                    lbl = Label(text=f"[CONJUNCTION] {p1} + {p2}\nEffect: {effect}", 
                                font_size=14, size_hint_y=None, height=60)
                    content.add_widget(lbl)
        
        if not found:
            content.add_widget(Label(text="No major conjunction active today.", size_hint_y=None, height=40))

        scroll.add_widget(content)
        layout.add_widget(scroll)
        return layout

    def create_weekly_view(self):
        layout = BoxLayout(orientation='vertical', padding=10)
        layout.add_widget(Label(text="Weekly Overview (Next 7 Days)", font_size=18, bold=True, size_hint_y=None, height=40))
        
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        content.bind(minimum_height=content.setter('height'))

        today = datetime.date.today()
        for d in range(7):
            day_date = today + datetime.timedelta(days=d)
            _, nak, pada = get_planet_pos(day_date, swe.MOON)
            lbl = Label(text=f"{day_date.strftime('%a, %d %b')}: Moon in {nak} (Pada {pada})", size_hint_y=None, height=30)
            content.add_widget(lbl)

        scroll.add_widget(content)
        layout.add_widget(scroll)
        return layout

    def create_monthly_view(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        content.bind(minimum_height=content.setter('height'))
        
        today = datetime.date.today()
        for d in range(30):
            day_date = today + datetime.timedelta(days=d)
            _, nak, pada = get_planet_pos(day_date, swe.MOON)
            txt = f"{day_date}: Moon in {nak} (Pada {pada})"
            content.add_widget(Label(text=txt, size_hint_y=None, height=30))

        scroll.add_widget(content)
        layout.add_widget(scroll)
        return layout

    def create_nakshatra_view(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text="Select Planet to View Nakshatra", font_size=18, bold=True, size_hint_y=None, height=40))

        spinner = Spinner(text='Moon', values=tuple(PLANETS.keys()), size_hint_y=None, height=45)
        res_label = Label(text="", font_size=16)

        def update_nakshatra(spinner_obj, text):
            p_id = PLANETS[text]
            long, nak, pada = get_planet_pos(datetime.date.today(), p_id)
            res_label.text = f"Planet: {text}\nDegree: {round(long, 2)}°\nNakshatra: {nak}\nPada: {pada}"

        spinner.bind(text=update_nakshatra)
        update_nakshatra(spinner, 'Moon')

        layout.add_widget(spinner)
        layout.add_widget(res_label)
        return layout

if __name__ == '__main__':
    AstroTradingApp().run()
