import numpy as np
import os

from parrec.parread import Parread


class Recread:
    def __init__(self, filename):
        basename, file_extension = os.path.splitext(filename)
        if file_extension.lower() == '.rec':
            self.recfile = filename
            self.parfile = Parread.get_parfile(filename)
        elif file_extension.lower() == '.par':
            self.parfile = filename
            recfile = basename + '.rec'
            if not os.path.exists(recfile):
                recfile = basename + '.REC'
                if not os.path.exists(recfile):
                    raise FileNotFoundError('Cannot find the corresponding REC file')
            self.recfile = recfile

    def read(self):
        parfile = Parread(self.parfile)
        pars = parfile.read()
        self.parameter = pars
        rec_size = os.path.getsize(self.recfile)
        xres = pars['ImageInformation'][0]['ReconResolution'][0]
        yres = pars['ImageInformation'][0]['ReconResolution'][1]
        nr_images = int(rec_size / 2 / xres / yres)
        nr_images_par = len(pars['ImageInformation'])
        if nr_images != nr_images_par:
            print('WARNING: The number of images in the .par file does not match the number of images in the .rec file')

        with open(self.recfile, "rb") as recfile:
            data = np.fromfile(recfile, dtype=np.uint16, count=int(rec_size/2))
            data = np.reshape(data, (xres, yres, nr_images), order='F')

        return data

    def read_image(self, image_nr):
        parfile = Parread(self.parfile)
        pars = parfile.read()
        self.parameter = pars
        rec_size = os.path.getsize(self.recfile)
        xres = pars['ImageInformation'][0]['ReconResolution'][0]
        yres = pars['ImageInformation'][0]['ReconResolution'][1]
        nr_images = int(rec_size / 2 / xres / yres)
        nr_images_par = len(pars['ImageInformation'])
        if nr_images != nr_images_par:
            print('WARNING: The number of images in the .par file does not match the number of images in the .rec file')

        if image_nr >= nr_images:
            raise ValueError('Cannot read image ' + str(image_nr) + '. The recfile only contains ' + str(nr_images) + ' images')

        with open(self.recfile, "rb") as recfile:
            recfile.seek(image_nr * xres * yres)
            data = np.fromfile(recfile, dtype=np.uint16, count=int(xres * yres))
            data = np.reshape(data, (xres, yres), order='F')

        return data
