# Python script to generate run.sh from folders.txt

def generate_script(input_file, output_file):
    try:
        # Open the input file to read folder names
        with open(input_file, 'r') as file:
            folder_ids = file.readlines()
        
        # Open the output file to write the script
        with open(output_file, 'w') as file:
            for folder_id in folder_ids:
                folder_id = folder_id.strip()  # Remove any leading/trailing whitespace
                if folder_id.startswith("#"):
                    continue
                if folder_id:  # Ensure the line is not blank
                    file.write(f'echo "exporting on charmm-gui-{folder_id}-edited"\n')
                    file.write(f'cd /hy-tmp/20250430-edited/charmm-gui-{folder_id}-edited\n')
                    file.write(f'gmx grompp -f step7_production.mdp -c step7_production.gro -p system.top -n index.ndx -o rerun.tpr > rerun_grompp.log\n')
                    file.write(f'gmx mdrun -s rerun.tpr -rerun step7_production.xtc -deffnm rerun -nt 1 > rerun_mdrun.txt\n')
                    file.write(f'echo \"Coul-SR:MEMBRANE-MEMBRANE\" | gmx energy -f rerun.edr -s rerun.tpr -o lipid_interactions.xvg -b 4000 > energy_Lipid_Coul.txt\n')
                    file.write(f'echo \"LJ-SR:MEMBRANE-MEMBRANE\" | gmx energy -f rerun.edr -s rerun.tpr -o lipid_interactions.xvg -b 4000 > energy_Lipid_LJ.txt\n')

                    # file.write(f'echo \"Enthalpy\" | gmx energy -f step7_production.edr -o potential_energy.xvg -b 500 > energy.txt\n')
                    # file.write(f'echo \"LJ-(SR)\" | gmx energy -f step7_production.edr -o potential_energy.xvg -b 500 > energy_LJ.txt\n')
                    # file.write(f'echo \"Coulomb-(SR)\" | gmx energy -f step7_production.edr -o potential_energy.xvg -b 500 > energy_Coulomb.txt\n')
                    # file.write('cd ..\n')
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function with the appropriate file names
generate_script('folders_export.txt', 'export.sh')