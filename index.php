<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
   "http://www.w3.org/TR/html4/loose.dtd">

<html>
   <head>
      <link rel="stylesheet" href="style.css" type="text/css" media="screen" title="no title" charset="utf-8">
      <link rel="stylesheet" href="style_code.css" type="text/css" media="screen" title="no title" charset="utf-8">
   </head>
   <body>
      <div id="main">
         
         <div class='title'>A Python wrapper for the Montage mosaicking software</div><br>
         
         <div class='subtitle'>Introduction</div><br>
         
         Python-montage is a pure python module that provides a python API to
         the <a href="http://montage.ipac.caltech.edu/">Montage</a> Astronomical
         Image Mosaic Engine, including both functions to access
         individual Montage commands, and high-level functions to facilitate
         mosaicking and reprojecting.
         <br><br>
         
         <center>
         <a href="https://sourceforge.net/projects/python-montage/files/">Download the latest version</a><br>(0.9.0, released 30 December 2009)
         </center>
         <br>

         To report bugs and request features, please use the Sourceforge <a href="http://sourceforge.net/tracker/?group_id=290994&atid=1230860">bug</a> and <a href="http://sourceforge.net/tracker/?group_id=290994&atid=1230863">feature request</a> trackers. To contact me directly, please use <b>robitaille at users dot sourceforge dot net</b>.<br><br>
         
         <div class='subtitle'>Installation</div><br>
         
         To install, simply run <code>python setup.py install</code> inside
         the <code>python-montage-x.x.x directory</code>.
         Alternatively, python-montage can be installed using <code>easy_install python-montage</code> if you have <code>setuptools</code> installed.<br><br>

         The only dependency for python-montage is the <a href="http://montage.ipac.caltech.edu/">Montage</a> software itself. Additionally, if the <a href="http://www.stsci.edu/resources/software_hardware/pyfits">pyfits</a> module is installed, a reproject_hdu function will be available. Finally, MPI is required in order to use the MPI-enabled Montage commands. Note that the Montage MPI-enabled commands are not installed by default.<br><br>
                  
         <div class='subtitle'>Documnentation</div><br>
         
         The python-montage module is imported using <code>import montage</code>.
         All Montage commands (except <code>mCoverageCheck</code>,
         <code>mJPEG</code>, <code>mMakeImg</code>, and
         <code>mTileImage</code>) are implemented. For example, to access
         <code>mProject</code>, use <code>montage.mProject</code>, and for usage
         instructions, use <code>help(montage.mProject)</code>.
         
         In addition, the following high-level functions are available:
         
         <ul>
            <li><code>montage.reproject</code>: reproject a FITS file
            <li><code>montage.reproject_hdu</code>: reproject a pyfits HDU image object
            <li><code>montage.mosaic</code>: mosaic all FITS files in a directory
         </ul>
         
         For details on how to use these, use the <code>help</code> command.<br><br>
         
         A few Montage commands can be run using MPI for parallelization (see
         <a
         href="http://montage.ipac.caltech.edu/docs/gridtools.html">here</a>).
         For MPI-enabled commands (such as <code>mProjExec</code>), the use of
         MPI is controlled via the <code>mpi=</code> argument. For example, to
         call <code>mProjExec</code> using MPI, call
         <code>montage.mProjExec(..., mpi=True)</code> (rather than
         <code>montage.mProjExecMPI</code>).<br><br>
         
         <div class='subtitle'>Example</div><br>
         
         The following example illustrates how python-montage can be used to call basic Montage commands as well as how to retrieve and access the status object.<br>
         
         <div class='code'>
         <?php include('demo.php');?>
         </div>
         
         
         
      </div>
   </body>
</html>
