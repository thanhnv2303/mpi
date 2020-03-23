from mpi4py import MPI
from exercise2.broadcast import broadcast
from exercise2.allgather import allgather
from exercise2.alltoall import alltoall
from exercise2.allreduce import allreduce
from exercise2.gather import gather
from exercise2.reduce import reduce
from exercise2.reducescatter import reducescatter
from exercise2.scan import scan
from exercise2.scatter import scatter
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if(rank==0):
    print("The number of processes:", comm.Get_size())

#create 3D topology
cartesian1d = comm.Create_cart(dims = [8],periods =[True],reorder=False)
coord1d = cartesian1d.Get_coords(rank)
print ("In 1D topology, Processor ",rank, " has coordinates ",coord1d)

broadcast()
scatter()
gather()
allgather()
alltoall()
reduce()
allreduce()
scan()
reducescatter()

