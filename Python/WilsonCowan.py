import math
import numpy as np
import matplotlib.pylab as plt


def sigmoid_function(x):
    return 1 / (1 + math.exp(-x))


def calculate_firing_rate(ie0, ie1, w, t, dt, uu, vv, wee, wie, ze, zi):
    i_e = ie0 + ie1 * math.sin(w*t)
    i_i = ii0 + ii1 * math.sin(w*t)
    dE = dt * (-uu + sigmoid_function((wee * uu) - (wie * vv) - ze + i_e))/tau
    dI = dt * (-vv + sigmoid_function((wei * uu) - (wii * vv) - zi + i_i))/tau
    uu_p = uu + dE
    vv_p = vv + dI
    return uu_p, vv_p

# ------------------------------------------------------------------------------------------------------------------
#                                                   No Drive
# ------------------------------------------------------------------------------------------------------------------
# settings
wee = 10
wie = 8
wei = 12
wii = 3
ze = 0.2
zi = 4
tau = 1
ie0 = 0
ie1 = 0
ii0 = 0
ii1 = 0
w = 0.25

step = .005
tstop = 100
dt = np.arange(0, tstop, step)
uu_p = np.zeros((len(dt), 1))
vv_p = np.zeros((len(dt), 1))

# initial conditions
uu0 = 0.1
vv0 = 0.05

for dt_idx in range(len(dt)):
    t = dt_idx * step
    if dt_idx == 0:
        uu_p[dt_idx], vv_p[dt_idx] = calculate_firing_rate(ie0, ie1, w, t, step, uu0, vv0, wee, wie, ze, zi)
    else:
        uu_p[dt_idx], vv_p[dt_idx] = calculate_firing_rate(ie0, ie1, w, t, step, uu_p[dt_idx - 1], vv_p[dt_idx - 1], wee, wie, ze, zi)

plt.figure()
plt.plot(dt, uu_p, label='uu', color='red')
plt.plot(dt, vv_p, label='vv', color='blue')
plt.xlabel('Time')
plt.legend()
plt.show()

plt.figure()
plt.plot(uu_p, vv_p)
plt.xlabel('I')
plt.ylabel('E')
plt.show()
# ------------------------------------------------------------------------------------------------------------------
#                                                   Driven
# ------------------------------------------------------------------------------------------------------------------
# settings
wei = 12
wii = 3
ze = 0.2
zi = 4
tau = 1
ie0 = 0
ie1 = 0.5
ii0 = 0
ii1 = 0.5
w = 0.25

step = .005
tstop = 100
dt = np.arange(0, tstop, step)
uu_p = np.zeros((len(dt), 1))
vv_p = np.zeros((len(dt), 1))

# initial conditions
uu0 = 0.1
vv0 = 0.05

for dt_idx in range(len(dt)):
    t = dt_idx * step
    if dt_idx == 0:
        uu_p[dt_idx], vv_p[dt_idx] = calculate_firing_rate(ie0, ie1, w, t, step, uu0, vv0, wee, wie, ze, zi)
    else:
        uu_p[dt_idx], vv_p[dt_idx] = calculate_firing_rate(ie0, ie1, w, t, step, uu_p[dt_idx - 1], vv_p[dt_idx - 1], wee, wie, ze, zi)

plt.figure()
plt.plot(dt, uu_p, label='uu', color='red')
plt.plot(dt, vv_p, label='vv', color='blue')
plt.xlabel('Time')
plt.legend()
plt.show()

plt.figure()
plt.plot(uu_p, vv_p)
plt.xlabel('I')
plt.ylabel('E')
plt.show()
