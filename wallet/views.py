import json
import os
from datetime import datetime

import requests
from dotenv import load_dotenv, find_dotenv
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from web3 import Web3

from wallet.models import WalletDetailDump
from wallet.serializers import (
    WalletSerializer,
    SendTransactionSerializer,
    TransactionSerializer,
)

load_dotenv(find_dotenv())

PROVIDER_HTTP_ENDPOINT = (
    f"https://sepolia.infura.io/v3/{os.environ.get('PROVIDER_API_KEY')}"
)
etherscan_api_key = os.environ.get("ETHERSCAN_API_KEY")

w3 = Web3(Web3.HTTPProvider(PROVIDER_HTTP_ENDPOINT))


class WalletViewSet(viewsets.ModelViewSet):
    queryset = WalletDetailDump.objects.all()
    serializer_class = WalletSerializer

    def get_serializer_class(self):
        if self.action == "send_found":
            return SendTransactionSerializer
        if self.action == "transaction_detail":
            return TransactionSerializer
        return WalletSerializer

    @action(url_path="send", detail=True, methods=["post"])
    def send_found(self, request, pk):
        wallet = WalletDetailDump.objects.get(id=pk)
        serializer = self.get_serializer(wallet, data=request.data)

        if serializer.is_valid():
            account_1 = wallet.public_address_key()
            private_key1 = wallet.private_key
            account_2 = request.data["address_to"]

            # get the nonce.  Prevents one from sending the transaction twice
            nonce = w3.eth.getTransactionCount(account_1)
            print(w3.toWei(request.data["value"], "ether"))

            # build a transaction in a dictionary
            tx = {
                "nonce": nonce,
                "to": account_2,
                "value": w3.toWei(request.data["value"], "ether"),
                "gas": 21000,
                "gasPrice": w3.toWei("50", "gwei"),
            }

            # sign the transaction
            signed_tx = w3.eth.account.sign_transaction(tx, private_key1)

            # send transaction
            w3.eth.sendRawTransaction(signed_tx.rawTransaction)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "amount",
                type=OpenApiTypes.INT,
                description="Filter by amount (ex. ?amount=210000000)",
            ),
            OpenApiParameter(
                "address",
                type=OpenApiTypes.STR,
                description="Filter by address (ex. ?address=0x6B624FA8af3497501876cCDC259ABA1CC81E371C)",
            ),
        ]
    )
    @action(url_path="transactions", detail=True, methods=["get"])
    def transaction_detail(self, request, pk):

        wallet = WalletDetailDump.objects.get(id=pk)
        transactions = []

        amount = self.request.query_params.get("amount")
        address_to = self.request.query_params.get("address")

        url = (
            "https://api-sepolia.etherscan.io/api"
            "?module=account"
            "&action=txlist"
            f"&address={wallet.public_address_key()}"
            "&startblock=0"
            "&endblock=99999999"
            "&page=1"
            "&offset=10"
            "&sort=asc"
            f"&apikey={etherscan_api_key}"
        )
        response = requests.get(url=url)

        for transaction_data in json.loads(response.text)["result"]:

            transaction_data["wallet_from"] = transaction_data["from"]
            transaction_data["timeStamp"] = datetime.fromtimestamp(
                int(transaction_data["timeStamp"])
            )

            if amount:
                if transaction_data["value"] == amount:
                    transactions.append(transaction_data)

            if address_to:
                if transaction_data["to"] == address_to:
                    transactions.append(transaction_data)

            if request.query_params == {}:
                transactions.append(transaction_data)

        results = TransactionSerializer(transactions, many=True).data
        return Response(results)
