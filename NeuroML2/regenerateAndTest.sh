#!/bin/bash

set -e

python GenerateWilsonCowanLEMS.py -ie0 0 -ii0 0
python GenerateWilsonCowanLEMS.py -ie0 0.5 -ii0 0.5

jnml LEMS_WC_drivenSim.xml -nogui
jnml LEMS_WC_slowSim.xml -nogui

