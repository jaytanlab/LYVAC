import os
import shutil

def copy_and_modify_folders(n_parallel=4):
    # Get all relevant directories in the current folder
    all_folders = [d for d in os.listdir() if d.startswith("charmm-gui-") and len(d) == 21]
    # Process each folder
    for folder in all_folders:
        original_path = f"./{folder}/gromacs"
        new_path = f"../{folder}-edited"
        
        # Copy gromacs folder to a new edited folder
        if os.path.exists(new_path):
            shutil.rmtree(new_path)
        shutil.copytree(original_path, new_path)

        # Modify README file
        # Modify README file
        readme_path = f"{new_path}/README"
        with open(readme_path, 'r') as file:
            lines = file.readlines()
        
        with open(readme_path, 'w') as file:
            for line in lines:
                if line.strip().startswith("setenv GMX_MAXCONSTRWARN"):
                    file.write("export GMX_MAXCONSTRWARN=-1\n")
                    # file.write("export OMP_NUM_THREADS=32\n")
                elif line.strip().startswith("unsetenv GMX_MAXCONSTRWARN"):
                    file.write("unset GMX_MAXCONSTRWARN\n")
                    # file.write("unset OMP_NUM_THREADS\n")
                elif line.lstrip().startswith("gmx mdrun -deffnm"):
                    if line.startswith("g"):
                        file.write(f"{line.strip()} -nt 84\n")
                    else:
                        file.write(f"{line}\n")
                elif line.lstrip().startswith("set cnt    = 2"):
                    file.write(f"cnt=2\n")
                elif line.lstrip().startswith("set cntmax = 6"):
                    file.write(f"cntmax=6\n")
                elif line.lstrip().startswith("while"):
                    file.write(f"while [ $cnt -le $cntmax ]\n")
                    file.write(f"do\n")
                elif line.lstrip().startswith("@ pcnt = "):
                    file.write(f"    pcnt=$((cnt - 1))\n")
                elif line.lstrip().startswith("@ cnt += 1"):
                    file.write(f"    cnt=$((cnt + 1))\n")
                elif line.lstrip().startswith("endif"):
                    file.write(f"    fi\n")
                elif line.lstrip().startswith("end"):
                    file.write(f"done\n")
                elif line.lstrip().startswith("if ($cnt == 2) then"):
                    file.write(f"    if [ $cnt -eq 2 ]; then\n")
                else:
                    file.write(line)

        # Modify .mdp files
        mdp_files = [
            'step6.2_equilibration.mdp', 'step6.3_equilibration.mdp',
            'step6.4_equilibration.mdp', 'step6.5_equilibration.mdp',
            'step6.6_equilibration.mdp', 'step6.0_minimization.mdp',
            'step6.1_minimization.mdp', "step7_production.mdp"
        ]
        
        nsteps_changes = {
            'step7_production.mdp': 1000000, # 20 ns
            'step6.0_minimization.mdp': 2000,
            'step6.1_minimization.mdp': 2000,
            'step6.2_equilibration.mdp': 100000,
            'step6.3_equilibration.mdp': 50000,
            'step6.4_equilibration.mdp': 50000,
            'step6.5_equilibration.mdp': 50000,
            'step6.6_equilibration.mdp': 50000,
        }
        nberendsen_changes = {
            'step6.2_equilibration.mdp': 0,
            'step6.3_equilibration.mdp': 0,
            'step6.4_equilibration.mdp': 0,
            'step6.5_equilibration.mdp': 0,
            'step6.6_equilibration.mdp': 0,
            'step7_production.mdp': 0
        }

        for mdp in mdp_files:
            mdp_path = f"{new_path}/{mdp}"
            if os.path.exists(mdp_path):
                with open(mdp_path, 'r') as file:
                    mdp_lines = file.readlines()
                
                with open(mdp_path, 'w') as file:
                    for mdp_line in mdp_lines:
                        if mdp in nberendsen_changes and "Pcoupl                   = berendsen" in mdp_line:
                            mdp_line = "Pcoupl                   = c-rescale\n"

                        if mdp in nsteps_changes and "nsteps                   =" in mdp_line:
                            mdp_line = f"nsteps                   = {nsteps_changes[mdp]}\n"

                        if "rcoulomb                 = 1.1" in mdp_line:
                            if mdp in 'step6.0_minimization.mdp':
                                mdp_line = "rcoulomb                 = 4.0\n"
                            elif mdp in ['step6.1_minimization.mdp', 'step6.2_equilibration.mdp', 'step6.3_equilibration.mdp', 'step6.4_equilibration.mdp', \
                                'step6.5_equilibration.mdp', 'step6.6_equilibration.mdp', 'step7_production.mdp']:
                                mdp_line = "rcoulomb                 = 2.0\n"
                        if "rvdw                     = 1.1" in mdp_line:
                            if mdp in 'step6.0_minimization.mdp':
                                mdp_line = "rvdw                     = 4.0\n"
                            elif mdp in ['step6.1_minimization.mdp', 'step6.2_equilibration.mdp', 'step6.3_equilibration.mdp', 'step6.4_equilibration.mdp', \
                                'step6.5_equilibration.mdp', 'step6.6_equilibration.mdp', 'step7_production.mdp']:
                                mdp_line = "rvdw                     = 2.0\n"

                        # if "nstxout                  = 5000" in mdp_line and mdp in ['step7_production.mdp']:
                        #     mdp_line = "nstxout                  = 5000\n"
                        # if "nstvout                  = 5000" in mdp_line and mdp in ['step7_production.mdp']:
                        #     mdp_line = "nstvout                  = 5000\n"
                        # if "nstfout                  = 5000" in mdp_line and mdp in ['step7_production.mdp']:
                        #     mdp_line = "nstfout                  = 5000\n"
                        # if "nstlog                   = 5000" in mdp_line and mdp in ['step7_production.mdp']:
                        #     mdp_line = "nstlog                   = 5000\n"
                        # if "nstenergy                = 5000" in mdp_line and mdp in ['step7_production.mdp']:
                        #     mdp_line = "nstenergy                = 5000\n"
                        # if "nstxout-compressed       = 5000" in mdp_line and mdp in ['step7_production.mdp']:
                        #     mdp_line = "nstxout-compressed       = 5000\n"
                        
                        file.write(mdp_line)
                    
                    if "step7_production.mdp" in mdp_path:
                        file.write("\nenergygrps = MEMBRANE")

# Call the function
copy_and_modify_folders()