import subprocess
from pathlib import Path

import numpy as np
from ase.io import read, write

def write_plumed_input(path, atoms):
    N_indices = np.flatnonzero(atoms.get_atomic_numbers() == 7) + 1
    N_list = ",".join(map(str, N_indices))
    Fe_indices = np.flatnonzero(atoms.get_atomic_numbers() == 26) + 1
    Fe_list = ",".join(map(str, Fe_indices))
    plumed_input=f"""UNITS LENGTH=A ENERGY=kj/mol
        d_N2: DISTANCE ATOMS={N_list}
        CN_N2: COORDINATION GROUPA={N_indices[0]} GROUPB={N_indices[1]} R_0=1.6
        CN_N_Fe: COORDINATION GROUPA={N_list} GROUPB={Fe_list} R_0=1.8
        PRINT ARG=d_N2,CN_N2,CN_N_Fe FILE=COLVAR"""
    with open(path / "plumed.dat", "w") as f:
        f.write(plumed_input)

if __name__=="__main__":
    # generate the colvar files
    idx_umb = 0
    while True:
        path_umb = Path.cwd() / f"U{idx_umb}"
        if not path_umb.is_dir(): break
        
        if not (path_umb / "md.xyz").exists():
            traj = read(path_umb / "md.traj", index=":")
            atoms = traj[0]
            write(path_umb / "md.xyz", traj)
        else:
            atoms = read(path_umb / "md.traj")
        
        box = ",".join(str(cellpar) for cellpar in atoms.get_cell().flatten())
        write_plumed_input(path_umb, atoms)
        
        subprocess.run(f"plumed driver --plumed plumed.dat --ixyz md.xyz --box {box} --length-units A", cwd=path_umb, shell=True)

        idx_umb += 1

    # generate wham input
    centers = np.linspace(1.1, 2.3, 75)
    with open(Path.cwd() / "wham_input.txt", "w") as f:
        f.write("T=700K\n")
        for i, center in enumerate(centers):
            f.write(f"U{i} {center} 1000.0\n")
        

