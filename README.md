# OFAC Wallet Address

Automated collection and distribution of OFAC (Office of Foreign Assets Control) sanctioned digital currency addresses.

## Overview

This repository automatically fetches and categorizes digital currency addresses from the OFAC SDN (Specially Designated Nationals) list. The workflow runs daily to check for updates and publishes the results as GitHub Releases for easy access.

## Purpose

The primary goal is to make OFAC sanctioned cryptocurrency addresses easily accessible through GitHub Releases. Users can download the latest sanctioned wallet lists without needing to parse the original XML data themselves.

## How It Works

1. **Daily Automated Fetch**: GitHub Actions workflow runs daily at 4:00 AM UTC
2. **Data Extraction**: Script fetches the SDN XML from OFAC API and extracts digital currency addresses
3. **Blockchain Categorization**: Addresses are categorized by blockchain (Bitcoin, Ethereum, Tron, etc.)
4. **Change Detection**: Calculates SHA256 hash to detect if there are any new updates
5. **Release Creation**: If changes are detected, creates a new GitHub Release with all wallet list files
6. **Skip If Unchanged**: If no changes detected, skips release creation to avoid duplicates

## File Structure

Each release contains the following files:

- `complete_sanctioned_wallet_list.txt` - All sanctioned addresses
- `bitcoin_sanctioned_wallet_list.txt` - Bitcoin addresses
- `ethereum_sanctioned_wallet_list.txt` - Ethereum addresses
- `tron_sanctioned_wallet_list.txt` - Tron addresses
- `binance_smart_chain_sanctioned_wallet_list.txt` - BSC addresses
- `unrecognized_blockchain_sanctioned_wallet_list.txt` - Addresses that couldn't be categorized
- And other blockchain-specific files as applicable

## Supported Blockchains

- Bitcoin (BTC, XBT)
- Ethereum (ETH, ARB, OP)
- Binance Smart Chain (BNB)
- Tron (TRX)
- Ripple (XRP)
- Solana (SOL)
- Polkadot (DOT)
- Avalanche (AVAX)
- Polygon (MATIC)
- Algorand (ALGO)
- Stellar (XLM)

## Usage

### Download Latest Lists

1. Go to the [Releases](../../releases) page
2. Download the latest release
3. Extract the wallet list files you need

### Manual Trigger

You can manually trigger the workflow from the Actions tab if needed.

## Technical Details

### Workflow

- **Schedule**: Daily at 4:00 AM UTC
- **Trigger**: Can also be manually triggered via `workflow_dispatch`
- **Release Naming**: `ofac-wallets-{yyyy-MM-dd}-{run_number}-{run_id}`

### Hash Verification

The script calculates a SHA256 hash of all wallet addresses to detect changes. The hash is stored in the release notes for verification and comparison.

## Credits

This script is based on the work from: [https://github.com/1020-1795/OFAC_SDN_Wallet_List](https://github.com/1020-1795/OFAC_SDN_Wallet_List)

## Data Source

Official OFAC SDN List API: `https://sanctionslistservice.ofac.treas.gov/api/download/sdn.xml`

## License

See [LICENSE](LICENSE) file for details.

## Disclaimer

This repository is for informational purposes only. Always verify with official OFAC sources for compliance requirements.