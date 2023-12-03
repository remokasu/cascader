from cascade import Cascader
from cascade import InvalidOffsetError, InvalidOperationError


def test_push():
    # push
    obj = Cascader(1)
    assert obj.get_values() == [1]
    obj = obj.push(2)
    assert obj.get_values() == [1, 2]
    obj = obj.push(3)
    assert obj.get_values() == [1, 2, 3]

def test_pop():
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

def test_swap():
    # swap
    obj = Cascader(1)
    obj = obj.push(2).push(3)
    obj = obj.swap()
    assert obj.get_values() == [1, 3, 2]
    obj = Cascader(1)
    try:
        obj = obj.swap()
        assert False
    except InvalidOperationError:
        assert True 

def test_dup():
    # dup
    obj = Cascader(1)
    obj = obj.push(2).push(3)
    obj = obj.dup()
    assert obj.get_values() == [1, 2, 3, 3]

def test_jump():
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
    except InvalidOffsetError:
        assert True
    obj = obj.jump(4)
    assert obj.value == 5
    try:
        obj = obj.jump(1)
        assert False
    except InvalidOffsetError:
        assert True

def test_head():
    # head
    obj = Cascader(1)
    obj = obj.push(2).push(3).push(4).push(5)
    obj = obj.head()
    assert obj.value == 5
    obj = obj.jump(-2)
    assert obj.value == 3
    obj = obj.head()
    assert obj.value == 5

def test_tail():
    # tail
    obj = Cascader(1)
    obj = obj.push(2).push(3).push(4).push(5)
    obj = obj.tail()
    assert obj.value == 1
    obj = obj.jump(2)
    assert obj.value == 3
    obj = obj.tail()
    assert obj.value == 1

def test_clone():
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
    except InvalidOffsetError:
        assert True

def test_pick():
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
    except InvalidOffsetError:
        assert True
    try:
        obj.pick(1)
        assert False
    except InvalidOffsetError:
        assert True

def test_pluck():
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
    except InvalidOffsetError:
        assert True

def test_clone():
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
    except InvalidOffsetError:
        assert True
    try:
        obj = obj.clone(1)
        assert False
    except InvalidOffsetError:
        assert True

def test_remove():
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
    except InvalidOffsetError:
        assert True
    try:
        obj = obj.remove(1)
        assert False
    except InvalidOffsetError:
        assert True

def test_insert():
    # insert
    obj = Cascader(1)
    obj = obj.push(2).push(3).push(4).push(5)
    obj = obj.insert(0, 6)
    assert obj.get_values() == [1, 2, 3, 4, 6, 5]
    obj = obj.insert(-5, 0)
    assert obj.get_values() == [0, 1, 2, 3, 4, 6, 5]
    obj = obj.insert(-1, 99)
    assert obj.get_values() == [0, 1, 2, 3, 4, 99, 6, 5]
    try:
        obj = obj.insert(9, 99)
        assert False
    except InvalidOffsetError:
        assert True
    try:
        obj = obj.insert(-9, 99)
        assert False
    except InvalidOffsetError:
        assert True

def test_reverse():
    # reverse
    obj = Cascader(1)
    obj = obj.push(2).push(3).push(4).push(5)
    obj = obj.reverse()
    assert obj.get_values() == [5, 4, 3, 2, 1]
    obj = obj.reverse()
    assert obj.get_values() == [1, 2, 3, 4, 5]


def test_update():
    # update
    obj = Cascader(1)
    obj = obj.push(2).push(3).push(4).push(5)
    obj.update(0, 6)
    obj.update(-1, 99)
    assert obj.get_values() == [1, 2, 3, 99, 6]

def test_if_():
    obj = Cascader(1)
    obj = obj.push(2).push(3).push(4).push(5).push(True)
    obj = obj.if_(-2)
    obj = obj.current()
    assert obj.value == 4

def test_ifelse():
    obj = Cascader(1)
    obj = obj.push(2).push(3).push(4).push(5).push(True)
    obj = obj.ifelse(-2, -1)
    obj = obj.current()
    assert obj.value == 4
    obj = Cascader(1)
    obj = obj.push(2).push(3).push(4).push(5).push(False)
    obj = obj.ifelse(-2, -1)
    obj = obj.current()
    assert obj.value == 5

if __name__ == '__main__':
    test_push()
    test_pop()
    test_swap()
    test_dup()
    test_jump()
    test_head()
    test_tail()
    test_clone()
    test_pick()
    test_pluck()
    test_clone()
    test_remove()
    test_insert()
    test_reverse()
    test_update()
    test_if_()