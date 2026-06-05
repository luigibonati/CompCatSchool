from ase.io import read, write
from mace.calculators import mace_mp

# set torch default dtype to float64
import torch
torch.set_default_dtype(torch.float64)

traj = read("../1_deal_selection/sel200/deal_selected.xyz", index=":")

# Use mace/mh-1 as fake DFT calculator
calc = mace_mp(model='mh-1', head='oc20_usemppbe', device='cuda', dtype=torch.float64)

for i, atoms in enumerate(traj):
    old_energy = atoms.get_potential_energy()
    atoms.set_calculator(calc)
    atoms.info["energy"] = atoms.get_potential_energy()
    atoms.set_array("forces", atoms.get_forces())
    print(f"Structure {i}: dE = {1000*(atoms.info['energy'] - old_energy)/len(atoms):.4f} meV/at")
    atoms.calc = None

write("deal_labeled.xyz", traj)

write("train.xyz", traj[:160])
write("val.xyz", traj[160:])