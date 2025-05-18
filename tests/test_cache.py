import unittest

from src.data.cache import Cache


class TestCache(unittest.TestCase):
    def test_merge_data_no_existing(self):
        cache = Cache()
        new_data = [{"id": 1}, {"id": 2}]
        merged = cache._merge_data(None, new_data, "id")
        self.assertEqual(merged, new_data)

    def test_merge_data_with_duplicates(self):
        cache = Cache()
        existing = [{"id": 1}, {"id": 2}]
        new_data = [{"id": 2}, {"id": 3}]
        merged = cache._merge_data(existing, new_data, "id")
        self.assertEqual(merged, [{"id": 1}, {"id": 2}, {"id": 3}])

    def test_set_get_prices_merges(self):
        cache = Cache()
        cache.set_prices("AAPL", [{"time": "2024-01-01", "p": 1}])
        # Duplicate date should not be added twice
        cache.set_prices("AAPL", [
            {"time": "2024-01-01", "p": 1},
            {"time": "2024-01-02", "p": 2},
        ])
        prices = cache.get_prices("AAPL")
        self.assertEqual(len(prices), 2)
        self.assertEqual(prices[1]["time"], "2024-01-02")


if __name__ == "__main__":
    unittest.main()
