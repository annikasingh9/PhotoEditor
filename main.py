import random
from PIL import Image, ImageDraw
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.effectwidget import EffectWidget, PixelateEffect
from kivy.uix.popup import Popup


class PhotoEditorApp(App):
    def build(self):
        return EditorLayout()


class EditorLayout(BoxLayout):
    def load_image(self):
        image_name = self.ids.image_name_input.text.strip()
        if not image_name:
            return

        image_path = image_name
        self.ids.display_area.source = image_path

    def apply_pointillism(self):
        img = Image.open(self.ids.display_area.source)
        canvas = Image.new("RGB", (img.size[0], img.size[1]), "white")
        pixels = img.load()
        for _ in range(50000):
            x, y = random.randint(0, img.size[0] - 1), random.randint(0, img.size[1] - 1)
            size = random.randint(12, 20)
            ellipsebox = [(x, y), (x + size, y + size)]
            draw = ImageDraw.Draw(canvas)
            draw.ellipse(ellipsebox, fill=(pixels[x, y][0], pixels[x, y][1], pixels[x, y][2]))
            del draw

        canvas.save("pointillism.png")
        self.ids.display_area.source = "pointillism.png"

    def apply_linedrawing(self):
        img = Image.open(self.ids.display_area.source)
        new_image = Image.new("RGB", (img.size[0], img.size[1]),(255, 255, 255))
        pixels = img.load()


        draw = ImageDraw.Draw(new_image)

        gray_image = img.convert("L")

        threshold = 30

        for x in range(1, img.size[0] - 1):
            for y in range(1, img.size[1] - 1):
                pixel_values = [
                    gray_image.getpixel((x - 1, y - 1)),
                    gray_image.getpixel((x, y - 1)),
                    gray_image.getpixel((x + 1, y - 1)),
                    gray_image.getpixel((x - 1, y)),
                    gray_image.getpixel((x, y)),
                    gray_image.getpixel((x + 1, y)),
                    gray_image.getpixel((x - 1, y + 1)),
                    gray_image.getpixel((x, y + 1)),
                    gray_image.getpixel((x + 1, y + 1)),
                ]

                gradient = sum(pixel_values) // 9

                if gradient > threshold:
                    draw.point((x, y), fill=(0, 0, 0))

        new_image.save("linedrawing.png")
        self.ids.display_area.source = "linedrawing.png"

    def apply_sepia(self):
        img = Image.open(self.ids.display_area.source)
        # new_image = Image.new("RGB", (img.size[0], img.size[1]),(255, 255, 255))

        pixels = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                red = pixels[x, y][0] * .393 + pixels[x, y][1] * .769 + pixels[x, y][2] * .189
                green = pixels[x, y][0] * .349 + pixels[x, y][1] * .686 + pixels[x, y][2] * .168
                blue = pixels[x, y][0] * .272 + pixels[x, y][1] * .534 + pixels[x, y][2] * .131
                if red > 255:
                    red = 255
                if green > 255:
                    green = 255
                if blue > 255:
                    blue = 255
                pixels[x, y] = (int(red), int(green), int(blue), 255)
        img.save("sepia.png")
        self.ids.display_area.source = "sepia.png"
    def apply_invert(self):
        img = Image.open(self.ids.display_area.source)

        pixels = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                pixels[x, y] = (255 - pixels[x, y][0], 255 - pixels[x, y][1], 255 - pixels[x, y][2])

        img.save("invert.png")
        self.ids.display_area.source = "invert.png"

    def apply_blackandwhite(self):

        img = Image.open(self.ids.display_area.source)

        # Convert the image to grayscale (black and white)
        img = img.convert('L')

        # Save the black and white image
        img.save("blackandwhite.png")
        self.ids.display_area.source = "blackandwhite.png"



if __name__ == '__main__':
    PhotoEditorApp().run()
