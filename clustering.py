import colorsys
from sklearn.cluster import KMeans
import numpy as np
from skimage import io, color

from collections import defaultdict

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

def fit_kmeans(hex_colours, n):
    # LAB colours are designed to be more perceptually uniform
    # than RGB colours. So, converting to lab means clustering is
    # substantially more effective.
    colours = np.array([hex_to_lab(colour) for colour in hex_colours])
    return KMeans(n_clusters=n, random_state=0).fit(colours)

def get_clusters_from_model(colours, model):
    clusters = defaultdict(list)
    for colour, cluster in zip(colours, model.labels_):
        clusters[cluster].append(colour)
    
    sorted_clusters = dict(sorted(clusters.items()))
    return sorted_clusters.values()

def get_centres_from_model(model):
    return [lab_to_hex(centre) for centre in model.cluster_centers_]
