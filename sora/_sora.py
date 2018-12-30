from IPython.display import display
from IPython.display import HTML
from glob import glob
from os import path
import base64


MIME_TYPES = {
    ".jpg": "image/jpeg",
    ".png": "image/png",
}


def _image_to_base64_src(image, mime):
    encoded_image_tmpl = "data:{0};base64,{1}"
    image_base64 = base64.b64encode(image).decode("utf-8")

    return encoded_image_tmpl.format(mime, image_base64)


def _html_img_item(src, item_width="33%", img_width="100%"):
    item_tmpl = """
        <div style="
            width: {1};
            padding: 10px">
            <img style="width: {2};" src="{0}"></img>
        </div>
    """

    return item_tmpl.format(src, item_width, img_width)


def _html_simple_grid(html_images_items):
    container_tmpl = """
    <div style="
        display: flex;
        justify-content: flex-start;
        align-items: center;
        align-content: center;
        flex-wrap: wrap">
        {0}
    </div>
    """

    html = container_tmpl.format("\n".join(html_images_items))
    return html


def _html_display(html):
    return display(HTML(html))


def _file_to_html(filepath, **kwargs):
    with open(filepath, "rb") as f:
        content = f.read()

    extension = path.splitext(filepath)[1]
    if extension not in MIME_TYPES:
        raise Exception("{0}: not supported file extension".format(filepath))

    encoded_image = _image_to_base64_src(content, MIME_TYPES[extension])

    return _html_img_item(encoded_image, **kwargs)

def sora(arg, **kwargs) :

    # width percentage of each grid cell,
    item_width = kwargs.get("width", "50%")
    # width percentage of each image,
    img_width = kwargs.get("width", "100%")

    html = ""
    if isinstance(arg, str):
        if arg[-1] == "/":
            # arg is a string with a trailing slash,
            # let's find all the images and display them in a grid
            dir_full_path = path.abspath(arg)
            html_images_items = []
            for ext in MIME_TYPES:
                files = glob(path.join(dir_full_path, "*{0}".format(ext)))
                html_images_items.extend([_file_to_html(f, **kwargs) for f in files])

            html = _html_simple_grid(html_images_items)
        else:
            # arg is a single file path
            html = _file_to_html(arg)
    # return print(html)
    return display(HTML(html))



