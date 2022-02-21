from conversions import hex_to_hsv

def is_pastel(color):
    hue, saturation, value = hex_to_hsv(color)
    return saturation < 0.5 and value > 0.5

def is_bright_pastel(colour):
    hue, saturation, value = hex_to_hsv(colour)
    return 0.5 <= saturation < 0.7 and value > 0.5

def is_bright(colour):
    hue, saturation, value = hex_to_hsv(colour)
    return saturation >= 0.7 and value > 0.5

def is_strong_dark(colour):
    hue, saturation, value = hex_to_hsv(colour)
    return saturation > 0.4 and value <= 0.5

def is_dull(colour):
    hue, saturation, value = hex_to_hsv(colour)
    return saturation <= 0.4 and value <= 0.5


def allowed_colour_filters(palette_size):
    allowed_filters = []
    if palette_size > 0:
        allowed_filters.append(is_bright_pastel)
        allowed_filters.append(is_pastel)
    if palette_size > 11:
        allowed_filters.append(is_bright)
    if palette_size > 19:
        allowed_filters.append(is_strong_dark)
    if palette_size > 30:
        allowed_filters.append(is_dull)
    return allowed_filters

def filter_allowed_colours(palette_size, all_colours):
    allowed_filters = allowed_colour_filters(palette_size)
    return [
        colour
        for colour in all_colours
        if any(f(colour) for f in allowed_filters)
    ]