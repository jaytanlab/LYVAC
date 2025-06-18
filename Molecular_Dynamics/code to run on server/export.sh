echo "exporting on charmm-gui-4606498400-edited"
cd /hy-tmp/20250430-edited/charmm-gui-4606498400-edited
gmx grompp -f step7_production.mdp -c step7_production.gro -p system.top -n index.ndx -o rerun.tpr > rerun_grompp.log
gmx mdrun -s rerun.tpr -rerun step7_production.xtc -deffnm rerun -nt 1 > rerun_mdrun.txt
echo "Coul-SR:MEMBRANE-MEMBRANE" | gmx energy -f rerun.edr -s rerun.tpr -o lipid_interactions.xvg -b 4000 > energy_Lipid_Coul.txt
echo "LJ-SR:MEMBRANE-MEMBRANE" | gmx energy -f rerun.edr -s rerun.tpr -o lipid_interactions.xvg -b 4000 > energy_Lipid_LJ.txt
echo "exporting on charmm-gui-4606498540-edited"
cd /hy-tmp/20250430-edited/charmm-gui-4606498540-edited
gmx grompp -f step7_production.mdp -c step7_production.gro -p system.top -n index.ndx -o rerun.tpr > rerun_grompp.log
gmx mdrun -s rerun.tpr -rerun step7_production.xtc -deffnm rerun -nt 1 > rerun_mdrun.txt
echo "Coul-SR:MEMBRANE-MEMBRANE" | gmx energy -f rerun.edr -s rerun.tpr -o lipid_interactions.xvg -b 4000 > energy_Lipid_Coul.txt
echo "LJ-SR:MEMBRANE-MEMBRANE" | gmx energy -f rerun.edr -s rerun.tpr -o lipid_interactions.xvg -b 4000 > energy_Lipid_LJ.txt
echo "exporting on charmm-gui-4606498678-edited"
cd /hy-tmp/20250430-edited/charmm-gui-4606498678-edited
gmx grompp -f step7_production.mdp -c step7_production.gro -p system.top -n index.ndx -o rerun.tpr > rerun_grompp.log
gmx mdrun -s rerun.tpr -rerun step7_production.xtc -deffnm rerun -nt 1 > rerun_mdrun.txt
echo "Coul-SR:MEMBRANE-MEMBRANE" | gmx energy -f rerun.edr -s rerun.tpr -o lipid_interactions.xvg -b 4000 > energy_Lipid_Coul.txt
echo "LJ-SR:MEMBRANE-MEMBRANE" | gmx energy -f rerun.edr -s rerun.tpr -o lipid_interactions.xvg -b 4000 > energy_Lipid_LJ.txt
echo "exporting on charmm-gui-4606498844-edited"
cd /hy-tmp/20250430-edited/charmm-gui-4606498844-edited
gmx grompp -f step7_production.mdp -c step7_production.gro -p system.top -n index.ndx -o rerun.tpr > rerun_grompp.log
gmx mdrun -s rerun.tpr -rerun step7_production.xtc -deffnm rerun -nt 1 > rerun_mdrun.txt
echo "Coul-SR:MEMBRANE-MEMBRANE" | gmx energy -f rerun.edr -s rerun.tpr -o lipid_interactions.xvg -b 4000 > energy_Lipid_Coul.txt
echo "LJ-SR:MEMBRANE-MEMBRANE" | gmx energy -f rerun.edr -s rerun.tpr -o lipid_interactions.xvg -b 4000 > energy_Lipid_LJ.txt
echo "exporting on charmm-gui-4606499333-edited"
cd /hy-tmp/20250430-edited/charmm-gui-4606499333-edited
gmx grompp -f step7_production.mdp -c step7_production.gro -p system.top -n index.ndx -o rerun.tpr > rerun_grompp.log
gmx mdrun -s rerun.tpr -rerun step7_production.xtc -deffnm rerun -nt 1 > rerun_mdrun.txt
echo "Coul-SR:MEMBRANE-MEMBRANE" | gmx energy -f rerun.edr -s rerun.tpr -o lipid_interactions.xvg -b 4000 > energy_Lipid_Coul.txt
echo "LJ-SR:MEMBRANE-MEMBRANE" | gmx energy -f rerun.edr -s rerun.tpr -o lipid_interactions.xvg -b 4000 > energy_Lipid_LJ.txt
echo "exporting on charmm-gui-4606499468-edited"
cd /hy-tmp/20250430-edited/charmm-gui-4606499468-edited
gmx grompp -f step7_production.mdp -c step7_production.gro -p system.top -n index.ndx -o rerun.tpr > rerun_grompp.log
gmx mdrun -s rerun.tpr -rerun step7_production.xtc -deffnm rerun -nt 1 > rerun_mdrun.txt
echo "Coul-SR:MEMBRANE-MEMBRANE" | gmx energy -f rerun.edr -s rerun.tpr -o lipid_interactions.xvg -b 4000 > energy_Lipid_Coul.txt
echo "LJ-SR:MEMBRANE-MEMBRANE" | gmx energy -f rerun.edr -s rerun.tpr -o lipid_interactions.xvg -b 4000 > energy_Lipid_LJ.txt
