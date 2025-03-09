from polaris.integrations import SEP31ReceiverIntegration
from polaris.sep10.token import SEP10Token
from polaris.models import Transaction, Asset
from rest_framework.request import Request
from typing import Dict, List


class AnchorCrossBorderPayment(SEP31ReceiverIntegration):

    def process_post_request(
        self,
        token: SEP10Token,
        request: Request,
        params: Dict,
        transaction: Transaction,
        *args: List,
        **kwargs: Dict,
    ):


        try:
                
            asset = Asset.objects.get(code=params['asset_code'])
            
            # fee = # deduce from quote_id
            # Send fee to anchor's main account via Stellar transaction
            # fee transaction
            stellar_server = Server(horizon_url=env.HORIZON_URI)
               
            fee_transaction = (
                TransactionBuilder(
                    source_account=source_keypair.public_key,
                    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
                    base_fee=100,
                    )
                    .append_payment_op(
                        destination=anchor_keypair.public_key,
                        amount=str(fee),
                        asset_code=asset.code,
                        asset_issuer=asset.issuer,
                    )
                    .set_timeout(30)
                    .build()
                )
                
            fee_transaction.sign(source_keypair)
            fee_transaction_envelope = fee_transaction.to_xdr()
                
               
            response = stellar_server.submit_transaction(fee_transaction_envelope)
            if response.get('hash') is None:
                return {"error": "Fee transaction failed"}
                
            # Process the main payment
            # Between the source and desination accounts
            return {}
                
        except Exception as e:
            return {"error": str(e)}