import sys
import types
import unittest
from unittest import mock

# Provide dummy modules for optional dependencies
sys.modules.setdefault("pandas", mock.MagicMock())
sys.modules.setdefault("requests", mock.MagicMock())

import src.tools.api as api


class TestMarketCap(unittest.TestCase):
    def test_get_market_cap(self):
        dummy_metric = types.SimpleNamespace(market_cap=123.0)
        with mock.patch.object(api, "get_financial_metrics", return_value=[dummy_metric]):
            result = api.get_market_cap("AAPL", "2024-01-01")
        self.assertEqual(result, 123.0)


if __name__ == "__main__":
    unittest.main()
