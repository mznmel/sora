# sora (صورة)
Sora means `image/picture` in Arabic. It is a simple library to display and embed images in Jupyter notebooks. You can use it to:

```python
from sora import sora

# Display a single image from a file:
sora('./test.jpg')

# Display all the images in a directory:
sora('./images/')


import tensorflow as tf
(x, _), (_, _) = tf.keras.datasets.cifar10.load_data()

# Display an image from a numpy array (ndarray):
sora(x[0])

# Display a collection of images from a numpy array (ndarray)
sora(x[0:10])

# You can also customize  the grid
sora(x[0:100], cell_width=42, cell_height=42, items_per_row=10)
```
