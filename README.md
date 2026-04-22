# bt_api_bigone

[![PyPI Version](https://img.shields.io/pypi/v/bt_api_bigone.svg)](https://pypi.org/project/bt_api_bigone/)
[![Python Versions](https://img.shields.io/pypi/pyversions/bt_api_bigone.svg)](https://pypi.org/project/bt_api_bigone/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/cloudQuant/bt_api_bigone/actions/workflows/ci.yml/badge.svg)](https://github.com/cloudQuant/bt_api_bigone/actions)
[![Docs](https://readthedocs.org/projects/bt-api-bigone/badge/?version=latest)](https://bt-api-bigone.readthedocs.io/)

---

<!-- English -->
# bt_api_bigone

> **BigONE exchange plugin for bt_api** — Unified REST API for **Spot** trading.

`bt_api_bigone` is a runtime plugin for [bt_api](https://github.com/cloudQuant/bt_api_py) that connects to **BigONE** exchange. It depends on [bt_api_base](https://github.com/cloudQuant/bt_api_base) for core infrastructure. It also ships `BigONERequestDataSpot` for **standalone use** without the full bt_api framework.

| Resource | Link |
|----------|------|
| English Docs | https://bt-api-bigone.readthedocs.io/ |
| Chinese Docs | https://bt-api-bigone.readthedocs.io/zh/latest/ |
| GitHub | https://github.com/cloudQuant/bt_api_bigone |
| PyPI | https://pypi.org/project/bt_api_bigone/ |
| Issues | https://github.com/cloudQuant/bt_api_bigone/issues |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| Main Project | https://github.com/cloudQuant/bt_api_py |

---

## Features

### 1 Asset Type

| Asset Type | Code | REST | Description |
|---|---|---|---|
| Spot | `BIGONE___SPOT` | ✅ | Spot trading |

### Dual API Modes

- **REST API** — Synchronous polling for order management, balance queries, historical data
- **Async REST API** — Async versions for all operations

### Plugin Architecture

Auto-registers at import time via `ExchangeRegistry`. Works seamlessly with `BtApi`:

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BIGONE___SPOT": {
        "api_key": "your_key",
        "secret": "your_secret",
    }
})

ticker = api.get_tick("BIGONE___SPOT", "BTC-USDT")
balance = api.get_balance("BIGONE___SPOT")
order = api.make_order(exchange_name="BIGONE___SPOT", symbol="BTC-USDT", volume=0.001, price=50000, order_type="limit")
```

### Standalone Use

```python
from bt_api_bigone import BigONERequestDataSpot

feed = BigONERequestDataSpot(
    api_key="your_api_key",
    secret_key="your_secret",
)

# Get ticker
ticker = feed.get_ticker("BTC-USDT")
print(ticker)

# Place order
order = feed.make_order("BTC-USDT", amount=0.001, price=50000, order_type="buy-limit")
print(order)

# Get balance
balance = feed.get_balance()
print(balance)
```

---

## Installation

### From PyPI (Recommended)

```bash
pip install bt_api_bigone
```

### From Source

```bash
git clone https://github.com/cloudQuant/bt_api_bigone
cd bt_api_bigone
pip install -e .
```

### Requirements

- Python `3.9` – `3.14`
- `bt_api_base >= 0.15`
- `PyJWT >= 1.7.1` for authentication
- `requests` for HTTP client

---

## Quick Start

### 1. Install

```bash
pip install bt_api_bigone
```

### 2. Get ticker (public — no API key needed)

```python
from bt_api_bigone import BigONERequestDataSpot

feed = BigONERequestDataSpot()
ticker = feed.get_ticker("BTC-USDT")
print(f"BTC-USDT price: {ticker}")
```

### 3. Place an order (requires API key)

```python
from bt_api_bigone import BigONERequestDataSpot

feed = BigONERequestDataSpot(
    api_key="your_api_key",
    secret_key="your_secret",
)

order = feed.make_order(
    symbol="BTC-USDT",
    amount=0.001,
    price=50000,
    order_type="buy-limit",
)
print(f"Order placed: {order}")
```

### 4. bt_api Plugin Integration

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BIGONE___SPOT": {
        "api_key": "your_key",
        "secret": "your_secret",
    }
})

# REST calls
ticker = api.get_tick("BIGONE___SPOT", "BTC-USDT")
balance = api.get_balance("BIGONE___SPOT")
```

---

## Architecture

```
bt_api_bigone/
├── src/bt_api_bigone/
│   ├── __init__.py
│   ├── plugin.py                     # register_plugin() — bt_api plugin entry point
│   ├── registry_registration.py     # register_bigone() — feeds registration
│   ├── exchange_data/
│   │   └── bigone_exchange_data.py # BigONEExchangeData — REST paths & symbol mapping
│   ├── feeds/live_bigone/
│   │   ├── __init__.py
│   │   ├── spot.py                  # BigONERequestDataSpot
│   │   └── request_base.py         # BigONERequestData — base class with all REST methods
│   └── errors/
│       └── bigone_translator.py    # (optional) BigONEErrorTranslator
└── configs/
    └── bigone.yaml                 # (optional) Full YAML config
```

---

## Supported Operations

| Category | Operation | Notes |
|---|---|---|
| **Market Data** | `get_ticker` / `get_tick` | 24hr rolling ticker |
| | `get_depth` | Order book depth |
| | `get_kline` | K-line/candlestick |
| | `get_trades` / `get_trade_history` | Recent trade history |
| **Account** | `get_balance` | Asset balances |
| | `get_account` | Full account info |
| | `get_open_orders` | All open orders |
| | `query_order` | Single order by ID |
| **Trading** | `make_order` | LIMIT/MARKET orders |
| | `cancel_order` | Cancel order by ID |
| **System** | `get_server_time` | Server time |
| | `get_exchange_info` | Exchange metadata |

---

## Supported BigONE Symbols

All BigONE trading pairs are supported, including:

- **Spot**: `BTC-USDT`, `ETH-USDT`, `SOL-USDT`, `XRP-USDT` ...

---

## Error Handling

All BigONE API errors are translated to bt_api_base `ApiError` subclasses via `BigONEErrorTranslator` (if implemented).

---

## Rate Limits

| Endpoint Category | Limit |
|---|---|
| Public endpoints | 100 requests / second |
| Trading endpoints | 50 requests / second |

---

## Documentation

| Doc | Link |
|-----|------|
| **English** | https://bt-api-bigone.readthedocs.io/ |
| **中文** | https://bt-api-bigone.readthedocs.io/zh/latest/ |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| Main Project | https://cloudquant.github.io/bt_api_py/ |

---

## License

MIT — see [LICENSE](LICENSE).

---

## Support

- [GitHub Issues](https://github.com/cloudQuant/bt_api_bigone/issues) — bug reports, feature requests
- Email: yunjinqi@gmail.com

---

---

## 中文

> **bt_api 的 BigONE 交易所插件** — 为**现货**交易提供统一的 REST API。

`bt_api_bigone` 是 [bt_api](https://github.com/cloudQuant/bt_api_py) 的运行时插件，连接 **BigONE** 交易所。依赖 [bt_api_base](https://github.com/cloudQuant/bt_api_base) 提供核心基础设施。同时提供 `BigONERequestDataSpot`，可**独立使用**无需完整 bt_api 框架。

| 资源 | 链接 |
|------|------|
| 英文文档 | https://bt-api-bigone.readthedocs.io/ |
| 中文文档 | https://bt-api-bigone.readthedocs.io/zh/latest/ |
| GitHub | https://github.com/cloudQuant/bt_api_bigone |
| PyPI | https://pypi.org/project/bt_api_bigone/ |
| 问题反馈 | https://github.com/cloudQuant/bt_api_bigone/issues |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| 主项目 | https://github.com/cloudQuant/bt_api_py |

---

## 功能特点

### 1 种资产类型

| 资产类型 | 代码 | REST | 说明 |
|---|---|---|---|
| 现货 | `BIGONE___SPOT` | ✅ | 现货交易 |

### 双 API 模式

- **REST API** — 同步轮询：订单管理、余额查询、历史数据
- **异步 REST API** — 所有操作的异步版本

### 插件架构

通过 `ExchangeRegistry` 在导入时自动注册，与 `BtApi` 无缝协作：

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BIGONE___SPOT": {
        "api_key": "your_key",
        "secret": "your_secret",
    }
})

ticker = api.get_tick("BIGONE___SPOT", "BTC-USDT")
balance = api.get_balance("BIGONE___SPOT")
order = api.make_order(exchange_name="BIGONE___SPOT", symbol="BTC-USDT", volume=0.001, price=50000, order_type="limit")
```

### 独立使用

```python
from bt_api_bigone import BigONERequestDataSpot

feed = BigONERequestDataSpot(
    api_key="your_api_key",
    secret_key="your_secret",
)

# 获取行情
ticker = feed.get_ticker("BTC-USDT")
print(ticker)

# 下单
order = feed.make_order("BTC-USDT", amount=0.001, price=50000, order_type="buy-limit")
print(order)

# 获取余额
balance = feed.get_balance()
print(balance)
```

---

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install bt_api_bigone
```

### 从源码安装

```bash
git clone https://github.com/cloudQuant/bt_api_bigone
cd bt_api_bigone
pip install -e .
```

### 系统要求

- Python `3.9` – `3.14`
- `bt_api_base >= 0.15`
- `PyJWT >= 1.7.1` 用于认证
- `requests` HTTP 客户端

---

## 快速开始

### 1. 安装

```bash
pip install bt_api_bigone
```

### 2. 获取行情（公开接口，无需 API key）

```python
from bt_api_bigone import BigONERequestDataSpot

feed = BigONERequestDataSpot()
ticker = feed.get_ticker("BTC-USDT")
print(f"BTC-USDT 价格: {ticker}")
```

### 3. 下单交易（需要 API key）

```python
from bt_api_bigone import BigONERequestDataSpot

feed = BigONERequestDataSpot(
    api_key="your_api_key",
    secret_key="your_secret",
)

order = feed.make_order(
    symbol="BTC-USDT",
    amount=0.001,
    price=50000,
    order_type="buy-limit",
)
print(f"订单已下单: {order}")
```

### 4. bt_api 插件集成

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BIGONE___SPOT": {
        "api_key": "your_key",
        "secret": "your_secret",
    }
})

# REST 调用
ticker = api.get_tick("BIGONE___SPOT", "BTC-USDT")
balance = api.get_balance("BIGONE___SPOT")
```

---

## 架构

```
bt_api_bigone/
├── src/bt_api_bigone/
│   ├── __init__.py
│   ├── plugin.py                     # register_plugin() — bt_api 插件入口
│   ├── registry_registration.py     # register_bigone() — feeds 注册
│   ├── exchange_data/
│   │   └── bigone_exchange_data.py # BigONEExchangeData — REST 路径和交易对映射
│   ├── feeds/live_bigone/
│   │   ├── __init__.py
│   │   ├── spot.py                  # BigONERequestDataSpot
│   │   └── request_base.py         # BigONERequestData — 基类，包含所有 REST 方法
│   └── errors/
│       └── bigone_translator.py    # (可选) BigONEErrorTranslator
└── configs/
    └── bigone.yaml                 # (可选) 完整 YAML 配置
```

---

## 支持的操作

| 类别 | 操作 | 说明 |
|---|---|---|
| **行情数据** | `get_ticker` / `get_tick` | 24小时滚动行情 |
| | `get_depth` | 订单簿深度 |
| | `get_kline` | K线/蜡烛图 |
| | `get_trades` / `get_trade_history` | 近期成交历史 |
| **账户** | `get_balance` | 资产余额 |
| | `get_account` | 完整账户信息 |
| | `get_open_orders` | 所有挂单 |
| | `query_order` | 按ID查询单笔订单 |
| **交易** | `make_order` | 限价/市价订单 |
| | `cancel_order` | 按ID撤销订单 |
| **系统** | `get_server_time` | 服务器时间 |
| | `get_exchange_info` | 交易所元数据 |

---

## 支持的 BigONE 交易对

全部 BigONE 交易对均支持，包括：

- **现货**: `BTC-USDT`, `ETH-USDT`, `SOL-USDT`, `XRP-USDT` ...

---

## 错误处理

所有 BigONE API 错误均翻译为 bt_api_base `ApiError` 子类（如果实现了 `BigONEErrorTranslator`）。

---

## 限流配置

| 端点类别 | 限制 |
|---|---|
| 公开接口 | 100 请求 / 秒 |
| 交易接口 | 50 请求 / 秒 |

---

## 文档

| 文档 | 链接 |
|-----|------|
| **英文文档** | https://bt-api-bigone.readthedocs.io/ |
| **中文文档** | https://bt-api-bigone.readthedocs.io/zh/latest/ |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| 主项目 | https://cloudquant.github.io/bt_api_py/ |

---

## 许可证

MIT — 详见 [LICENSE](LICENSE)。

---

## 技术支持

- [GitHub Issues](https://github.com/cloudQuant/bt_api_bigone/issues) — bug 报告、功能请求
- 邮箱: yunjinqi@gmail.com