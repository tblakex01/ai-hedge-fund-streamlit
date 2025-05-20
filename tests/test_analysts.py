import unittest
from importlib import reload


class TestAnalystOrderMap(unittest.TestCase):
    def test_order_map_matches_order(self):
        mod = reload(__import__("src.utils.analysts", fromlist=[""]))
        order_map = mod.ANALYST_ORDER_MAP
        for idx, (display, _) in enumerate(mod.ANALYST_ORDER):
            self.assertEqual(order_map[display], idx)
        self.assertEqual(order_map["Risk Management"], len(mod.ANALYST_ORDER))


if __name__ == "__main__":
    unittest.main()
