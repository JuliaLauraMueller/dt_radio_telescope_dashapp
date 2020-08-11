from astropy.io import fits
from util.helpers import *


#########################
# Datamodel Object
#########################

class Datamodel:
    """
    This class creates the datamodel with loading fits-files and saving png.files
    """

    def __init__(self, path, directions, folder, index):
        """
        This methods will be called when an object of this class is instantiated. It initializes variables and calls
        methods.

        :param path: The path name
        :param directions: The directions from given sources
        :param folder: The folder name
        :param index: The index of datamodel
        """
        print('creating datamodel ' + str(index))
        #self.skymodel = fits.open(path + folder + '.skymodel.fits')
        self.psf = fits.open(path + folder + '.psf.fits')
        self.flat = casa_image(fits.open(path + folder + '.image.flat.fits'), 'Flat', directions)
        self.residual = casa_image(fits.open(path + folder + '.residual.fits'), 'Residual', directions)
        self.fidelity = casa_image(fits.open(path + folder + '.fidelity.fits'), 'Fidelity', directions)

        print('creating skymodel and psf plots')
        #save_png_plot(self.skymodel, 'Skymodel')
        save_png_plot(self.psf, 'Psf')


#########################
# CASA Image Object
#########################

class casa_image:
    """
    This class creates a CASA image object and plots it with various histograms and statistical information.
    """

    def __init__(self, fits, name, directions):
        """
        This methods will be called when an object of this class is instantiated. It initializes variables and calls
        methods.

        :param fits: The fits-file
        :param name: The name of the fits-file
        :param directions: The directions from given sources
        """
        print('-- initializing ' + name)
        self.name = name
        self.fits = fits
        self.data = get_FITS_data(fits)

        print('---- creating masks')
        self.data_onsource = create_masked_data(fits, directions, invert=True)
        self.data_offsource = create_masked_data(fits, directions)

        print('---- creating image')
        self.image = create_image(self.data, name + '-Image')

        print('---- creating histograms')
        self.hist = create_hist(self.data, name + ' Distribution')
        self.hist_onsource = create_hist(self.data_onsource, 'Onsource Distribution')
        self.hist_offsource = create_hist(self.data_offsource, 'Offsource Distribution')

        print('---- calculating RMS and DR')
        self.rms = calculate_RMS(self.data)
        self.rms_onsource = calculate_RMS(self.data_onsource)
        self.rms_offsource = calculate_RMS(self.data_offsource)
        self.dr = calculate_DR(self.data, self.rms)
        self.dr_onsource = calculate_DR(self.data_onsource, self.rms_onsource)
        self.dr_offsource = calculate_DR(self.data_offsource, self.rms_offsource)

        self.stats = stats_dict(self.data)


