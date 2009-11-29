import os
import random
import string

import commands as m
from status import MontageError


def _make_work_dir():

    # Create overall work dir
    if not os.path.exists('/tmp/pymontage/'):
        os.mkdir('/tmp/pymontage/')

    # Create sub-directory
    random_id = "".join([random.choice(string.letters) for i in xrange(16)])
    work_dir = "/tmp/pymontage/"+random_id
    os.mkdir(work_dir)

    return work_dir

try:

    import pyfits

    def reproject_hdu(in_hdu, **kwargs):
        '''
        Reproject an image (HDU version)

        Required Arguments

            *in_hdu* [ pyfits HDU ]
                Input FITS file to be reprojected.

        Optional Arguments

            See reproject(...)
        '''

        # Make work directory
        work_dir = _make_work_dir()

        in_image = work_dir + '/in.fits'
        out_image = work_dir + '/out.fits'

        pyfits.writeto(in_image, in_hdu.data, in_hdu.header)

        reproject(in_image, out_image, **kwargs)

        out_hdu = pyfits.open(out_image)[0]

        return out_hdu

except:
    pass


def reproject(in_image, out_image, bitpix=None, north_aligned=False,
    system=None, equinox=None, factor=None):
    '''
    Reproject an image

    Required Arguments

        *in_image* [ string ]
            Input FITS file to be reprojected.

        *out_image* [ string ]
            Path of output FITS file to be created.

    Optional Arguments

        *bitpix* [ value ]
            BITPIX value for the ouput FITS file (default is -64). Possible
            values are: 8 (character or unsigned binary integer), 16 (16-bit
            integer), 32 (32-bit integer), -32 (single precision floating
            point), -64 (double precision floating point).

        *north_aligned* [ True | False ]
            Align the pixel y-axis with North

        *system* [ value ]
            Specifies the coordinate system
            Possible values are: EQUJ EQUB ECLJ ECLB GAL SGAL

        *equinox* [ value ]
            If a coordinate system is specified, the equinox can also be given
            in the form YYYY. Default is J2000.

        *factor* [ value ]
            Drizzle factor (see mProject)
    '''

    # Remember start directory
    start_dir = os.path.abspath('.')

    # Find path to input file
    in_image = os.path.abspath(in_image)
    out_image = os.path.abspath(out_image)

    # Make work directory
    work_dir = _make_work_dir()

    # Go to work directory
    os.chdir(work_dir)

    # Create raw directory
    os.mkdir('raw')
    os.mkdir('final')

    # Link to image
    os.symlink(in_image, 'raw/image.fits')

    # Make image table
    m.mImgtbl('raw', 'images_raw.tbl', corners=True)

    # Make new north-aligned header
    m.mMakeHdr('images_raw.tbl', 'header.hdr', north_aligned=north_aligned,
        system=system, equinox=equinox)

    try:
        m.mProjectPP('raw/image.fits', 'final/image.fits', 'header.hdr')
    except MontageError:
        m.mProject('raw/image.fits', 'final/image.fits', 'header.hdr')

    m.mConvert('final/image.fits', 'final/image_b.fits', bitpix=bitpix)

    os.rename('final/image_b.fits', out_image)

    # Go to start directory
    os.chdir(start_dir)

    # Deleting work directory
    print "Deleting work directory " + work_dir
    os.system("rm -r " + work_dir)

    return


def mosaic(input_dir, output_dir, header=None, mpi=False,
    background_match=False, imglist=None, combine="mean", exact_size=False):

    assert combine=='mean' or combine=='median' or combine=='count', \
            "combine should be one of mean/median/count"

    # Find absolute path to files
    start_dir = os.path.abspath('.')
    input_dir = os.path.abspath(input_dir)
    work_dir = _make_work_dir()
    output_dir = os.path.abspath(output_dir)
    if header:
        header = os.path.abspath(header)
    if imglist:
        imglist = os.path.abspath(imglist)

    # Create output dir
    if os.path.exists(output_dir):
        raise Exception("Output directory already exists")
    else:
        os.mkdir(output_dir)

    # Go to work directory
    os.chdir(work_dir)

    # Create symbolic links
    os.symlink(input_dir, 'raw')
    os.symlink(output_dir, 'final')
    if header:
        os.symlink(header, 'header.hdr')
    if imglist:
        os.symlink(imglist, 'imglist')

    # Create temporary directories for Montage
    os.mkdir('projected')
    if background_match:
        os.mkdir('diffs')
        os.mkdir('corrected')

    # List frames to mosaic
    print "Listing raw frames"
    m.mImgtbl('raw', 'images_raw.tbl', img_list=imglist)

    # Compute header if needed
    if not header:
        print "Computing optimal header"
        m.mMakeHdr('images_raw.tbl', 'header.hdr')


    # Projecting raw frames
    print "Projecting raw frames"
    m.mProjExec('images_raw.tbl', 'header.hdr', 'projected', 'stats.tbl',
                    raw_dir='raw', mpi=mpi)

    # List projected frames
    m.mImgtbl('projected', 'images_projected.tbl')

    if background_match:

        # Modeling background

        print "Modeling background"
        m.mOverlaps('images_projected.tbl', 'diffs.tbl')
        m.mDiffExec('diffs.tbl', 'header.hdr', 'diffs', proj_dir='projected',
                    mpi=mpi)
        m.mFitExec('diffs.tbl', 'fits.tbl', 'diffs')
        m.mBgModel('images_projected.tbl', 'fits.tbl', 'corrections.tbl',
                    n_iter=32767, level_only=True)

        # Matching background
        print "Matching background"
        m.mBgExec('images_projected.tbl', 'corrections.tbl', 'corrected',
                    proj_dir='projected')
        os.system('cp corrections.tbl final/')

        # Mosaicking frames
        print "Mosaicking BCD frames"

        m.mImgtbl('corrected', 'images_corrected.tbl')
        m.mAdd('images_corrected.tbl', 'header.hdr', 'final/mosaic64.fits',
                    img_dir='corrected', type=combine, exact=exact_size)
        os.system('cp images_projected.tbl final/')
        os.system('cp images_corrected.tbl final/')

    else:

        # Mosaicking frames
        print "Mosaicking BCD frames"

        m.mAdd('images_projected.tbl', 'header.hdr', 'final/mosaic64.fits',
                    img_dir='projected', type=combine, exact=exact_size)
        os.system('cp images_projected.tbl final/')

    m.mConvert('final/mosaic64.fits', 'final/mosaic.fits', bitpix=-32)
    m.mConvert('final/mosaic64_area.fits', 'final/mosaic_area.fits',
                bitpix=-32)

    os.remove("final/mosaic64.fits")
    os.remove("final/mosaic64_area.fits")

    # Go to start directory
    os.chdir(start_dir)

    # Deleting work directory
    print "Deleting work directory "+work_dir
    os.system("rm -r " + work_dir)

    return
