from neuromllite.NetworkGenerator import check_to_generate_or_run
from neuromllite import Simulation

from neuromllite import Network, Population, Projection, Cell, Synapse, InputSource, Input
from neuromllite import RandomConnectivity, RectangularRegion, RelativeLayout

import sys

# This function generates the overview of the network using neuromllite
def internal_connections(pops):
    for pre in pops:
        for post in pops:

            weight = W[pops.index(post)][pops.index(pre)]
            print('Connection %s -> %s weight: %s'%(pre.id,
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

net.parameters = { 'wee':      10,
                   'wei':      12,
                   'wie':      -8,
                   'wii':      -3}  

r1 = RectangularRegion(id='WilsonCowan', x=0,y=0,z=0,width=1000,height=100,depth=1000)
net.regions.append(r1)

exc_cell = Cell(id='Exc', lems_source_file='WC_Parameters.xml')
inh_cell = Cell(id='Inh', lems_source_file='RateBased.xml') #  hack to include this file too.  
net.cells.append(exc_cell)
net.cells.append(inh_cell)

exc_pop = Population(id='Excitatory', 
                     size=1, 
                     component=exc_cell.id, 
                     properties={'color': '0.8 0 0','radius':10},
                     relative_layout = RelativeLayout(region=r1.id,x=-20,y=0,z=0))

inh_pop = Population(id='Inhibitory', 
                     size=1, 
                     component=inh_cell.id, 
                     properties={'color': '0 0 0.8','radius':10},
                     relative_layout = RelativeLayout(region=r1.id,x=20,y=0,z=0))

net.populations.append(exc_pop)
net.populations.append(inh_pop)

exc_syn = Synapse(id='rsExc', lems_source_file='WC_Parameters.xml')
inh_syn = Synapse(id='rsInh', lems_source_file='RateBased.xml')
net.synapses.append(exc_syn)
net.synapses.append(inh_syn)

syns = {exc_pop.id:exc_syn.id, inh_pop.id:inh_syn.id}

W = [['wee', 'wie'],
     ['wei','wii']]

# Add internal connections
pops = [exc_pop, inh_pop]
internal_connections(pops)

# Add offset inputs

net.parameters['exc_input'] = '0nA'
net.parameters['inh_input'] = '0nA'
net.parameters['input_delay'] = '20ms'
net.parameters['input_duration'] = '60ms'

#net.parameters['scaling'] = '1nA'

input_source_e = InputSource(id='Exc_in',
                             neuroml2_input='PulseGenerator',
                             parameters={'amplitude':'exc_input', 'delay':'input_delay', 'duration':'input_duration'})
net.input_sources.append(input_source_e)
net.inputs.append(Input(id='Exc_stim',
                        input_source=input_source_e.id,
                        population=exc_pop.id,
                        percentage=100))
                        
input_source_i = InputSource(id='Inh_in',
                             neuroml2_input='PulseGenerator',
                             parameters={'amplitude':'inh_input', 'delay':'input_delay', 'duration':'input_duration'})
net.input_sources.append(input_source_i)
net.inputs.append(Input(id='Inh_stim',
                        input_source=input_source_i.id,
                        population=inh_pop.id,
                        percentage=100))

# Save to JSON format
net.id = 'WC'
new_file = net.to_json_file('WC.json')

sim = Simulation(id='SimWC',
                                    duration='100',
                                    dt='0.005',
                                    network=new_file,
                                    recordRates={'all':'*'},
                                    plots2D={'E-I':{'x_axis':'Excitatory/0/Exc/r',
                                                    'y_axis':'Inhibitory/0/Inh/r'}})
                            
sim.to_json_file('SimWC.nmllite.json')

check_to_generate_or_run(sys.argv,sim)
