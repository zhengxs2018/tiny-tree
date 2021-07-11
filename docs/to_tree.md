# to_tree 行转树

`array` 和 `tree` 在程序开发中是常见的两种数据结构，它们之间的转换也很普遍。

`tree` 对人友好，但对存储和查找不太友好，所以一般在使用的时候转成 `array`，在使用时再转成 `tree`。

toTree 的默认行为如下：

- 默认 `id` 作为节点的唯一关系列。
- 默认 `parentId` 作为上级关系列。
- 如果 `parentId` 是 `None` 或 `undefined`，将被认为是一级节点。
- 除 `children` 属性外 (**会改变原始数据**)，不修改任何内容。

**注:** 以上行为都可以通过传递参数改变。

## 默认

```python
from tiny_tree.to_tree import to_tree

data = [
  { "id": 10000, "parentId": None, "title": "标题 1" },
  { "id": 20000, "parentId": None, "title": "标题 2" },
  { "id": 11000, "parentId": 10000, "title": "标题 1-1" },
]

print(to_tree(data))
# [
#   {
#     "id": 10000,
#     "parentId": None,
#     "title": '标题 1',
#     "children": [
#       { "id": 11000, "parentId": 10000, "title": '标题 1-1', "children": [] }
#     ]
#   },
#   { "id": 20000, "parentId": None, "title": '标题 2', "children": [] },
# ]
```

## 自定义导出内容

通过 `root` 参数指定一级节点。

```python
from tiny_tree.to_tree import to_tree

data = [
  { "id": 10000, "parentId": 0, "title": "标题 1" },
  { "id": 20000, "parentId": 0, "title": "标题 2" },
  { "id": 11000, "parentId": 10000, "title": "标题 1-1" },
]

print(to_tree(data, root = 0))
# [
#   {
#     "id": 10000,
#     "parentId": 0,
#     "title": '标题 1',
#     "children": [
#       { "id": 11000, "parentId": 10000, "title": '标题 1-1', "children": [] }
#     ]
#   },
#   { "id": 20000, "parentId": 0, "title": '标题 2', "children": [] },
# ]
```

有时候可能不确定那个，这时可以传递函数动态判断

```python
from tiny_tree.to_tree import to_tree

data = [
  { "id": 1, "parentId": 'aa' },
  { "id": 2, "parentId": 'aa' },
  { "id": 3, "parentId": 1 },
]

print(to_tree(data, root = lambda result: result['aa']))
```

## 自定义关系

不同的场景和不同的使用对象，都会导致数据结构存在很大的差异，这时可以手动指定关系列。

```python
from tiny_tree.to_tree import to_tree

data = [
  { "sid": 1, "pid": None },
  { "sid": 2, "pid": None },
  { "sid": 3, "pid": 1 },
]

print(to_tree(data, id_key = 'sid', parent_key = 'pid', child_key = 'items'))
```

## 转换数据

如果需要将数据转成其他结构，可以使用 `transform` 参数。

```python
from tiny_tree.to_tree import to_tree

data = [
  { "id": 2, "parentId": None },
  { "id": 3, "parentId": 1 },
  { "id": 1, "parentId": None },
]

def transform(row, index):
  # 如果需要过滤数据，就返回 None
  # 返回 None 的数据会被过滤掉
  if row['id'] == 3:
    return None

  # 浅拷贝
  data = row.copy()

  # 设置默认值
  data.setdefault('checked', False)

  return data

print(to_tree(data, transform=transform))
# [
#   { "id": 1, "parentId": None, "checked": False, "children": [] },
#   { "id": 2, "parentId": None, "checked": False, "children": [] }
# ]
```

**注:** 修改会导致原始对象也被改变

## 根据父级处理子级

很多时候可能需要操作子级，但插件循环的时候是不知道有多少个子级的，只有处理完才知道。

```python
from tiny_tree.to_tree import to_tree

data = [
  { "id": 1, "parentId": None },
  { "id": 2, "parentId": None }
]

# 需要后处理的数据
post_data = []

def transform(row, index):
  if row['id'] == 2:
    # 因为对象的引用
    # 可以直接保存返回的数据
    # 修改这个对象，也会改变结果的内容
    post_data.append(row)

  return row

result = to_tree(data, transform = transform)

# 处理后续数据
for node in post_data:
  node.setdefault('hidden', True)

# 打印结果
print(result)
# ->
# [
#   { "id": 1, "parentId": None, "children": [] },
#   { "id": 2, "parentId": None, hidden: True, "children": [] }
# ]
```

## 排序

> 配置 `insert` 后，内部不再做插入操作。

默认不会进行任何排序操作，可以使用 `insert` 自定义插入位置。

```python
from tiny_tree.to_tree import to_tree
from tiny_tree.helpers import sort_insert

data = [
  { "id": 20000, "parentId": None, "sort": 1 },
  { "id": 10000, "parentId": None, "sort": 0 },
  { "id": 30000, "parentId": None, "sort": 2 },
]

print(to_tree(data, insert = sort_insert('sort')))
# ->
# [
#   { "id": 10000, "parentId": None, "sort": 0, "children": [] },
#   { "id": 20000, "parentId": None, "sort": 1, "children": [] },
#   { "id": 30000, "parentId": None, "sort": 2, "children": [] }
# ]
```

自定义

```python
from tiny_tree.to_tree import to_tree
from tiny_tree.util import find_index

data = [
  { "id": 20000, "parentId": None, "sort": 1 },
  { "id": 10000, "parentId": None, "sort": 0 },
  { "id": 30000, "parentId": None, "sort": 2 },
]

def sort_insert(siblings: List[dict], node: dict) -> None:
  index = find_index(siblings, lambda row, *_: node['sort'] - row['sort'])
  if index == -1:
    siblings.append(node)
  else:
    siblings.insert(index, node)

print(to_tree(data, insert = sort_insert))
```
