import tkinter as tk
from tkinter import filedialog as fd
from pathlib import Path
import pandas as pd
import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage, Image
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.app import App

kivy.require('1.11.0')
SAMPLE = Path(__file__).parent.parent / 'inne' / 'sample_img.png'


class Core(GridLayout):
    def __init__(self, **kwargs):
        super(Core, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 3
        self.directory = None
        self.images = []
        self.len_images = None
        self.current_image = None
        self.pos_ = []
        self.neg_ = []

        self.image_lay = GridLayout(cols=2, rows=1)
        self.image = Image(source=str(SAMPLE))
        self.image_data = Label(text='')
        self.image_lay.add_widget(self.image)
        self.image_lay.add_widget(self.image_data)

        self.controls = GridLayout(cols=2, rows=1)
        # self.confirm = Button(text='Confirm')
        # self.confirm.bind(on_press=self._confirm)
        self.open = Button(text='Open')
        self.open.bind(on_press=self._open)
        # self.controls.add_widget(self.confirm)
        self.controls.add_widget(self.open)

        self.rate_lay = GridLayout(rows=1, cols=2)
        self.pos_but = Button(text='Positive')
        self.pos_but.bind(on_press=self._pos)
        self.neg_but = Button(text='Negative')
        self.neg_but.bind(on_press=self._neg)
        self.rate_lay.add_widget(self.pos_but)
        self.rate_lay.add_widget(self.neg_but)

        self.save_lay = GridLayout(rows=1, cols=2)
        self.file_name = TextInput(hint_text='File Name:', font_size=32)
        self.save_but = Button(text='Save')
        self.save_but.bind(on_press=self._save)
        self.save_lay.add_widget(self.file_name)
        self.save_lay.add_widget(self.save_but)

        self.add_widget(self.image_lay)
        self.add_widget(self.controls)

    def _open(self, _):
        root = tk.Tk()
        root.withdraw()
        directory = fd.askdirectory(
            title='Select Directory',
            initialdir='/')
        self.directory = Path(directory)
        for i in self.directory.iterdir():
            if i.suffix in ['.jpg', '.png']:
                self.images.append(i)
        self.current_image = 0
        self.len_images = len(self.images)
        self.image.source = str(self.images[self.current_image])
        self.image.reload()
        self.add_widget(self.rate_lay)

    def _pos(self, _):
        if len(self.images):
            index = self.current_image % self.len_images
            image = str(self.images[self.current_image % self.len_images])
            self.current_image += 1
            self.image.source = str(self.images[self.current_image % self.len_images])
            self.image.reload()
            self.images.pop(index)
            self.len_images = len(self.images)
            self.pos_.append(str(image))
        else:
            self.remove_widget(self.rate_lay)
            self.add_widget(self.save_lay)
            self.image.source = str(SAMPLE)
            self.image.reload()

    def _neg(self, _):
        if len(self.images):
            index = self.current_image % self.len_images
            image = str(self.images[self.current_image % self.len_images])
            self.current_image += 1
            self.image.source = str(self.images[self.current_image % self.len_images])
            self.image.reload()
            self.images.pop(index)
            self.len_images = len(self.images)
            self.neg_.append(str(image))
        else:
            self.remove_widget(self.rate_lay)
            self.add_widget(self.save_lay)
            self.image.source = str(SAMPLE)
            self.image.reload()

    def _save(self, _):
        data = pd.DataFrame(
            {1: self.pos_,
             0: self.neg_}
        )
        file = self.directory / f'{self.file_name.text}.csv'
        data.to_csv(str(file))
        self.remove_widget(self.save_lay)


class ImagesRateApp(App):
    def build(self):
        return Core()


if __name__ == '__main__':
    ImagesRateApp().run()
