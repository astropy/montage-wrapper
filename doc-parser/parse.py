import os
import glob
import textwrap
import string

from BeautifulSoup import BeautifulSoup


def optional(command, option):
    if command == 'mExec' and option == 'workspace-dir':
        return True
    if command == 'mMakeHdr' and option in ['system', 'equinox']:
        return True
    if command == 'mFixNan' and option in ['minblank', 'maxblank']:
        return True
    if command == 'mRotate' and option in ['ra', 'dec', 'xsize', 'ysize']:
        return True
    if command == 'mTileHdr' and option in ['xpad', 'ypad']:
        return True
    if command == 'mSubimage' and option in ['ysize']:
        return True
    if command == 'mSubimage_pix' and option in ['ypixsize']:
        return True
    return False


def suboptional(command, option):
    if command == 'mRotate' and option in ['ysize']:
        return True
    if command == 'mTileHdr' and option in ['ypad']:
        return True
    if command == 'mMakeHdr' and option in ['equinox']:
        return True
    return False


# MPI stuff
mpi_enabled = ['mProjExec', 'mFitExec', 'mDiffExec', 'mBgExec', 'mAdd', 'mAddExec']
mpi_description = "If set to True, will use the MPI-enabled versions of the Montage executable."
nproc_description = "If mpi is set to True, n_proc is the number of processes to run simultaneously (default is 8)"

opt_dict = {}
opt_dict['-d'] = 'debug'
opt_dict['-e'] = 'exact'
opt_dict['-X'] = 'whole'
opt_dict['-c'] = 'corners'
opt_dict['-b'] = 'output_invalid'
opt_dict['-l'] = 'level_only'
opt_dict['-p'] = 'pixel_location'
opt_dict['-a'] = 'all_pixels'
opt_dict['-f'] = 'fast_mode'
opt_dict['-r'] = 'recursive'
opt_dict['-n'] = 'no_area'
opt_dict['-k'] = 'keep'


def option_name(command, option):
    '''
    Given a Montage command and an option, returns an explicit name for the option
    '''
    if command == 'mMakeHdr' and option == '-n':
        return 'north_aligned'
    elif command == 'mImgtbl' and option == '-a':
        return 'include_area'
    elif command == 'mShrink' and option == '-f':
        return 'fixed_size'
    elif command == 'mArchiveGet' and option == '-r':
        return 'raw'
    elif option in opt_dict:
        return opt_dict[option]
    else:
        raise Exception("Don't know what to do with %s for %s" % (option, command))

req_dict = {}
req_dict['blankval'] = 'blank_value'
req_dict['colname'] = 'column_name'
req_dict['corrdir'] = 'corr_dir'
req_dict['diffdir'] = 'diff_dir'
req_dict['fieldlistfile'] = 'fieldlist'
req_dict['flatdir'] = 'flat_dir'
req_dict['imgdir'] = 'img_dir'
req_dict['imglist'] = 'img_list'
req_dict['img_image'] = 'in_image'
req_dict['localfile'] = 'local_file'
req_dict['maxblank'] = 'max_blank'
req_dict['maxiter'] = 'max_iter'
req_dict['maxval'] = 'max_val'
req_dict['minblank'] = 'min_blank'
req_dict['minval'] = 'min_val'
req_dict['niter'] = 'n_iter'
req_dict['ntilex'] = 'n_tile_x'
req_dict['ntiley'] = 'n_tile_y'
req_dict['nx'] = 'n_x'
req_dict['ny'] = 'n_y'
req_dict['outfile'] = 'out_file'
req_dict['pixsize'] = 'pix_size'
req_dict['projdir'] = 'proj_dir'
req_dict['rawdir'] = 'raw_dir'
req_dict['refimg'] = 'ref_img'
req_dict['refmag'] = 'ref_mag'
req_dict['remoteref'] = 'remote_ref'
req_dict['restartrec'] = 'restart_rec'
req_dict['rotang'] = 'rotation_angle'
req_dict['scaleColumn'] = 'scale_column'
req_dict['statusfile'] = 'status_file'
req_dict['tiledir'] = 'tile_dir'
req_dict['weightfile'] = 'weight_file'


def required_argument_name(command, argument):
    '''
    Given a Montage command and an argument, returns a sanitized name for the argument
    '''

    argument = argument.replace('.fits', '_image')
    argument = argument.replace('.tbl', '_table')
    argument = argument.replace('.hdr', '_header')
    argument = argument.replace('-', '_')

    if argument in ['level', 'debug']:
        return 'debug_level'
    elif argument == 'in1_image':
        return 'in_image_1'
    elif argument == 'in2_image':
        return 'in_image_2'

    if len(set(argument) - set(string.letters + "_" + string.digits)) == 0:
        if argument in req_dict:
            return req_dict[argument]
        else:
            return argument
    elif argument == 'hdr.template':
        return 'template_header'
    elif argument == 'object|location':
        return 'object_or_location'
    else:
        raise Exception("Don't know what to do with %s for %s" % (argument, command))

# Construct text wrapper for docstring
docwrapper = textwrap.TextWrapper(
                initial_indent=" " * 8, subsequent_indent=" " * 8, width=78)

# Construct text wrapper for function declaration
defwrapper = textwrap.TextWrapper(
                initial_indent="", subsequent_indent=" " * 10, width=78)

# Construct text wrapper for function description
descwrapper = textwrap.TextWrapper(
                initial_indent="    ", subsequent_indent="    ", width=78)

# Open output file
fo = open('commands.py', 'wb')
fo.write('import subprocess\nimport status\nimport shlex\nfrom .commands_extra import *\n')

# Cycle through API files
for api_file in glob.glob(os.path.join('api/', '*.html')):

    # Read file
    html = file(api_file, 'rb').read()

    # Fix some tags
    html = html.replace(u'</i</dd>', u'</i></dt>')
    html = html.replace(u'!<DOCTYP', u'<!DOCTYP')
    html = html.replace(u'-niter', u'niter')
    html = html.replace(u'NaN-value', u'nan_value')
    html = html.replace(u'<a href="mArchiveGet.html>', u'<a href="mArchiveGet.html">')
    html = html.replace(u'<dt>\n  <dt>', '<dt>')
    # Parse HTML
    soup = BeautifulSoup(html)

    # Find command name
    command = ''.join(soup.find('h1').findAll(text=True))

    # Find all options
    description = None
    options = []
    options_descr = []
    n_args = 0

    for element in soup.findAll('dl'):

        if element['class'] == 'description' and not description:
            description = ''.join(element.find('dd').findAll(text=True))

        if element['class'] == 'args' and n_args < 2:

            n_args += 1

            for arg in element.findAll('dt'):
                options.append(''.join(arg.findAll(text=True)))

            for desc in element.findAll('dd'):
                options_descr.append(''.join(desc.findAll(text=True)))

    optional_arguments = ''
    required_arguments = ''
    optional_docstring = ''
    required_docstring = ''

    if command in mpi_enabled:
        code = '    if mpi:\n        command = "mpirun -n %%i %sMPI" %% n_proc\n    else:\n        command = "%s"\n' % (command, command)
    else:
        code = '    command = "%s"\n' % command

    # Special case
    code = code.replace('mSubimage_pix', 'mSubimage -p')

    for i, arg in enumerate(options):

        options[i] = options[i].replace('(optional)', '')
        option = options[i].split()
        option_description = options_descr[i].strip()
        option_description = option_description.replace('\n', ' ')
        option_description = string.join(option_description.split(), " ")
        option_description = option_description.replace('.fits', '_image')
        option_description = option_description.replace('.tbl', '_table')
        option_description = option_description.replace('.hdr', '_header')
        option_description = option_description.replace('switch', 'option')
        option_description = option_description.replace('flag', 'option')
        option_description = option_description.replace('. (', ' (')

        if command in ['mAdd', 'mAddExec'] and option[0] == '-p':
            option_description = option_description.replace('-p option', 'imgdir option')
            option_description = option_description.replace('mAdd modules', 'mAdd command')
        elif command == 'mBgModel':
            option_description = option_description.replace('without switch, ', '')
        elif command == 'mImgtbl':
            option_description = option_description.replace('"-r" (recursive) option', 'recursive option')
            option_description = option_description.replace('"-c" (corners)', 'corners')
            option_description = option_description.replace('Example: example.fieldlist.', '')
            option_description = option_description.replace('Example: example.imglist.', '')
            option_description = option_description.replace('proessing', 'processing')
        elif command == 'mConvert' and option[0] == '-b':
            option_description = option_description.replace('integer) ', 'integer), ')
            option_description = option_description.replace('point) ', 'point), ')
        elif command == 'mDiff':
            option_description = option_description.replace('-n option', 'the no_area option')
            option_description = option_description.replace(' in1_area.fits', '')
            option_description = option_description.replace(' in2_area.fits', '')
        elif command == 'mShrink':
            option_description = option_description.replace('-f (fixed-size)', 'fixed_size')
        elif command == 'mSubset':
            option_description = option_description.replace('-c option', 'corners option')
        elif command == 'mHdr':
            if option[0] == 'object|location':
                option_description = "Object string or coordinate location"
            if option[0] == '-s':
                option_description = 'Specify a coordinate system. Can be one of: "equatorial" or "eq" (default), "ecliptic" or "ec" "galactic", "ga", "supergalactic" or "sgal"'
        elif command == 'mArchiveGet':
            if option[0] == 'remote_ref':
                option_description = "URL of remote FITS file to retrieve"
        elif command == 'mFixNan':
            option_description = option_description.replace('"-v" option', 'nan_value option')
        elif command == 'mHdrtbl':
            option_description = option_description.replace('"-r" (recursive) option', 'recursive option')
            option_description = option_description.replace('"-c" option', 'corners option')
            option_description = option_description.replace('Example: example.imglist.', '')
            option_description = option_description.replace('"-c" (corners)', 'corners')
        elif command == 'mExec':
            option_description = option_description.replace('("-r" option)', '(raw_dir option)')

        for argument in req_dict:
            option_description = option_description.replace(argument, req_dict[argument])

        # First, boolean arguments
        if len(option) == 1 and option[0][0] == '-':

            variable = option_name(command, option[0])

            optional_arguments += ', %s=False' % variable

            optional_docstring += '\n    %s : bool, optional\n' % variable + docwrapper.fill(option_description) + '\n'

            code += '    if %s:\n        command += " %s"\n' % (variable, option[0])

        elif len(option) == 2 and option[0][0] == '-':

            variable = required_argument_name(command, option[1])

            default = 'None'
            optional_arguments += ', %s=%s' % (variable, default)

            optional_docstring += '\n    %s : value, optional\n' % variable + docwrapper.fill(option_description) + '\n'

            code += '    if %s:\n        command += " %s %%s" %% str(%s)\n' % (variable, option[0], variable)

        elif option[0][0] != '-' and optional(command, option[0]):

            if suboptional(command, option[0]):
                pad = "    "
            else:
                pad = ""

            variables = ""

            variable = required_argument_name(command, option[0])
            if_statement = [pad + "    if %s" % variable]
            for opt in option[1:]:
                variable = required_argument_name(command, opt)
                if_statement += ["%s" % variable]

            code += string.join(if_statement, " and ") + ":\n"

            for opt in option:

                variable = required_argument_name(command, opt)
                variables += variable + ", "

                default = 'None'
                optional_arguments += ', %s=%s' % (variable, default)

                code += pad + '        command += " %%s" %% str(%s)\n' % variable

            optional_docstring += '\n    %s : value, optional\n' % variables[:-2] + docwrapper.fill(option_description) + '\n'

        elif option[0][0] != '-':

            variables = ""

            for opt in option:

                variable = required_argument_name(command, opt)
                variables += variable + ", "

                required_arguments += ', %s' % variable

                if variable in ['object_or_location', 'remote_ref']:
                    code += "    command += ' \"' + str(%s) + '\"'\n" % variable
                else:
                    code += '    command += " " + str(%s)\n' % variable

            required_docstring += '\n    %s : value\n' % variables[:-2] + docwrapper.fill(option_description) + '\n'

    if command in mpi_enabled:

        optional_arguments += ', mpi=False, n_proc=8'
        optional_docstring += '\n    mpi : bool, optional\n' + docwrapper.fill(mpi_description) + '\n'
        optional_docstring += '\n    n_proc : int, optional\n' + docwrapper.fill(nproc_description) + '\n'

    arguments = 'def %s(%s%s):' % (command, required_arguments[2:], optional_arguments)
    arguments = '\n' + defwrapper.fill(arguments) + '\n'

    description = descwrapper.fill(description)

    docstring = "    '''\n%s\n" % description

    if len(required_docstring.strip()) > 0 or len(optional_docstring.strip()) > 0:
        docstring += "\n    Parameters"
        docstring += "\n    ----------\n"

    if len(required_docstring.strip()) > 0:
        docstring += required_docstring

    if len(optional_docstring.strip()) > 0:
        docstring += optional_docstring

    docstring += "    '''\n"

    code += '    p = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,\n        stderr=subprocess.PIPE)\n    stderr = p.stderr.read()\n    if stderr:\n        raise Exception(stderr)\n    return status.parse_struct("%s", p.stdout.read().strip())\n\n' % command

    fo.write(arguments)
    fo.write(docstring)
    fo.write(code)

fo.close()
