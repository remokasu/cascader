# Cascader: 連結リストでスタックを表現するためのクラス

- 動作環境: Python >=3.10

<br>

# 使い方

## 初期化
``` python
data = Cascader(1)  # 1 で初期化
```
## push: 末尾に追加
``` python
data = data.push(2)  # 2 を末尾に追加
data = data.push(3)  # 3 を末尾に追加
# 1 -> 2 -> 3
```

## pop: 末尾を削除
``` python
data = Cascader(1)
data = data.push(2).push(3).push(4).push(5)
# 1 -> 2 -> 3 -> 4 -> 5
data = data.pop()  # 末尾を削除
# 1 -> 2 -> 3 -> 4
```

## swap: 末尾とその一つ前を入れ替え
``` python
data = Cascader(1)
data = data.push(2).push(3).push(4).push(5)
# 1 -> 2 -> 3 -> 4 -> 5
data = data.swap()  # 末尾とその一つ前を入れ替え
# 1　-> 2 -> 3 -> 5 -> 4
```

## dup: 末尾を複製して末尾に追加
``` python
data = Cascader(1)
data = data.push(2).push(3).push(4).push(5)
# 1 -> 2 -> 3 -> 4 -> 5
data = data.dup()  # 末尾を複製して末尾に追加
# 1 -> 2 -> 3 -> 4 -> 5 -> 5
```

## jump: 指定のindexに移動
``` python
data = Cascader(1)
data = data.push(2).push(3).push(4).push(5)
# 1 -> 2 -> 3 -> 4 -> 5
data = data.jump(2)  # 指定のindexに移動
# 1 -> 2 -> 3
```

## clone: 指定のindexの要素を複製して末尾に追加
``` python
data = Cascader(1)
data = data.push(2).push(3).push(4).push(5)
# 1 -> 2 -> 3 -> 4 -> 5
data = data.clone(3)  # 指定のindexの要素を複製して末尾に追加
# 1 -> 2 -> 3 -> 4 -> 5 -> 4
```

## reverse: 逆順
``` python
data = Cascader(1)
data = data.push(2).push(3).push(4).push(5)
# 1 -> 2 -> 3 -> 4 -> 5
data = data.reverse()  # 逆順
# 5 -> 4 -> 3 -> 2 -> 1
```

## pick: 指定のindexの要素を返す
``` python
data = Cascader(1)
data = data.push(2).push(3).push(4).push(5)
# 1 -> 2 -> 3 -> 4 -> 5
data = data.pick(3)  # 指定のindexの要素を返す
# 4
```

## pluck: 指定のindexの要素を削除して末尾に追加（=移動）
``` python
data = Cascader(1)
data = data.push(2).push(3).push(4).push(5)
# 1 -> 2 -> 3 -> 4 -> 5
data = data.pluck(3)  # 指定のindexの要素を削除して最後に追加（移動）
# 1 -> 2 -> 3 -> 5 -> 4
```

## insert: 指定のindexに要素を挿入
``` python
data = Cascader(1)
data = data.push(2).push(3).push(4).push(5)
# 1 -> 2 -> 3 -> 4 -> 5
data = data.insert(3, 10)  # 指定のindexに要素を挿入
# 1 -> 2 -> 3 -> 10 -> 4 -> 5
```

## remove: 指定のindexの要素を削除
``` python
data = Cascader(1)
data = data.push(2).push(3).push(4).push(5)
# 1 -> 2 -> 3 -> 4 -> 5
data = data.remove(3)  # 指定のindexの要素を削除
# 1 -> 2 -> 3 -> 5
```