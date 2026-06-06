# 3. Reactive flux
A reactive flux simulation starts from a canonically-distributed set of transition state structures, which are attributed random velocities and propagated in the NVE ensemble until they committ to either the reactants or products basins. This allows to evaluate the transmission coefficient and obtain an exact rate constant beyond the transition state theory approximation. 

## Content
- `transition_state_structures.xyz`: the initial transition state structures gathered from `../2_umbrella_sampling`.
- `reactive_flux.py`: script to run the reactive flux simulations. Because of the limited number of structures and short relaxation time it works in sequence, but it can be easily parallelized for more challenging systems. 
- `trajectories.tar.gz`: the resulting atomistic trajectories and $\langle \dot{q}(0) h(q - q^{\ddagger}) \rangle$ values. To reduce the directory size, the atomistic trajectories are subsampled every 10,000 steps.

## Typical use
After loading a Python/Conda environment with ASE, PLUMED, and MACE, the reactive flux simulations can be immediately run using
`python reactive_flux.py`

The analysis of the data is then performed in `../analyse_results.ipynb`.
