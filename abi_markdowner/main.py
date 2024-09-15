# main.py

import json
import toml
import argparse
from abi_markdowner.abi_markdowner import generate_markdown_from_abi
from abi_markdowner.file_io import read_abi_from_file, save_markdown_to_file

# Default values
SC_PATH = './'
OUTPUT_FILE_PATH = 'README.md'
CARGO_TOML_PATH = 'Cargo.toml'
DEPLOYMENTS_JSON_PATH = 'deployments.json'

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Generate README.md from ABI.")
    parser.add_argument('--sc-path', type=str, default=SC_PATH, help="Path to the smart contract project.")
    sc_path = parser.parse_args().sc_path
    parser.add_argument('--output-file', type=str, default=sc_path + OUTPUT_FILE_PATH, help="Output file path for the generated Markdown.")
    parser.add_argument('--cargo-toml', type=str, default=sc_path + CARGO_TOML_PATH, help="Path to Cargo.toml file.")
    parser.add_argument('--deployments-json', type=str, default=sc_path + DEPLOYMENTS_JSON_PATH, help="Path to the deployments.json file.")
    return parser.parse_args()

def load_cargo_toml(cargo_toml_path):
    """Load the Cargo.toml file and return the package name."""
    with open(cargo_toml_path, 'r') as file:
        cargo_toml = toml.load(file)
    return cargo_toml['package']['name']

def load_deployments(deployments_json_path):
    """Load deployments from the specified JSON file."""
    try:
        with open(deployments_json_path, 'r') as file:
            deployments = json.load(file)
            return {
                'mainnet': deployments.get('mainnet', []),
                'devnet': deployments.get('devnet', []),
                'testnet': deployments.get('testnet', [])
            }
    except FileNotFoundError:
        return {
            'mainnet': [],
            'devnet': [],
            'testnet': []
        }

def main():
    """Main function to generate Markdown from ABI."""
    args = parse_arguments()

    # Load the package name from Cargo.toml
    package_name = load_cargo_toml(args.cargo_toml)

    # Construct the ABI file path
    abi_file_path = f"{args.sc_path}output/{package_name}.abi.json"
    
    # Read the ABI from the file
    abi = read_abi_from_file(abi_file_path)

    # Load deployments from the JSON file
    deployments = load_deployments(args.deployments_json)

    # Generate Markdown content
    markdown_content = generate_markdown_from_abi(abi, deployments)

    # Save the Markdown content to a file
    save_markdown_to_file(markdown_content, args.output_file)

    print(f"Markdown file generated: {args.output_file}")

if __name__ == '__main__':
    main()
