import json

from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from hdwallet.utils import generate_mnemonic
from typing import Optional


def create_new_hd_wallet():

    MNEMONIC: str = generate_mnemonic(language="english", strength=128)
    # Secret passphrase/password for mnemonic
    PASSPHRASE: Optional[str] = None

    # Initialize Ethereum mainnet BIP44HDWallet
    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
    # Get Ethereum BIP44HDWallet from mnemonic
    bip44_hdwallet.from_mnemonic(
        mnemonic=MNEMONIC, language="english", passphrase=PASSPHRASE
    )
    # Clean default BIP44 derivation indexes/paths
    bip44_hdwallet.clean_derivation()

    # Get Ethereum BIP44HDWallet information's from address index
    for address_index in range(10):
        # Derivation from Ethereum BIP44 derivation path
        bip44_derivation: BIP44Derivation = BIP44Derivation(
            cryptocurrency=EthereumMainnet,
            account=0,
            change=False,
            address=address_index,
        )
        # Drive Ethereum BIP44HDWallet
        bip44_hdwallet.from_path(path=bip44_derivation)
        # Clean derivation indexes/paths
        bip44_hdwallet.clean_derivation()

    return json.dumps(bip44_hdwallet.dumps())
