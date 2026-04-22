from __future__ import annotations

from typing import TYPE_CHECKING

from bt_api_base.balance_utils import simple_balance_handler

from bt_api_bigone.exchange_data import BigONEExchangeDataSpot
from bt_api_bigone.feeds.live_bigone.spot import BigONERequestDataSpot

if TYPE_CHECKING:
    from bt_api_base.registry import ExchangeRegistry


def register_bigone(registry: ExchangeRegistry) -> None:
    registry.register_feed("BIGONE___SPOT", BigONERequestDataSpot)
    registry.register_exchange_data("BIGONE___SPOT", BigONEExchangeDataSpot)
    registry.register_balance_handler("BIGONE___SPOT", simple_balance_handler)
