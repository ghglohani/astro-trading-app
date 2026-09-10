from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
import datetime
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const

PLANETS = {
    'Moon': const.MOON,
    'Sun': const.SUN,
    'Mercury': const.MERCURY,
    'Venus': const.VENUS,
    'Mars': const.MARS,
    'Jupiter': const.JUPITER,
    'Saturn': const.SATURN,
    'Uranus': const.URANUS,
    'Neptune': const.NEPTUNE,
    'Pluto': const.PLUTO
}

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

def get_planet_pos(date_obj, planet_code):
    dt = Datetime(date_obj.strftime('%Y/%m/%d'), '00:00', '+00:00')
    pos = GeoPos('00n00', '000e00')
    chart = Chart(dt, pos, hsys=const.HOUSES_PLACIDUS)
    obj = chart.get(planet_code)
    
    # Sidereal Adjustment (approx Ayanamsa)
    lon = (obj.lon - 24.1) % 360
    nak_num = int(lon / (360 / 27))
    pada = int((lon % (360 / 27)) / (360 / 108)) + 1
    return lon, NAKSHATRAS[nak_num], pada

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

        p_positions = {p_name: get_planet_pos(today, p_code)[0] for p_name, p_code in PLANETS.items()}
        
        p_keys = list(PLANETS.keys())
        found = False
        for i in range(len(p_keys)):
            for j in range(i+1, len(p_keys)):
                p1, p2 = p_keys[i], p_keys[j]
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
            _, nak, pada = get_planet_pos(day_date, PLANETS['Moon'])
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
            _, nak, pada = get_planet_pos(day_date, PLANETS['Moon'])
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
            p_code = PLANETS[text]
            long_val, nak, pada = get_planet_pos(datetime.date.today(), p_code)
            res_label.text = f"Planet: {text}\nDegree: {round(long_val, 2)}°\nNakshatra: {nak}\nPada: {pada}"

        spinner.bind(text=update_nakshatra)
        update_nakshatra(spinner, 'Moon')

        layout.add_widget(spinner)
        layout.add_widget(res_label)
        return layout

if __name__ == '__main__':
    AstroTradingApp().run()
