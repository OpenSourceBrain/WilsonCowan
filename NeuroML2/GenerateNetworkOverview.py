from neuromllite.NetworkGenerator import check_to_generate_or_run
from neuromllite import Simulation
from neuromllite import Network, Population, Projection, Cell, Synapse, RectangularRegion, RandomLayout

import sys

# This function generates the overview of the network using neuromllite

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

# Add projections
net.projections.append(Projection(id='projEE',
                                 presynaptic=exc_pop.id,
                                 postsynaptic=exc_pop.id,
                                 synapse=exc_syn.id))
                                 
net.projections.append(Projection(id='projEI',
                                 presynaptic=exc_pop.id,
                                 postsynaptic=inh_pop.id,
                                 synapse=exc_syn.id))
                                 
net.projections.append(Projection(id='projIE',
                                 presynaptic=inh_pop.id,
                                 postsynaptic=exc_pop.id,
                                 synapse=inh_syn.id,
                                 weight=-1))
                                 
net.projections.append(Projection(id='projII',
                                 presynaptic=inh_pop.id,
                                 postsynaptic=inh_pop.id,
                                 synapse=inh_syn.id,
                                 weight=-1))

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
