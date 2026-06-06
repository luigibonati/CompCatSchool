from pathlib import Path
import shutil

import numpy as np

from ase.io import read, write


if __name__=="__main__":
    # US settings
    centers = np.linspace(1.1, 2.3, 75)

    # identify structure closest to center
    movingrestraint_traj = read(Path.cwd().parent / "1_movingrestraint/md.traj", index=":")
    N_indices = np.flatnonzero(movingrestraint_traj[0].get_atomic_numbers() == 7)
    
    distances = []
    for atoms in movingrestraint_traj:
        d = atoms.get_distance(N_indices[0], N_indices[1])
        distances.append(d)
    distances = np.array(distances)

    for i, center in enumerate(centers):
        umb_dir = Path.cwd() / f"U{i}"
        umb_dir.mkdir()

        idx = np.argmin(np.abs(distances - center))

        atoms = movingrestraint_traj[idx]
        write(umb_dir / "start.xyz", atoms)

        shutil.copy(Path.cwd() / "us.py", umb_dir)
        shutil.copy(Path.cwd() / "job.sh", umb_dir)

        with open(umb_dir / "job.sh", "a") as f:
            f.write("\n")
            f.write(f"python us.py {center}")
