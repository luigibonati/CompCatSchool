# 1. Moving restraint
In a moving restraint simulation, a quadratic bias is gradually shifted in time to force the system from the reactants to the products of the rare events. This allows to gather a trajectory that samples the reactive region and can be used to initialize an umbrella sampling simulation.

## Content
- `start.xyz`: an initial structure for the reactants (see `0_system`).
- `movingrestraint.py`: script to run the moving restraint simulation. It relies on ASE to drive the dynamics and PLUMED to apply the bias.
- `md.traj`: the resulting moving restraint trajectory.

## Typical use
After loading a Python/Conda environment with ASE, PLUMED, and MACE, it is sufficient to execute
`python movingrestraint.py`
