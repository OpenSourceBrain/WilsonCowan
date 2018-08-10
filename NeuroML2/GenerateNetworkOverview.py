import numpy as np
from neuromllite.NetworkGenerator import check_to_generate_or_run
from neuromllite import Simulation
from neuromllite import Network, Population, Projection, RandomConnectivity

import sys

# This function generates the overview of the network using neuromllite
def internal_connections(pops):
    for pre in pops:
        for post in pops:

            weight = W[pops.index(post)][pops.index(pre)]
            print('Connection %s -> %s weight %s'%(pre.id,
            post.id, weight))
            if weight!=0:

                net.projections.append(Projection(id='proj_%s_%s'%(pre.id,post.id),
                                                    presynaptic=pre.id,
                                                    postsynaptic=post.id,
                                                    synapse='rs',
                                                    type='continuousProjection',
                                                    delay=0,
                                                    weight=weight,
                                                    random_connectivity=RandomConnectivity(probability=1)))
# Build the network
net = Network(id='WC')
net.notes = 'A simple WC network'

print(net)

p0 = Population(id='Excitatory', size=1, component='iaf', properties={'color': '.8 0 0'})
p1 = Population(id='Inhibitory', size=1, component='iaf', properties={'color': '0 0 .8'})

print(p1.to_json())
net.populations.append(p0)
net.populations.append(p1)

W = np.array([[10, -8],
              [12, -3]])

# Add internal connections
pops = [p0, p1]
internal_connections(pops)

# Save to JSON format
net.id = 'WC'
print (net.to_json())
new_file = net.to_json_file('WC.json')

check_to_generate_or_run(sys.argv,
                         Simulation(id='SimExample1',network=new_file))
