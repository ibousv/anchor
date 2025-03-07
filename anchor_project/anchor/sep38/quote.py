
from typing import List, Dict, Optional, Union
from decimal import Decimal
from rest_framework.request import Request
from polaris.models import Asset, OffChainAsset, DeliveryMethod, Quote
from polaris.integrations import QuoteIntegration
from polaris.sep10.token import SEP10Token


class AnchorQuote(QuoteIntegration):
    def get_prices(
        self,
        token: SEP10Token,
        request: Request,
        sell_asset: Union[Asset, OffChainAsset],
        sell_amount: Decimal,
        buy_assets: List[Union[Asset, OffChainAsset]],
        sell_delivery_method: Optional[DeliveryMethod] = None,
        buy_delivery_method: Optional[DeliveryMethod] = None,
        country_code: Optional[str] = None,
        *args,
        **kwargs,
    ) -> List[Decimal]:
        prices = []
        for buy_asset in buy_assets:
            try:
                prices.append(
                    get_estimated_rate(
                        sell_asset,
                        buy_asset,
                        sell_amount=sell_amount
                    )
                )
            except RequestException:
                raise RuntimeError("unable to fetch prices")
        return prices

    def get_price(
        self,
        token: SEP10Token,
        request: Request,
        sell_asset: Union[Asset, OffChainAsset],
        buy_asset: Union[Asset, OffChainAsset],
        buy_amount: Optional[Decimal] = None,
        sell_amount: Optional[Decimal] = None,
        sell_delivery_method: Optional[DeliveryMethod] = None,
        buy_delivery_method: Optional[DeliveryMethod] = None,
        country_code: Optional[str] = None,
        *args,
        **kwargs,
    ) -> Decimal:
        try:
            return get_estimated_rate(
                sell_asset,
                buy_asset,
                sell_amount=sell_amount,
                buy_amount=buy_amount
            )
        except RequestException:
            raise RuntimeError("unable to fetch price")

    def post_quote(self, token: SEP10Token, request: Request, quote: Quote, *args, **kwargs) -> Quote:
        # fee computation
        sell_amount = quote.sell_amount
        fee = sell_amount * Decimal('0.01')
        effective_sell_amount = sell_amount - fee
        # Obtain the exchange rate
        exchange_rate = self.get_current_exchange_rate(
            quote.sell_asset, quote.buy_asset)
        # Calculate buy amount based on effective sell amount and rate
        buy_amount = effective_sell_amount * exchange_rate

        quote.price = exchange_rate
        quote.fee = fee
        quote.sell_amount = sell_amount
        quote.buy_amount = buy_amount
        quote.expires_at = self.calculate_expiration()

        return quote
