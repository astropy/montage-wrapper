import os
import shutil as sh
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

    return work_dir + "/"

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
    system=None, equinox=None, factor=None, cleanup=True):
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

    # Find path to input and output file
    in_image = os.path.abspath(in_image)
    out_image = os.path.abspath(out_image)

    # Make work directory
    work_dir = _make_work_dir()

    # Create raw directory
    os.mkdir(work_dir + 'raw')
    os.mkdir(work_dir + 'final')

    # Link to image
    os.symlink(in_image, work_dir + 'raw/image.fits')

    # Make image table
    m.mImgtbl(work_dir + 'raw', work_dir + 'images_raw.tbl', corners=True)

    # Make new north-aligned header
    m.mMakeHdr(work_dir + 'images_raw.tbl', work_dir + 'header.hdr', north_aligned=north_aligned,
        system=system, equinox=equinox)

    try:
        m.mProjectPP(work_dir + 'raw/image.fits', work_dir + 'final/image.fits', work_dir + 'header.hdr')
    except MontageError:
        m.mProject(work_dir + 'raw/image.fits', work_dir + 'final/image.fits', work_dir + 'header.hdr')

    m.mConvert(work_dir + 'final/image.fits', out_image, bitpix=bitpix)

    if cleanup:
        # Deleting work directory
        print "Deleting work directory %s" % work_dir
        os.system("rm -r " + work_dir)
    else:
        # Leave work directory as it is
        print "Leaving work directory %s" % work_dir

    return


def mosaic(input_dir, output_dir, header=None, mpi=False, n_proc=8,
    background_match=False, imglist=None, combine="mean", exact_size=False,
    cleanup=True, bitpix=-32):

    assert combine=='mean' or combine=='median' or combine=='count', \
            "combine should be one of mean/median/count"

    # Find path to input and output directory
    input_dir = os.path.abspath(input_dir) + "/"
    output_dir = os.path.abspath(output_dir) + "/"

    # Make work directory
    work_dir = _make_work_dir()

    # Find path to header file if specified
    if header:
        header = os.path.abspath(header)

    # Find path to image list if specified
    if imglist:
        imglist = os.path.abspath(imglist)

    # Create output dir
    if os.path.exists(output_dir):
        raise Exception("Output directory already exists")
    else:
        os.mkdir(output_dir)

    # Create symbolic links
    os.symlink(input_dir, work_dir + 'raw')

    if header:
        os.symlink(header, work_dir + 'header.hdr')

    if imglist:
        os.symlink(imglist, work_dir + 'imglist')

    # Create temporary directories for Montage
    os.mkdir(work_dir + 'projected')
    if background_match:
        os.mkdir(work_dir + 'diffs')
        os.mkdir(work_dir + 'corrected')

    # List frames to mosaic
    print "Listing raw frames"
    m.mImgtbl(work_dir + 'raw', work_dir + 'images_raw.tbl', img_list=imglist)

    # Compute header if needed
    if not header:
        print "Computing optimal header"
        m.mMakeHdr(work_dir + 'images_raw.tbl', work_dir + 'header.hdr')


    # Projecting raw frames
    print "Projecting raw frames"
    m.mProjExec(work_dir + 'images_raw.tbl', work_dir + 'header.hdr', work_dir + 'projected', work_dir + 'stats.tbl',
                    raw_dir=work_dir + 'raw', mpi=mpi, n_proc=n_proc)

    # List projected frames
    m.mImgtbl(work_dir + 'projected', work_dir + 'images_projected.tbl')

    if background_match:

        # Modeling background

        print "Modeling background"
        m.mOverlaps(work_dir + 'images_projected.tbl', work_dir + 'diffs.tbl')
        m.mDiffExec(work_dir + 'diffs.tbl', work_dir + 'header.hdr', work_dir + 'diffs', proj_dir=work_dir + 'projected',
                    mpi=mpi, n_proc=n_proc)
        m.mFitExec(work_dir + 'diffs.tbl', work_dir + 'fits.tbl', work_dir + 'diffs')
        m.mBgModel(work_dir + 'images_projected.tbl', work_dir + 'fits.tbl', work_dir + 'corrections.tbl',
                    n_iter=32767, level_only=True)

        # Matching background
        print "Matching background"
        m.mBgExec(work_dir + 'images_projected.tbl', work_dir + 'corrections.tbl', work_dir + 'corrected',
                    proj_dir=work_dir + 'projected')
        sh.copy(work_dir + 'corrections.tbl', output_dir)

        # Mosaicking frames
        print "Mosaicking BCD frames"

        m.mImgtbl(work_dir + 'corrected', work_dir + 'images_corrected.tbl')
        m.mAdd(work_dir + 'images_corrected.tbl', work_dir + 'header.hdr', output_dir + 'mosaic64.fits',
                    img_dir=work_dir + 'corrected', type=combine, exact=exact_size)
        sh.copy(work_dir + 'images_projected.tbl', output_dir)
        sh.copy(work_dir + 'images_corrected.tbl', output_dir)

    else:

        # Mosaicking frames
        print "Mosaicking BCD frames"

        m.mAdd(work_dir + 'images_projected.tbl', work_dir + 'header.hdr', output_dir + 'mosaic64.fits',
                    img_dir=work_dir + 'projected', type=combine, exact=exact_size)
        sh.copy(work_dir + 'images_projected.tbl', output_dir)

    m.mConvert(output_dir + 'mosaic64.fits', output_dir + 'mosaic.fits', bitpix=bitpix)
    m.mConvert(output_dir + 'mosaic64_area.fits', output_dir + 'mosaic_area.fits',
                bitpix=bitpix)

    os.remove(output_dir + "mosaic64.fits")
    os.remove(output_dir + "mosaic64_area.fits")

    if cleanup:
        # Deleting work directory
        print "Deleting work directory %s" % work_dir
        os.system("rm -r " + work_dir)
    else:
        # Leave work directory as it is
        print "Leaving work directory %s" % work_dir

    return
