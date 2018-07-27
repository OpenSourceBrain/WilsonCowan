import math
import sys
import numpy as np
import matplotlib.pylab as plt
import argparse

def sigmoid_function(x):
    return 1 / (1 + math.exp(-x))


def calculate_firing_rate(ie0, ie1, ii0, ii1, w, t, dt, uu, vv, wee, wei, wie, wii, ze, zi):
    i_e = ie0 + ie1 * math.sin(w*t)
    i_i = ii0 + ii1 * math.sin(w*t)
    dE = dt * (-uu + sigmoid_function((wee * uu) - (wie * vv) - ze + i_e))/tau
    dI = dt * (-vv + sigmoid_function((wei * uu) - (wii * vv) - zi + i_i))/tau
    uu_p = uu + dE
    vv_p = vv + dI
    return uu_p, vv_p

def inverse_sigmoid(x):
    return -math.log(abs(1/x - 1))

def calculate_isoclines(ie0, ie1, ii0, ii1, w,  e, i, wee, wie, wei, wii, ze, zi):
    i_e = ie0 + ie1 * math.sin(w*t)
    i_i = ii0 + ii1 * math.sin(w*t)
    E = sigmoid_function((wee * e) - (wie * i) - ze + i_e)
    I = sigmoid_function((wei * e) - (wii * i) - zi + i_i)
    return E, I

parser = argparse.ArgumentParser(description='Parameters for the Wilson and Cowan Simulation')
parser.add_argument('-wee', type=float, dest='wee', help='Weight between Excitatory - Excitatory layers')
parser.add_argument('-wei', type=float, dest='wei', help='Weight between Excitatory - Inhibitory layers')
parser.add_argument('-wie', type=float, dest='wie', help='Weight between Excitatory - Inhibitory layers')
parser.add_argument('-wii', type=float, dest='wii', help='Weight between Inhibitory - Inhibitory layers')
parser.add_argument('-ze', type=float, dest='ze', help='')
parser.add_argument('-zi', type=float, dest='zi', help='')
parser.add_argument('-ie1', type=float, dest='ie1', help='Current')
parser.add_argument('-ii1', type=float, dest='ii1', help='Current')
parser.add_argument('-w', type=float, dest='w', help='Phase')
args = parser.parse_args()

# settings
tau = 1.
ie0 = 0
ii0 = 0

step = .005
tstop = 100
dt = np.arange(0, tstop, step)
uu_p = np.zeros((len(dt), 1))
vv_p = np.zeros((len(dt), 1))

I = np.zeros((len(dt), 1))
E = np.zeros((len(dt), 1))

# initial conditions
uu0 = 0.1
vv0 = 0.05

if args.ie1 or args.ii1 != 0:
    savefile = 'NoDrive.dat'
else:
    savefile = 'Drive.dat'

data_file = open(savefile, 'w')

for dt_idx in range(len(dt)):
    t = dt_idx * step
    if dt_idx == 0:
        uu_p[dt_idx], vv_p[dt_idx] = calculate_firing_rate(ie0, args.ie1, ii0, args.ii1, args.w, t, step, uu0,
                                                           vv0, args.wee, args.wei, args.wie, args.wii, args.ze, args.zi)
    else:
        uu_p[dt_idx], vv_p[dt_idx] = calculate_firing_rate(ie0, args.ie1, ii0, args.ii1, args.w, t, step, uu_p[dt_idx - 1],
                                                           vv_p[dt_idx - 1], args.wee, args.wei, args.wie, args.wii,
                                                           args.ze, args.zi)
    data_file.write('%s\t%s\t%s\n'%(t/1000., uu_p[dt_idx][0], vv_p[dt_idx][0]))
    E[dt_idx], I[dt_idx] = calculate_isoclines(ie0, args.ie1, ii0, args.ii1, args.w, uu_p[dt_idx][0], vv_p[dt_idx][0],
                                               args.wee, args.wie, args.wei, args.wii, args.ze, args.zi)
data_file.close()


plt.figure()
plt.plot(dt, uu_p, label='uu', color='red')
plt.plot(dt, vv_p, label='vv', color='blue')
plt.xlabel('Time')
plt.legend()

plt.figure()
plt.plot(uu_p, vv_p)
plt.plot(vv_p, E, label=r'$\frac{dE}{dt}=0$', linestyle='-.')
plt.plot(I, uu_p, label=r'$\frac{dI}{dt}=0$', linestyle='-.')
plt.legend()
plt.xlabel('I')
plt.ylabel('E')
if not '-nogui' in sys.argv:
    plt.show()