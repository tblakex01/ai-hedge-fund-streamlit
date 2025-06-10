import importlib
import sys
import types
import unittest
from unittest import mock


class TestDisplayUtils(unittest.TestCase):
    def setUp(self):
        # Create fake colorama module
        fore = types.SimpleNamespace(GREEN="GREEN", RED="RED", YELLOW="YELLOW", WHITE="WHITE", CYAN="CYAN", BLUE="BLUE")
        style = types.SimpleNamespace(BRIGHT="BRIGHT", RESET_ALL="RESET")
        fake_colorama = types.SimpleNamespace(Fore=fore, Style=style)
        fake_tabulate = lambda *args, **kwargs: "table"
        fake_tabulate_mod = types.SimpleNamespace(tabulate=fake_tabulate)
        fake_analysts = types.SimpleNamespace(
            ANALYST_ORDER=[("Ben Graham", "bg"), ("Bill Ackman", "ba")],
            ANALYST_ORDER_MAP={"Ben Graham": 0, "Bill Ackman": 1, "Risk Management": 2},
        )
        self.patches = [
            mock.patch.dict(
                sys.modules,
                {
                    "colorama": fake_colorama,
                    "tabulate": fake_tabulate_mod,
                    "src.utils.analysts": fake_analysts,
                },
            )
        ]
        for p in self.patches:
            p.start()
        self.display = importlib.import_module("src.utils.display")

    def tearDown(self):
        for p in self.patches:
            p.stop()
        if "src.utils.display" in sys.modules:
            del sys.modules["src.utils.display"]

    def test_sort_agent_signals(self):
        signals = [
            ["Bill Ackman", "", "", ""],
            ["Ben Graham", "", "", ""],
        ]
        sorted_signals = self.display.sort_agent_signals(signals)
        self.assertEqual(sorted_signals[0][0], "Ben Graham")

    def test_sort_agent_signals_unknown(self):
        signals = [
            ["Unknown Analyst", "", "", ""],
            ["Ben Graham", "", "", ""],
        ]
        sorted_signals = self.display.sort_agent_signals(signals)
        # Known analyst should come first
        self.assertEqual(sorted_signals[0][0], "Ben Graham")
        # Unknown analyst falls back to end
        self.assertEqual(sorted_signals[1][0], "Unknown Analyst")

    def test_format_backtest_row(self):
        row = self.display.format_backtest_row("2024-01-01", "AAPL", "BUY", 10, 1.0, 10, 10.0, 1, 0, 0)
        self.assertEqual(row[0], "2024-01-01")
        self.assertIn("AAPL", row[1])
        self.assertIn("BUY", row[2])

    def test_format_backtest_row_summary(self):
        row = self.display.format_backtest_row("2024-01-01", "", "HOLD", 0, 0, 0, 0, 0, 0, 0, is_summary=True, total_value=10, return_pct=1.0, cash_balance=5.0, total_position_value=5.0, sharpe_ratio=1.1, sortino_ratio=1.0, max_drawdown=0.5)
        self.assertIn("PORTFOLIO SUMMARY", row[1])
        self.assertEqual(row[-1], "RED0.50%RESET")

    def test_format_backtest_row_negative_return(self):
        row = self.display.format_backtest_row("2024-01-02", "", "SELL", 0, 0, 0, 0, 0, 0, 0, is_summary=True, total_value=10, return_pct=-1.0, cash_balance=5.0, total_position_value=5.0, sharpe_ratio=0.5, sortino_ratio=0.4, max_drawdown=0.2)
        self.assertIn("RED-1.00%RESET", row[9])


if __name__ == "__main__":
    unittest.main()
