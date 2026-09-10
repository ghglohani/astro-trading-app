from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
import datetime
import swisseph as swe
from rules import get_conjunction_effect

swe.set_sid_mode(swe.SIDM_LAHIRI)

PLANETS = {
    'Moon': swe.MOON, 'Sun': swe.SUN, 'Mercury': swe.MERCURY,
    'Venus': swe.VENUS, 'Mars': swe.MARS, 'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN, 'Rahu': swe.MEAN_NODE, 'Uranus': swe.URANUS,
    'Neptune': swe.NEPTUNE, 'Pluto': swe.PLUTO
}

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", 
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", 
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", 
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

def get_planet_pos(date_obj, planet_id):
    julian_day = swe.julday(date_obj.year, date_obj.month, date_obj.day, 5.5)
    res, _ = swe.calc_ut(julian_day, planet_id, swe.FLG_SIDEREAL)
    longitude = res[0]
    nak_num = int(longitude / (360 / 27))
    pada = int((longitude % (360 / 27)) / (360 / 108)) + 1
    return longitude, NAKSHATRAS[nak_num], pada

class MainApp(App):
    def build(self):
        self.title = "Astro Trading Dashboard"
        panel = TabbedPanel(do_default_tab=False)

        # Tab 1: Daily
        t1 = TabbedPanelHeader(text="Daily")
        t1.content = self.create_daily_view()
        panel.add_widget(t1)

        # Tab 2: Weekly
        t2 = TabbedPanelHeader(text="Weekly")
        t2.content = self.create_weekly_view()
        panel.add_widget(t2)

        # Tab 3: Monthly & Search
        t3 = TabbedPanelHeader(text="Monthly/Search")
        t3.content = self.create_monthly_view()
        panel.add_widget(t3)

        # Tab 4: Nakshatra Chart
        t4 = TabbedPanelHeader(text="Nakshatra")
        t4.content = self.create_nakshatra_view()
        panel.add_widget(t4)

        return panel

    def create_daily_view(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        today = datetime.date.today()
        layout.add_widget(Label(text=f"Daily Transit Market Impact ({today})", font_size=20, bold=True, size_hint_y=None, height=40))
        
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        content.bind(minimum_height=content.setter('height'))

        p_positions = {p: get_planet_pos(today, p_id)[0] for p, p_id in PLANETS.items()}
        
        # Check Conjunctions (within 6 degrees)
        p_keys = list(PLANETS.keys())
        found = False
        for i in range(len(p_keys)):
            for j in range(i+1, len(p_keys)):
                p1, p2 = p_keys[i], p_keys[j]
                diff = abs(p_positions[p1] - p_positions[p2])
                if diff <= 6.0:
                    found = True
                    effect = get_conjunction_effect(p1, p2)
                    lbl = Label(text=f"[ACTIVE CONJUNCTION] {p1} + {p2}\nEffect: {effect}", 
                                font_size=14, size_hint_y=None, height=60)
                    content.add_widget(lbl)
        
        if not found:
            content.add_widget(Label(text="No major planetary conjunction active today.", size_hint_y=None, height=40))

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
            _, nak, _ = get_planet_pos(day_date, swe.MOON)
            lbl = Label(text=f"{day_date.strftime('%A, %d %b')}: Moon in {nak} Nakshatra", size_hint_y=None, height=30)
            content.add_widget(lbl)

        scroll.add_widget(content)
        layout.add_widget(scroll)
        return layout

    def create_monthly_view(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        search_bar = TextInput(hint_text="Search planet or nakshatra...", size_hint_y=None, height=40)
        layout.add_widget(search_bar)
        
        scroll = ScrollView()
        self.search_results = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.search_results.bind(minimum_height=self.search_results.setter('height'))
        
        today = datetime.date.today()
        for d in range(30):
            day_date = today + datetime.timedelta(days=d)
            _, nak, pada = get_planet_pos(day_date, swe.MOON)
            txt = f"{day_date}: Moon in {nak} (Pada {pada})"
            self.search_results.add_widget(Label(text=txt, size_hint_y=None, height=30))

        scroll.add_widget(self.search_results)
        layout.add_widget(scroll)
        return layout

    def create_nakshatra_view(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text="Select Planet to View Nakshatra", font_size=18, bold=True, size_hint_y=None, height=40))

        spinner = Spinner(text='Moon', values=tuple(PLANETS.keys()), size_hint_y=None, height=45)
        res_label = Label(text="", font_size=16)

        def update_nakshatra(spinner, text):
            p_id = PLANETS[text]
            long, nak, pada = get_planet_pos(datetime.date.today(), p_id)
            res_label.text = f"Planet: {text}\nDegree: {round(long, 2)}°\nNakshatra: {nak}\nPada: {pada}"

        spinner.bind(text=update_nakshatra)
        update_nakshatra(spinner, 'Moon')

        layout.add_widget(spinner)
        layout.add_widget(res_label)
        return layout

if __name__ == '__main__':
    MainApp().run()
