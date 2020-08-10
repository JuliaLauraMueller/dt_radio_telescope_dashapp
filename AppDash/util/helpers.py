from matplotlib import pyplot as plt
from astropy.wcs import WCS
import numpy as np
import plotly.express as px
import pandas as pd


#########################
# Helper Functions
#########################
def get_FITS_data(fits):
    """
    Returns the fits data from a CASA image.

    :param fits: The fits-data
    :return: data: Data in fits format
    """
    data = np.array(fits[0].data).squeeze()
    return data


def create_image(data, title):
    """
    Returns an image as a figure.

    :param data: The data for the image
    :param title: The title of the image
    :return: image: The image as a figure
    """
    labels = {'color': 'Jy/beam'}
    image = px.imshow(data, color_continuous_scale="jet", origin='lower', labels=labels, width=800, height=800,
                      title=title)
    return image


def create_hist(data, title):
    """
    Returns a histogram of given data (pandas DataFrame).

    :param data: The data for the histogram
    :param title: The title of the histogram
    :return: hist: The histogram as a figure
    """
    df = pd.DataFrame(data=data.flatten().astype('f8'), columns=['Jy/beam']).dropna()
    hist = px.histogram(df, nbins=128, x='Jy/beam', title=title, height=350)
    rms = calculate_RMS(data)
    dr = calculate_DR(data, rms)

    hist.add_annotation(
        x=0.95,
        y=0.80,
        xref="paper",
        yref="paper",
        xanchor="right",
        yanchor="top",
        text="RMS " + str(rms) + "<br>" + "DR " + str(dr),
        showarrow=True,
        font=dict(
            family="Courier New, monospace",
            size=20,
            color="#ffffff"
        ),
        align="left",
        ax=20,
        ay=-30,
        bordercolor="#c7c7c7",
        borderwidth=2,
        borderpad=4,
        bgcolor="#ff7f0e",
        opacity=0.8
    )
    hist.update_layout(showlegend=False)
    return hist


def save_png_plot(fits, title):
    """
    Plots fits image of given image data and saves it as png-file.

    :param fits: The data of the image
    :param title: Title of the image
    """
    fig = plt.figure(figsize=(8, 4))
    ax = fig.add_subplot(111)

    img = ax.imshow(get_FITS_data(fits), cmap='jet', origin='lower')
    ax.set_title(title, fontsize=14)
    cmap = plt.colorbar(img, ax=ax)

    plt.savefig('assets/' + title + '.png', bbox_inches="tight")


def calculate_pixcoord(fits, direction):
    """
    Returns calculated pixel coordinates as a list. Transforms world coordinates to pixel coordinates with the given
    directions right ascension and declination.

    :param fits: The fits-data
    :param direction: The given direction as a list
    :return: pixel_coords: Calculated pixel coordinates
    """
    wcs = WCS(fits[0].header, fix=False)

    ra_deg = direction[0]
    dec_deg = direction[1]

    coordinates = np.array(wcs.wcs_world2pix(ra_deg, dec_deg, 0, ra_dec_order=True))
    pixel_coords = np.array([coordinates[1], coordinates[0]])
    return pixel_coords


def calculate_mask(data, coordinates, invert=False):
    """
    Returns the calculated mask as a list from given image data and coordinates.

    :param data: The image data
    :param coordinates: The calculated coordinates from given directions
    :param invert: Boolean initialized with False
    :return: masked_array: The calculated mask
    """
    if invert:
        mask = np.ones(data.shape, dtype=bool)
    else:
        mask = np.zeros(data.shape, dtype=bool)

    for coord in coordinates:
        mask[int(coord[0]) - 50:int(coord[0]) + 50, int(coord[1]) - 50:int(coord[1]) + 50] = not invert

    masked_array = np.ma.masked_array(data, mask, fill_value=float('NaN'))
    return masked_array


def create_masked_data(fits, directions, invert=False):
    """
    Returns masked data from given fits-file and calculated pixel coordinates.

    :param fits: The fits-data
    :param directions: The directions from given sources
    :param invert: Boolean initialized with False
    :return: masked_data: The masked data
    """
    coordinates = []
    for direction in directions:
        coordinates.append(calculate_pixcoord(fits, direction))

    masked_data = calculate_mask(get_FITS_data(fits), coordinates, invert)
    return masked_data.filled()


def calculate_RMS(data):
    """
    Returns the calculated rms (root mean square) from given image data.

    :param data: The image data
    :return: rms: The calculated root mean square
    """
    rms = np.sqrt(np.nanmean(np.square(data)))
    return rms.round(4)


def calculate_DR(data, rms):
    """
    Returns the calculated dr (dynamic range) from given data and rms.

    :param data: The image data
    :param rms: The calculated root mean square
    :return: dr: The calculated dynamic range
    """
    dr = np.nanmax(data) / rms
    return dr.round(4)


def stats_dict(data):
    """
    Returns the statistical information from given image data.

    :param data: The image data
    :return: stat: The statistical information
    """
    stats = {'size': np.size(data),
             'max': np.nanmax(data).round(3),
             'min': np.nanmin(data).round(3),
             'mean': np.mean(data).round(3),
             'median': np.median(data).round(3),
             'sigma': np.std(data).round(3),
             'sum': np.sum(data).round(3)}
    return stats