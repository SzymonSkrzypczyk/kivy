"""
App enabling user to apply filters on an image
"""
import tkinter as tk
from tkinter import filedialog as fd
from uuid import uuid4
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

SAMPLE = Path(__file__).parent.parent / 'inne' / 'sample_img.png'
TEST_PATH = Path(__file__).parent / f'{uuid4()}.png'
TEST_PATH.touch()


class Core(GridLayout):
    def __init__(self, **kwargs):
        super(Core, self).__init__(**kwargs)
        self.path = None
        self.cols = 1
        self.rows = 4
        self.directory = None
        self.file_name = None

        self.save_lay = GridLayout(cols=3, rows=1)
        self.save_lay.name = TextInput(hint_text='Enter Name:')
        self.directory_but = Button(text='Directory')
        self.directory_but.bind(on_press=self.select_directory)
        self.but_confirm = Button(text='Confirm')
        self.but_confirm.bind(on_press=self.confirm_save)
        self.save_lay.add_widget(self.directory_but)
        self.save_lay.add_widget(self.save_lay.name)
        self.save_lay.add_widget(self.but_confirm)

        self.images_lay = GridLayout(cols=2, rows=1)
        self.img1 = Image(source=str(SAMPLE))
        self.img2 = Image(source=str(SAMPLE))
        self.images_lay.add_widget(self.img1)
        self.images_lay.add_widget(self.img2)

        self.button_lay = GridLayout(cols=4, rows=2)
        self.blur = Button(text='Blur')
        self.blur.bind(on_press=self.edit)
        self.mini = Button(text='Mini')
        self.mini.bind(on_press=self.edit)
        self.contour = Button(text='Contour')
        self.contour.bind(on_press=self.edit)
        self.detail = Button(text='Detail')
        self.detail.bind(on_press=self.edit)
        self.edge = Button(text='Edge Enh.')
        self.edge.bind(on_press=self.edit)
        self.emboss = Button(text='Emboss')
        self.emboss.bind(on_press=self.edit)
        self.find = Button(text='Find Edges')
        self.find.bind(on_press=self.edit)
        self.smooth = Button(text='Smooth')
        self.smooth.bind(on_press=self.edit)

        self.button_lay.add_widget(self.blur)
        self.button_lay.add_widget(self.mini)
        self.button_lay.add_widget(self.contour)
        self.button_lay.add_widget(self.detail)
        self.button_lay.add_widget(self.edge)
        self.button_lay.add_widget(self.emboss)
        self.button_lay.add_widget(self.find)
        self.button_lay.add_widget(self.smooth)

        self.bottom_lay = GridLayout(cols=3, rows=1)
        self.confirm = Button(text='Confirm')
        self.confirm.bind(on_press=self._confirm)
        self.save = Button(text='Save')
        self.save.bind(on_press=self._save)
        self.file = Button(text='Open')
        self.file.bind(on_press=self.open_file)
        self.bottom_lay.add_widget(self.confirm)
        self.bottom_lay.add_widget(self.save)
        self.bottom_lay.add_widget(self.file)

        self.add_widget(self.images_lay)
        self.add_widget(self.button_lay)
        self.add_widget(self.bottom_lay)

    def edit(self, but):
        if but.text == 'Blur':
            im = Img.open(str(self.path))
            im1 = im.filter(ImageFilter.BLUR)
            im1.save(str(TEST_PATH))
            self.img2.source = str(TEST_PATH)
            self.img2.reload()

        elif but.text == 'Mini':
            im = Img.open(str(self.path))
            im1 = im.filter(ImageFilter.MinFilter)
            im1.save(str(TEST_PATH))
            self.img2.source = str(TEST_PATH)
            self.img2.reload()

        elif but.text == 'Contour':
            im = Img.open(str(self.path))
            im1 = im.filter(ImageFilter.CONTOUR)
            im1.save(str(TEST_PATH))
            self.img2.source = str(TEST_PATH)
            self.img2.reload()

        elif but.text == 'Detail':
            im = Img.open(str(self.path))
            im1 = im.filter(ImageFilter.DETAIL)
            im1.save(str(TEST_PATH))
            self.img2.source = str(TEST_PATH)
            self.img2.reload()

        elif but.text == 'Edge Enh.':
            im = Img.open(str(self.path))
            im1 = im.filter(ImageFilter.EDGE_ENHANCE)
            im1.save(str(TEST_PATH))
            self.img2.source = str(TEST_PATH)
            self.img2.reload()

        elif but.text == 'Emboss':
            im = Img.open(str(self.path))
            im1 = im.filter(ImageFilter.EMBOSS)
            im1.save(str(TEST_PATH))
            self.img2.source = str(TEST_PATH)
            self.img2.reload()

        elif but.text == 'Find Edges':
            im = Img.open(str(self.path))
            im1 = im.filter(ImageFilter.FIND_EDGES)
            im1.save(str(TEST_PATH))
            self.img2.source = str(TEST_PATH)
            self.img2.reload()

        elif but.text == 'Smooth':
            im = Img.open(str(self.path))
            im1 = im.filter(ImageFilter.SMOOTH)
            im1.save(str(TEST_PATH))
            self.img2.source = str(TEST_PATH)
            self.img2.reload()

    def open_file(self, _):
        root = tk.Tk()
        root.withdraw()
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=[('PNG', '*.png'), ('JPG', '*.jpg')])
        self.path = Path(filename)

    def _confirm(self, _):
        self.img1.source = str(self.path)

    def _save(self, _):
        self.remove_widget(self.save_lay)
        self.add_widget(self.save_lay)

    def confirm_save(self, _):
        file = self.directory / f'{self.save_lay.name.text}'
        file.touch()
        file.write_bytes(TEST_PATH.read_bytes())
        self.remove_widget(self.save_lay)

    def select_directory(self, _):
        root = tk.Tk()
        root.withdraw()
        directory = fd.askdirectory(
            title='Select Directory',
            initialdir='/',)
        self.directory = Path(directory)


class ImageEffectApp(App):
    def build(self):
        return Core()


if __name__ == '__main__':
    ImageEffectApp().run()
    TEST_PATH.unlink()
