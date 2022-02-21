from skimage import color
import colorsys


def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_lab(rgb):
    rgb_decimal = tuple(x/255 for x in rgb)
    return color.rgb2lab([[rgb_decimal]])[0][0]

def lab_to_rgb(lab):
    rgb_decimal = color.lab2rgb([[lab]])[0][0]
    return tuple(int(round(x*255, 0)) for x in rgb_decimal)

def lab_to_hex(lab):
    rgb = lab_to_rgb(lab)
    return rgb_to_hex(rgb)

def hex_to_lab(hex):
    rgb = hex_to_rgb(hex)
    lab = rgb_to_lab(rgb)
    return lab

def rgb_to_hex(rgb):
    rgb_ints = tuple_to_int(rgb)
    return '#%02x%02x%02x' % (rgb_ints[0], rgb_ints[1], rgb_ints[2])

def tuple_to_int(tuple):
    return [int(round(x, 0)) for x in tuple]

def rgb_to_hsv(rgb):
    rgb_decimal = tuple(x/255 for x in rgb)
    return colorsys.rgb_to_hsv(*rgb_decimal)

def hex_to_hsv(hex):
    rgb = hex_to_rgb(hex)
    return rgb_to_hsv(rgb)
