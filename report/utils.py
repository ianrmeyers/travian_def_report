import csv
import datetime


def clean_negative_coords(coords):
    coords_x = coords[0]
    coords_y = coords[1]

    coords_x = coords_x.replace('−', '-')
    coords_y = coords_y.replace('−', '-')

    if coords_x[0] == '-':
        coords_x = coords_x[1:]
        coords_x = int(coords_x) * -1

    if coords_y[0] == '-':
        coords_y = coords_y[1:]
        coords_y = int(coords_y) * -1

    return int(coords_x), int(coords_y)
