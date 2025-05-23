from sample_processing import my_processing
from unittest.mock import patch
import unittest


class ExampleTest(unittest.TestCase):
    # @patch("sample_processing.ShoppingSiteAPI")
    def test_my_processing(self):
        # def test_my_processing(self, APIMock):
        with patch("sample_processing.ShoppingSiteAPI") as APIMock:
            api = APIMock()
            api.search_items.return_value = [
                "モック商品1",
                "モック商品2",
                "モック商品3",
            ]

            self.assertEqual(
                my_processing(), "モック商品1,モック商品2,モック商品3が見つかりました"
            )
        self.assertEqual(my_processing(), "商品1,商品2,商品3が見つかりました")
        # ↑ 上記構文はwith文の外なのでpatchが適用されない。


if __name__ == "__main__":
    unittest.main()
