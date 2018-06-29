import math
import numpy as np
import matplotlib.pylab as plt

def sigmoid(x, theta, a):
    return 1 / (1 + math.exp(-a * (x - theta)))


wee = 12
wei = 4
wie = 13
wii = 11
ae = 1.2
ai = 1
theta_e = 2.8
theta_i = 4
re = 1
ri = 1
ke = .98
ki = .97
q = 0
p = 0

step = .02
tstop = .5
population = np.arange(0, tstop, step)
I = np.zeros((len(population), 1))
E = np.zeros((len(population), 1))

for e_idx, e in enumerate(population):
    x = e / (ke - (re * e))
    I[e_idx] = ((wee * e) - 1/(sigmoid(x, theta_e, ae)) + p) / wei

for i_idx, i in enumerate(population):
    x = i / (ki - (ri * i))
    E[i_idx] = ((wii * i) + 1/(sigmoid(x, theta_i, ai)) - q) / wie

plt.figure()
plt.plot(E, population, label='dE/dt')
plt.legend()
plt.show()
plt.figure()
plt.plot(I, population, label='dI/dt')
plt.legend()
plt.show()

plt.figure()
plt.plot(population, E, label='dE/dt')
plt.plot(I, population, label='dI/dt')
plt.legend()
plt.show()
