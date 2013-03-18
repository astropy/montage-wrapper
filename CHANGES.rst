0.9.6 (unreleased)
------------------

- Nothing changed yet.


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
