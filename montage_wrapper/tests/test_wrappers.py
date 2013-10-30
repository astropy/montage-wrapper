import os
import tempfile
from hashlib import md5

import numpy as np
from astropy.wcs import WCS
from astropy.io import fits

from .. import mosaic


class TestMosaic(object):

    def setup_class(self):

        np.random.seed(12345)

        w = WCS(naxis=2)

        lon = np.linspace(10., 11., 5)
        lat = np.linspace(20., 21., 5)

        self.tmpdir = tempfile.mkdtemp()
        os.mkdir(os.path.join(self.tmpdir, 'raw'))

        for i in range(len(lon)):
            for j in range(len(lat)):

                w.wcs.crpix = [50.5, 50.5]
                w.wcs.cdelt = np.array([-0.0066667, 0.0066667])
                w.wcs.crval = [lon[i], lat[j]]
                w.wcs.ctype = [b"RA---TAN", b"DEC--TAN"]
                w.wcs.crota = [0, np.random.uniform(0., 360.)]

                header = w.to_header()

                hdu = fits.PrimaryHDU(header=header)
                hdu.data = np.random.random((100,100))
                hdu.writeto(os.path.join(self.tmpdir, 'raw', 'test_{0:02d}_{1:02d}.fits'.format(i, j)), clobber=True)

    def test_mosaic(self):
        mosaic(os.path.join(self.tmpdir, 'raw'),os.path.join(self.tmpdir, 'mosaic'))
        hdu = fits.open(os.path.join(self.tmpdir, 'mosaic', 'mosaic.fits'))[0]
        assert md5(hdu.data).hexdigest() == "3377373e039b3f934262151e82beaaf1"
