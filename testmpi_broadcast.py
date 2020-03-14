from mpi4py import MPI
import numpy
from prettytable import PrettyTable
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

t = PrettyTable(["Amount(element)",'Size(bytes)', 'Time(s)','Rate (MB/s)'])
#broad cast nonbuffer

if rank == 0:
    data1={'test':'success'}
else:
    data1 = None

data1 = comm.bcast(data1, root=0)


#broad cast has buffer

i=1

while(i<=2*10**6):
    global data
    global wt1
    if rank == 0:
        data = numpy.arange(i, dtype='i')
    else:
        data = numpy.empty(i, dtype='i')
    wt1 = MPI.Wtime()
    comm.Bcast(data, root=0)
    wt2 = MPI.Wtime() - wt1
    size = sys.getsizeof(data)
    rate = size / wt2
    rate /= 10 ** 6
    # add size , time , rate to report
    t.add_row([i, size, wt2, rate])
    i *= 2

if rank == 0:
    print("Sender:")
else:
    print("Receiver:")

print(t)