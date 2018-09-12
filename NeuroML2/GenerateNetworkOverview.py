import numpy as np
from neuromllite.NetworkGenerator import check_to_generate_or_run
from neuromllite import Simulation

from neuromllite import Network, Population, Projection, Cell, Synapse
from neuromllite import RandomConnectivity, RectangularRegion, RandomLayout

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
                                                    synapse=syns[pre.id],
                                                    type='continuousProjection',
                                                    delay=0,
                                                    weight=weight,
                                                    random_connectivity=RandomConnectivity(probability=1)))
# Build the network
net = Network(id='WC')
net.notes = 'A simple WC network'

r1 = RectangularRegion(id='WilsonCowan', x=0,y=0,z=0,width=1000,height=100,depth=1000)
net.regions.append(r1)

exc_cell = Cell(id='Exc', lems_source_file='WC_Parameters.xml')
inh_cell = Cell(id='Inh', lems_source_file='RateBased.xml') #  hack to include this file too.  

exc_pop = Population(id='Excitatory', 
                     size=1, 
                     component=exc_cell.id, 
                     properties={'color': '.8 0 0'},
                     random_layout = RandomLayout(region=r1.id))

inh_pop = Population(id='Inhibitory', 
                     size=1, 
                     component=inh_cell.id, 
                     properties={'color': '0 0 .8'},
                     random_layout = RandomLayout(region=r1.id))

net.populations.append(exc_pop)
net.populations.append(inh_pop)

exc_syn = Synapse(id='rsExc', lems_source_file='WC_Parameters.xml')
inh_syn = Synapse(id='rsInh', lems_source_file='RateBased.xml')
net.synapses.append(exc_syn)
net.synapses.append(inh_syn)

syns = {exc_pop.id:exc_syn.id, inh_pop.id:inh_syn.id}

W = np.array([[10, -8],
              [12, -3]])

# Add internal connections
pops = [exc_pop, inh_pop]
internal_connections(pops)

# Save to JSON format
net.id = 'WC'
print (net.to_json())
new_file = net.to_json_file('WC.json')

check_to_generate_or_run(sys.argv,
                         Simulation(id='SimExample1',
                                    duration='100',
                                    dt='0.025',
                                    network=new_file,
                                    recordRates={'all':'*'}))
