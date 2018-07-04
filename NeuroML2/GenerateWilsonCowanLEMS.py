import os
import random
import argparse
import numpy as np

from neuroml import (NeuroMLDocument, Network, Population, ContinuousConnectionInstanceW, ContinuousProjection,
                     ExplicitInput, SineGeneratorDL, SineGenerator, Property, Location, Instance, IncludeType)
import neuroml.writers as writers
from pyneuroml.lems.LEMSSimulation import LEMSSimulation
random.seed(42)


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
                                                       post_component='rs%s' %to_pop,
                                                       weight=w_to_from_pop
                                                       )
            projection.continuous_connection_instance_ws.append(connection)
            connection_count += 1


def generatePopulationSimulationLEMS(n_pops, baseline, pops, duration, dl):
    # Create simulation
    # Create LEMS file
    dl_str = 'DL' if dl else ''
    sim_id = 'LEMS_WC_%s%s.xml' %(baseline,dl_str)
    dt = 0.005
    ls = LEMSSimulation(sim_id, duration, dt, 'net')
    colours = ['#ff0000', '#0000ff']
    colours2 = ['#ff7777', '#7777ff']

    # Add additional LEMS files
    # Add Wilson and Cowan Components
    ls.include_lems_file('RateBased.xml', include_included=True)
    ls.include_lems_file('WC_Parameters%s.xml'%dl_str, include_included=True)
    # Add the network definition
    ls.include_lems_file('WC_%s%s.net.nml' %(baseline,dl_str), include_included=True)

    disp2 = 'd2'
    ls.create_display(disp2, 'Rates', -.1, 1.2)
    for pop_idx, pop in enumerate(pops):
        for n_pop in range(n_pops[pop_idx]):
            ls.add_line_to_display(disp2,  'r_%s' %pop, '%sPop/%d/%s/%s' % (pop, n_pop, pop, 'R' if dl else 'r'),   color=colours[pop_idx])

    disp1 = 'd1'
    ls.create_display(disp1, 'iSyn', -2, 8)
    for pop_idx, pop in enumerate(pops):
        for n_pop in range(n_pops[pop_idx]):
            ls.add_line_to_display(disp1, 'iSyn_%s' %pop, '%sPop/%d/%s/iSyn' % (pop, n_pop, pop),   color=colours[pop_idx], scale=1 if dl else '1nA')
            ls.add_line_to_display(disp1, 'f_%s' %pop, '%sPop/%d/%s/f' % (pop, n_pop, pop),   color=colours2[pop_idx])

    of1 = 'of_%s' %pop
    ls.create_output_file(of1, 'WC_%s%s.dat' %(baseline,dl_str))
    for pop_idx, pop in enumerate(pops):
        # save rates in output file
        for n_pop in range(n_pops[pop_idx]):
            ls.add_column_to_output_file(of1, 'r_%s' %pop, '%sPop/%d/%s/%s' %(pop, n_pop, pop, 'R' if dl else 'r'))

    save_path = os.path.join(sim_id)
    ls.save_to_file(file_name=save_path)

parser = argparse.ArgumentParser(description='Parameters for the Wilson and Cowan.')
parser.add_argument('-ie0', help='excitatory population input current', type=float)
parser.add_argument('-ii0', help='inhibitory population input current', type=float)
parser.add_argument('-dims', help='generate dimensional model', action='store_true', default=False)

args = parser.parse_args()

dl = not args.dims
print('Generating as dimensionless: %s'%dl)
dl_str = 'DL' if dl else ''

pops = ['Exc', 'Inh'] # E would give errors in NEURON; EDL is not a nice variable name...
n_pops = [1, 1]
w_to_from_pops = np.array([[10, -8],
                           [12, -3]])
                           
silentSynapsisDL = 'silent1DL'

if args.ie0 or args.ii0 > 0:
    baseline = 'driven'
else:
    baseline = 'slow'

nml_doc = NeuroMLDocument(id='WC_%s%s' % (baseline, dl_str))
duration = 100 # ms

for pop_idx, pop in enumerate(pops):
    if dl:
        pulse = SineGeneratorDL(id='mod_%s' %pop, phase='0', delay='0ms', duration='%sms'%duration, amplitude=args.ie0, period='25ms')
        nml_doc.sine_generator_dls.append(pulse)
    else:
        pulse = SineGenerator(id='mod_%s' %pop, phase='0', delay='0ms', duration='%sms'%duration, amplitude='%snA'%args.ie0, period='25ms')
        nml_doc.sine_generators.append(pulse)

# Create the network
net = Network(id='net')
nml_doc.networks.append(net)
nml_doc.includes.append(IncludeType('RateBased.xml'))

nml_doc.includes.append(IncludeType('WC_Parameters%s.xml'%dl_str))

colours = ['0 0 1', '1 0 0']
for pop_idx, pop in enumerate(pops):
    population = Population(id='%sPop' %pop, component=(pops[pop_idx]), size=n_pops[pop_idx], type='populationList')
    net.populations.append(population)
    population.properties.append(Property(tag='color', value=colours[pop_idx]))
    population.properties.append(Property(tag='radius', value='10'))

    for n_pop in range(n_pops[pop_idx]):
        inst = Instance(id=n_pop)
        population.instances.append(inst)
        inst.location = Location(x=-20 if 'E' in pop else 20,
                                 y=0,
                                 z=0)


for from_idx, from_pop in enumerate(pops):
    for to_idx, to_pop in enumerate(pops):
        generatePopulationProjection(pops[from_idx], pops[to_idx], n_pops[from_idx], n_pops[to_idx],
                                     w_to_from_pops[to_idx, from_idx], net)

# Add inputs
for pop_idx, pop in enumerate(pops):
    for n_idx in range(n_pops[pop_idx]):
        exp_input = ExplicitInput(target='%sPop/%i/%s' %(pop, n_idx, pop), input='mod_%s' %pops[pop_idx], destination='synapses')
        net.explicit_inputs.append(exp_input)

nml_file = 'WC_%s%s.net.nml' %(baseline,dl_str)
writers.NeuroMLWriter.write(nml_doc, nml_file)

print('Written NeuroML file: %s'%nml_file)

generatePopulationSimulationLEMS(n_pops, baseline, pops, duration, dl)