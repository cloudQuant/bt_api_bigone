from bt_api_base.error import ErrorTranslator, UnifiedErrorCode


class BigONEErrorTranslator(ErrorTranslator):
    ERROR_MAP = {
        "INVALID_TOKEN": (UnifiedErrorCode.INVALID_API_KEY, "Invalid or expired token"),
        "TOKEN_EXPIRED": (UnifiedErrorCode.SESSION_EXPIRED, "Token has expired"),
        "INVALID_API_KEY": (UnifiedErrorCode.INVALID_API_KEY, "Invalid API key"),
        "INVALID_SIGNATURE": (UnifiedErrorCode.INVALID_SIGNATURE, "Signature verification failed"),
        "PERMISSION_DENIED": (UnifiedErrorCode.PERMISSION_DENIED, "Insufficient permissions"),
        "RATE_LIMIT_EXCEEDED": (UnifiedErrorCode.RATE_LIMIT_EXCEEDED, "Rate limit exceeded"),
        "INVALID_PARAMETER": (UnifiedErrorCode.INVALID_PARAMETER, "Invalid parameter"),
        "MISSING_PARAMETER": (UnifiedErrorCode.MISSING_PARAMETER, "Missing required parameter"),
        "INVALID_ASSET_PAIR": (UnifiedErrorCode.INVALID_SYMBOL, "Invalid trading pair"),
        "INSUFFICIENT_BALANCE": (UnifiedErrorCode.INSUFFICIENT_BALANCE, "Insufficient balance"),
        "ORDER_NOT_FOUND": (UnifiedErrorCode.ORDER_NOT_FOUND, "Order not found"),
        "ORDER_FILLED": (UnifiedErrorCode.ORDER_ALREADY_FILLED, "Order already filled"),
        "MARKET_CLOSED": (UnifiedErrorCode.MARKET_CLOSED, "Market is closed"),
    }


__all__ = ["BigONEErrorTranslator"]
