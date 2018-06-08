import math
import numpy as np
import matplotlib.pylab as plt


def sigmoid_function(x):
    return 1 / (1 + math.exp(-x))


def calculate_firing_rate(ie0, ie1, w, t, dt, uu, wee, wie, ze):
    i_e = ie0 + ie1 * math.sin(w*t)
    iSyn = wee * uu
    f = sigmoid_function(iSyn)
    dE = dt * (-uu + f)/tau
    # dE = dt * (-uu + sigmoid_function((wee * uu) - (wie * vv) - ze + i_e))/tau
    uu_p = uu + dE
    return uu_p, iSyn, f

# ------------------------------------------------------------------------------------------------------------------
#                                                   No Drive
# ------------------------------------------------------------------------------------------------------------------
# settings
wee = 10
wie = 8
wei = 12
wii = 3
ze = 0.2
tau = 1
ie0 = 0
ie1 = 0
w = 0.25

step = .005
tstop = 100
dt = np.arange(0, tstop, step)
uu_p = np.zeros((len(dt), 1))
f = np.zeros((len(dt), 1))
iSyn = np.zeros((len(dt), 1))

# initial conditions
uu0 = 0.1

for dt_idx in range(len(dt)):
    t = dt_idx * step
    if dt_idx == 0:
        uu_p[dt_idx], iSyn[dt_idx], f[dt_idx] = calculate_firing_rate(ie0, ie1, w, t, step, uu0, wee, wie, ze)
    else:
        uu_p[dt_idx], iSyn[dt_idx], f[dt_idx] = calculate_firing_rate(ie0, ie1, w, t, step, uu_p[dt_idx - 1], wee, wie, ze)

plt.figure()
plt.plot(dt, uu_p, label='uu', color='red')
plt.xlabel('Time')
plt.legend()
plt.show()

plt.figure()
plt.plot(dt, iSyn, label='Isyn')
plt.plot(dt, f, label='f')
plt.xlabel('Time')
plt.legend()
plt.show()
