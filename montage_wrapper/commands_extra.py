# This file contains commands for which wrappers could not be
# auto-generated from the HTML docs

import subprocess
import shlex

from . import status


def mCoverageCheck(in_table, out_table, mode, polygon=None, ra=None,
                   dec=None, width=None, height=None, rotation=None,
                   radius=None, header=None, status_file=None):
    '''
    mCoverageCheck can be used to subset an image metadata table (containing
    FITS/WCS information or image corners) by determining which records in the
    table represent images that overlap with a region definition (box or
    circle in the sky) given on the command line.

    Parameters
    ----------

    in_table : str
        Input metadata table.

    out_table : str
        Output metadata table, to contain subset of in_table.

    mode : str
        How to check for coverage:

        - 'points': use a polygon with points specified by polygon=

        - 'box': use a rectangular box with center given by ra= and
          dec=, and the width given by width=. Optionally, the
          height and rotation can be given by height= and rotation=

        - 'circle': use a circle with center given by ra= and dec= and
          radius given by radius=

        - 'point': use a point given by ra= and dec=

        - 'header': use a header file given by header=

    polygon : list
        A polygon which should be given as [(ra1, dec1), (ra2,
        dec2), ..., (raN, decN)].

    ra : float, optional
        The right ascension of the box, circle, or point

    dec : float, optional
        The declination of the box, circle, or point

    width : float, optional
        The width of the box

    height : float, optional
        The height of the box

    rotation : float, optional
        The rotation of the box

    radius : float, optional
        The radius of the circle

    header : str, optional
        A header file

    status_file : str, optional
        Output and errors are sent to status_file instead of to stdout
    '''

    command = "mCoverageCheck"
    if status_file:
        command += " -s %s" % str(status_file)
    command += " " + str(in_table)
    command += " " + str(out_table)
    command += " -" + mode
    if mode == 'points':
        if polygon is None:
            raise Exception("polygon= needs to be specified for mode='points'")
        for point in polygon:
            command += " " + str(point[0])
            command += " " + str(point[1])
    elif mode == 'box':
        if ra is None:
            raise Exception("ra= needs to be specified for mode='box'")
        if dec is None:
            raise Exception("dec= needs to be specified for mode='box'")
        if width is None:
            raise Exception("width= needs to be specified for mode='box'")
        command += " " + str(ra)
        command += " " + str(dec)
        command += " " + str(width)
        if height is not None:
            command += " " + str(height)
            if rotation is not None:
                command += " " + str(rotation)
        else:
            if rotation is not None:
                raise Exception("Cannot specify rotation without height")

    elif mode == 'circle':
        if ra is None:
            raise Exception("ra= needs to be specified for mode='circle'")
        if dec is None:
            raise Exception("dec= needs to be specified for mode='circle'")
        if radius is None:
            raise Exception("radius= needs to be specified for mode='circle'")
        command += " " + str(ra)
        command += " " + str(dec)
        command += " " + str(radius)
    elif mode == 'point':
        if ra is None:
            raise Exception("ra= needs to be specified for mode='point'")
        if dec is None:
            raise Exception("dec= needs to be specified for mode='point'")
        command += " " + str(ra)
        command += " " + str(dec)
    elif mode == 'header':
        if header is None:
            raise Exception("header= needs to be specified for mode='header'")
        command += " " + header
    else:
        raise Exception("Unknown mode: %s" % mode)
    p = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stderr = p.stderr.read()
    if stderr:
        raise Exception(stderr)
    return status.parse_struct("mCoverageCheck", p.stdout.read().strip())
    
    
def mTileImage(in_image, tiles_x, tiles_y, overlap_x=None, overlap_y=None):
    '''
    mTileImage splits up an image into a given number of tiles.
    An overlap between each tile can optionally be specified. 

    Parameters
    ----------

    in_image : str
        Input FITS file
        
    tiles_x : int
        Number of tiles along x axes.

    tiles_y : int
        Number of tiles along y axes.
        
    overlap_x : int, optional
        Pixel overlap in x direction.
        
    overlap_y : int, optional
        Pixel overlap in y direction.
    '''
    command = "mTileImage"
    if overlap_x or overlap_y:
        command += " -o %s,%s" % (overlap_x, overlap_y)
    command += " -n %s,%s" % (tiles_x, tiles_y)
    command += " " + str(in_image)
    p = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    stderr = p.stderr.read()
    if stderr:
        raise Exception(stderr)
    return status.parse_struct("mTileImage", p.stdout.read().strip())
    