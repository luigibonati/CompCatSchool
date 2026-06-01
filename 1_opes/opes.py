from ase.calculators.plumed import Plumed
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.bussi import Bussi
from ase.io import read,  write, Trajectory
from ase import units
import time
import numpy as np
from pathlib import Path
import os
from mace.calculators import mace_mp
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--temperature", type=float, default=700)
parser.add_argument("--bias", type=str, default="OPES_METAD_EXPLORE")
parser.add_argument("--barrier", type=float, default=1.0)
parser.add_argument("--system", type=str, default="../0_system/init_config.xyz")
args = parser.parse_args()

# Load system
atoms = read(args.system)

# Setup MACE calculator
calc = mace_mp(model='mh-0', head='oc20_usemppbe', device='cuda')

# MD settings
temperature = args.temperature # K
timestep = 0.5 # fs
total_time = 500 # 500 # ps
taut = 100 # fs
interval_info = 100 # steps
interval_traj = interval_info # steps

# Create output directory
root = Path.cwd()
outdir = root / f"{int(temperature)}K_{'metad' if args.bias=='OPES_METAD' else 'explore'}_b{args.barrier}"
outdir.mkdir(parents=True, exist_ok=True)
os.chdir(outdir)

# Write PLUMED input file
with open("plumed.dat", "w") as f:
    f.write(f"""
UNITS LENGTH=A ENERGY=eV

Fe: GROUP ATOMS={','.join(map(str, (np.argwhere(atoms.get_atomic_numbers()==26)+1).flatten().tolist()))}
N: GROUP  ATOMS={','.join(map(str, (np.argwhere(atoms.get_atomic_numbers()==7)+1).flatten().tolist()))}

d_N2: DISTANCE ATOMS={np.argwhere(atoms.get_atomic_numbers()==7)[0,0]+1},{np.argwhere(atoms.get_atomic_numbers()==7)[1,0]+1}
com_N2: COM ATOMS=N
c_N_Fe: COORDINATION GROUPA=N GROUPB=Fe R_0=2.5

w_d_N2: UPPER_WALLS ARG=d_N2 AT=2 KAPPA=0.2 EXP=2 EPS=0.1
w_com_N2: UPPER_WALLS ARG=com_N2.z AT=10 KAPPA=1

opes: {args.bias} ARG=d_N2,c_N_Fe PACE=100 BARRIER={args.barrier} TEMP={temperature} STATE_WFILE=STATES STATE_WSTRIDE=100

PRINT STRIDE={interval_info} ARG=* FILE=COLVAR
FLUSH STRIDE=100
""" )

# Setup PLUMED
plumed_input = open("plumed.dat", "r").read().splitlines()
plumed_calc = Plumed(calc, plumed_input, timestep * units.fs, atoms, units.kB*temperature)
atoms.calc = plumed_calc

# Setup MD dynamics
MaxwellBoltzmannDistribution(atoms, temperature_K=temperature)
dyn = Bussi(atoms, timestep * units.fs, temperature, taut * units.fs)

# Logger
t0 = time.time()

log_file = open("ENERGY", "w")
log_file.write("# time_ps Epot_eV Ekin_eV Etot_eV Temp_K CPU_Time_s\n")
log_file.flush()

def log_status(a=atoms, dyn=dyn, f=log_file):
    epot = float(a.get_potential_energy()[0])
    ekin = float(a.get_kinetic_energy())
    etot = epot + ekin
    temp = float(a.get_temperature())
    time_ps = dyn.get_time() / units.fs / 1000
    cpu_time = time.time() - t0

    f.write(f"{time_ps:12.6f} {epot:16.8f} {ekin:16.8f} {etot:16.8f} {temp:12.6f} {cpu_time:12.6f}\n")
    f.flush()

dyn.attach(log_status, interval_info)

# Save trajectory
traj = Trajectory("traj.traj", "w", atoms)
dyn.attach(traj, interval_traj)

# Run simulation
nsteps = int((total_time*1000)//timestep)
dyn.run(nsteps)

# Convert trajectory to XYZ format
traj = read("traj.traj", index=":")
write("traj.xyz", traj)