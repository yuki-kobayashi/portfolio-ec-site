class ShoppingSiteAPI:

    def search_items(self, name):
        return ["商品1", "商品2", "商品3"]

    def purchase(self, item_id):
        pass


def my_processing():
    api = ShoppingSiteAPI()
    return ",".join(api.search_items("商品")) + "が見つかりました"


if __name__ == "__main__":
    print(my_processing())
