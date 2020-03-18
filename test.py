from mpi4py import MPI
import numpy
from mpi4py.MPI import Cartcomm

comm = MPI.COMM_WORLD

rank = comm.Get_rank()
status = MPI.Status()


cartesian3d = comm.Create_cart(dims = [3,3],periods =[False,False],reorder=False)
coord3d = cartesian3d.Get_coords(rank)
print ("In 3D topology, Processor ",rank, " has coordinates ",coord3d)

data = rank
w1=MPI.Wtime()
result =comm.scan(data,MPI.SUM)
w2= MPI.Wtime() - w1
print("Rank :",rank)
print("result",result)
print("Wait time :",w2)
comm.Barrier()
cartesian2d = cartesian3d.Sub(remain_dims=[False,True])
rank2d = cartesian2d.Get_rank()
coord2d = cartesian2d.Get_coords(rank2d)
print ("In 2D topology, Processor ",rank,"  has coordinates ", coord2d)

w1=MPI.Wtime()
result =comm.scan(data,MPI.SUM)
w2= MPI.Wtime() - w1
print("result",result)
print("Wait time :",w2)

w1=MPI.Wtime()
result =comm.scan(data,MPI.SUM)
w2= MPI.Wtime() - w1
print("result",result)
print("Wait time :",w2)
print('----------------------------')


