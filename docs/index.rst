********************************************
Python Montage wrapper (``montage_wrapper``)
********************************************

.. _numpy: http://www.numoy.org

Introduction
============

This Astropy-affiliated package provides a python wrapper to the Montage
Astronomical Image Mosaic Engine, including both functions to access
individual Montage commands, and high-level functions to facilitate mosaicking
and re-projecting.

Download
========

The latest stable release can be downloaded from `here
<https://pypi.python.org/pypi/montage-wrapper>`_.

Installation
============

This package is a wrapper, not a replacement, for the IPAC Montage mosaicking
software. Therefore, Montage will need to be downloaded from
`http://montage.ipac.caltech.edu <http://montage.ipac.caltech.edu>`_. Once you
have downloaded the latest release on Montage from that website, the
installation should look like::

    tar xvzf Montage_v3.3.tar.gz
    cd Montage_v3.3
    make

then move the ``Montage_v3.3`` directory to wherever you would like to keep
the installation, and add ``<installation_dir>/Montage_v3.3/bin`` to your
``$PATH``, where ``<installation_dir>`` is the directory inside which you put
``Montage_v3.3`` (Montage does not support ``make install``). To check that
Montage is correctly installed, you can type::

    mAdd

If you see something like::

    [struct stat="ERROR", msg="Usage: mAdd [-p imgdir] [-n(o-areas)] [-a mean|median|count] [-e(xact-size)] [-d level] [-s statusfile] images.tbl template.hdr out.fits"]

then the installation succeeded. Otherwise, if you see::

    mAdd: command not found

then you will need to make sure that the ``Montage_v3.3/bin`` contains
commands like ``mAdd``, and that the directory is correctly in your ``$PATH``.


Once the IPAC Montage package is installed, you can install the
Python wrapper with::

    tar xvzf montage-wrapper-x.x.x.tar.gz
    cd montage-wrapper-x.x.x
    python setup.py install

(replacing ``x.x.x`` with the actual version number). The only dependencies
are numpy_ and astropy_.

Using `montage_wrapper`
=======================

Montage commands
----------------

The Montage wrapper is imported using::

    >>> import montage_wrapper

or, for clarity::

    >>> import montage_wrapper as montage

All Montage commands (except ``mJPEG``, ``mMakeImg``, and ``mTileImage``)
are accessible via Python functions. For example, to access ``mProject``, use::

    >>> montage.mProject(...)  # doctest: +SKIP

and see :func:`~montage_wrapper.commands.mProject` for available options. Each
Montage command returns a :class:`~montage_wrapper.status.Struct` object that
contains information/diagnostics. The following example shows how to use the
Montage command wrappers, and how to access the diagnostics::

    >>> montage.mArchiveList('2MASS', 'K', 'm31', 0.5, 0.5, 'm31_list.tbl')  # doctest: +SKIP
    count : 18
    stat : OK
    >>> montage.mMakeHdr('m31_list.tbl', 'header.hdr', north_aligned=True)  # doctest: +SKIP
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
    >>> s = montage.mMakeHdr('m31_list.tbl', 'header.hdr', north_aligned=True)  # doctest: +SKIP
    >>> s.stat  # doctest: +SKIP
    'OK'
    >>> s.lon1  # doctest: +SKIP
    11.267467

See `Reference/API`_ for a full list of available commands and documentation.

High-level functions
--------------------

In addition to wrappers to the individual Montage commands, the following high-level functions are available:

* `~montage_wrapper.wrappers.reproject`: reproject a FITS file
* `~montage_wrapper.wrappers.reproject_hdu`: reproject an FITS HDU object
* `~montage_wrapper.wrappers.mosaic`: mosaic all FITS files in a directory

For example, to mosaic all FITS files in a directory called `raw` using background matching, use:

    >>> montage.mosaic('raw', 'mosaic', background_match=True)  # doctest: +SKIP

In this specific example, a mosaic header will automatically be constructed
from the input files.

For more details on how to use these, see the `Reference/API`_ section.

MPI
---

A few Montage commands can be run using MPI for parallelization (see here).
For MPI-enabled commands (such as `~montage_wrapper.commands.mProjExec`), the use of
MPI is controlled via the mpi= argument. For example, to call ``mProjExec``
using MPI, call ``montage.mProjExec(..., mpi=True)`` (rather than
``montage.mProjExecMPI``, which does not exist). Note however that this
requires the MPI versions of the Montage commands to be installed (which is
not the case by default).

Different MPI installations require different commands (e.g. ``mpirun`` vs
``mpiexec``) as well as different options, so it is possible to customize the
MPI command::

    >>> import montage_wrapper as montage
    >>> montage.set_mpi_command('mpiexec -n {n_proc} {executable}')

The command string should include ``{n_proc}``, which will be replaced by the
number of proceses, and ``{executable}``, which will be replaced by the
appropriate Montage executable. The current MPI command can be accessed with::

    >>> from montage_wrapper.mpi import MPI_COMMAND
    >>> MPI_COMMAND
    'mpiexec -n {n_proc} {executable}'

Reference/API
=============

.. automodapi:: montage_wrapper.wrappers
.. automodapi:: montage_wrapper.commands
.. automodapi:: montage_wrapper.status
