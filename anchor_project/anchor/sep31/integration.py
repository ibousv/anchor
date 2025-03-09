from polaris.integrations import SEP31ReceiverIntegration
from polaris.sep10.token import SEP10Token
from polaris.models import Transaction, Asset, Quote
from rest_framework.request import Request
from typing import Dict, List
from dotenv import load_dotenv

class AnchorCrossBorderPayment(SEP31ReceiverIntegration):

    load_dotenv()
    
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
            # user_for_id method
            # verify if the user exists via the sep12 endpoint 
            # GET /customer?id=<customer-id>&type=<customer-type>
            # But those params remains optional
            sending_user = user_for_id(params.get("sender_id"))
            receiving_user = user_for_id(params.get("receiver_id"))

            asset = Asset.objects.get(code=params['asset_code'])
            if asset is None:
                return {"error": "Asset not found"}

            stellar_server = Server(horizon_url=os.environ.get("HORIZON_URI"))
            anchor_keypair = Keypair.from_secret(os.environ.get("ANCHOR_SEED"))
            source_keypair = Keypair.from_public_key(sending_user["account"])
            destination_keypair = Keypair.from_public_key(receiving_user["account"])
      
            # fee from quote_id
            quote_id = params.get("quote_id")
            quote = Quote.objects.get(id=quote_id)
            fee = quote.fee
            if fee is None:
                return {"error": f"Fee not found for the given quote id : {quote_id} "}

            # Send fee to anchor's main account via payment transaction
            fee_transaction = (
                TransactionBuilder(
                    source_account=source_keypair.public_key,
                    network_passphrase=os.environ.get("STELLAR_NETWORK_PASSPHRASE"),
                    base_fee=100,
                    )
                    .append_payment_op(
                        destination=anchor_keypair.public_key,
                        amount=str(fee),
                        asset_code=asset.code,
                        asset_issuer=asset.issuer,
                    )
                    .set_timeout(180)
                    .build()
                )
                
            fee_transaction.sign(source_keypair)
            fee_transaction_envelope = fee_transaction.to_xdr()
                
            response = stellar_server.submit_transaction(fee_transaction_envelope)
            if response.get('hash') is None:
                return {"error": "Fee transaction failed"}

            #update transaction status
            transaction.status = Transaction.STATUS.completed
            transaction.amount_fee = fee
            transaction.save()


            # Process the main payment transaction
            # Between the source and desination accounts
            # the effective amount we will send after the fee deduction
            effective_sell_amount = params['amount'] - fee
            main_transaction = (
                TransactionBuilder(
                    source_account=source_keypair.public_key,
                    network_passphrase=os.environ.get("STELLAR_NETWORK_PASSPHRASE"),
                    base_fee=100,
                    )
                    .append_payment_op(
                        destination=destination_keypair.public_key,
                        amount=str(effective_sell_amount),
                        asset_code=asset.code,
                        asset_issuer=asset.issuer,
                    )
                    .set_timeout(180)
                    .build()
                )

            main_transaction.sign(source_keypair)
            main_transaction_envelope = main_transaction.to_xdr()
            response = stellar_server.submit_transaction(main_transaction_envelope)
            if response.get('hash') is None:
                return {"error": "Main transaction failed"}
                # Rollback fee transaction
                # Send fee back to source account if the trnsaction failed
                fee_transaction = (
                    TransactionBuilder(
                        source_account=anchor_keypair.public_key,
                        network_passphrase=os.environ.get("STELLAR_NETWORK_PASSPHRASE"),
                        base_fee=100,
                        )
                        .append_payment_op(
                            destination=source_keypair.public_key,
                            amount=str(fee),
                            asset_code=asset.code,
                            asset_issuer=asset.issuer,
                        )
                        .set_timeout(180)
                        .build()
                )
                fee_transaction.sign(anchor_keypair)
            

            # Update transaction status
            transaction.status = Transaction.STATUS.completed
            transaction.amount_in = params['amount']
            transaction.amount_fee = fee
            transaction.amount_out = amount_after_fee
            transaction.save()

            return {}
                
        except Exception as e:
            return {"error": str(e)}