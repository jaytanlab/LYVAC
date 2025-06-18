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
                    file.write(f'echo "working on charmm-gui-{folder_id}-edited"\n')
                    file.write(f'cd /hy-tmp/20250430-edited/charmm-gui-{folder_id}-edited\n')
                    file.write(f'sed -i \'s/\\r//g\' ./README\n')
                    file.write(f'timeout 3600s bash -c \"time bash ./README > out.txt 2>&1\"\n')
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function with the appropriate file names
generate_script('folders.txt', 'run.sh')