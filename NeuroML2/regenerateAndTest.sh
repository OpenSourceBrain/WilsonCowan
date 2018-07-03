#!/bin/bash

set -e

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

omv all -V 

