import numpy as np
import matplotlib.pyplot as plt

k = 1000
m = 0.22*2+0.4
x0 = -0.3
v0 = 0
tf = 0.2
N = 100
w = np.sqrt(k/m)
T2 = np.pi /w


t = np.linspace(0,T2,N)
x = x0*np.cos(w*t)+(v0/w)*np.sin(w*t)
v = -x0*w*np.sin(w*t)
v2 = v[:N//2]
vm = np.sum(v2)/(N/2)
print("Vitesse moyenne", vm)

plt.figure()
plt.plot(t,x)
plt.show()

plt.figure()
plt.plot(t,v)
#plt.scatter(T2/2,vm)
plt.show()