import random as rd
import numpy as np
from matplotlib import pyplot as plt
from prog_mem_v1 import Vehicule
vehicules = Vehicule.Vehicules
for v in vehicules:
    v.algo1()
for v in vehicules:
    v.algo2()

# for v in vehicules:
#     v.alg3()
print(len(Vehicule.Masters))
states = [v.state for v in Vehicule.Vehicules]
print("ND = " , states.count("ND"))
print("CH = " , states.count("CH"))
print("CM =  ", states.count("CM"))
print("*******************")

for v in Vehicule.Vehicules :
    print ((v.X , v.Y) , v.weight)
Data = np.array([(v.X , v.Y) for v in Vehicule.Vehicules])
M=np.array([(v.X , v.Y) for v in Vehicule.Masters ])
ND=np.array([(v.X , v.Y) for v in Vehicule.Vehicules if v.state == "ND" ])
NDv=np.array([v for v in Vehicule.Vehicules if v.state == "ND" ])

cluster=np.array([(v.X , v.Y) for v in Vehicule.Masters[0].cluster])
# k = np.array([(v.weight) for v in NDv ])
# print (k)
plt.scatter(Data[: , 0] , Data[: , 1])
plt.scatter(M[: , 0] , M[: , 1] , color = "red")
plt.scatter(ND[: , 0] , ND[: , 1] , color = "orange"  , label="ND")
# plt.scatter(Vehicule.Vehicules[ind].X , Vehicule.Vehicules[ind].Y, color="black")
# if (len(cluster) > 0 ):
#     plt.scatter(cluster[: , 0] , cluster[: , 1] , color = "yellow")
plt.show()
