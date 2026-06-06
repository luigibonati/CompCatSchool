# 2. Umbrella sampling
An umbrella sampling simulation consists of a set of windows where a quadratic bias is applied along the collective variable range of interest. Each simulation samples therefore a different region of phase space along the reactive event, and their statistics can be combined to obtain a final free energy profile.

## Content
- `prepare_simulations.py`: uses the trajectory from `../1_movingrestraint` to generate one directory per umbrella sampling simulation.
- `simulations.tar.gz`: the simulation results, it contains one directory per umbrella window.
- `us.py`: script to run the restrained simulation. `prepare_simulations.py` copies this script in each window sub-directory.
- `run_plumed.py`: processes the umbrella sampling trajectories to print a collective variable file and generates the `wham_input.txt`.
- `wham_input.txt`: metadata file with the location and force constant of the umbrella biasses, required for data processing (see `../analyse_results.ipynb`).
- `transition_state_structures.xyz`: structures gathered from the simulations (see `../analyse_results.ipynb`), within a small interval around the transition state collective variable value.

## Typical use
After loading a Python/Conda environment with ASE, PLUMED, and MACE, the umbrella directories can be generated using
`python prepare_simulations.py`

Second, each umbrella can be run independently, for example using a bash loop
`for i in {0..74}; do cd U$i; sbatch job.sh; cd ..; done`
Where `job.sh` executes `python us.py xxx`, with xxx the desired value of the umbrella center.

Third, the collective variable values and WHAM input can be gathered using `python run_plumed.py`.
