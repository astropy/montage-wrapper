import os
import shutil
import tempfile
from hashlib import md5

import numpy as np
from numpy.testing import assert_allclose
from astropy.wcs import WCS
from astropy.io import fits
from astropy.tests.helper import pytest

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

    def teardown_class(self):
        shutil.rmtree(self.tmpdir)

    def test_mosaic(self):
        mosaic(os.path.join(self.tmpdir, 'raw'),os.path.join(self.tmpdir, 'mosaic'), hdu=0)
        hdu = fits.open(os.path.join(self.tmpdir, 'mosaic', 'mosaic.fits'))[0]
        assert hdu.data.shape == (288, 282)
        valid = hdu.data[~np.isnan(hdu.data)]
        assert len(valid) == 65029
        assert_allclose(np.std(valid), 0.12658458001333581)
        assert_allclose(np.mean(valid), 0.4995945318627074)
        assert_allclose(np.median(valid), 0.5003376603126526)

    @pytest.mark.xfail()  # results are not consistent on different machines
    def test_mosaic_background_match(self):
        mosaic(os.path.join(self.tmpdir, 'raw'),os.path.join(self.tmpdir, 'mosaic_bkgmatch'), background_match=True)
        hdu = fits.open(os.path.join(self.tmpdir, 'mosaic_bkgmatch', 'mosaic.fits'))[0]
        assert hdu.data.shape == (288, 282)
        valid = hdu.data[~np.isnan(hdu.data)]
        assert len(valid) == 65029
        assert_allclose(np.std(valid), 0.12661606622654725)
        assert_allclose(np.mean(valid), 0.4994805202294361)
        assert_allclose(np.median(valid), 0.5002447366714478)
