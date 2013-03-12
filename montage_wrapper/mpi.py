MPI_COMMAND = 'mpirun -n {n_proc} {executable}'

def set_mpi_command(command):
    """
    Set the MPI Command to use.
    
    This should contain {n_proc} to indicate the number of processes, and
    {executable} to indicate the name of the executable.
    
    Parameters
    ----------
    command: str
        The MPI command for running executables
        
    Examples
    --------
    
    Use ``mpirun``:
    
    >>> set_mpi_command('mpirun -n {n_proc} {executable}')

    Use ``mpiexec`` with host list:
    
    >>> set_mpi_command('mpiexec -f mpd.hosts -np {n_proc} {executable}')
    """
    MPI_COMMAND = command
    
def _get_mpi_command(executable=None, n_proc=None):
    return MPI_COMMAND.format(executable=executable, n_proc=n_proc)