# scanner.py

import subprocess
import yaml

def run_tools(domain):
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    tools = config['enumeration_tools']
    subdomains = set()

    for tool in tools:
        command = tool.format(domain=domain)
        print(f"\nRunning: {command}")
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL)
            output = result.decode('utf-8').splitlines()
            subdomains.update(output)
        except subprocess.CalledProcessError as e:
            print(f"Error running {command}: {e}")

    # Filter out empty lines or invalid data
    subdomains = {s.strip() for s in subdomains if s.strip()}
    return subdomains
