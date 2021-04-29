import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simps

def calcul_vitesse_piston(  deformation_ressort : float,
                            raideur:float,
                            masse : float,
                            N = 100,v0 = 0.0):

    pulsation = np.sqrt(raideur/masse)
    periode = 2*np.pi /pulsation
    #temp_course = 

    # temps d'une demi periode
    t = np.linspace(0,periode/2,N)
    # Position du piston
    x = -deformation_ressort*np.cos(pulsation*t)+(v0/pulsation)*np.sin(pulsation*t)
    # profile de vitesse
    v = deformation_ressort*pulsation*np.sin(pulsation*t)

    #print("x = ",x)
    #print("v = ",v)
    plt.plot(t,x)
    #plt.show()
    plt.plot(t,v)
    #plt.show()
    # index of x == 0
    itp = np.where(abs(x) < 0.01)[0][0]+1
    #print(itp)
    # temps de course du piston
    tp = t[itp]
    print("temps de course = ",tp)
    return itp,t,x,v

def vitesse_moyenne(v):
    return np.sum(v)/(len(v))

def circulation(v ,
                t ,
                tp = 0.0,
                integrale = False):
    
    if integrale:
        dgamma = 0.5*v**2
        gamma = simps(dgamma, t)
    else:
        vm = vitesse_moyenne(v)
        gamma = 0.5*vm**2*tp
    return gamma