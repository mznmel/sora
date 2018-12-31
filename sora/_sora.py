from IPython.display import display
from IPython.display import HTML
from glob import glob
from os import path
import base64
from PIL import Image
import io
import math
import numpy as np

MIME_TYPES = {
    ".jpg": "image/jpeg",
    ".png": "image/png",
}


def _image_to_base64_src(image, mime):
    encoded_image_tmpl = "data:{0};base64,{1}"
    image_base64 = base64.b64encode(image).decode("utf-8")

    return encoded_image_tmpl.format(mime, image_base64)


def _html_img(src):
    item_tmpl = """
        <img src="{0}"></img>
    """

    return item_tmpl.format(src)


def _html_display(html):
    return display(HTML(html))


def _file_to_html(filepath, **kwargs):
    with open(filepath, "rb") as f:
        content = f.read()

    extension = path.splitext(filepath)[1]
    if extension not in MIME_TYPES:
        raise Exception("{0}: not supported file extension".format(filepath))

    encoded_image = _image_to_base64_src(content, MIME_TYPES[extension])

    return _html_img(encoded_image, **kwargs)


def _images_to_grid(list_images, cell_width=32, cell_height=32, items_per_row=3):
    # create a new canvas

    if len(list_images) <= items_per_row:
        canvas_width = len(list_images) * cell_width
    else:
        canvas_width = items_per_row * cell_width
    canvas_height = int(math.ceil(len(list_images) / items_per_row)) * cell_height
    canvas = Image.new("RGB", (canvas_width, canvas_height), "white")

    # draw the images in a grid
    for i, img in enumerate(list_images):
        x = (i % items_per_row) * cell_width
        y = (int(math.floor(i/items_per_row))) * cell_height

        img = list_images[i]
        img.thumbnail((cell_width, cell_height))
        canvas.paste(img, box=(x, y))
        img.close()

    canvas_base64 = _image_obj_to_src(canvas)

    return _html_img(canvas_base64)

def _image_obj_to_src(image_obj):
    with io.BytesIO() as output:
        image_obj.save(output, format="JPEG")
        base64_src = _image_to_base64_src(output.getvalue(), MIME_TYPES[".jpg"])

    return base64_src

def _load_directory(dir_path):
    dir_full_path = path.abspath(dir_path)

    all_imgs = []
    for ext in MIME_TYPES:
        files = glob(path.join(dir_full_path, "*{0}".format(ext)))
        for f in files:
            img = Image.open(f)
            all_imgs.append(img)

    return all_imgs


def sora(arg, **kwargs):
    html = ""
    if isinstance(arg, str):
        # arg is a string
        if arg[-1] == "/":
            # arg is a string with a trailing slash,
            # let's find all the images and display them in a grid
            all_images = _load_directory(arg)
            cell_width = kwargs.get("cell_width", 32)
            cell_height = kwargs.get("cell_height", 32)
            items_per_row = kwargs.get("items_per_row", 2)
            html = _images_to_grid(all_images, cell_width, cell_height, items_per_row)
        else:
            # arg is a single file path
            html = _file_to_html(arg)
    elif isinstance(arg, np.ndarray):
        # arg is a numpy array
        if arg.ndim == 3:
            # single image
            img = Image.fromarray(arg)
            base64_src = _image_obj_to_src(img)
            html = _html_img(base64_src)

    return display(HTML(html))



