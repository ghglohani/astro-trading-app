from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
import datetime
import math

# Pure Python Planetary Orbital Calculations (Ephemeris-Free)
LAHIRI_AYANAMSA = 24.1

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", 
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", 
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", 
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

CONJUNCTION_RULES = {
    ("Moon", "Mars"): "General Positive Momentum",
    ("Moon", "Mercury"): "Sometimes Positive and Sometimes Negative Momentum",
    ("Moon", "Jupiter"): "Sometimes Positive and Sometimes Negative Momentum",
    ("Moon", "Venus"): "Majority times Negative Momentum",
    ("Moon", "Saturn"): "Sometimes Positive and Sometimes Negative Momentum",
    ("Moon", "Uranus"): "General Positive Momentum",
    ("Mars", "Mercury"): "General Positive Momentum",
    ("Mars", "Jupiter"): "General Negative Momentum",
    ("Jupiter", "Uranus"): "Major Positive Momentum",
    ("Saturn", "Uranus"): "Major Negative in Bearish Sign",
}

# Average planetary daily motion in degrees
PLANET_RATES = {
    'Sun': (280.46, 0.985647),
    'Moon': (218.32, 13.176396),
    'Mercury': (252.25, 4.092334),
    'Venus': (181.98, 1.602130),
    'Mars': (355.43, 0.524033),
    'Jupiter': (34.35, 0.083091),
    'Saturn': (50.08, 0.033459),
    'Uranus': (314.05, 0.011728),
    'Neptune': (304.35, 0.005981),
    'Pluto': (238.90, 0.003960)
}

def calculate_planet_longitude(date_obj, planet):
    epoch = datetime.date(2000, 1, 1)
    days_since_epoch = (date_obj - epoch).days
    
    base_long, rate = PLANET_RATES.get(planet, (0.0, 1.0))
    tropical_deg = (base_long + rate * days_since_epoch) % 360
    
    # Sidereal (Lahiri) Longitude
    sidereal_deg = (tropical_deg - LAHIRI_AYANAMSA) % 360
    nak_num = int(sidereal_deg / (360 / 27))
    pada = int((sidereal_deg % (360 / 27)) / (360 / 108)) + 1
    return sidereal_deg, NAKSHATRAS[nak_num], pada

class AstroTradingApp(App):
    def build(self):
        self.title = "Astro Trading Dashboard"
        panel = TabbedPanel(do_default_tab=False)

        t1 = TabbedPanelHeader(text="Daily")
        t1.content = self.create_daily_view()
        panel.add_widget(t1)

        t2 = TabbedPanelHeader(text="Weekly")
        t2.content = self.create_weekly_view()
        panel.add_widget(t2)

        t3 = TabbedPanelHeader(text="Monthly")
        t3.content = self.create_monthly_view()
        panel.add_widget(t3)

        t4 = TabbedPanelHeader(text="Nakshatra")
        t4.content = self.create_nakshatra_view()
        panel.add_widget(t4)

        return panel

    def create_daily_view(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        today = datetime.date.today()
        layout.add_widget(Label(text=f"Daily Market Transit ({today})", font_size=18, bold=True, size_hint_y=None, height=40))
        
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        content.bind(minimum_height=content.setter('height'))

        planets_list = list(PLANET_RATES.keys())
        p_positions = {p: calculate_planet_longitude(today, p)[0] for p in planets_list}
        
        found = False
        for i in range(len(planets_list)):
            for j in range(i+1, len(planets_list)):
                p1, p2 = planets_list[i], planets_list[j]
                diff = abs(p_positions[p1] - p_positions[p2])
                if diff <= 6.0 or diff >= 354.0:
                    found = True
                    effect = CONJUNCTION_RULES.get((p1, p2)) or CONJUNCTION_RULES.get((p2, p1)) or "Active Planetary Conjunction"
                    lbl = Label(text=f"[CONJUNCTION] {p1} + {p2}\nEffect: {effect}", 
                                font_size=14, size_hint_y=None, height=60)
                    content.add_widget(lbl)
        
        if not found:
            content.add_widget(Label(text="No major active conjunction today.", size_hint_y=None, height=40))

        scroll.add_widget(content)
        layout.add_widget(scroll)
        return layout

    def create_weekly_view(self):
        layout = BoxLayout(orientation='vertical', padding=10)
        layout.add_widget(Label(text="Weekly Moon Transit", font_size=18, bold=True, size_hint_y=None, height=40))
        
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        content.bind(minimum_height=content.setter('height'))

        today = datetime.date.today()
        for d in range(7):
            day_date = today + datetime.timedelta(days=d)
            _, nak, pada = calculate_planet_longitude(day_date, 'Moon')
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
            _, nak, pada = calculate_planet_longitude(day_date, 'Moon')
            txt = f"{day_date}: Moon in {nak} (Pada {pada})"
            content.add_widget(Label(text=txt, size_hint_y=None, height=30))

        scroll.add_widget(content)
        layout.add_widget(scroll)
        return layout

    def create_nakshatra_view(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text="Select Planet to View Nakshatra", font_size=18, bold=True, size_hint_y=None, height=40))

        spinner = Spinner(text='Moon', values=tuple(PLANET_RATES.keys()), size_hint_y=None, height=45)
        res_label = Label(text="", font_size=16)

        def update_nakshatra(spinner_obj, text):
            long_val, nak, pada = calculate_planet_longitude(datetime.date.today(), text)
            res_label.text = f"Planet: {text}\nDegree: {round(long_val, 2)}°\nNakshatra: {nak}\nPada: {pada}"

        spinner.bind(text=update_nakshatra)
        update_nakshatra(spinner, 'Moon')

        layout.add_widget(spinner)
        layout.add_widget(res_label)
        return layout

if __name__ == '__main__':
    AstroTradingApp().run()
