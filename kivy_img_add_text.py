"""
App created in order to add text onto an image
"""
from random import choice
import tkinter as tk
from tkinter import filedialog as fd
from pathlib import Path
from PIL import Image as Img, ImageFilter
import cv2
import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.image import AsyncImage, Image
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.app import App

kivy.require('1.11.0')
SAMPLE = Path(__file__).parent.parent / 'inne' / 'sample_img.png'
FONTS = [i for i in dir(cv2) if i.startswith('FONT_')]
TEMP_IMG = Path(__file__).parent / 'temp.jpg'
TEMP_IMG.touch(exist_ok=True)
TEMP2_IMG = Path(__file__).parent / 'temp2.jpg'
TEMP2_IMG.touch(exist_ok=True)


class Core(GridLayout):
    def __init__(self, **kwargs):
        super(Core, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 3
        self.file = None
        self.image_width = 100
        self.image_height = 100
        self.current_x = 0
        self.current_y = 0
        self.font_size = 12
        self.font_name = FONTS[0]
        self.font_col = (209, 80, 0, 255)

        self.img_lay = GridLayout(cols=2, rows=1)
        self.img1 = Image(source=str(SAMPLE))
        self.img2 = Image(source=str(SAMPLE))
        self.img_lay.add_widget(self.img1)
        self.img_lay.add_widget(self.img2)

        self.controls = GridLayout(cols=5, rows=1)
        self.open = Button(text='Open')
        self.open.bind(on_press=self._open)
        self.clear = Button(text='Clear')
        self.clear.bind(on_press=self._clear)
        self.add = Button(text='Add')
        self.add.bind(on_press=self._add)
        self.save = Button(text='Save')
        self.save.bind(on_press=self._save)
        self.settings = Button(text='Settings')
        self.settings.bind(on_press=self._settings)
        self.controls.add_widget(self.open)
        self.controls.add_widget(self.clear)
        self.controls.add_widget(self.add)
        self.controls.add_widget(self.save)
        self.controls.add_widget(self.settings)

        self.pos_lay = GridLayout(cols=1, rows=3)

        self.x_lay = GridLayout(cols=2, rows=1)
        self.x_slider = Slider(min=0, max=self.image_width)
        self.x_slider.bind(value=self._on_val1)
        self.x_text = Label(text='0')
        self.x_lay.add_widget(self.x_slider)
        self.x_lay.add_widget(self.x_text)

        self.y_lay = GridLayout(cols=2, rows=1)
        self.y_slider = Slider(min=0, max=self.image_height)
        self.y_slider.bind(value=self._on_val2)
        self.y_text = Label(text='0')
        self.y_lay.add_widget(self.y_slider)
        self.y_lay.add_widget(self.y_text)
        self.text = TextInput(hint_text='Your Text', font_size=24)

        self.pos_lay.add_widget(self.text)
        self.pos_lay.add_widget(self.x_lay)
        self.pos_lay.add_widget(self.y_lay)

        self.add_widget(self.img_lay)
        self.add_widget(self.controls)
        self.add_widget(self.pos_lay)

    def _open(self, _):
        root = tk.Tk()
        root.withdraw()
        file = fd.askopenfilename(
            title='Select File',
            initialdir='/',
            filetypes=[('PNG', '*.png'), ('JPEG', '*.jpg')])
        if file:
            self.file = Path(file)
            self.img1.source = str(self.file)

            img = Img.open(str(self.file))
            self.image_width, self.image_height = img.size
            self.x_slider.max = self.image_width
            self.y_slider.max = self.image_height

            TEMP_IMG.write_bytes(self.file.read_bytes())
            TEMP2_IMG.write_bytes(self.file.read_bytes())
            self.img2.source = str(TEMP_IMG)
            self.img1.reload()
            self.img2.reload()

    def _clear(self, _):
        self.file = None
        self.text.text = ''
        self.img1.source = str(SAMPLE)
        self.img2.source = str(SAMPLE)
        self.img1.reload()
        self.img2.reload()
        self.x_slider.value = 0
        self.x_slider.max = 100
        self.y_slider.value = 0
        self.y_slider.max = 100

    def _add(self, _):
        TEMP2_IMG.write_bytes(TEMP_IMG.read_bytes())
        self.img2.reload()

    def _settings(self, _):
        def _on_col(_, val):
            col = [int(i * 255) for i in val]
            self.font_col = col

        def _conf(_):
            self.font_size = int(font_text.text)
        layout = GridLayout(cols=1, padding=10)

        _color = ColorPicker()
        _color.bind(color=_on_col)
        font_text = TextInput(hint_text='Font Size', font_size=28)
        confirm = Button(text='Confirm')
        confirm.bind(on_press=_conf)
        close = Button(text="Close")

        layout.add_widget(_color)
        layout.add_widget(font_text)
        layout.add_widget(confirm)
        layout.add_widget(close)

        popup = Popup(title='Settings',
                      content=layout)
        popup.open()

        close.bind(on_press=popup.dismiss)

    def _save(self, _):
        if self.file:
            self.file.write_bytes(TEMP_IMG.read_bytes())
            self.img2.reload()
            self.img1.reload()

    def _on_val1(self, _, val):
        self.current_x = int(val)
        self.x_text.text = f'{self.current_x}'
        if self.file:
            TEMP_IMG.write_bytes(TEMP2_IMG.read_bytes())
            img = cv2.imread(str(TEMP_IMG))
            cv2.putText(
                img,
                self.text.text,
                (self.current_x, self.current_y),
                2,
                self.font_size,
                self.font_col,
                3
            )
            cv2.imwrite(str(TEMP_IMG), img)
            self.img2.source = str(TEMP_IMG)
            self.img2.reload()

    def _on_val2(self, _, val):
        self.current_y = int(val)
        self.y_text.text = f'{self.current_y}'
        if self.file:
            TEMP_IMG.write_bytes(TEMP2_IMG.read_bytes())
            img = cv2.imread(str(TEMP_IMG))
            cv2.putText(
                img,
                self.text.text,
                (self.current_x, self.current_y),
                2,
                self.font_size,
                self.font_col,
                3
            )
            cv2.imwrite(str(TEMP_IMG), img)
            self.img2.source = str(TEMP_IMG)
            self.img2.reload()


class ImgTextApp(App):
    def build(self):
        return Core()


if __name__ == '__main__':
    ImgTextApp().run()
    TEMP_IMG.unlink()
