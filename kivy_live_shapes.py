from typing import Tuple
import tkinter as tk
from tkinter import filedialog as fd
from pathlib import Path
from PIL import Image as Img, ImageFilter
import cv2
import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage, Image
from kivy.uix.switch import Switch
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.app import App

kivy.require('1.11.0')
SAMPLE = Path(__file__).parent.parent / 'inne' / 'sample_img.png'
TEMP_IMG = Path(__file__).parent / 'temp.png'
TEMP_IMG.touch(exist_ok=True)
TEMP2_IMG = Path(__file__).parent / 'temp2.png'
TEMP2_IMG.touch(exist_ok=True)


class Core(GridLayout):
    def __init__(self, **kwargs):
        super(Core, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 4
        self.file = None
        # vectors' coordination
        self.start_x = 0
        self.radius = 1
        self.start_y = 0
        self.end_x = 100
        self.end_y = 100

        # images
        self.image_lay = GridLayout(cols=2, rows=1)
        self.image = Image(source=str(SAMPLE))
        self.image_live = Image(source=str(SAMPLE))
        self.image_lay.add_widget(self.image)
        self.image_lay.add_widget(self.image_live)

        # controls
        self.controls = GridLayout(cols=5, rows=1)
        self.open = Button(text='Open')
        self.open.bind(on_press=self._open)
        self.save = Button(text='Save')
        self.save.bind(on_press=self._save)
        self.clear = Button(text='Clear')
        self.clear.bind(on_press=self._clear)
        self.switch = Switch(active=True)
        self.confirm = Button(text='Next')
        self.confirm.bind(on_press=self._confirm)
        self.controls.add_widget(self.open)
        self.controls.add_widget(self.save)
        self.controls.add_widget(self.clear)
        self.controls.add_widget(self.switch)
        self.controls.add_widget(self.confirm)

        # shapes lay
        self.shapes_lay = GridLayout(cols=1, rows=1)
        self.shapes_spinner = Spinner(text='Vector', values=['Vector', 'Circle', 'Rectangle'])
        self.shapes_spinner.bind(text=self._val_spin)
        self.shapes_lay.add_widget(self.shapes_spinner)

        # VECTOR SLIDERS
        self.slider_x_lay_vector = GridLayout(cols=2, rows=1)
        self.slider_x_vector = Slider(min=0, max=100)
        self.slider_x_vector.bind(value=self._on_val_x_vector)
        self.x_val_vector = Label(text='0')
        self.slider_x_lay_vector.add_widget(self.slider_x_vector)
        self.slider_x_lay_vector.add_widget(self.x_val_vector)

        self.slider_y_lay_vector = GridLayout(cols=2, rows=1)
        self.slider_y_vector = Slider(min=0, max=100)
        self.slider_y_vector.bind(value=self._on_val_y_vector)
        self.y_val_vector = Label(text='0')
        self.slider_y_lay_vector.add_widget(self.slider_y_vector)
        self.slider_y_lay_vector.add_widget(self.y_val_vector)

        self.slider_lay_vector = GridLayout(cols=1, rows=2)
        self.slider_lay_vector.add_widget(self.slider_x_lay_vector)
        self.slider_lay_vector.add_widget(self.slider_y_lay_vector)

        # RECTANGLE SLIDERS
        self.slider_x_lay_rectangle = GridLayout(cols=2, rows=1)
        self.slider_x_rectangle = Slider(min=0, max=100)
        self.slider_x_rectangle.bind(value=self._on_val_x_rectangle)
        self.x_val_rectangle = Label(text='0')
        self.slider_x_lay_rectangle.add_widget(self.slider_x_rectangle)
        self.slider_x_lay_rectangle.add_widget(self.x_val_rectangle)

        self.slider_y_lay_rectangle = GridLayout(cols=2, rows=1)
        self.slider_y_rectangle = Slider(min=0, max=100)
        self.slider_y_rectangle.bind(value=self._on_val_y_rectangle)
        self.y_val_rectangle = Label(text='0')
        self.slider_y_lay_rectangle.add_widget(self.slider_y_rectangle)
        self.slider_y_lay_rectangle.add_widget(self.y_val_rectangle)

        self.slider_lay_rectangle = GridLayout(cols=1, rows=2)
        self.slider_lay_rectangle.add_widget(self.slider_x_lay_rectangle)
        self.slider_lay_rectangle.add_widget(self.slider_y_lay_rectangle)

        # CIRCLE SLIDERS
        self.slider_x_lay_circle = GridLayout(cols=2, rows=1)
        self.slider_x_circle = Slider(min=0, max=100)
        self.slider_x_circle.bind(value=self._on_val_x_circle)
        self.x_val_circle = Label(text='0')
        self.slider_x_lay_circle.add_widget(self.slider_x_circle)
        self.slider_x_lay_circle.add_widget(self.x_val_circle)

        self.slider_y_lay_circle = GridLayout(cols=2, rows=1)
        self.slider_y_circle = Slider(min=0, max=100)
        self.slider_y_circle.bind(value=self._on_val_y_circle)
        self.y_val_circle = Label(text='0')
        self.slider_y_lay_circle.add_widget(self.slider_y_circle)
        self.slider_y_lay_circle.add_widget(self.y_val_circle)

        self.radius_lay = GridLayout(cols=2, rows=1)
        self.radius_slider = Slider(min=1, max=100)
        self.radius_slider.bind(value=self._on_val_radius)
        self.radius_text = Label(text='1')
        self.radius_lay.add_widget(self.radius_slider)
        self.radius_lay.add_widget(self.radius_text)

        self.slider_lay_circle = GridLayout(cols=1, rows=3)
        self.slider_lay_circle.add_widget(self.slider_x_lay_circle)
        self.slider_lay_circle.add_widget(self.slider_y_lay_circle)
        self.slider_lay_circle.add_widget(self.radius_lay)

        # MAIN LAYOUTS
        self.add_widget(self.image_lay)
        self.add_widget(self.controls)
        self.add_widget(self.shapes_lay)

    def _open(self, _):
        self.remove_widget(self.slider_lay_vector)
        self.remove_widget(self.slider_lay_circle)
        self.remove_widget(self.slider_lay_rectangle)
        root = tk.Tk()
        root.withdraw()
        file = fd.askopenfilename(
            title='Select a File',
            initialdir='/',
            filetypes=[("PNG", "*.png"), ('JPEG', '*.jpg')])
        if file:
            self.file = Path(file)
            self.image.source = str(self.file)
            TEMP_IMG.write_bytes(self.file.read_bytes())
            TEMP2_IMG.write_bytes(self.file.read_bytes())
            self.image.reload()
            self.image_live.source = str(TEMP_IMG)
            self.image_live.reload()
            self.add_widget(self.slider_lay_vector)
            img = Img.open(str(self.file))
            self.slider_x_vector.max = img.size[0]
            self.slider_y_vector.max = img.size[1]
            self.slider_x_rectangle.max = img.size[0]
            self.slider_y_rectangle.max = img.size[1]
            self.slider_x_circle.max = img.size[0]
            self.slider_y_circle.max = img.size[1]

    def _save(self, _):
        self.file.write_bytes(TEMP_IMG.read_bytes())
        self.image.source = str(self.file)
        self.image.reload()

    def _clear(self, _):
        self.remove_widget(self.slider_lay_vector)
        self.remove_widget(self.slider_lay_circle)
        self.remove_widget(self.slider_lay_rectangle)
        self.slider_x_vector.value = 0
        self.slider_y_vector.value = 0
        self.switch.active = True
        self.image_live.source = str(SAMPLE)
        self.image.source = str(SAMPLE)
        self.image.reload()
        self.image_live.reload()
        self.shapes_spinner.text = 'Vector'
        self.remove_widget(self.slider_lay_vector)

    def _confirm(self, _):
        # self.file.write_bytes(TEMP_IMG.read_bytes())
        TEMP2_IMG.write_bytes(TEMP_IMG.read_bytes())
        self.image_live.source = str(TEMP_IMG)
        self.start_x = 0
        self.start_y = 0
        self.end_x = 100
        self.end_y = 100

    def _on_val_x_vector(self, _, val):
        self.x_val_vector.text = str(int(val))
        if self.switch.active:
            self.start_x = int(val)
        else:
            self.end_x = int(val)
        self._draw_vector((self.start_x, self.start_y), (self.end_x, self.end_y))

    def _on_val_y_vector(self, _, val):
        self.y_val_vector.text = str(int(val))
        if self.switch.active:
            self.start_y = int(val)
        else:
            self.end_y = int(val)
        self._draw_vector((self.start_x, self.start_y), (self.end_x, self.end_y))

    def _draw_vector(self, start: Tuple[int, int], end: Tuple[int, int]):
        TEMP_IMG.write_bytes(TEMP2_IMG.read_bytes())
        img = cv2.imread(str(TEMP_IMG))
        cv2.arrowedLine(img,
                        (start[0], start[1]),
                        (end[0], end[1]),
                        color=(0, 0, 0),
                        thickness=5)
        cv2.imwrite(str(TEMP_IMG), img)
        self.image_live.reload()

    def _on_val_x_rectangle(self, _, val):
        self.x_val_rectangle.text = str(int(val))
        if self.switch.active:
            self.start_x = int(val)
        else:
            self.end_x = int(val)
        self._draw_rectangle((self.start_x, self.start_y), (self.end_x, self.end_y))

    def _on_val_y_rectangle(self, _, val):
        self.y_val_rectangle.text = str(int(val))
        if self.switch.active:
            self.start_y = int(val)
        else:
            self.end_y = int(val)
        self._draw_rectangle((self.start_x, self.start_y), (self.end_x, self.end_y))

    def _draw_rectangle(self, start: Tuple[int, int], end: Tuple[int, int]):
        TEMP_IMG.write_bytes(TEMP2_IMG.read_bytes())
        img = cv2.imread(str(TEMP_IMG))
        cv2.rectangle(img,
                      (start[0], start[1]),
                      (end[0], end[1]),
                      color=(0, 0, 0),
                      thickness=5)
        cv2.imwrite(str(TEMP_IMG), img)
        self.image_live.reload()

    def _on_val_x_circle(self, _, val):
        self.x_val_rectangle.text = str(int(val))
        self.start_x = int(val)
        self._draw_circle((self.start_x, self.start_y), self.radius)

    def _on_val_y_circle(self, _, val):
        self.x_val_rectangle.text = str(int(val))
        self.start_y = int(val)
        self._draw_circle((self.start_x, self.start_y), self.radius)

    def _on_val_radius(self, _, val):
        self.radius_text.text = str(int(val))
        self.radius = int(val)
        self._draw_circle((self.start_x, self.start_y), self.radius)

    def _draw_circle(self, start: Tuple[int, int], radius: int):
        TEMP_IMG.write_bytes(TEMP2_IMG.read_bytes())
        img = cv2.imread(str(TEMP_IMG))
        cv2.circle(img,
                   (start[0], start[1]),
                   radius=radius,
                   color=(0, 0, 0),
                   thickness=5)
        cv2.imwrite(str(TEMP_IMG), img)
        self.image_live.reload()

    def _val_spin(self, _, text):
        # delete all shapes' layouts
        self.remove_widget(self.slider_lay_vector)
        self.remove_widget(self.slider_lay_rectangle)
        self.remove_widget(self.slider_lay_circle)
        # validate shapes
        if self.file is not None:
            if text == 'Vector':
                self.add_widget(self.slider_lay_vector)
            elif text == 'Circle':
                self.add_widget(self.slider_lay_circle)
            elif text == 'Rectangle':
                self.add_widget(self.slider_lay_rectangle)
            print(text)


class VectorApp(App):
    def build(self):
        return Core()


if __name__ == '__main__':
    VectorApp().run()
    TEMP_IMG.unlink()
    TEMP2_IMG.unlink()
