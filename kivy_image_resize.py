import tkinter as tk
from tkinter import filedialog as fd
from pathlib import Path
from PIL import Image as Img, ImageFilter
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

        self.image_lay = GridLayout(cols=2, rows=1)
        self.image = Image(source=str(SAMPLE))
        self.image_data = Label(text='')
        self.image_lay.add_widget(self.image)
        self.image_lay.add_widget(self.image_data)

        self.controls = GridLayout(cols=2, rows=1)
        self.confirm = Button(text='Confirm')
        self.confirm.bind(on_press=self._confirm)
        self.open = Button(text='Open')
        self.open.bind(on_press=self._open)
        self.controls.add_widget(self.confirm)
        self.controls.add_widget(self.open)

        self.size_lay = GridLayout(cols=2, rows=1)
        # width
        self.width_lay = GridLayout(cols=1, rows=2)
        self.width_lab = Label(text='Width', font_size=24)
        self.width_spinner = Spinner(text='1920', values=[str(i) for i in range(1, 1921)])
        self.width_lay.add_widget(self.width_lab)
        self.width_lay.add_widget(self.width_spinner)
        # height
        self.height_lay = GridLayout(cols=1, rows=2)
        self.height_lab = Label(text='Height', font_size=24)
        self.height_spinner = Spinner(text='1080', values=[str(i) for i in range(1, 1080)])
        self.height_lay.add_widget(self.height_lab)
        self.height_lay.add_widget(self.height_spinner)
        self.size_lay.add_widget(self.width_lay)
        self.size_lay.add_widget(self.height_lay)

        self.add_widget(self.image_lay)
        self.add_widget(self.controls)

    def _confirm(self, _):
        width = int(self.width_spinner.text)
        height = int(self.height_spinner.text)

        if len(self.images):
            index = self.current_image % self.len_images
            image = str(self.images[self.current_image % self.len_images])
            self.current_image += 1
            img = Img.open(image)
            img = img.resize((width, height))
            img.save(image)
            self.image.source = str(self.images[self.current_image % self.len_images])
            self.image.reload()
            self.images.pop(index)
            self.len_images = len(self.images)
        else:
            self.remove_widget(self.size_lay)
            self.image.source = str(SAMPLE)
            self.image.reload()

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
        self.add_widget(self.size_lay)


class ResizeApp(App):
    def build(self):
        return Core()


if __name__ == '__main__':
    ResizeApp().run()
