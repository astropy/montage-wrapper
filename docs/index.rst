**********************
Python Montage wrapper
**********************

Introduction
============

Python-montage is a pure python module that provides a python wrapper to the
Montage Astronomical Image Mosaic Engine, including both functions to access
individual Montage commands, and high-level functions to facilitate
mosaicking and re-projecting.

Installation
============

Python-montage is a wrapper, not a replacement, for the IPAC Montage
mosaicking software. Therefore, Montage will need to be installed (see
`http://montage.ipac.caltech.edu <http://montage.ipac.caltech.edu>`_ for
more details). Once the IPAC Montage package is installed, you can install
python-montage with::

    python setup.py install

The only dependencies are `Numpy <http://www.numpy.org>`_ and `Astropy
<http://www.astropy.org>`_.

Using `montage`
===============

Montage commands
----------------

The python-montage module is imported using::

    import montage

All Montage commands (except ``mJPEG``, ``mMakeImg``, and ``mTileImage``)
are accessible via Python functions. For example, to access ``mProject``, use::

    montage.mProject(...)

and see :func:`~montage.commands.mProject` for available options. Each
Montage command returns a :class:`~montage.status.Struct` object that
contains information/diagnostics. The following example shows how to use the
Montage command wrappers, and how to access the diagnostics::

    >>> montage.mArchiveList('2MASS', 'K', 'm31', 0.5, 0.5, 'm31_list.tbl')
    count : 18
    stat : OK
    >>> montage.mMakeHdr('m31_list.tbl', 'header.hdr', north_aligned=True)
    count : 18
    lat4 : 41.744136
    stat : OK
    lat1 : 40.912238
    lat3 : 41.744136
    latsize : 0.831951
    clon : 10.717965
    lonsize : 0.830562
    posang : 0.0
    lon4 : 11.274528
    lat2 : 40.912238
    lon1 : 11.267467
    clat : 41.32951
    lon2 : 10.168464
    lon3 : 10.161403
    >>> s = montage.mMakeHdr('m31_list.tbl', 'header.hdr', north_aligned=True)
    >>> s.stat
    'OK'
    >>> s.lon1
    11.267467

See `Reference/API`_ for a full list of available commands and documentation.

High-level functions
--------------------

In addition to wrappers to the individual Montage commands, the following high-level functions are available:

* `~montage.wrappers.reproject`: reproject a FITS file
* `~montage.wrappers.reproject_hdu`: reproject an FITS HDU object
* `~montage.wrappers.mosaic`: mosaic all FITS files in a directory

For example, to mosaic all FITS files in a directory called `raw` using background matching, use:

    >>> montage.mosaic('raw', 'mosaic', background_match=True)

In this specific example, a mosaic header will automatically be constructed
from the input files.

For more details on how to use these, see the `Reference/API`_ section.

MPI
---

A few Montage commands can be run using MPI for parallelization (see here).
For MPI-enabled commands (such as `~montage.commands.mProjExec`), the use of
MPI is controlled via the mpi= argument. For example, to call ``mProjExec``
using MPI, call ``montage.mProjExec(..., mpi=True)`` (rather than
``montage.mProjExecMPI``, which does not exist).

Reference/API
=============

.. automodapi:: montage.wrappers
.. automodapi:: montage.commands
