from mpi4py import MPI
import functools

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size =comm.Get_size()

#alltoall data from all process and reduce them in each process
def reducescatter(comm=comm,size=size):
    data =[i for i in range(size)]

    print("Original data:", data)
    data = comm.alltoall(data)
    result = functools.reduce(lambda a,b :a+b ,data)

    print("data receive:", result)
    print()

if(rank==0):
    print("The number of processes:", size)

#create 3D topology
cartesian3d = comm.Create_cart(dims = [2,2,2],periods =[False,False,False],reorder=False)
coord3d = cartesian3d.Get_coords(rank)
print ("In 3D topology, Processor ",rank, " has coordinates ",coord3d)

reducescatter()

#create 2D topology by decrease the dim
cartesian2d = cartesian3d.Sub(remain_dims=[False,True,True])
rank2d = cartesian2d.Get_rank()
coord2d = cartesian2d.Get_coords(rank2d)
print ("In 1D topology, Processor ",rank,"  has coordinates ", coord2d)
reducescatter()

#create 1D topology by decrease the dim
cartesian1d = cartesian2d.Sub(remain_dims=[False,True])
rank1d = cartesian1d.Get_rank()
coord1d = cartesian1d.Get_coords(rank1d)
print ("In 2D topology, Processor ",rank,"  has coordinates ", coord1d)
reducescatter()

print("************************************************************************************************************")

