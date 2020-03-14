from mpi4py import MPI
import numpy

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
status = MPI.Status()
if rank == 0:
    data = numpy.arange(2000000, dtype=numpy.double)
    req = comm.Isend([data,2000000,MPI.DOUBLE], dest=1, tag=11)
    req.wait()
    print("sender:",data)
elif rank == 1:
    data= numpy.empty(2000000, dtype=numpy.double)
    print("recieve:", data)
    req = comm.Irecv([data,2000000,MPI.DOUBLE],source=0, tag=11)
    req.wait()
    print("recieve:",data)