import tkinter as tk
from tkinter import filedialog as fd
from pathlib import Path
from uuid import uuid4
import kivy
from PIL import Image as Img
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage, Image
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.app import App

kivy.require('1.11.0')
SAMPLE = Path(__file__).parent.parent / 'inne' / 'sample_img.png'
TEMP_FILE = Path(__file__).parent / 'temp.png'
TEMP_FILE.touch(exist_ok=True)


class Core(GridLayout):
    def __init__(self, **kwargs):
        super(Core, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 3
        self.file = None

        self.image_lay = GridLayout(cols=2, rows=1)
        self.image = Image(source=str(SAMPLE))
        self.image_crop = Image(source=str(SAMPLE))
        self.image_lay.add_widget(self.image)
        self.image_lay.add_widget(self.image_crop)

        self.controls = GridLayout(cols=3, rows=1)
        self.open = Button(text='Open')
        self.open.bind(on_press=self._open)
        self.save = Button(text='Save')
        self.save.bind(on_press=self._save)
        self.show = Button(text='Show')
        self.show.bind(on_press=self._show)
        self.controls.add_widget(self.open)
        self.controls.add_widget(self.save)
        self.controls.add_widget(self.show)

        self.slider_lay = GridLayout(rows=4, cols=2)
        self.slider_x_beg = Slider(min=1, max=400)
        self.slider_x_beg.bind(value=self.on_val1)
        self.slider_x_lab = Label(text='1')
        self.slider_y_beg = Slider(min=1, max=400)
        self.slider_y_beg.bind(value=self.on_val2)
        self.slider_y_lab = Label(text='1')
        self.slider_x_end = Slider(min=1, max=400)
        self.slider_x_end.bind(value=self.on_val3)
        self.slider_x_lab_end = Label(text='1')
        self.slider_y_end = Slider(min=1, max=400)
        self.slider_y_end.bind(value=self.on_val4)
        self.slider_y_lab_end = Label(text='1')

        self.slider_lay.add_widget(self.slider_x_beg)
        self.slider_lay.add_widget(self.slider_x_lab)
        self.slider_lay.add_widget(self.slider_y_beg)
        self.slider_lay.add_widget(self.slider_y_lab)
        self.slider_lay.add_widget(self.slider_x_end)
        self.slider_lay.add_widget(self.slider_x_lab_end)
        self.slider_lay.add_widget(self.slider_y_end)
        self.slider_lay.add_widget(self.slider_y_lab_end)

        self.add_widget(self.image_lay)
        self.add_widget(self.controls)

    def _open(self, _):
        self.remove_widget(self.slider_lay)
        root = tk.Tk()
        root.withdraw()
        file = fd.askopenfilename(
            title='Select a File',
            initialdir='/',
            filetypes=[("PNG", "*.png"), ('JPEG', '*.jpg')])
        if file:
            self.file = Path(file)
            self.image.source = str(self.file)
            self.image.reload()
            self.add_widget(self.slider_lay)
            img = Img.open(str(self.file))
            self.slider_x_beg.max = img.size[0]
            self.slider_y_beg.max = img.size[1]
            self.slider_x_end.max = img.size[0]
            self.slider_y_end.max = img.size[1]

    def _save(self, _):
        ...

    def _show(self, _):
        img = Img.open(str(self.file))
        cropped_img = img.crop((int(self.slider_x_lab.text),
                                int(self.slider_y_lab.text),
                                int(self.slider_x_lab_end.text),
                                int(self.slider_y_lab_end.text)))
        cropped_img.save(str(TEMP_FILE))
        self.image_crop.source = str(TEMP_FILE)
        self.image_crop.reload()

    def on_val1(self, _, val):
        self.slider_x_lab.text = str(int(val))

    def on_val2(self, _, val):
        self.slider_y_lab.text = str(int(val))

    def on_val3(self, _, val):
        self.slider_x_lab_end.text = str(int(val))

    def on_val4(self, _, val):
        self.slider_y_lab_end.text = str(int(val))


class CropApp(App):
    def build(self):
        return Core()


if __name__ == '__main__':
    CropApp().run()
    TEMP_FILE.unlink()
