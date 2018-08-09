from neuromllite.NetworkGenerator import check_to_generate_or_run
from neuromllite import Simulation
from neuromllite import Network, Population, Projection

import sys

# This function generates the overview of the network using neuromllite

# Build the network
net = Network(id='WC')
net.notes = 'A simple WC network'

print(net)

p0 = Population(id='Excitatory', size=1, component='iaf', properties={'color': '.8 0 0'})
p1 = Population(id='Inhibitory', size=1, component='iaf', properties={'color': '0 0 .8'})

print(p1.to_json())
net.populations.append(p0)
net.populations.append(p1)

# Add projections
net.projections.append(Projection(id='proj0',
                                 presynaptic=p0.id,
                                 postsynaptic=p1.id))
net.projections.append(Projection(id='proj1',
                                 presynaptic=p1.id,
                                 postsynaptic=p0.id))

# Save to JSON format
net.id = 'WC'
print (net.to_json())
new_file = net.to_json_file('WC.json')

check_to_generate_or_run(sys.argv,
                         Simulation(id='SimExample1',network=new_file))
