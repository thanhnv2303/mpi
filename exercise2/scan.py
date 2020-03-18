from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size =comm.Get_size()

#scan from process 0 to the end, data = this process data add previous process data
def scan(rank=rank,comm=comm):
    data =rank
    print("Original data:", data)
    data = comm.scan(data, MPI.SUM)

    print("data receive:", data)
    print()

if(rank==0):
    print("The number of processes:", size)

#create 3D topology
cartesian3d = comm.Create_cart(dims = [2,2,2],periods =[False,False,False],reorder=False)
coord3d = cartesian3d.Get_coords(rank)
print ("In 3D topology, Processor ",rank, " has coordinates ",coord3d)

scan()

#create 2D topology by decrease the dim
cartesian2d = cartesian3d.Sub(remain_dims=[False,True,True])
rank2d = cartesian2d.Get_rank()
coord2d = cartesian2d.Get_coords(rank2d)
print ("In 1D topology, Processor ",rank,"  has coordinates ", coord2d)
scan()

#create 1D topology by decrease the dim
cartesian1d = cartesian2d.Sub(remain_dims=[False,True])
rank1d = cartesian1d.Get_rank()
coord1d = cartesian1d.Get_coords(rank1d)
print ("In 2D topology, Processor ",rank,"  has coordinates ", coord1d)

scan(rank)
print("************************************************************************************************************")

