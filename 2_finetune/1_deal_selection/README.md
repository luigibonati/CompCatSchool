## DEAL selection

see https://github.com/luigibonati/DEAL for instructions

#run deal to select 200 structures
deal -c deal.yaml --max 200 -f traj.xyz

#chemiscope analysis:
deal-chemiscope -t deal_trajectory_uncertainty.xyz --colvar ../../../1_opes/700K_explore/COLVAR