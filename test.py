from cascade import Cascader

# push
obj = Cascader(1)
assert obj.get_values() == [1]
obj = obj.push(2)
assert obj.get_values() == [1, 2]
obj = obj.push(3)
assert obj.get_values() == [1, 2, 3]

# pop
obj = Cascader(1)
obj = obj.push(2).push(3)
obj = obj.pop()
assert obj.get_values() == [1, 2]
obj = obj.pop()
assert obj.get_values() == [1]
obj = obj.pop()
assert obj.get_values() == [None]
obj = obj.pop()
assert obj.get_values() == [None]

# swap
obj = Cascader(1)
obj = obj.push(2).push(3)
obj = obj.swap()
assert obj.get_values() == [1, 3, 2]
obj = Cascader(1)
try:
    obj = obj.swap()
    assert False
except IndexError:
    assert True

# dup
obj = Cascader(1)
obj = obj.push(2).push(3)
obj = obj.dup()
assert obj.get_values() == [1, 2, 3, 3]

# jump
obj = Cascader(1)
obj = obj.push(2).push(3).push(4).push(5)
obj = obj.jump(0)
assert obj.get_values() == [1, 2, 3, 4, 5]
obj = obj.jump(-1)
assert obj.value == 4
obj = obj.jump(-3)
assert obj.value == 1
try:
    obj = obj.jump(-1)
    assert False
except IndexError:
    assert True
obj = obj.jump(4)
assert obj.value == 5
try:
    obj = obj.jump(1)
    assert False
except IndexError:
    assert True


# head
obj = Cascader(1)
obj = obj.push(2).push(3).push(4).push(5)
obj = obj.head()
assert obj.value == 5
obj = obj.jump(-2)
assert obj.value == 3
obj = obj.head()
assert obj.value == 5

# tail
obj = Cascader(1)
obj = obj.push(2).push(3).push(4).push(5)
obj = obj.tail()
assert obj.value == 1

# clone
obj = Cascader(1)
obj = obj.push(2).push(3).push(4).push(5)
obj = obj.clone(-2)
assert obj.get_values() == [1, 2, 3, 4, 5, 3]
obj = obj.clone(0)
assert obj.get_values() == [1, 2, 3, 4, 5, 3, 3]
try:
    obj = obj.clone(1)
    assert False
except IndexError:
    assert True

# pick
obj = Cascader(1)
obj = obj.push(2).push(3).push(4).push(5)
assert obj.pick(-1).value == 4
assert obj.pick(-2).value == 3
assert obj.pick(-3).value == 2
assert obj.pick(-4).value == 1
try:
    obj.pick(-5)
    assert False
except IndexError:
    assert True
try:
    obj.pick(1)
    assert False
except IndexError:
    assert True

# pluck
obj = Cascader(1)
obj = obj.push(2).push(3).push(4).push(5)
obj = obj.pluck(0)
assert obj.get_values() == [1, 2, 3, 4, 5]
obj = obj.pluck(-1)
assert obj.get_values() == [1, 2, 3, 5, 4]
obj = obj.pluck(-2)
assert obj.get_values() == [1, 2, 5, 4, 3]
obj = obj.pluck(-3)
assert obj.get_values() == [1, 5, 4, 3, 2]
obj = obj.pluck(-4)
assert obj.get_values() == [5, 4, 3, 2, 1]
try:
    obj.pluck(-5)
    assert False
except IndexError:
    assert True

# clone
obj = Cascader(1)
obj = obj.push(2).push(3).push(4).push(5)
obj = obj.clone(0)
assert obj.get_values() == [1, 2, 3, 4, 5, 5]
obj = obj.clone(-2)
assert obj.get_values() == [1, 2, 3, 4, 5, 5, 4]
obj = obj.clone(-5)
assert obj.get_values() == [1, 2, 3, 4, 5, 5, 4, 2]
try:
    obj = obj.clone(-8)
    assert False
except IndexError:
    assert True
try:
    obj = obj.clone(1)
    assert False
except IndexError:
    assert True

# remove
obj = Cascader(1)
obj = obj.push(2).push(3).push(4).push(5)
obj = obj.remove(0)
assert obj.get_values() == [1, 2, 3, 4]
obj = obj.remove(-3)
assert obj.get_values() == [2, 3, 4]
try:
    obj = obj.remove(-3)
    assert False
except IndexError:
    assert True
try:
    obj = obj.remove(1)
    assert False
except IndexError:
    assert True

# insert
obj = Cascader(1)
obj = obj.push(2).push(3).push(4).push(5)
obj = obj.insert(0, 6)
assert obj.get_values() == [1, 2, 3, 4, 6, 5]
obj = obj.insert(-5, 0)
assert obj.get_values() == [0, 1, 2, 3, 4, 6, 5]
obj = obj.insert(-1, 99)
assert obj.get_values() == [0, 1, 2, 3, 4, 99, 6, 5]

# reversed
obj = Cascader("first")
obj = obj.push("second").push("third")
obj = obj.reverse()
assert obj.get_values() == ["third", "second",  "first"]

# update
obj = Cascader(1)
obj = obj.push(2).push(3).push(4).push(5)
obj.update(0, 6)
obj.update(-1, 99)
assert obj.get_values() == [1, 2, 3, 99, 6]

# # len
# obj = Cascader(1)
# obj = obj.push(2).push(3).push(4).push(5)
# assert len(obj) == 5

# # index
# obj = Cascader(1)
# obj = obj.push(2).push(3).push(4).push(5)
# assert obj[0] == 1
# assert obj[1] == 2
# assert obj[2] == 3
# assert obj[3] == 4
# assert obj[4] == 5
# assert obj[-1] == 5
# assert obj[-2] == 4
# assert obj[-3] == 3
# assert obj[-4] == 2
# assert obj[-5] == 1
# assert obj[1:3] == [2, 3]


# # insert
# obj = Cascader(1)
# obj = obj.push(2).push(3).push(4).push(5)
# obj = obj.insert(1, 6)
# assert obj.get_values() == [(1, 0), (6, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
# obj = obj.insert(0, 10)
# assert obj.get_values() == [(10, 0), (1, 1), (6, 2), (2, 3), (3, 4), (4, 5), (5, 6)]
# obj = obj.insert(-1, 99)
# assert obj.get_values() == [(10, 0), (1, 1), (6, 2), (2, 3), (3, 4), (4, 5), (5, 6), (99, 7)]