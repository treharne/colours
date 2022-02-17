import json
import random
from colours import COLOURS
from clustering import fit_kmeans, get_centres_from_model, get_clusters_from_model


def cell(colour):
    return "<td style='background-color: " + colour + "; color: #ffffff', width=150, align=center>" + colour + "</td>"

def row(cells):
    return "<tr height=150>" + ''.join(cells) + "</tr>"


def colours_grid(colours):
    table = "<table>"
    row_cells = []
    for i, colour in enumerate(colours):
        row_cells.append(cell(colour))
        if (i+1) % 5 == 0:
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
    <body style='font-family: sans-serif'>
    """
    html_page += body
    html_page += """
    </body>
    </html>
    """
    return html_page


def write_colours_page(colours, filename="all_colours.html"):
    html = html_boilerplate(colours_grid(colours))
    with open(filename, "w") as file:
        file.write(html)

def write_random_colours_page(colours, n, filename="random_colours.html"):
    n_random_colours = random.sample(colours, n)
    write_colours_page(n_random_colours, filename)

def write_clustered_colours_page(colours, n, filename="clustered_colours.html"):
    model = fit_kmeans(colours, n)
    clusters = get_clusters_from_model(colours, model)
    centres = get_centres_from_model(model)

    body = "<h1>Clustered colours</h1>"
    body += "<h2>Centres</h2>"
    body += colours_grid(centres)
    for cluster, centre in zip(clusters, centres):
        body += "<h2>Cluster</h2>"
        body += "Centre"
        body += colours_grid([centre])
        body += "Colours"
        body += colours_grid(cluster)

    html = html_boilerplate(body)
    with open(filename, "w") as file:
        file.write(html)

def write_palettes_page(colours, max_n, filename="colour_palettes.html"):
    body = "<h1>Colour palettes</h1>"
    for n in range(1, max_n+1):
        model = fit_kmeans(colours, n)
        centres = get_centres_from_model(model)
        body += "<h2>Palette of " + str(n) + " colours</h2>"
        body += colours_grid(centres)

    html = html_boilerplate(body)
    with open(filename, "w") as file:
        file.write(html)

def write_palettes_json(colours, max_n, filename="colour_palettes.json"):
    palettes = [[]]
    for n in range(1, max_n+1):
        model = fit_kmeans(colours, n)
        centres = get_centres_from_model(model)
        palettes.append(centres)

    body = {"palettes": palettes}
    with open(filename, "w") as file:
        file.write(json.dumps(body))

if __name__ == "__main__":
    write_colours_page(COLOURS)
    write_random_colours_page(COLOURS, 15)
    write_clustered_colours_page(COLOURS, 15)
    write_palettes_page(COLOURS, 40)
    write_palettes_json(COLOURS, 40)
