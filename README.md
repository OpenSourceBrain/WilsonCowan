## Wilson and Cowan model

The models in this repo are based on: From Excitatory and Inhibitory Interactions in Localized Populations of Model Neurons Hugh R. Wilson and Jack D. Cowan; Biophys J. 1972 January; 12:1-24. [doi:10.1016/S0006-3495(72)86068-5](https://dx.doi.org/10.1016%2FS0006-3495(72)86068-5)

### Model
The Wilson and Cowan model describes the dynamics and interaction between the excitatory and inhibitory population of neurons.

![](https://raw.githubusercontent.com/OpenSourceBrain/WilsonCowan/master/NeuroML2/img/WC.gv.png)

Following the Bard Ermentrout's implementation in [xppau](http://www.math.pitt.edu/~bard/xpp/xpp.html), the dynamics of the model is defined as:

<a href="https://www.codecogs.com/eqnedit.php?latex=\tau_i&space;\frac{dR_i}{dt}&space;=&space;-r_i&space;&plus;&space;\phi&space;(w_{ei}\cdot&space;r_{e}&space;-&space;w_{ii}&space;\cdot&space;r_i&space;-&space;z_i)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\tau_i&space;\frac{dR_i}{dt}&space;=&space;-r_i&space;&plus;&space;\phi&space;(w_{ei}\cdot&space;r_{e}&space;-&space;w_{ii}&space;\cdot&space;r_i&space;-&space;z_i)" title="\tau_i \frac{dR_i}{dt} = -r_i + \phi (w_{ei}\cdot r_{e} - w_{ii} \cdot r_i - z_i)" /></a>

<a href="https://www.codecogs.com/eqnedit.php?latex=\tau_e&space;\frac{dR_e}{dt}&space;=&space;-r_e&space;&plus;&space;\phi&space;(w_{ee}\cdot&space;r_{e}&space;-&space;w_{ei}&space;\cdot&space;r_i&space;-&space;z_e)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\tau_e&space;\frac{dR_e}{dt}&space;=&space;-r_e&space;&plus;&space;\phi&space;(w_{ee}\cdot&space;r_{e}&space;-&space;w_{ei}&space;\cdot&space;r_i&space;-&space;z_e)" title="\tau_e \frac{dR_e}{dt} = -r_e + \phi (w_{ee}\cdot r_{e} - w_{ei} \cdot r_i - z_e)" /></a>

where u and v represents the proportion of excitatory and inhibitory cells firing, i_e and i_i are input currents, z_e and z_i correspond to constant modulatory currents that are applied to the populations, w<sub>ee</sub>, w<sub>ei</sub>, w<sub>ie</sub>, w<sub>ii</sub> are the connections synaptic coupling strength between the excitatory-excitatory, excitatory-inhibitory, inhibitory-excitatory, and inhibitory-inhibitory population respectively.

### Simulations
Simulations for the Wilson and Cowan model are available in XPP, NEURON, Python and NeuroML. Using the different simulators we analysed the dynamics with (right images below) and without (left images below) an additional sinusoidal input current.

#### XPP
Although we did not analyse this simulation, for completeness the links for the XPP can be found [here](https://github.com/OpenSourceBrain/WilsonCowan/tree/master/XPP).

#### NEURON
See [here](https://github.com/OpenSourceBrain/WilsonCowan/tree/master/NEURON).

To run the simulation on the NEURON folder type:
```
nrnivmodl
nrngui wc.hoc
```

<p float="left">
   <img src="https://raw.githubusercontent.com/OpenSourceBrain/WilsonCowan/master/NEURON/img/NEURON_no_drive_rate.png" width="400" />
   <img src="https://raw.githubusercontent.com/OpenSourceBrain/WilsonCowan/master/NEURON/img/NEURON_driven_rate.png" width="400" />
</p>

#### Python
To run the simulation on the Python folder type:
```
python WilsonCowan.py -wee 10. -wei 12. -wie 8. -wii 3. -ze 0.2 -zi 4. -ie1 0 -ii1 0 -w 0.25
python WilsonCowan.py -wee 10. -wei 12. -wie 8. -wii 3. -ze 0.2 -zi 4. -ie1 0.5 -ii1 0.5 -w 0.25
 ```

<p float="left">
   <img src="https://raw.githubusercontent.com/OpenSourceBrain/WilsonCowan/master/Python/img/Python_no_drive.png" width="400" />
   <img src="https://raw.githubusercontent.com/OpenSourceBrain/WilsonCowan/master/Python/img/Python_driven.png" width="400" />
</p>

#### NeuroML2
To run the simulation on the NeuroML2 folder type:
```
jnml LEMS_WC_slow.xml
jnml LEMS_WC_driven.xml
```
<p float="left">
  <img src="https://raw.githubusercontent.com/OpenSourceBrain/WilsonCowan/master/NeuroML2/img/NeuroML_no_drive.png" width="400" />
  <img src="https://raw.githubusercontent.com/OpenSourceBrain/WilsonCowan/master/NeuroML2/img/NeuroML_driven.png" width="400" />
</p>

### Model dynamics
We also explored the generated dynamics of the models in NeuroML2 and Python.

While a more detailed description of the dynamics and isoline analysis with different parameters can be found [here](https://github.com/OpenSourceBrain/WilsonCowan/tree/master/Python/README.md), a short example of isocline analysis in NeuroML2 can be found in this [jupyter notebook].

### Requirements

The simulations require [NEURON](https://www.neuron.yale.edu/neuron/download) and [jnml](https://github.com/NeuroML/jNeuroML) to be installed..

[![Build Status](https://travis-ci.com/OpenSourceBrain/WilsonCowan.svg?branch=master)](https://travis-ci.com/OpenSourceBrain/WilsonCowan)



