import json

from django.db import transaction
from rest_framework import serializers

from wallet.main import create_new_hd_wallet
from wallet.models import WalletDetailDump, Addresses


class AddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addresses
        fields = "__all__"


class WalletSerializer(serializers.ModelSerializer):
    balance = serializers.ReadOnlyField()
    public_key = serializers.ReadOnlyField(source="public_address_key")

    class Meta:
        model = WalletDetailDump
        fields = ("id", "cryptocurrency", "network", "public_key", "balance")
        read_only_fields = ("id", "cryptocurrency", "network", "public_key", "balance")

    def create(self, validated_data):
        with transaction.atomic():
            new_wallet = json.loads(create_new_hd_wallet())
            addresses = new_wallet["addresses"]
            del new_wallet["addresses"]
            wallet = WalletDetailDump.objects.create(**new_wallet)
            Addresses.objects.create(**addresses, wallet=wallet)
            return wallet


class SendTransactionSerializer(WalletSerializer):
    public_key = serializers.ReadOnlyField(source="public_address_key")
    address_to = serializers.CharField()
    value = serializers.DecimalField(max_digits=10, decimal_places=8)

    class Meta:
        model = WalletDetailDump
        fields = (
            "public_key",
            "address_to",
            "value",
        )


class TransactionSerializer(serializers.Serializer):

    blockNumber = serializers.IntegerField()
    timeStamp = serializers.DateTimeField()
    hash = serializers.CharField(max_length=256)
    nonce = serializers.IntegerField()
    blockHash = serializers.CharField(max_length=256)
    transactionIndex = serializers.IntegerField()
    wallet_from = serializers.CharField(max_length=256)
    to = serializers.CharField(max_length=256)
    value = serializers.IntegerField()
    gas = serializers.IntegerField()
    gasPrice = serializers.IntegerField()
    isError = serializers.IntegerField()
    txreceipt_status = serializers.IntegerField()
    input = serializers.CharField(max_length=256)
    contractAddress = serializers.CharField(max_length=256, allow_null=True)
    cumulativeGasUsed = serializers.IntegerField()
    gasUsed = serializers.IntegerField()
    confirmations = serializers.IntegerField()
    methodId = serializers.CharField(max_length=256)
    functionName = serializers.CharField(max_length=256, allow_null=True)
