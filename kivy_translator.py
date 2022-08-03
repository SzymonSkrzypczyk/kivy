from translate import Translator
import kivy
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
import requests
from bs4 import BeautifulSoup
import mysql.connector as con

kivy.require('1.11.0')
LANGUAGES = {
    'English': 'en',
    'Polish': 'pl',
    'German': 'de',
    'French': 'fr',
    'Japanese': 'ja'
}


class Core(GridLayout):
    def __init__(self, **kwargs):
        super(Core, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 3
        self.spacing = 4

        self.lang_lay = GridLayout(rows=1, cols=2)
        self.words_lay = GridLayout(rows=1, cols=3)

        self.original_lang = Spinner(text='English', values=tuple(LANGUAGES.keys()))
        self.target_lang = Spinner(text='Polish', values=tuple(LANGUAGES.keys()))
        self.lang_lay.add_widget(self.original_lang)
        self.lang_lay.add_widget(self.target_lang)

        self.original_text = TextInput(hint_text='Enter...', multiline=True, font_size=32)
        self.target_text = TextInput(multiline=True, font_size=32)
        # self.change_but = Button(text='Change')
        self.target_text.disabled = True
        self.words_lay.add_widget(self.original_text)
        # self.words_lay.add_widget(self.change_but)
        self.words_lay.add_widget(self.target_text)

        self.transale_but = Button(text='Translate')
        self.transale_but.bind(on_press=self.translate)

        self.add_widget(self.lang_lay)
        self.add_widget(self.words_lay)
        self.add_widget(self.transale_but)

    def translate(self, _):
        to_lang = LANGUAGES[self.target_lang.text]
        from_lang = LANGUAGES[self.original_lang.text]
        original_text = self.original_text.text
        tr = Translator(from_lang=from_lang, to_lang=to_lang)
        self.target_text.text = tr.translate(original_text)


class TransApp(App):
    def build(self):
        return Core()


if __name__ == '__main__':
    TransApp().run()
