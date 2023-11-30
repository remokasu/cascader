from cascade import Cascader

# push
obj = Cascader(1)
assert obj.get_values_with_index() == [(1, 0)]
obj = obj.push(2)
assert obj.get_values_with_index() == [(1, 0), (2, 1)]
obj = obj.push(3)
assert obj.get_values_with_index() == [(1, 0), (2, 1), (3, 2)]

# pop
obj = Cascader(1)
obj = obj.push(2).push(3)
obj = obj.pop()
assert obj.get_values_with_index() == [(1, 0), (2, 1)]
obj = obj.pop()
assert obj.get_values_with_index() == [(1, 0)]
print(obj.get_values_with_index())
obj = obj.pop()
assert obj.get_values_with_index() == [(None, 0)]

# swap
obj = Cascader(1)
obj = obj.push(2).push(3)
obj = obj.swap()
assert obj.get_values_with_index() == [(1, 0), (3, 1), (2, 2)]

# dup
obj = Cascader(1)
obj = obj.push(2).push(3)
obj = obj.dup()
assert obj.get_values_with_index() == [(1, 0), (2, 1), (3, 2), (3, 3)]

# pluck
obj = Cascader(1)
obj = obj.push(2).push(3).push(4).push(5)
obj = obj.pluck(1)
assert obj.get_values_with_index() == [(1, 0), (3, 1), (4, 2), (5, 3), (2, 4)]
obj = obj.pluck(-1)
print(obj.get_values_with_index())
assert obj.get_values_with_index() == [(1, 0), (3, 1), (4, 2), (5, 3), (2, 4), (2, 5)]
obj = obj.pluck(0)
print(obj.get_values_with_index())
assert obj.get_values_with_index() == [(3, 0), (4, 1), (5, 2), (2, 3), (2, 4), (1, 5)]

# pick
obj = Cascader(1)
obj = obj.push(2).push(3).push(4).push(5)
obj = obj.pick(1)
print("pick", obj.get_values_with_index())
assert obj.get_values_with_index() == [(2, 0)]

# clone
obj = Cascader(1)
obj = obj.push(2).push(3).push(4).push(5)
obj = obj.clone(2)
assert obj.get_values_with_index() == [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (3, 5)]  
obj = obj.clone(-1)
assert obj.get_values_with_index() == [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (3, 5), (3, 6)]
obj = obj.clone(0)
assert obj.get_values_with_index() == [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (3, 5), (3, 6), (1, 7)]

# jump
obj = Cascader(1)
obj = obj.push(2).push(3).push(4).push(5)
obj = obj.jump(1)
assert obj.get_values_with_index() == [(1, 0), (2, 1)]

# remove
obj = Cascader(1)
obj = obj.push(2).push(3).push(4).push(5)
obj = obj.remove(1)
assert obj.get_values_with_index() == [(1, 0), (3, 1), (4, 2), (5, 3)]

# len
obj = Cascader(1)
obj = obj.push(2).push(3).push(4).push(5)
assert len(obj) == 5

# index
obj = Cascader(1)
obj = obj.push(2).push(3).push(4).push(5)
assert obj[0] == 1
assert obj[1] == 2
assert obj[2] == 3
assert obj[3] == 4
assert obj[4] == 5
assert obj[-1] == 5
assert obj[-2] == 4
assert obj[-3] == 3
assert obj[-4] == 2
assert obj[-5] == 1
assert obj[1:3] == [2, 3]

# reversed
obj = Cascader("first")
obj = obj.push("second").push("third")
obj = obj.reverse()
assert obj.get_values_with_index() == [("third", 0), ("second", 1), ("first", 2)]

# insert
obj = Cascader(1)
obj = obj.push(2).push(3).push(4).push(5)
obj = obj.insert(1, 6)
assert obj.get_values_with_index() == [(1, 0), (6, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
obj = obj.insert(0, 10)
assert obj.get_values_with_index() == [(10, 0), (1, 1), (6, 2), (2, 3), (3, 4), (4, 5), (5, 6)]
obj = obj.insert(-1, 99)
assert obj.get_values_with_index() == [(10, 0), (1, 1), (6, 2), (2, 3), (3, 4), (4, 5), (5, 6), (99, 7)]