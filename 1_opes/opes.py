from ase.calculators.plumed import Plumed, restart_from_trajectory
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.bussi import Bussi
from ase.io import read,  write, Trajectory
from ase import units

from mace.calculators import mace_mp

import numpy as np

# Load system
atoms = read("../0_system/init_config.xyz")

# Setup MACE calculator
calc = mace_mp(model='mh-0', head='oc20_usemppbe')

# MD settings
temperature = 700 # K
kT = units.kB*temperature
timestep = 0.5 # fs
taut = 100 # fs
total_time = 100 # ps
nb_steps = int((total_time*1000)//timestep)
interval_info = 100 # steps
interval_traj = 100 # steps

# Write PLUMED input file
with open("plumed.dat", "w") as f:
    f.write(f"""
UNITS LENGTH=A ENERGY=eV

Fe: GROUP ATOMS={','.join(map(str, (np.argwhere(atoms.get_atomic_numbers()==26)+1).flatten().tolist()))}
N: GROUP  ATOMS={','.join(map(str, (np.argwhere(atoms.get_atomic_numbers()==7)+1).flatten().tolist()))}

d_N2: DISTANCE ATOMS={np.argwhere(atoms.get_atomic_numbers()==7)[0,0]+1},{np.argwhere(atoms.get_atomic_numbers()==7)[1,0]+1}
com_N2: COM ATOMS=N
c_N_Fe: COORDINATION GROUPA=N GROUPB=Fe R_0=2.5

UPPER_WALLS ARG=d_N2 AT=2 KAPPA=0.2 EXP=2 EPS=0.1
UPPER_WALLS ARG=com_N2.z AT=10 KAPPA=1

opes: OPES_METAD_EXPLORE ARG=d_N2,c_N_Fe PACE=100 BARRIER=1 TEMP={temperature} STATE_WFILE=STATES STATE_WSTRIDE=1*100

PRINT STRIDE={interval_info} ARG=* FILE=COLVAR
FLUSH STRIDE=100
""" )

# Setup PLUMED
plumed_input = open("plumed.dat", "r").read().splitlines()
plumed_calc = Plumed(calc, plumed_input, timestep * units.fs, atoms, kT)
atoms.calc = plumed_calc

# Setup MD dynamics
MaxwellBoltzmannDistribution(atoms, temperature_K=temperature)
dyn = Bussi(atoms, timestep * units.fs, temperature, taut * units.fs)

# Save energies and temperature
energy_log = []

def log_status(a=atoms, dyn=dyn):
    epot = float(a.get_potential_energy()[0])
    ekin = float(a.get_kinetic_energy())
    etot = epot + ekin
    temp = float(a.get_temperature())
    time_fs = dyn.get_time() / units.fs

    energy_log.append([time_fs, epot, ekin, etot, temp])

dyn.attach(log_status, interval_info)

# Save trajectory
traj = Trajectory("traj.traj", "w", atoms)
dyn.attach(traj, interval_traj)

# Run simulation
dyn.run(nb_steps)

np.savetxt(
    "ENERGY",
    np.asarray(energy_log),
    delimiter=" ",
    header="time_fs Epot_eV Ekin_eV Etot_eV Temp_K",
    fmt="%12.6f"
)

traj = read("traj.traj", index=":")
write("traj.xyz", traj)