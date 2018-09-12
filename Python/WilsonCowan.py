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

#-wee 10. -wei 12. -wie 8. -wii 3. -ze 0.2 -zi 4. -ie1 0 -ii1 0 -w 0.25

parser = argparse.ArgumentParser(description='Parameters for the Wilson and Cowan Simulation')

parser.add_argument('-wee', type=float, dest='wee', default=10., help='Weight between Excitatory - Excitatory layers')
parser.add_argument('-wei', type=float, dest='wei', default=12., help='Weight between Excitatory - Inhibitory layers')
parser.add_argument('-wie', type=float, dest='wie', default=8., help='Weight between Excitatory - Inhibitory layers')
parser.add_argument('-wii', type=float, dest='wii', default=3., help='Weight between Inhibitory - Inhibitory layers')
parser.add_argument('-ze', type=float, dest='ze', default=0.2, help='')
parser.add_argument('-zi', type=float, dest='zi', default=4., help='')
parser.add_argument('-ie1', type=float, dest='ie1', default=0, help='Current')
parser.add_argument('-ii1', type=float, dest='ii1', default=0, help='Current')
parser.add_argument('-w', type=float, dest='w', default=0.25, help='Phase')

parser.add_argument('-tstop', type=float, dest='tstop', default=100, help='Duration')

parser.add_argument('-nogui', action='store_true', default=False, help='No GUI')

args = parser.parse_args()

# settings
tau = 1.
ie0 = 0
ii0 = 0

dt = .005

times = np.arange(0, args.tstop, dt)
uu_p = np.zeros((len(times), 1))
vv_p = np.zeros((len(times), 1))

# initial conditions
uu0 = 0.1
vv0 = 0.05

if args.ie1 !=0 or args.ii1 != 0:
    savefile = 'Drive.dat'
else:
    savefile = 'NoDrive.dat'

data_file = open(savefile, 'w')

for t_idx in range(len(times)):
    t = t_idx * dt
    if t_idx == 0:
        uu_p[t_idx], vv_p[t_idx] = calculate_firing_rate(ie0, args.ie1, ii0, args.ii1, args.w, t, dt, uu0,
                                                           vv0, args.wee, args.wei, args.wie, args.wii, args.ze, args.zi)
    else:
        uu_p[t_idx], vv_p[t_idx] = calculate_firing_rate(ie0, args.ie1, ii0, args.ii1, args.w, t, dt, uu_p[t_idx - 1],
                                                           vv_p[t_idx - 1], args.wee, args.wei, args.wie, args.wii,
                                                           args.ze, args.zi)
    data_file.write('%s\t%s\t%s\n'%(t/1000., uu_p[t_idx][0], vv_p[t_idx][0]))

data_file.close()


print("Finished running simulation of %sms, saved data to %s"%(args.tstop,savefile))

if not args.nogui:
    plt.figure()
    plt.plot(times, uu_p, label='E', color='red')
    plt.plot(times, vv_p, label='I', color='blue')
    plt.xlabel('Time')
    plt.ylabel('Firing Rate')
    plt.legend()

    pop_step = .02
    pop_stop = 1
    population = np.arange(pop_step, pop_stop, pop_step)
    I = np.zeros((len(population), 1))
    E = np.zeros((len(population), 1))
    for e_idx, e in enumerate(population):
        I[e_idx] = 1 / args.wie * (math.log(1/e - 1) - args.ze + args.wee * e)

    for i_idx, i in enumerate(population):
        E[i_idx] = - 1 / args.wei * (math.log(1/i - 1) - args.zi - args.wii * i)

    plt.figure()
    plt.plot(vv_p, uu_p, label='EI trajectory', color='b',linewidth=0.8)
    plt.plot(population, E, label=r'$\frac{dI}{dt}=0$', linestyle='-.', color='r',linewidth=0.8)
    plt.plot(I, population, label=r'$\frac{dE}{dt}=0$', linestyle='-.',color='g',linewidth=0.8)
    plt.legend(loc='upper left')
    plt.xlabel('I')
    plt.ylabel('E')
    
    num_points = 20
    points = [i/float(num_points) for i in range(num_points+1)]
    
    for e in points:
        for i in points:
            t = 0
            dt = 0.03
            ee, ii = calculate_firing_rate(ie0, args.ie1, ii0, args.ii1, args.w, t, dt, e,
                                                           i, args.wee, args.wei, args.wie, args.wii,
                                                           args.ze, args.zi)
            #print("Point (%s,%s) -> (%s,%s)"%(e,i,ee,ii))
            plt.plot([i,ii], [e,ee], color='#111111',linewidth=0.4)
            plt.plot([i], [e], color='#333333',marker='.',markersize=30*(abs(e-ee)+abs(i-ii)))

    plt.show()
    


