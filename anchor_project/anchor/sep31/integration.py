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

        # retrieve fee and send it to the anchor
        sending_user = user_for_id(params.get("sender_id"))
        receiving_user = user_for_id(params.get("receiver_id"))
        if not sending_user or not sending_user.kyc_approved:
            return {"error": "customer_info_needed", "type": "sep31-sender"}
        if not receiving_user or not receiving_user.kyc_approved:
            return {"error": "customer_info_needed", "type": "sep31-receiver"}
        transaction_fields = params.get("fields", {}).get("transaction")
        if not transaction_fields:
            return {
                "error": "transaction_info_needed",
                "fields": {
                    "transaction": {
                        "routing_number": {
                            "description": "routing number of the destination bank account"
                        },
                        "account_number": {
                            "description": "bank account number of the destination"
                        },
                    }
                }
            }
        try:
            verify_bank_account(
                transaction_fields.get("routing_number"),
                transaction_fields.get("account_number")
            )
        except ValueError:
            return {"error": "invalid routing or account number"}
        sending_user.add_transaction(transaction)
        receiving_user.add_transaction(transaction)


