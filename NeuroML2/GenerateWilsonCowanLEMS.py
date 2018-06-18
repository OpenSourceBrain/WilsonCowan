import os
import random
import numpy as np

from neuroml import (NeuroMLDocument, Network, Population, ContinuousConnectionInstanceW, ContinuousProjection,
                     ExplicitInput, SineGeneratorDL, Property, Location, Instance)
import neuroml.writers as writers
from pyneuroml.lems.LEMSSimulation import LEMSSimulation


def generatePopulationProjection(from_pop, to_pop, n_from_pop, n_to_pop, w_to_from_pop, net):
    connection_count = 0
    projection = ContinuousProjection(id='%s_%s' % (from_pop, to_pop),
                                      presynaptic_population='%sPop' % from_pop,
                                      postsynaptic_population='%sPop' % to_pop)
    net.continuous_projections.append(projection)
    for idx_from_pop in range(n_from_pop):
        for idx_to_pop in range(n_to_pop):
            connection = ContinuousConnectionInstanceW(id=connection_count,
                                                       pre_cell='../%sPop/%i/%s' %  (from_pop, idx_from_pop, from_pop),
                                                       post_cell='../%sPop/%i/%s' % (to_pop, idx_to_pop, to_pop),
                                                       pre_component=silentSynapsisDL,
                                                       post_component='rsWC',
                                                       weight=w_to_from_pop
                                                       )
            projection.continuous_connection_instance_ws.append(connection)
            connection_count += 1


def generatePopulationSimulationLEMS(n_pops, baseline, pops):
    # Create simulation
    # Create LEMS file
    sim_id = 'LEMS_WCSlowSim.xml'
    sim_t = 100
    dt = 0.005
    ls = LEMSSimulation(sim_id, sim_t, dt, 'net')
    colours = ['#0000ff', '#ff0000']

    # Add additional LEMS files
    # Add Wilson and Cowan Components
    ls.include_lems_file('WilsonCowan.xml', include_included=True)
    ls.include_lems_file('LEMS_WC_Parameters_Slow.xml', include_included=True)
    # Add the network definition
    ls.include_lems_file('WC_Slow.nml', include_included=True)

    disp2 = 'd2'
    ls.create_display(disp2, 'Rates', -5, 105)
    for pop_idx, pop in enumerate(pops):
        for n_pop in range(n_pops[pop_idx]):
            ls.add_line_to_display(disp2, 'r_%s' %pop, '%sPop/%d/%s/R' % (pop, n_pop, pop),   color=colours[pop_idx])

    save_path = os.path.join(sim_id)
    ls.save_to_file(file_name=save_path)

pops = ['EDL', 'IDL']
n_pops = [1, 1]
w_to_from_pops = np.array([[10, 12],
                           [-8, -3]])
silentSynapsisDL = 'silent1DL'

nml_doc = NeuroMLDocument(id='WC_slow')

for pop_idx, pop in enumerate(pops):
    pulse = SineGeneratorDL(id='mod_%s' %pop, phase='0', delay='0ms', duration='100ms', amplitude='0', period='5ms')
    nml_doc.sine_generator_dls.append(pulse)

# Create the network
net = Network(id='net')
nml_doc.networks.append(net)

colours = ['0 0 1', '1 0 0']
for pop_idx, pop in enumerate(pops):
    population = Population(id='%sPop' %pop, component=(pops[pop_idx]).upper(), size=n_pops[pop_idx], type='populationList')
    net.populations.append(population)
    population.properties.append(Property(tag='color', value=colours[pop_idx]))

    for n_pop in range(n_pops[pop_idx]):
        inst = Instance(id=n_pop)
        population.instances.append(inst)
        inst.location = Location(x=str(random.random() * 100),
                                 y=str(random.random() * 100),
                                 z=str(random.random() * 100 ))


for from_idx, from_pop in enumerate(pops):
    for to_idx, to_pop in enumerate(pops):
        generatePopulationProjection(pops[from_idx], pops[to_idx], n_pops[from_idx], n_pops[to_idx],
                                     w_to_from_pops[to_idx, from_idx], net)

# Add inputs
for pop_idx, pop in enumerate(pops):
    for n_idx in range(n_pops[pop_idx]):
        exp_input = ExplicitInput(target='%sPop/%i/%s' %(pop, n_idx, pop), input='mod_%s' %pops[pop_idx], destination='synapses')
        net.explicit_inputs.append(exp_input)

nml_file = 'WC_Slow.nml'
writers.NeuroMLWriter.write(nml_doc, nml_file)

baseline = 'slow'
generatePopulationSimulationLEMS(n_pops, baseline, pops)