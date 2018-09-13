import numpy as np
from neuromllite.NetworkGenerator import check_to_generate_or_run
from neuromllite import Simulation

from neuromllite import Network, Population, Projection, Cell, Synapse
from neuromllite import RandomConnectivity, RectangularRegion, RandomLayout

import sys
from neuromllite.sweep.ParameterSweep import *

# This function generates the overview of the network using neuromllite
def internal_connections(net, pops, W, syns):
    for pre in pops:
        for post in pops:

            weight = W[pops.index(post)][pops.index(pre)]
            print('Connection %s -> %s weight %s'%(pre.id, post.id, weight))

            net.projections.append(Projection(id='proj_%s_%s'%(pre.id,post.id),
                                                presynaptic=pre.id,
                                                postsynaptic=post.id,
                                                synapse=syns[pre.id],
                                                type='continuousProjection',
                                                delay=0,
                                                weight=weight,
                                                random_connectivity=RandomConnectivity(probability=1)))
                                                    
def generate(wee=10.,wei=12.,wie=8.,wii=3.):

    # Build the network
    net = Network(id='WC')
    net.notes = 'A simple WC network'
    
    net.parameters = { 'wee': wee,
                       'wei': wei,
                       'wie': wie,
                       'wii': wii }

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

    W = [['wee', '-1*wie'],
         ['wei', '-1*wii']]

    # Add internal connections
    pops = [exc_pop, inh_pop]
    internal_connections(net, pops, W, syns)

    # Save to JSON format
    net.id = 'WC'
    print (net.to_json())
    new_file = net.to_json_file('WC.json')

    sim = Simulation(id='SimExample1',
                    duration='100',
                    dt='0.025',
                    network=new_file,
                    recordRates={'all':'*'})
    sim_file = sim.to_json_file('%s.json'%sim.id)
                                        
    return sim, net
                                        
                                        
if __name__ == "__main__":
    
    
    if '-sweep' in sys.argv:
        
        sim, net = generate(wei=0,wie=0,wee=0,wii=0)
        sim, net = generate()
        
        weight_range1 = [0,2.5,5,7.5,10]
        #weight_range1 = [(i)/3. for i in range(50)]
        
        fixed = {}
 
        vary = {'wee':weight_range1}
        #vary = {'wii':weight_range1}
    

        simulator = 'PyNN_NEST'
        simulator = 'jNeuroML'
        simulator = 'jNeuroML_NetPyNE'
        simulator = 'jNeuroML_NEURON'
        simulator = 'jNeuroML'

        nmllr = NeuroMLliteRunner('%s.json'%sim.id,
                                  simulator=simulator)

        ps = ParameterSweep(nmllr, 
                            vary, 
                            fixed,
                            num_parallel_runs=1,
                            plot_all=True, 
                            heatmap_all=True,
                            show_plot_already=False,
                            peak_threshold=.9,
                            verbose=True)

        report = ps.run()
        ps.print_report()

        ps.plotLines(vary.keys()[0],'average_last_1percent',save_figure_to='average_last_1percent.png')
        
        import matplotlib.pyplot as plt

        plt.show()
    
    elif '-disconnected' in sys.argv:
        
        sim, net = generate(wei=0,wie=0,wee=0,wii=0)
        check_to_generate_or_run(sys.argv, sim)
    
    else:
        
        sim, net = generate()
        check_to_generate_or_run(sys.argv, sim)
        
