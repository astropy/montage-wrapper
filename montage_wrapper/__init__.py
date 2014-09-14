# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
This is an Astropy affiliated package.
"""

# Affiliated packages may add whatever they like to this file, but
# should keep this content at the top.
# ----------------------------------------------------------------------------
from ._astropy_init import *
# ----------------------------------------------------------------------------

# For egg_info test builds to pass, put package imports here.
if not _ASTROPY_SETUP_:

    from .commands import *
    from .wrappers import *
    from .mpi import set_mpi_command

    # Check whether Montage is installed
    installed = False
    for dir in os.environ['PATH'].split(':'):
        if os.path.exists(dir + '/mProject'):
            installed = True
            break

    import textwrap

    error_wrap = textwrap.TextWrapper(initial_indent=" " * 11,
                                      subsequent_indent=" " * 11,
                                      width=72)

    MONTAGE_MISSING = """
    ERROR: Montage commands could not be found.

    In order to use the montage_wrapper module, you will first need to
    install the IPAC Montage software from:

        http://montage.ipac.caltech.edu

    and ensure that the Montage commands (e.g. mAdd, mProject, etc.) are in
    your $PATH. Your current $PATH variable contains the following paths,
    but none of them contain the Montage commands:

        PATH = {path}

    If the Montage commands are in one of these directories, then please
    report this as an issue with montage-wrapper.
    """.format(path=error_wrap.fill(os.environ['PATH']).strip())

    ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'

    if not ON_RTD and not installed:
        print(MONTAGE_MISSING)
        import sys
        sys.exit(1)
