import os

from django.db import models
from dotenv import load_dotenv, find_dotenv

from web3 import Web3

load_dotenv(find_dotenv())


PROVIDER_HTTP_ENDPOINT = (
    f"https://sepolia.infura.io/v3/{os.environ.get('PROVIDER_API_KEY')}"
)
w3 = Web3(Web3.HTTPProvider(PROVIDER_HTTP_ENDPOINT))


class WalletDetailDump(models.Model):
    cryptocurrency = models.CharField(max_length=256)
    symbol = models.CharField(max_length=256)
    network = models.CharField(max_length=256)
    strength = models.SmallIntegerField()
    entropy = models.CharField(max_length=256)
    mnemonic = models.CharField(max_length=256)
    language = models.CharField(max_length=256)
    passphrase = models.CharField(max_length=256, null=True)
    seed = models.CharField(max_length=256)
    root_xprivate_key = models.CharField(max_length=256)
    root_xpublic_key = models.CharField(max_length=256)
    xprivate_key = models.CharField(max_length=256)
    xpublic_key = models.CharField(max_length=256)
    uncompressed = models.CharField(max_length=256)
    compressed = models.CharField(max_length=256)
    chain_code = models.CharField(max_length=256)
    private_key = models.CharField(max_length=256)
    public_key = models.CharField(max_length=256)
    wif = models.CharField(max_length=256)
    finger_print = models.CharField(max_length=256)
    semantic = models.CharField(max_length=256)
    path = models.CharField(max_length=256, null=True)
    hash = models.CharField(max_length=256)

    def public_address_key(self):
        return self.addresses.get_queryset().get(wallet_id=self.id).p2pkh

    def balance(self):
        eth_wallet = w3.toChecksumAddress(self.public_address_key())
        wei_value = w3.eth.get_balance(eth_wallet)
        eth_value = w3.fromWei(wei_value, "ether")
        return eth_value


class Addresses(models.Model):
    wallet = models.ForeignKey(
        WalletDetailDump, on_delete=models.CASCADE, related_name="addresses"
    )
    p2pkh = models.CharField(max_length=256)
    p2sh = models.CharField(max_length=256)
    p2wpkh = models.CharField(max_length=256)
    p2wpkh_in_p2sh = models.CharField(max_length=256)
    p2wsh = models.CharField(max_length=256)
    p2wsh_in_p2sh = models.CharField(max_length=256)
