# Python code to convert an image to ASCII image.
from PIL import Image, ImageEnhance, ImageOps
import requests

def calculate_brightness(image):
    greyscale_image = image.convert('L')
    histogram = greyscale_image.histogram()
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for index in range(0, scale):
        ratio = histogram[index] / pixels
        brightness += ratio * (-scale + index)

    return 1 if brightness == 255 else brightness / scale

def scale_image(image, new_width, scale):
    """Resizes an image preserving the aspect ratio.
    """
    (original_width, original_height) = image.size
    aspect_ratio = original_height/float(original_width)
    new_height = int(aspect_ratio * new_width)

    new_image = image.resize((new_width, int(new_height*scale)))
    return new_image

def convert_to_grayscale(image):
    image = image.convert('L')
    image = ImageOps.autocontrast(image, 1, 1)
    return image

def map_pixels_to_chars(image, chars, range_width=20):
    """Maps each pixel to an ascii char based on the range
    in which it lies.

    0-255 is divided into 11 ranges of 25 pixels each.
    """

    pixels_in_image = list(image.getdata())
    pixels_to_chars = [chars[int(pixel_value/range_width)] for pixel_value in
            pixels_in_image]

    return pixels_to_chars

def convert_image_to_blocks(url, new_width=7, red=False):
    chars = ["<:a:841663381298741319>","<:b:841663399859585065>","<:c:841663418145832991>", "<:d:841663436198903818>", "<:e:841663454825938946>","<:f:841663479228137482>","<:g:841663506071945266>","<:h:841663525700108308>","<:i:841663540720435290>","<:j:841663555068624896>","<:k:841663698119819322>","<:l:841663722790584350>","<:m:841663825320738866>"]
    if red == True:
        chars = ["<:a:841663381298741319>", "<:1:841689526271082546>", "<:2:841689543068876830>", "<:3:841689563754659898>", "<:4:841689579832213534>", "<:5:841689592671371285>", "<:61:841692981191114763>", "<:6:841689691048378389>", "<:7:841689707976982538>", "<:8:841689722567786516>", "<:9:841689736383823943>", "<:0:841689749818966057>", "<:01:841691375669608448>"]
    image = Image.open(requests.get(url, stream=True).raw)
    image = scale_image(image, 7, 1.25)
    image = convert_to_grayscale(image)

    pixels_to_chars = map_pixels_to_chars(image, chars)
    len_pixels_to_chars = len(pixels_to_chars)

    image_ascii = [pixels_to_chars[index: index + new_width] for index in range(0, len_pixels_to_chars, new_width)]
    out = ""
    for row in image_ascii:
        row = " ".join(list(map(str,row)))
        out += row+"\n"
    return out

def convert_image_to_ascii(url, reverse, new_width=50):
    chars = ["@", "@", "&", "0", "9", "f", "2", "i", "/", ":", ",", ".", " "]
    if reverse == True:
        chars.reverse()
    image = Image.open(requests.get(url, stream=True).raw)
    image = scale_image(image, 50, 0.47)
    image = convert_to_grayscale(image)

    pixels_to_chars = "".join(map_pixels_to_chars(image, chars))
    len_pixels_to_chars = len(pixels_to_chars)

    image_ascii = [pixels_to_chars[index: index + new_width] for index in range(0, len_pixels_to_chars, new_width)]

    return "```" + "\n".join(image_ascii) + "```"