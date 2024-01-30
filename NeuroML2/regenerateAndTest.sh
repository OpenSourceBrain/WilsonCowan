#!/bin/bash
set -ex

rm LEMS*ml *nml

python GenerateWilsonCowanLEMS.py -ie0 0   -ii0 0    # dimensionless
python GenerateWilsonCowanLEMS.py -ie0 0.5 -ii0 0.5  # dimensionless

python GenerateWilsonCowanLEMS.py -ie0 0   -ii0 0    -dims
python GenerateWilsonCowanLEMS.py -ie0 0.5 -ii0 0.5  -dims

pynml LEMS_WC_drivenDL.xml -nogui
pynml LEMS_WC_slowDL.xml -nogui

pynml LEMS_WC_driven.xml -nogui
pynml LEMS_WC_slow.xml -nogui

pynml LEMS_WC_driven.xml -neuron -run -nogui
pynml LEMS_WC_slow.xml -neuron -run -nogui

python GenerateNetworkOverview.py -jnml
pynml LEMS_SimWC.xml -neuron -run -nogui

cd test_files

python Spiking.py -jnml

cd -

omv all -V
