# Cascader
- 概要: 連結リストでスタックを表現するためのクラス
- 動作環境: Python >=3.10

# 用語
- (tail): 一番古いデータ
- (head): 一番新しいデータ
- (current): 現在位置
- (prev): 現在位置の一つ前
- (next): 現在位置の一つ次
- 連結リスト: データをノードオブジェクトで連結したデータ構造
- スタック: 連結リストの先頭にデータを追加していくデータ構造
- オフセット: 連結リストの現在位置からの相対位置。0 は現在位置、1 は現在位置の次 (next)、-1 は現在位置の一つ前 (prev) を表す。マイナス方向は (tail) に向かう方向、プラス方向は (head) に向かう方向。

例:
``` text
 1 -> 2 -> 3 -> 4 -> 5
 ↑ (tail)            ↑ (head)
                     ↑ (current)
                ↑ (prev)
                          ↑ (next)
-4   -3   -2   -1    0    1    2    3    4 (offset)
```

# 使い方

## 初期化
``` python
data = Cascader(1)  # 1 で初期化
# 1
```

## push: 
- 現在位置 (current) の次 (next) に要素を追加
- 追加した要素は (current) になる
- 伝統的なスタックの push とは異なり、(current) が (head) でなくても追加できる
``` python
data = Cascader(1)
# 1
data = data.push(2)  # 2 追加
# 1 -> 2
data = data.push(3)  # 3 追加
# 1 -> 2 -> 3
```

## pop: (current) を削除
``` python
data = Cascader(1)
data = data.push(2).push(3).push(4).push(5)
# 1 -> 2 -> 3 -> 4 -> 5
data = data.pop()  # 削除
# 1 -> 2 -> 3 -> 4
```

## swap: (current) とその一つ前を入れ替え
``` python
data = Cascader(1)
data = data.push(2).push(3).push(4).push(5)
# 1 -> 2 -> 3 -> 4 -> 5
data = data.swap()  # 入れ替え
# 1 -> 2 -> 3 -> 5 -> 4
```

## dup: (current) を複製して (head) の次 (next) に追加
``` python
data = Cascader(1)
data = data.push(2).push(3).push(4).push(5)
# 1 -> 2 -> 3 -> 4 -> 5
data = data.dup()  # 複製して追加
# 1 -> 2 -> 3 -> 4 -> 5 -> 5
```

## jump: 指定の要素に移動
ジャンプ先は (current) からの相対位置で指定する。
``` python
data = Cascader(1)
data = data.push(2).push(3).push(4).push(5)
# 1 -> 2 -> 3 -> 4 -> 5
#                     ↑ (current)
data = data.jump(-2)  # ジャンプ
# 1 -> 2 -> 3 -> 4 -> 5
#           ↑ (current)
```

## clone: 指定の要素の要素を複製して (current) の次に追加
- 複製対象は (current) からの相対位置で指定する
``` python
data = Cascader(1)
data = data.push(2).push(3).push(4).push(5)
# 1 -> 2 -> 3 -> 4 -> 5
#                     ↑ (current)
data = data.clone(-3)  # 複製して追加
# 1 -> 2 -> 3 -> 4 -> 5 -> 2
#                          ↑ (current)
```

## reverse: 逆順
``` python
data = Cascader(1)
data = data.push(2).push(3).push(4).push(5)
# 1 -> 2 -> 3 -> 4 -> 5
data = data.reverse()  # 逆順
# 5 -> 4 -> 3 -> 2 -> 1
```

## pick: 指定の要素を返す
- (current) からの相対位置で指定する
- pick した要素は新規の Cascader として返される
- 元の Cascader は変更されない
``` python
data = Cascader(1)
data = data.push(2).push(3).push(4).push(5)
# 1 -> 2 -> 3 -> 4 -> 5
#                     ↑ (current)
data = data.pick(-3)
# 2
```

## pluck: 指定の要素を削除して末尾に追加
- (current) からの相対位置で指定する
``` python
data = Cascader(1)
data = data.push(2).push(3).push(4).push(5)
# 1 -> 2 -> 3 -> 4 -> 5
#                     ↑ (current)
data = data.pluck(-3)  # 削除して末尾に追加
# 1 -> 2 -> 3 -> 5 -> 2
```

## insert: 指定の位置の前に要素を挿入
- (current) からの相対位置で指定する
``` python
data = Cascader(1)
data = data.push(2).push(3).push(4).push(5)
# 1 -> 2 -> 3 -> 4 -> 5
data = data.insert(-3, 10)  # 挿入
# 1 -> 10 -> 2 -> 3 -> 4 -> 5
```

## remove: 指定の要素を削除
- (current) からの相対位置で指定する
``` python
data = Cascader(1)
data = data.push(2).push(3).push(4).push(5)
# 1 -> 2 -> 3 -> 4 -> 5
data = data.remove(-3)  # 削除
# 1 -> 3 -> 4 -> 5
```

## head: (head) へ移動
``` python
data = Cascader(1)
data = data.push(2).push(3).push(4).push(5)
data = data.jump(-3)  # ジャンプ
# 1 -> 2 -> 3 -> 4 -> 5
#      ↑ (current)
data = data.head()  # (head) へ移動
# 1 -> 2 -> 3 -> 4 -> 5
#                     ↑ (current)
```

## tail: (tail) へ移動
``` python
data = Cascader(1)
data = data.push(2).push(3).push(4).push(5)
# 1 -> 2 -> 3 -> 4 -> 5
#                     ↑ (current)
data = data.tail()  # (tail) へ移動
# 1 -> 2 -> 3 -> 4 -> 5
# ↑ (current)
```