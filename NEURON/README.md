Note from [original implementation on ModelDB](https://senselab.med.yale.edu/ModelDB/ShowModel.cshtml?model=76879) 
by Bill Lytton:

From Excitatory and Inhibitory Interactions in Localized Populations of Model Neurons
Hugh R. Wilson and Jack D. Cowan; Biophys J. 1972 January; 12:1-24. [doi:10.1016/S0006-3495(72)86068-5](https://dx.doi.org/10.1016%2FS0006-3495(72)86068-5)

To run:

    nrnivmodl
    nrngui wc.hoc

Buttons marked 'slow' use movierun so as to allow the trajectory to be viewed
during the run. 

Parameters can be set in the PointProcessManager.  Then use 'As set' button to run
without resetting the parameters.

This implementation was copied from Bard Ermentrout's xppaut file: wc.ode
(included)
