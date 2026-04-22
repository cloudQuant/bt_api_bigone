from __future__ import annotations

from typing import TYPE_CHECKING, Any

from bt_api_base.plugins.protocol import PluginInfo

from bt_api_bigone import __version__
from bt_api_bigone.registry_registration import register_bigone

if TYPE_CHECKING:
    from bt_api_base.registry import ExchangeRegistry


def register_plugin(registry: ExchangeRegistry, runtime_factory: Any) -> PluginInfo:
    register_bigone(registry)
    return PluginInfo(
        name="bt_api_bigone",
        version=__version__,
        core_requires=">=0.15,<1.0",
        supported_exchanges=("BIGONE___SPOT",),
        supported_asset_types=("SPOT",),
    )
