import os
import sys
import unittest
from unittest import mock

# Provide dummy modules for optional dependencies
sys.modules.setdefault("pandas", mock.MagicMock())
sys.modules.setdefault("requests", mock.MagicMock())

import src.tools.api as api

class TestAPIUtils(unittest.TestCase):
    def test_get_api_headers_with_key(self):
        with mock.patch.dict(os.environ, {"FINANCIAL_DATASETS_API_KEY": "abc"}):
            self.assertEqual(api._get_api_headers(), {"X-API-KEY": "abc"})

    def test_get_api_headers_without_key(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(api._get_api_headers(), {})

    def test_get_prices_uses_session(self):
        with mock.patch.object(api, "session") as mock_session:
            mock_session.get.return_value.status_code = 200
            mock_session.get.return_value.json.return_value = {"ticker": "AAPL", "prices": []}
            with mock.patch.dict(os.environ, {"FINANCIAL_DATASETS_API_KEY": "k"}):
                api.get_prices("AAPL", "2020-01-01", "2020-02-01")
            mock_session.get.assert_called_once()
            args, kwargs = mock_session.get.call_args
            self.assertIn("timeout", kwargs)
            self.assertEqual(kwargs["headers"], {"X-API-KEY": "k"})

if __name__ == "__main__":
    unittest.main()
