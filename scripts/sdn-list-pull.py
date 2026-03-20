import requests
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime
import hashlib
import os
import sys

# URL to fetch the SDN XML directly from the API
SDN_XML_URL = 'https://sanctionslistservice.ofac.treas.gov/api/download/sdn.xml'

# Namespace dictionary to handle the XML namespaces
namespaces = {
    'ns': 'https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/XML'
}

# Blockchain categorization map based on currency type (direct mapping)
currency_chain_map = {
    'BTC': 'Bitcoin',
    'XBT': 'Bitcoin',
    'ETH': 'Ethereum',
    'BNB': 'Binance Smart Chain',
    'TRX': 'Tron',
    'XRP': 'Ripple',
    'SOL': 'Solana',
    'DOT': 'Polkadot',
    'AVAX': 'Avalanche',
    'MATIC': 'Polygon',
    'ALGO': 'Algorand',
    'XLM': 'Stellar',
    'ARB': 'Ethereum',
    'OP': 'Ethereum'
}

def recognize_base_chain_from_address(address):
    if address.startswith(('1', '3', 'bc1')):
        return 'Bitcoin'
    elif address.startswith('0x'):
        return 'Ethereum'
    elif address.startswith('T'):
        return 'Tron'
    else:
        return 'Unknown'

def calculate_hash(wallet_list):
    content = '\n'.join(sorted(wallet_list))
    return hashlib.sha256(content.encode()).hexdigest()

def get_previous_hash():
    try:
        response = requests.get('https://api.github.com/repos/{GITHUB_REPOSITORY}/releases/latest'.replace('{GITHUB_REPOSITORY}', os.getenv('GITHUB_REPOSITORY', '')))
        if response.status_code == 200:
            release_data = response.json()
            return release_data.get('body', '').split('Hash: ')[-1].strip() if 'Hash: ' in release_data.get('body', '') else None
    except:
        pass
    return None

def get_digital_currency_addresses():
    print("Starting to fetch the SDN XML file...")
    try:
        response = requests.get(SDN_XML_URL)
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            print("Successfully fetched the XML file.")
            root = ET.fromstring(response.content)
            print("Parsed the XML content.")
            
            complete_wallet_list = [] 
            blockchain_wallets = defaultdict(list)
            unrecognized_wallets = [] 
            
            for id_element in root.findall('.//ns:id', namespaces):
                id_type = id_element.find('ns:idType', namespaces)
                id_number = id_element.find('ns:idNumber', namespaces)
                
                if id_type is not None and 'Digital Currency Address' in id_type.text:
                    currency_type = id_type.text.split(' - ')[-1]
                    wallet_address = id_number.text if id_number is not None else 'N/A'
                    print(f"Currency: {currency_type}, Address: {wallet_address}")
                    
                    complete_wallet_list.append(wallet_address)
                    
                    if currency_type in currency_chain_map:
                        blockchain = currency_chain_map[currency_type]
                    else:
                        blockchain = recognize_base_chain_from_address(wallet_address)
                    
                    if blockchain != 'Unknown':
                        blockchain_wallets[blockchain].append(wallet_address)
                    else:
                        unrecognized_wallets.append(wallet_address)
            
            current_hash = calculate_hash(complete_wallet_list)
            previous_hash = get_previous_hash()
            
            print(f"Current hash: {current_hash}")
            print(f"Previous hash: {previous_hash}")
            
            if current_hash == previous_hash:
                print("No changes detected. Skipping release creation.")
                with open(os.getenv('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
                    f.write(f"has_changes=false\n")
                sys.exit(0)
            
            print("Changes detected. Creating files...")
            with open(os.getenv('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
                f.write(f"has_changes=true\n")
                f.write(f"content_hash={current_hash}\n")
            
            os.makedirs("OFAC_Sanctioned_Wallet_Lists", exist_ok=True)
            
            complete_list_file = "OFAC_Sanctioned_Wallet_Lists/complete_sanctioned_wallet_list.txt"
            print(f"Attempting to write to {complete_list_file}...")
            with open(complete_list_file, "w") as f:
                f.write(f"# Last Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")
                for address in complete_wallet_list:
                    f.write(f"{address}\n")
            print(f"File written successfully to {complete_list_file}.")
            
            for blockchain, addresses in blockchain_wallets.items():
                blockchain_file_name = f"OFAC_Sanctioned_Wallet_Lists/{blockchain.lower().replace(' ', '_')}_sanctioned_wallet_list.txt"
                print(f"Attempting to write to {blockchain_file_name}...")
                with open(blockchain_file_name, "w") as f:
                    f.write(f"# Last Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")
                    for address in addresses:
                        f.write(f"{address}\n")
                print(f"File written successfully to {blockchain_file_name}.")
            
            if unrecognized_wallets:
                unrecognized_file = "OFAC_Sanctioned_Wallet_Lists/unrecognized_blockchain_sanctioned_wallet_list.txt"
                print(f"Attempting to write to {unrecognized_file}...")
                with open(unrecognized_file, "w") as f:
                    f.write(f"# Last Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")
                    for address in unrecognized_wallets:
                        f.write(f"{address}\n")
                print(f"File written successfully to {unrecognized_file}.")
                    
        else:
            print(f"Failed to fetch SDN XML from the API: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

get_digital_currency_addresses()
