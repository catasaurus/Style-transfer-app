from django.shortcuts import render
from django.http import HttpResponse
import tensorflow_hub as hub
import tensorflow as tf
from tensorflow import keras
from matplotlib import gridspec
import matplotlib.pylab as plt
import PIL
import numpy as np
import os
from PIL import Image
from pathlib import Path


# model functions. I know it is ugly that i'm not importing it but i don't want it to break becuase of the dir i am running the file from :(
def load_image(image_path):
    #img = tf.io.read_file(image_path)
    img = tf.constant(image_path, dtype='string')
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
    hub_module = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
    style_image = load_image(style_image_path)
    content_image = load_image(content_image_path)
    outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
    stylized_image = outputs[0]
    stylzd_image = tensor_to_image(stylized_image)
    return stylzd_image


# Views
def main_page(request):
	return render(request, 'index.html')


def image_api(request):
	base_path = Path(__file__).resolve().parent.parent
	# save files so that they can be read easily by the load_image function
	# style image
	#style_image_filesave = fs.save(request.FILES['img'].name, request.FILES['img'])
	#style_image_path = fs.url(style_image_filesave)
	# image to style
	#image_to_style_filesave = fs.save(request.FILES['img_tostyle'].name, request.FILES['img_tostyle'])
	#image_tostyle_path = fs.url(image_to_style_filesave)
	# get styled image
	styled_image = style_image(request.FILES['img'].read(), request.FILES['img_tostyle'].read())
	styled_image = styled_image.save(base_path / 'styled_image.png')
	styled_image = open(base_path / 'styled_image.png', 'rb').read()
	os.remove(base_path / 'styled_image.png')
	return HttpResponse(styled_image, content_type='image/png')
