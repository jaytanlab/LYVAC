# Python script to generate run.sh from folders.txt
import re

def generate_script(input_file):
    # Open the input file to read folder names
    with open(input_file, 'r') as file:
        folder_ids = file.readlines()
    
    for folder_idx in range(0, len(folder_ids), 2):
        folder_id1 = folder_ids[folder_idx]
        folder_id2 = folder_ids[folder_idx + 1]

        folder_id1 = folder_id1.strip()
        folder_id2 = folder_id2.strip()
        
        try:
            donor_Ave, donor_EstErr, donor_RMSD = 0, 0, 0
            with open(f"./charmm-gui-{folder_id1}-edited/energy_Lipid_Coul.txt", "r") as fin:
                lines = fin.readlines()
                line = lines[6]
                line = re.sub(r'\s+', ' ', line).strip().split(' ')
                donor_Ave = float(line[1])
                donor_EstErr = float(line[2])
                donor_RMSD = float(line[3])
            with open(f"./charmm-gui-{folder_id1}-edited/energy_Lipid_LJ.txt", "r") as fin:
                lines = fin.readlines()
                line = lines[6]
                line = re.sub(r'\s+', ' ', line).strip().split(' ')
                donor_Ave += float(line[1])
                donor_EstErr += float(line[2])
                donor_RMSD += float(line[3])

            acceptor_Ave, acceptor_EstErr, acceptor_RMSD = 0, 0, 0
            with open(f"./charmm-gui-{folder_id2}-edited/energy_Lipid_Coul.txt", "r") as fin:
                lines = fin.readlines()
                line = lines[6]
                line = re.sub(r'\s+', ' ', line).strip().split(' ')
                acceptor_Ave = float(line[1])
                acceptor_EstErr = float(line[2])
                acceptor_RMSD = float(line[3])
            with open(f"./charmm-gui-{folder_id2}-edited/energy_Lipid_LJ.txt", "r") as fin:
                lines = fin.readlines()
                line = lines[6]
                line = re.sub(r'\s+', ' ', line).strip().split(' ')
                acceptor_Ave += float(line[1])
                acceptor_EstErr += float(line[2])
                acceptor_RMSD += float(line[3])

            total_Ave = donor_Ave + acceptor_Ave
            total_EstErr = donor_EstErr + acceptor_EstErr
            total_RMSD = donor_RMSD + acceptor_RMSD

            print(f"{folder_id1}/{folder_id2}: total_Ave {total_Ave} total_EstErr {total_EstErr} total_RMSD {total_RMSD}")

        except Exception as e:
            print(f"{folder_id1}/{folder_id2}: An error occurred: {e}")

# Call the function with the appropriate file names
generate_script('folders_export.txt')