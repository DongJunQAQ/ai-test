from function_calling.amap import get_location, nearby_search


def test_get_location():
    print(get_location("0000000", "宜昌"))
    print(get_location("宜昌东站", "宜昌"))


def test_nearby_search():
    print(nearby_search("111.370163,30.658286", "麦当劳"))
    print(nearby_search("111.370163,30.658286", "星巴克"))
    print(nearby_search("111.370163,30.658286", "蜜雪冰城"))


test_get_location()
print()
test_nearby_search()
