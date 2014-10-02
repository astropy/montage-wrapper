0.9.9 (unreleased)
------------------

- Fix bug that caused drizzle factor to be ignored in reproject, reproject_hdu,
  and reproject_cube.

0.9.8 (2014-09-14)
------------------

- Added wrapper for mTileImage command. [#14]

- Fix typo in name of mFixNaN command. [#16]

- Ensure that reproject_hdu cleans up any temporary directories. [#17]

- Make sure that temporary directories created by mosaic() are always removed. [#19]

- The code base is now fully Python 2 and 3 compatible, and 2to3 is no longer used. [#20]

- Use the astropy-helpers package. [#21]

0.9.7 (2013-11-02)
------------------

- Disabled configuration file since it is not used. This gets rid of the
  warning at import time.

- No longer check if Montage is in the PATH on install, but instead just on
  import.

0.9.6 (2013-10-31)
------------------

- Added missing files required for installation

- Added a unit test for `mosaic`

0.9.5 (2013-03-18)
------------------

- removed unused files

- added documentation about setting custom MPI command

0.9.4 (2013-03-18)
------------------

- python-montage is now an Astropy affiliated package, and has been
  renamed to montage_wrapper.

- improved performance of mosaic() by ignoring frames that don't overlap with
  the requested header. Also improved exceptions in mosaic().

- new function ``reproject_cube`` to reproject a FITS cube slice by slice
  (thanks to Adam Ginsburg).

- various bug fixes reported by users, and improved documentation.

0.9.3
-----

- Fixed bug with user-specified work directory

- Allow user to specify whether to only adjust levels when carrying out
  the background matching

0.9.2
-----

- Migrated to GitHub

- Improved handing to check whether Montage commands are present

- Improved handling of temporary work directory

0.9.1
-----

- Minor bug fixes and improvements

0.9.0
-----

- Initial release
