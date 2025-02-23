from decimal import Decimal
from django import forms
from rest_framework.request import Request
from anchor.models import Transaction
from polaris.templates import Template
from polaris.integrations import (
    DepositIntegration,
    TransactionForm
)
from anchor.services.users import user_for_account, create_user
from anchor.forms import ContactForm, AddressForm

class AnchorDeposit(DepositIntegration):
    def form_for_transaction(
        self, request: Request, transaction: Transaction,
        post_data: dict = None, amount: Decimal = None, *args, **kwargs
    ):
        if not transaction.amount_in:
            return TransactionForm(transaction, post_data) if post_data else TransactionForm(transaction, initial={"amount": amount})

        user = user_for_account(transaction.stellar_account)
        if not user:
            return ContactForm(post_data) if post_data else ContactForm()
        elif not user.full_address:
            return AddressForm(post_data) if post_data else AddressForm()
        else:
            return None

    def after_form_validation(self, request: Request, form: forms.Form, transaction: Transaction, *args, **kwargs):
        if isinstance(form, TransactionForm):
            return
        if isinstance(form, ContactForm):
            create_user(form)
        elif isinstance(form, AddressForm):
            user = user_for_account(transaction.stellar_account)
            user.full_address = form.cleaned_data
            user.save()

    def content_for_template(self, request: Request, template: Template, form: forms.Form = None, transaction: Transaction = None, *args, **kwargs):
        return {"icon_label": "Anchor Inc."} if form or template == Template.MORE_INFO else None
