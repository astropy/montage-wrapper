import numpy as np

from astropy.table import Table

from ..commands import *


def test_all():

    stat = mArchiveList('2MASS', 'k', 'M31', 0.2, 0.2, 'm31_2mass_k.tbl')
    assert stat.stat == 'OK'

    t = Table.read('m31_2mass_k.tbl', format='ascii.ipac')
    stat = mArchiveGet(t[0]['URL'], 'test.fits')
    assert stat.stat == 'OK'

    stat = mArchiveExec('m31_2mass_k.tbl')
    assert stat.stat == 'OK'

    stat = mBestImage('m31_2mass_k.tbl', 10.717773, 41.064461)
    assert stat.stat == 'OK'
    assert stat.file == "2mass-atlas-971024n-k0080044.fits.gz"

    stat = mGetHdr('2mass-atlas-971024n-k0080044.fits.gz', 'header.hdr')
    assert stat.stat == 'OK'

    t = Table()
    t['ra'] = np.random.uniform(10.70, 10.72, 100)
    t['dec'] = np.random.uniform(41.05, 41.07, 100)
    t['flux'] = np.random.random(100)
    t.write('sources.tbl', format='ascii.ipac')

    stat = mCatMap('sources.tbl', 'test_with_sources.fits', 'header.hdr', column='flux')
    assert stat.stat == 'OK'

    stat = mMakeHdr('m31_2mass_k.tbl', 'full_header.hdr')
    assert stat.stat == 'OK'

    stat = mExec('2MASS', 'k', n_tile_x=1, n_tile_y=1, level_only=True, keep=False,
                   remove=True, output_image='test_mosaic.fits',
                   region_header='full_header.hdr')
    assert stat.stat == 'OK'

    # Currently fails due to a bug in Montage
    # stat = mFixNaN('2mass-atlas-971024n-k0080044.fits.gz', 'test_nan.fits',
    #                  nan_value=3)
    # assert stat.stat == 'OK'
    # stat = mFixNaN('2mass-atlas-971024n-k0080044.fits.gz', 'test_blank.fits',
    #                  nan_value=3, min_blank=1, max_blank=3)
    # assert stat.stat == 'OK'

    stat = mHdr('M31', 0.3, 'test.hdr', system='eq', height=0.2, pix_size=10, rotation=22)
    assert stat.stat == 'OK'

    stat = mHdrCheck('2mass-atlas-971024n-k0080044.fits.gz')
    assert stat.stat == 'OK'

    stat = mHdrtbl('.', 'header_table.tbl')
    assert stat.stat == 'OK'

    stat = mPix2Coord('test.hdr', 10, 10)
    assert stat.stat == 'OK'

    stat = mProject('2mass-atlas-971024n-k0080044.fits.gz', 'test.fits', 'test.hdr', factor=0.7, scale=1.2)
    assert stat.stat == 'OK'

    stat = mProjectPP('2mass-atlas-971024n-k0080044.fits.gz', 'test.fits', 'test.hdr', factor=0.7, scale=1.2)
    assert stat.stat == 'OK'

    stat = mPutHdr('2mass-atlas-971024n-k0080044.fits.gz', 'new.fits', 'header.hdr')
    assert stat.stat == 'OK'

    stat = mRotate('2mass-atlas-971024n-k0080044.fits.gz', 'rotated.fits', rotation_angle=10)
    assert stat.stat == 'OK'

    stat = mShrink('2mass-atlas-971024n-k0080044.fits.gz', 'shrunk.fits', 3)
    assert stat.stat == 'OK'

    stat = mSubimage('2mass-atlas-971024n-k0080044.fits.gz', 'sub.fits', 10.717773, 41.064461, 0.1)
    assert stat.stat == 'OK'

    stat = mSubimage_pix('2mass-atlas-971024n-k0080044.fits.gz', 'subpix.fits', 10, 20, 30)
    assert stat.stat == 'OK'

    stat = mSubset('m31_2mass_k.tbl', 'test.hdr', 'subset.tbl')
    assert stat.stat == 'OK'

    stat = mTANHdr('test.hdr', 'new.hdr')
    assert stat.stat == 'OK'

    stat = mTblSort('m31_2mass_k.tbl', 'crval1', 'sorted.tbl')
    assert stat.stat == 'OK'

    stat = mTileHdr('test.hdr', 'new.hdr', 10, 10, 0, 0)
    assert stat.stat == 'OK'
