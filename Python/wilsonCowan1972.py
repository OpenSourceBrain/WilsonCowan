from __future__ import division

import sys
import math
import numpy as np
import matplotlib.pylab as plt
import argparse

def transduction_function(x, theta, a):
    return 1 / (1 + math.exp(-a * (x - theta)))


def inverse_transduction_function(x, theta, a):
    print x, math.log((1-x)/x)
    return - 1/a * (math.log((1-x)/x)) + theta

parser = argparse.ArgumentParser(description='Parameters for the Wilson and Cowan Simulation')
parser.add_argument('-wee', type=int, dest='wee', help='Weight between Excitatory - Excitatory layers')
parser.add_argument('-wei', type=int, dest='wei', help='Weight between Excitatory - Inhibitory layers')
parser.add_argument('-wie', type=int, dest='wie', help='Weight between Excitatory - Inhibitory layers')
parser.add_argument('-wii', type=int, dest='wii', help='Weight between Inhibitory - Inhibitory layers')
parser.add_argument('-ae', type=float, dest='ae', help='Maximum slope value for the excitatory population')
parser.add_argument('-ai', type=float, dest='ai', help='Maximum slope value for the inhibitory population')
parser.add_argument('-theta_e', type=float, dest='theta_e', help='Membrane time constant for excitatory population')
parser.add_argument('-theta_i', type=float, dest='theta_i', help='Membrane time constant for inhibitory population')
args = parser.parse_args()

re = 1
ri = 1
ke = 1
ki = 1
q = 0
p = 0

step = .002
tstop = .5
population = np.arange(step, tstop, step)
I = np.zeros((len(population), 1))
E = np.zeros((len(population), 1))

for e_idx, e in enumerate(population):
    x = e / (ke - (re * e))
    I[e_idx] = ((args.wee * e) - inverse_transduction_function(x, args.theta_e, args.ae) + p) / args.wei

for i_idx, i in enumerate(population):
    x = i / (ki - (ri * i))
    E[i_idx] = ((args.wii * i) + inverse_transduction_function(x, args.theta_i, args.ai) - q) / args.wie

plt.figure()
plt.plot(E, population, label=r'$\frac{dI}{dt}=0$')
plt.xlabel('E')
plt.legend()
plt.figure()
plt.plot(I, population, label=r'$\frac{dE}{dt}=0$')
plt.xlabel('I')
plt.legend()

plt.figure()
plt.plot(population, E, label=r'$\frac{dI}{dt}=0$', linestyle='-.')
plt.plot(I, population, label=r'$\frac{dE}{dt}=0$', linestyle='-.')
plt.legend()
plt.ylabel('E')
plt.xlabel('I')
# plt.xlim(0, .5)
# plt.ylim(0, .5)

if not '-nogui' in sys.argv:
    plt.show()

print 'end'
