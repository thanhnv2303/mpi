from mpi4py import MPI
from prettytable import PrettyTable
import sys
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size =comm.Get_size()

def bcast():
    if rank == 0:
        data = {'from': rank,
                'msg': "Hello this message from process 0 "}
    else:
        data = None

    wt1 = MPI.Wtime()
    data = comm.bcast(data, root=0)
    wt2 = MPI.Wtime() - wt1

    return data,wt2
def scatter():
    if rank == 0:
        data = [i for i in range(size)]
    else:
        data = None

    wt1 = MPI.Wtime()
    data = comm.scatter(data, root=0)
    wt2 = MPI.Wtime() - wt1

    return data, wt2


def gather():
    data = rank
    wt1= MPI.Wtime()
    data = comm.gather(data, root=0)
    wt2 = MPI.Wtime() - wt1

    return data, wt2
def Bcast():
    if rank == 0:
        data = np.arange(10**7, dtype='i')
    else:
        data = np.empty(10**7, dtype='i')
    wt1 = MPI.Wtime()
    comm.Bcast(data, root=0)
    wt2 = MPI.Wtime() - wt1

    return data, wt2

def Scatter():
    sendbuf = None
    if rank == 0:
        sendbuf = np.empty([size, 10**7], dtype='i')
        sendbuf.T[:, :] = range(size)
    recvbuf = np.empty(10**7, dtype='i')
    wt1 = MPI.Wtime()
    comm.Scatter(sendbuf, recvbuf, root=0)

    wt2 = MPI.Wtime() - wt1

    return sendbuf, wt2


def Gather():
    sendbuf = np.zeros(10**7, dtype='i') + rank
    recvbuf = None
    if rank == 0:
        recvbuf = np.empty([size, 10**7], dtype='i')
    wt1 = MPI.Wtime()
    comm.Gather(sendbuf, recvbuf, root=0)
    wt2 = MPI.Wtime() - wt1

    return sendbuf, wt2

if rank == 0 :
    print("The number of processes:", size)

def test_perfomencetopo(collective):
    table = PrettyTable(["rank",'data size(bytes)', '3D topo time(s)','2D topo time(s)','1D topo time(s)'])
    #create 3D topology
    comm.Create_cart(dims = [2,2,2],periods =[True,True,True],reorder=False)

    data,wt3d = collective()
    comm.Barrier()
    data_size = sys.getsizeof(data)
    test_info=[rank,data_size,wt3d]

    # create 2D topology
    comm.Create_cart(dims=[4, 2], periods=[True, True], reorder=False)
    data, wt2d = collective()
    comm.Barrier()
    test_info.append(wt2d)

    # create 1D topology
    comm.Create_cart(dims=[8], periods=[True], reorder=False)
    data, wt1d = collective()
    comm.Barrier()
    test_info.append(wt1d)


    test_info = comm.gather(test_info, root=0)
    if rank == 0 :
        last_row =["Total",0,0,0,0]
        for i in test_info:
            for j in range(4):
                last_row[j+1]+=i[j+1]
            table.add_row(i)
        table.add_row(last_row)
        print("Test performance three topology in:", collective.__name__)
        print(table)
        print("------------------------------------------------------------------------------------------------------------------------------")

test_perfomencetopo(bcast)
test_perfomencetopo(scatter)
test_perfomencetopo(gather)


test_perfomencetopo(Bcast)
test_perfomencetopo(Scatter)
test_perfomencetopo(Gather)