"""
App created in order to create datasets based on images with either positive or negative sentiment
, which is evaluated by a user
"""
import tkinter as tk
from tkinter.filedialog import askdirectory
from pathlib import Path
import pandas as pd
import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.app import App
from web_scraping.german_words import get_results

kivy.require('1.11.0')
MAX_ROWS = 20
NO_IMAGE = Path(__file__).parent.parent / 'inne' / 'sample_img.png'


class Core(GridLayout):
    def __init__(self, **kwargs):
        super(Core, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 3
        self.directory = None
        self.categories = None
        self.images = []
        self.len_images = 978987965858
        self.current_image = 0
        self.final = {}
        self.label_buttons = {}

        self.image_lay = GridLayout(rows=1, cols=3)
        self.previous = Button(text='Previous')
        self.previous.bind(on_press=self._previous)
        self.img1 = Image(source=str(NO_IMAGE))
        self.next = Button(text='Next')
        self.next.bind(on_press=self._next)
        self.image_lay.add_widget(self.previous)
        self.image_lay.add_widget(self.img1)
        self.image_lay.add_widget(self.next)

        self.controls_lay = GridLayout(rows=1, cols=2)
        self.labels_but = Button(text='Labels')
        self.labels_but.bind(on_press=self.labels)
        self.directory_but = Button(text='Directory')
        self.directory_but.bind(on_press=self.get_directory)
        self.controls_lay.add_widget(self.directory_but)
        self.controls_lay.add_widget(self.labels_but)

        self.labels_lay = GridLayout(rows=1, cols=2)
        self.confirm = Button(text='Confirm')
        self.confirm.bind(on_press=self._confirm)
        self.spinner = Spinner(text='2', values=[str(i) for i in range(2, 21)])
        self.labels_lay.add_widget(self.spinner)
        self.labels_lay.add_widget(self.confirm)

        self.assess_lay = GridLayout(rows=2, cols=1)
        self.upper_assess = Button(text='Confirm')
        self.lower_assess = GridLayout(rows=5, cols=4)
        self.assess_lay.add_widget(self.upper_assess)
        self.assess_lay.add_widget(self.lower_assess)

        self.save_lay = GridLayout(cols=2, rows=1)
        self.file_name = TextInput(hint_text='File Name:', font_size=24)
        self.save_but = Button(text='Save')
        self.save_but.bind(on_press=self.save)
        self.save_lay.add_widget(self.file_name)
        self.save_lay.add_widget(self.save_but)

        self.add_widget(self.image_lay)
        self.add_widget(self.controls_lay)

    def get_directory(self, _):
        root = tk.Tk()
        root.withdraw()
        directory = askdirectory(
            title='Select Directory',
            initialdir='/', )
        self.directory = Path(directory)
        for i in self.directory.iterdir():
            if i.suffix in ['.jpg', '.png']:
                self.images.append(i)
        self.len_images = len(self.images)

    def labels(self, _):
        self.remove_widget(self.labels_lay)
        self.add_widget(self.labels_lay)

    def _confirm(self, _):
        self.remove_widget(self.labels_lay)
        for i in range(int(self.spinner.text)):
            but = Button(text=f'{i}')
            but.bind(on_press=self.current_)
            self.label_buttons[but] = i
            self.lower_assess.add_widget(but)
        self.add_widget(self.assess_lay)

    def _next(self, _):
        if self.current_image > self.len_images:
            self.current_image = 0
        if self.images:
            self.current_image += 1
            self.img1.source = str(self.images[self.current_image % self.len_images])
            self.img1.reload()

    def _previous(self, _):
        if self.current_image < 0:
            self.current_image = self.len_images
        if self.images:
            self.current_image -= 1
            self.img1.source = str(self.images[self.current_image % self.len_images])
            self.img1.reload()

    def current_(self, but):
        if len(self.images) and self.current_image < self.len_images:
            self.final[str(self.images[self.current_image])] = but.text
            self.images.pop(self.current_image)
            self.len_images = len(self.images)
            self._next(but)
            print(but.text)
        else:
            # success !
            self.remove_widget(self.assess_lay)
            self.add_widget(self.save_lay)

    def save(self, _):
        data = pd.DataFrame([self.final])
        path = self.directory / f'{self.file_name.text}.csv'
        data.to_csv(str(path))
        self.remove_widget(self.save_lay)


class LabelApp(App):
    def build(self):
        return Core()


if __name__ == '__main__':
    LabelApp().run()
