# Free energy estimation with umbrella sampling and reaction rate constant calculation
This folder is divided in three subdirectories, one per elementary step required to compute an exact reaction rate constant. All simulations rely on a pretrained MACE model and on PLUMED for biassing the system. The `analyze_results.ipynb` notebook contains a complete and commented data analysis workflow.

The workflow is the following:
1. Perform a moving restraint simulation starting from the reactants to gather a set of initial structures for umbrella sampling.
1. Perform an umbrella sampling simulation with uniformly distributed quadratic umbrellas along the chosen collective variable.
1. After evaluating the free energy, gather structures atop the transition state for a reactive flux calculation.

This workflow allows to obtain the reaction free energy profile, the reaction rate constant within the transition state theory approximation, and the exact reaction rate constant.

## Folders
- `1_movingrestraint`: moving-restraint simulation to sample the reactive path.
- `2_umbrella_sampling`: umbrella sampling simulation to gather data on the reactive path.
- `3_reactive_flux`: reactive flux simulation to obtain the exact rate constant.

Each folder contains its own `README.md` file with additional information on its content.
