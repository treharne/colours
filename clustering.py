from sklearn.cluster import KMeans, SpectralClustering
import numpy as np

from collections import defaultdict

from conversions import hex_to_lab, lab_to_hex

def fit_kmeans(hex_colours, n):
    # LAB colours are designed to be more perceptually uniform
    # than RGB colours. So, converting to lab means clustering is
    # substantially more effective.
    colours = np.array([hex_to_lab(colour) for colour in hex_colours])
    return KMeans(n_clusters=n, random_state=0).fit(colours)

def fit_spectral(hex_colours, n):
    colours = np.array([hex_to_lab(colour) for colour in hex_colours])
    return SpectralClustering(
        n_clusters=n, 
        affinity="nearest_neighbors",
        assign_labels='discretize', 
        # n_init=20,
        # n_neighbors=3,
        random_state=5,
    ).fit(colours)


def distance(lab1, lab2):
    return np.linalg.norm(lab1 - lab2)

def colour_distances(base_colour, colours):
    base_colour_lab = hex_to_lab(base_colour)
    colours_lab = (hex_to_lab(colour) for colour in colours)
    return [distance(base_colour_lab, colour_lab) for colour_lab in colours_lab]

def nearest_colour(base_colour, colours):
    distances = colour_distances(base_colour, colours)
    return colours[np.argmin(distances)]

def nearest_colours(base_colour, colours, n=10):
    distances = colour_distances(base_colour, colours)
    return sorted(colours, key=lambda colour: distances[colours.index(colour)])[:n]

def get_clusters_from_model(colours, model):
    clusters = defaultdict(list)
    for colour, cluster in zip(colours, model.labels_):
        clusters[cluster].append(colour)
    
    sorted_clusters = dict(sorted(clusters.items()))
    return sorted_clusters.values()

def get_means_from_kmeans(model):
    return [lab_to_hex(centre) for centre in model.cluster_centers_]

def get_means_from_spectral(clusters):
    return [
        lab_to_hex(np.mean([hex_to_lab(colour) for colour in cluster], axis=0))
        for cluster in clusters
    ]

def get_cluster_medioids(centres, clusters):
    return [
        nearest_colour(centre, cluster) 
        for centre, cluster in zip(centres, clusters)
    ]