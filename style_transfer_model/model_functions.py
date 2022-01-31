# functions to use model
# code to load model from Tensorflow Hub
import tensorflow_hub as hub
import tensorflow as tf
from tensorflow import keras
from matplotlib import gridspec
import matplotlib.pylab as plt
import PIL
import numpy as np
import os

# load model from Hub
hub_handle = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
hub_module = hub.load(hub_handle)


#function to load image to standards 
def load_image(image_path):
    img = tf.io.read_file(image_path)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = img[tf.newaxis, :]
    return img

#function to convert a tensor to a Pillow image
def tensor_to_image(tensor):
    tensor = tensor*255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor)>3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return PIL.Image.fromarray(tensor)

def style_image(style_image_path, content_image_path):
    style_image = load_image(style_image_path)
    content_image = load_image(content_image_path)
    outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
    stylized_image = outputs[0]
    stylzd_image = tensor_to_image(stylized_image)
    return stylzd_image

def load_image_v2(image_variable):
    img = image_variable
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = img[tf.newaxis, :]
    return img

def style_several_times(times, content_image_path):
    anime_images = os.listdir('../input/anime-faces/data')
    number = 0
    anime_image = style_image('../input/anime-faces/data/' + anime_images[number], content_image_path)
    number += 1
    anime_image.save('./anime_image', format='png')
    for i in range(times):
        stylez_image = '../input/anime-faces/data/' + anime_images[number]
        stylez_image = load_image(stylez_image)
        anime_image = load_image('./anime_image')
        outputs = hub_module(tf.constant(anime_image), tf.constant(stylez_image))
        anime_image = outputs[0]
        number += 1
        anime_image = tensor_to_image(anime_image)
        anime_image.save('./anime_image', format='png')
    return anime_image
