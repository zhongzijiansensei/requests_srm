# import re
# str = 'a9079fec2-38e8-48ae-87e6-1f42dd9fae90b'
# r=re.search("a(.+?)b", str)
# print (r.group())
import jsonpath
r = {
    "store": {
        "book": [
            {
                "category": "reference",
                "author": "NigelRees",
                "title": "SayingsoftheCentury",
                "price": 8.95
            },
            {
                "category": "fiction",
                "author": "EvelynWaugh",
                "title": "SwordofHonour",
                "price": 12.99
            },
            {
                "category": "fiction",
                "author": "HermanMelville",
                "title": "MobyDick",
                "isbn": "0-553-21311-3",
                "price": 8.99
            },
            {
                "category": "fiction",
                "author": "J.R.R.Tolkien",
                "title": "TheLordoftheRings",
                "isbn": "0-395-19395-8",
                "price": 22.99
            }
        ],
        "bicycle": {
            "color": "red",
            "price": 19.95
        }
    },
    "expensive": 10
}
k = jsonpath.jsonpath(r, "$.store.book[?(@.price < 10)].price")
print(k)