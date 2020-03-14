from mpi4py import MPI
import numpy
import sys


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

from prettytable import PrettyTable

#table to write test
t = PrettyTable(["Amount(element)",'Size(bytes)', 'Time(s)','Rate (MB/s)'])
i=1

while(i<=2*10**6):
    global data
    global wt1
    #sender
    if rank == 0:
        data = numpy.arange(i, dtype=numpy.double)
        # set time start to send
        wt1 = MPI.Wtime()
        req = comm.Isend([data,i,MPI.DOUBLE], dest=1, tag=23)
        req.wait()


    #receiver
    elif rank == 1:
        data = numpy.empty(i, dtype=numpy.double)
        wt1 = MPI.Wtime()
        #set time start to receive
        req = comm.Irecv([data,i,MPI.DOUBLE],source=0,tag=23)
        req.wait()


    #wait time
    wt2 = MPI.Wtime() - wt1
    size = sys.getsizeof(data)
    rate= size/wt2
    rate/=10**6
    # add size , time , rate to report
    t.add_row([i, size, wt2,rate])
    i*=2
if rank == 0:
    print("Sender:")
elif rank == 1:
    print("Receiver:")

print(t)
