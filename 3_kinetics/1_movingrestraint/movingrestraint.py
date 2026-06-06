from pathlib import Path

import numpy as np

import ase
from ase.io import read, write, Trajectory
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.calculators.plumed import Plumed

from mace.calculators import mace_mp


def get_plumed_input(atoms):
    """
    Returns a plumed input file as list of strings to bias the distance between the two N atoms.
    """
    N_indices = np.flatnonzero(atoms.get_atomic_numbers() == 7) + 1
    N_list = ",".join(map(str, N_indices))
    plumed_input = f"""
        UNITS LENGTH=A ENERGY=kj/mol
            
        d_N2: DISTANCE ATOMS={N_list}
        
        com_N2: COM ATOMS={N_list}
        pos_N2: POSITION ATOM=com_N2
        
        w_com_N2: UPPER_WALLS ARG=pos_N2.z AT=10 KAPPA=1

        MOVINGRESTRAINT ARG=d_N2 STEP0=0 AT0=1.2 KAPPA0=250.0 STEP1=10000 AT1=2.5 KAPPA1=250.0
    """
    return [line.strip() for line in plumed_input.splitlines() if line.strip()]


if __name__=="__main__":
    # MD settings
    steps = 10_000 # number of steps
    step = 10 # saving frequency
    temperature = 700.0 # K
    timestep = 0.5 * ase.units.fs # time step
    tau = 0.01 / ase.units.fs # Langevin friction

    # load the system
    atoms = read(Path.cwd() / "start.xyz")
    
    # set the mace calculator
    mace_calc = mace_mp(model="mh-0", head="oc20_usemppbe", device="cuda")
    # add the plumed calculator
    plumed_input = get_plumed_input(atoms)
    plumed_calc = Plumed(mace_calc, plumed_input, timestep, atoms, ase.units.kB * temperature)

    # initialize the MD
    MaxwellBoltzmannDistribution(atoms, temperature_K=temperature)
    dyn = Langevin(
        atoms=atoms,
        timestep=timestep,
        temperature_K=temperature,
        friction=tau,
    )
    
    trajectory = Trajectory(Path.cwd() / "md.traj", "w", atoms)
    dyn.attach(trajectory, step)

    # run the MD
    dyn.run(steps)
    trajectory.close()


