import json
import random
import filters
from bs4 import BeautifulSoup as bs

from colours import COLOURS
from clustering import fit_kmeans, fit_spectral, get_cluster_medioids, get_means_from_kmeans, get_clusters_from_model, get_means_from_spectral, nearest_colours


def cell(colour):
    return "<td style='background-color: " + colour + "; color: #ffffff' width=150 align=center>" + colour + "</td>"

def row(cells):
    return "<tr height=150 align=center>" + ''.join(cells) + "</tr>"

def colours_grid(colours, n_cols=5):
    table = "<table align=center>"
    row_cells = []
    for i, colour in enumerate(colours):
        row_cells.append(cell(colour))
        if (i+1) % n_cols == 0:
            table += row(row_cells)
            row_cells = []

    if row_cells:
        table += row(row_cells)
    table += "</table>"
    return table

def html_boilerplate(body):
    html_page = """
    <!DOCTYPE html>
    <html>
    <head>
    <title>Colours</title>
    </head>
    <body style='font-family: sans-serif' align=center>
    """
    html_page += body
    html_page += """
    </body>
    </html>
    """
    return html_page

def write(body, filename):
    with open(filename, "w") as file:
        file.write(body)

def write_html(body, filename):
    soup = bs(body, features="html.parser")
    html = soup.prettify()
    write(html, filename)

def write_colours_page(colours, filename="all_colours.html"):
    html = html_boilerplate(colours_grid(colours, n_cols=15))
    write_html(html, filename)

def write_random_colours_page(colours, n, filename="random_colours.html"):
    n_random_colours = random.sample(colours, n)
    write_colours_page(n_random_colours, filename)


def write_kmeans_clustered_colours_page(colours, n, filename="kmeans_clustered_colours.html"):
    model = fit_kmeans(colours, n)
    clusters = get_clusters_from_model(colours, model)
    means = get_means_from_kmeans(model)
    medioids = get_cluster_medioids(means, clusters)

    body = "<h1>K-Means Clustered colours</h1>"
    body += "<h2>Centres</h2>"
    body += colours_grid(means)
    for cluster, mean, medioid in zip(clusters, means, medioids):
        body += "<h2>Cluster</h2>"
        body += "Mean, Medioid"
        body += colours_grid([mean, medioid])
        body += "Colours"
        body += colours_grid(cluster)

    html = html_boilerplate(body)
    write_html(html, filename)


def write_spectral_clustered_colours_page(colours, n, filename="spectral_clustered_colours.html"):
    model = fit_spectral(colours, n)
    clusters = get_clusters_from_model(colours, model)
    means = get_means_from_spectral(clusters)
    medioids = get_cluster_medioids(means, clusters)

    body = "<h1>Spectral clustered colours</h1>"
    body += "<h2>Centres</h2>"
    body += colours_grid(means)

    for cluster, mean, medioid in zip(clusters, means, medioids):
        body += "<h2>Cluster</h2>"
        body += "Mean, Medioid"
        body += colours_grid([mean, medioid])
        body += "Colours"
        body += colours_grid(cluster)

    html = html_boilerplate(body)
    write_html(html, filename)


def write_palettes_json(all_colours, max_n, filename="colour_palettes.json"):
    palettes = [[]]
    for n in range(1, max_n+1):
        colours = filters.filter_allowed_colours(n, all_colours)
        model = fit_kmeans(colours, n)

        means = get_means_from_kmeans(model)
        clusters = get_clusters_from_model(colours, model)
        medioids = get_cluster_medioids(means, clusters)

        palettes.append(medioids)

    body = {"palettes": palettes}

    write(json.dumps(body), filename)

def write_palettes_page(all_colours, max_n, filename="filtered_palettes.html"):
    body = "<h1>Filtered palettes</h1>"
    body += "<table align=center>"

    body += "<tr align=center><td align=center valign=top>"
    body += "<h1>K-Means</h1>"

    for n in range(1, max_n+1):
        colours = filters.filter_allowed_colours(n, all_colours)
        model = fit_kmeans(colours, n)
        clusters = get_clusters_from_model(colours, model)
        means = get_means_from_kmeans(model)
        medioids = get_cluster_medioids(means, clusters)

        body += "<h2>Palette of " + str(n) + " colours</h2>"
        body += colours_grid(medioids)

    body += "</td><td align=center valign=top>"
    body += "<h1>Spectral</h1>"

    for n in range(1, max_n+1):
        colours = filters.filter_allowed_colours(n, all_colours)
        model = fit_spectral(colours, n)
        clusters = get_clusters_from_model(colours, model)
        means = get_means_from_spectral(clusters)
        medioids = get_cluster_medioids(means, clusters)
        body += "<h2>Palette of " + str(n) + " colours</h2>"
        body += colours_grid(medioids)

    body += "</td></tr></table>"

    html = html_boilerplate(body)

    write_html(html, filename)


def write_maplike_colours_page(colours, filename="maplike_colours.html"):
    body = "<h1>Colours that look like map colours</h1>"

    map_blue = '#95C1E1'
    body += "<h2>Map blue</h2>"
    body += colours_grid([map_blue])
    body += "<p>Colours that look like map blue</p>"
    body += colours_grid(nearest_colours(map_blue, colours, n=15))

    map_green = '#C4D9A0'
    body += "<h2>Map green</h2>"
    body += colours_grid([map_green])
    body += "<p>Colours that look like map green</p>"
    body += colours_grid(nearest_colours(map_green, colours, n=15))

    html = html_boilerplate(body)

    write_html(html, filename)


def write_filtered_colours_page(colours, filename="filtered_colours.html"):
    body = "<h1>Colours filtered by certain properties</h1>"

    body += "<h2>Pastel colours</h2>"
    body += colours_grid(c for c in colours if filters.is_pastel(c))

    body += "<h2>Bright Pastel colours</h2>"
    body += colours_grid(c for c in colours if filters.is_bright_pastel(c))


    body += "<h2>Bright colours</h2>"
    body += colours_grid(c for c in colours if filters.is_bright(c))

    body += "<h2>Strong Dark colours</h2>"
    body += colours_grid(c for c in colours if filters.is_strong_dark(c))

    body += "<h2>Dull colours</h2>"
    body += colours_grid(c for c in colours if filters.is_dull(c))

    html = html_boilerplate(body)
    
    write_html(html, filename)


if __name__ == "__main__":
    write_colours_page(COLOURS)
    write_random_colours_page(COLOURS, 15)
    write_filtered_colours_page(COLOURS)
    write_kmeans_clustered_colours_page(COLOURS, 15)
    write_spectral_clustered_colours_page(COLOURS, 15)
    write_maplike_colours_page(COLOURS)
    write_palettes_json(COLOURS, 40)
    write_palettes_page(COLOURS, 40)

