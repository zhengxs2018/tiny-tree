# tiny-tree

> 快速，轻量，无依赖的树结构数据处理函数库。

---

- 一个循环解决行转树的问题
- 除添加 **children** 属性外，不会修改任何数据
- 支持任意关系字段，如：非 **id**，**parentId**, **children** 字段支持
- 支持接管插入行为，如：自定义插入顺序
- 支持动态导出树节点

## 快速开始

### 文档

- [to_tree 行转树](./docs/to_tree.md)
- [to_rows 树转行](./docs/to_tows.md)

**注意**: 因为引入了 `typing` 模块，需要 `python>=3.6`。

### 安装

```shell
# 不支持 python2
$ pip3 install tiny-tree
```

### 使用

```python
from tiny_tree.to_tree import to_tree

to_tree([
  { "id": 10000, "parentId": None, "title": "标题 1" },
  { "id": 20000, "parentId": None, "title": "标题 2" },
  { "id": 11000, "parentId": 10000, "title": "标题 1-1" },
])
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

支持任意关系字段的数据

```python
from tiny_tree.to_tree import to_tree, ROOT_ID
from tiny_tree.helpers import sort_insert, add_property

data = [
  { "uid": 10000, "pid": None, "title": "标题 1", "sort": 1 },
  { "uid": 20000, "pid": None, "title": "标题 2", "sort": 2 },
  { "uid": 11000, "pid": 10000, "title": "标题 1-1", "sort": 3 },
]

tree = to_tree(
  data,
  # 如果 parentId 为 None
  # 使用 ROOT_ID 作为 key 保存
  # 支持函数，动态返回
  root=ROOT_ID,

  # 默认: id
  id_key="uid",

  # 默认：parentId
  parent_key="pid",

  # 挂载子级的属性名称，默认：children
  child_key="items",

  # 数据预处理，接收一个自定义函数
  # 可以在这里操作行数据，返回 None 将被跳过
  transform=add_property('checked', False),

  # 接管插入行为
  # 接收一个自定义函数
  insert=sort_insert('sort')
)

print(tree)
# output:
# [
#   {
#     "uid": 10000,
#     "pid": None,
#     "title": '标题 1',
#     "sort": 1,
#     "checked": false,
#     "items": [
#       { "uid": 11000, "pid": 10000, "title": '标题 1-1', "sort": 3, "checked": false, "items": [] }
#     ]
#   },
#   { "uid": 20000, "pid": None, "title": '标题 2', "sort": 2, "checked": false, "items": [] }
# ]
```

## 本地开发

### 安装打包工具

```bash
# 安装 build 模块
$ python3 -m pip install build

# 安装 twine 包
$ python3 -m pip install twine
```

### 启动开发模式

```bash
# 启动开发模式
# See https://packaging.python.org/guides/distributing-packages-using-setuptools/#id68
$ python3 -m pip install -e . --no-deps

# 代码打包
$ python3 -m build --wheel

# 检查发布内容
$ twine check dist/*

# 发布正式包，需要 pypi 账号
$ twine upload dist/*

# 发布测试包，需要 pypi 账号
$ twine upload --repository testpypi dist/*
```

## 相关推荐

- [js.tree](https://github.com/zhengxs2018/js.tree)

## License

- MIT
