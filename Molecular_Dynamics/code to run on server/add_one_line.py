import os

def process_mdp_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Remove existing energygrps line (strip comments too)
    lines = [line for line in lines if not line.strip().startswith('energygrps')]

    # Ensure file ends with newline
    if lines and not lines[-1].endswith('\n'):
        lines[-1] += '\n'

    # Add new energygrps line at the end
    lines.append('energygrps = MEMBRANE\n')

    # Write back to file
    with open(filepath, 'w') as f:
        f.writelines(lines)
    print(f'Updated: {filepath}')

def main():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == 'step7_production.mdp':
                filepath = os.path.join(root, file)
                process_mdp_file(filepath)

if __name__ == '__main__':
    main()
