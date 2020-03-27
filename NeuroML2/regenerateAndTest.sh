#!/bin/bash

set -e

rm LEMS*ml *nml

python GenerateWilsonCowanLEMS.py -ie0 0   -ii0 0    # dimensionless
python GenerateWilsonCowanLEMS.py -ie0 0.5 -ii0 0.5  # dimensionless

python GenerateWilsonCowanLEMS.py -ie0 0   -ii0 0    -dims
python GenerateWilsonCowanLEMS.py -ie0 0.5 -ii0 0.5  -dims

jnml LEMS_WC_drivenDL.xml -nogui
jnml LEMS_WC_slowDL.xml -nogui

jnml LEMS_WC_driven.xml -nogui
jnml LEMS_WC_slow.xml -nogui

jnml LEMS_WC_driven.xml -neuron -run -nogui
jnml LEMS_WC_slow.xml -neuron -run -nogui

python GenerateNetworkOverview.py -jnml
jnml LEMS_SimWC.xml -neuron -run -nogui 

cd test_files

python Spiking.py -jnml

cd -

omv all -V 

