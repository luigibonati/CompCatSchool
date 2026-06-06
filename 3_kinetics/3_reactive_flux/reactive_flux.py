from pathlib import Path
import numpy as np
import ase
from ase.io import read, Trajectory
from ase.md.verlet import VelocityVerlet
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from mace.calculators import mace_mp


def Distance(atoms, i1, i2):
    """
    Compute the distance between atoms i1 and i2 and its gradient w.r.t. the atomic coordinates.
    """
    r = atoms.get_distance(i1, i2, mic=True, vector=True)
    value = np.linalg.norm(r)
    
    grad = np.zeros(atoms.get_positions().shape, float)
    grad[i1, :] += -r / value
    grad[i2, :] += r / value

    return value, grad


def run_reactive_flux_trajectory(atoms, fn_traj, fn_out, calc, q_ts, steps=1_000, temperature=700.0, timestep=0.5):
    atoms.calc = calc
    MaxwellBoltzmannDistribution(atoms, temperature_K=temperature)

    # Compute initial flux at t=0 (\dot{q}_0)
    q0, grad_q0 = Distance(atoms, 96, 97)
    q0_dot = np.dot(grad_q0.flatten(), atoms.get_velocities().flatten())

    # Setup Dynamics
    dyn = VelocityVerlet(atoms, timestep=timestep * ase.units.fs)
    trajectory = Trajectory(fn_traj, "w", atoms)
    dyn.attach(trajectory)

    history = []
    committed = False

    for step in range(steps):
        dyn.step()
        q, _ = Distance(atoms, 96, 97)

        # For the first step, save the value of q0_dot
        if step == 0:
            history.append([step * timestep, q, q0_dot])
        else:
            # Compute current Heaviside value (1 if product, 0 if reactant)
            h = 1.0 if q >= q_ts else 0.0
            history.append([step * timestep, q, q0_dot * h])

        # Check for commitment to stable states
        if q > 2.2 or q < 1.4:
            committed = True

            # Maintain uniform file lengths by freezing the final flux value for the remaining time.
            for remaining_step in range(step + 1, steps):
                history.append([remaining_step * timestep, q, q0_dot * h])

            break  # Stop the expensive MACE calculator loop early

    if not committed:
        print(f"WARNING: {fn_traj} reached the step limit without committing to a stable state.")

    # Save data (every file will now have exactly 'steps' rows)
    np.savetxt(fn_out, np.array(history), header="time(fs) CV_val flux_component")
    trajectory.close()


if __name__ == "__main__":
    q_ts = 1.6719  # TS collective variable value (Angstrom)

    ts_structures = read(Path.cwd() / "transition_state_structures.xyz", index=":")
    path_trajs = Path.cwd() / "trajectories"
    path_trajs.mkdir(exist_ok=True)

    # Initialize the MACE calculator once
    mace_calc = mace_mp(model="mh-0", head="oc20_usemppbe", device="cuda")

    for i_atoms, atoms in enumerate(ts_structures):
        fn_traj = path_trajs / f"{i_atoms}.traj"
        fn_out = path_trajs / f"{i_atoms}.txt"

        run_reactive_flux_trajectory(atoms.copy(), fn_traj, fn_out, mace_calc, q_ts)
