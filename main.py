import json
import random
from colours import COLOURS
from clustering import fit_kmeans, get_cluster_medians, get_means_from_model, get_clusters_from_model, nearest_colours


def cell(colour):
    return "<td style='background-color: " + colour + "; color: #ffffff', width=150, align=center>" + colour + "</td>"

def row(cells):
    return "<tr height=150>" + ''.join(cells) + "</tr>"


def colours_grid(colours, n_cols=5):
    table = "<table align=centre>"
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
    <body style='font-family: sans-serif' align=centre>
    """
    html_page += body
    html_page += """
    </body>
    </html>
    """
    return html_page


def write_colours_page(colours, filename="all_colours.html"):
    html = html_boilerplate(colours_grid(colours, n_cols=15))
    with open(filename, "w") as file:
        file.write(html)

def write_random_colours_page(colours, n, filename="random_colours.html"):
    n_random_colours = random.sample(colours, n)
    write_colours_page(n_random_colours, filename)

def write_clustered_colours_page(colours, n, filename="clustered_colours.html"):
    model = fit_kmeans(colours, n)
    clusters = get_clusters_from_model(colours, model)
    means = get_means_from_model(model)
    medians = get_cluster_medians(means, clusters)

    body = "<h1>Clustered colours</h1>"
    body += "<h2>Centres</h2>"
    body += colours_grid(means)
    for cluster, mean, median in zip(clusters, means, medians):
        body += "<h2>Cluster</h2>"
        body += "Mean, Median"
        body += colours_grid([mean, median])
        body += "Colours"
        body += colours_grid(cluster)

    html = html_boilerplate(body)
    with open(filename, "w") as file:
        file.write(html)

def write_palettes_page(colours, max_n, filename="colour_palettes.html"):
    body = "<h1>Colour palettes</h1>"
    for n in range(1, max_n+1):
        model = fit_kmeans(colours, n)
        centres = get_means_from_model(model)
        body += "<h2>Palette of " + str(n) + " colours</h2>"
        body += colours_grid(centres)

    html = html_boilerplate(body)
    with open(filename, "w") as file:
        file.write(html)

def write_palettes_json(colours, max_n, filename="colour_palettes.json"):
    palettes = [[]]
    for n in range(1, max_n+1):
        model = fit_kmeans(colours, n)
        means = get_means_from_model(model)
        clusters = get_clusters_from_model(colours, model)
        medians = get_cluster_medians(means, clusters)
        palettes.append(medians)

    body = {"palettes": palettes}
    with open(filename, "w") as file:
        file.write(json.dumps(body))


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
    with open(filename, "w") as file:
        file.write(html)

if __name__ == "__main__":
    write_colours_page(COLOURS)
    write_random_colours_page(COLOURS, 15)
    write_clustered_colours_page(COLOURS, 15)
    write_palettes_page(COLOURS, 40)
    write_palettes_json(COLOURS, 40)
    write_maplike_colours_page(COLOURS)

