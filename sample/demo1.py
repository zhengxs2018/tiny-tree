from tiny_tree.to_tree import to_tree

data = [
  { "id": 10000, "parentId": None, "title": "标题 1" },
  { "id": 20000, "parentId": None, "title": "标题 2" },
  { "id": 11000, "parentId": 10000, "title": "标题 1-1" },
]

print(to_tree(data))
