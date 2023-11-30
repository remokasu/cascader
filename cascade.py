'''
A Cascader is a data structure that allows you to push and pop objects to and from the top of a stack.
The stack is implemented as a linked list, so you can also push and pop objects from the bottom of the stack.
You can also swap the top two objects, duplicate the top object, and jump to a specific index in the stack.
'''

from typing import Any


class Cascader:
    def __init__(self, obj, prev=None, next=None, index=0):
        self.obj = obj
        self.prev = prev
        self.next = next
        self.error = ""
        self._index = index

    ###########################################################
    # Properties
    ###########################################################

    @property
    def value(self) -> Any:
        return self.obj

    @property
    def index(self) -> int:
        return self._index

    ###########################################################
    # Stack Methods
    ###########################################################

    def push(self, obj) -> 'Cascader':
        new_index = self._index + 1
        new_cascader = Cascader(obj, prev=self, next=None, index=new_index)
        if self.next is not None:
            self.next.prev = new_cascader
            new_cascader.next = self.next
        self.next = new_cascader
        return new_cascader

    def pop(self) -> 'Cascader':
        if self.prev is None:
            new_cascade = Cascader(None, None, None)
            new_cascade.set_error("Error: No more objects to pop")
            return new_cascade
        new_index = self.prev._index
        self.prev.next = None
        return self.prev

    def swap(self) -> 'Cascader':
        '''
        Swap the top two elements
        '''
        if self.prev is not None:
            self.obj, self.prev.obj = self.prev.obj, self.obj
        return self

    def dup(self) -> 'Cascader':
        '''
        Duplicate the top element
        '''
        return self.push(self.obj)

    def jump(self, index: int) -> 'Cascader':
        '''
        Jump to the specified index
        '''
        if index == self._index:
            return self
        elif index > self._index:
            return self.push(None).jump(index)
        else:
            return self.pop().jump(index)

    def clone(self, index: int) -> 'Cascader':
        '''
        Copy the element at the specified index to the top
        '''
        index = self._format_index(index)
        if index == self._get_last_index():
            return self.dup()
        # Move to the specified index
        target = self
        while target._index != index:
            target = target.prev
            if target is None:
                raise IndexError("Index out of range")
        return self.push(target.obj)

    def pick(self, index: int) -> 'Cascader':
        '''
        Return a new Cascader with the element at the specified index
        '''
        index = self._format_index(index)
        if index == self._get_last_index():
            return self.dup()
        # Move to the specified index
        target = self
        while target._index != index:
            target = target.prev
            if target is None:
                raise IndexError("Index out of range")
        new_cascader = Cascader(target.obj, None, None, 0)
        return new_cascader

    def pluck(self, index: int) -> 'Cascader':
        '''
        '''
        index = self._format_index(index)
        if index == self._get_last_index():
            return self.dup()
        # Move to the specified index
        target = self
        while target._index != index:
            target = target.prev
            if target is None:
                raise IndexError("Index out of range")
        # Remove the specified element
        if target.prev is not None:
            target.prev.next = target.next
        if target.next is not None:
            target.next.prev = target.prev
        # Reconnect the remaining chain
        if target.next:
            target.next._index -= 1
            target.next._update_index()
        # Reset the index and push to the top
        target._index = 0
        target.prev = None
        target.next = None
        return self.push(target.obj)

    def insert(self, index: int, obj: Any) -> 'Cascader':
        # Move to the specified index
        index = self._format_index(index)
        if index == self._get_last_index():
            return self.push(obj)
        target = self
        while target._index != index:
            target = target.prev
            if target is None:
                raise IndexError("Index out of range")
        # Insert the specified element
        new_cascader = Cascader(obj, target.prev, target, target._index)
        if target.prev is not None:
            target.prev.next = new_cascader
            target.prev = new_cascader
        else:
            target.prev = new_cascader
        target._index += 1
        # Reconnect the remaining chain
        target = target.next
        while target is not None:
            target._index += 1
            target = target.next
        return self

    def reverse(self) -> 'Cascader':
        current = self
        while current.next is not None:
            current = current.next
        new_cascader = Cascader(current.obj, None, None, 0)
        current = current.prev
        while current is not None:
            new_cascader = new_cascader.push(current.obj)
            current = current.prev
        return new_cascader

    def remove(self, index: int) -> 'Cascader':
        return self.pluck(index).pop()

    ###########################################################
    # Getter Methods
    ###########################################################

    def get_values(self) -> list[Any]:
        values = [self.obj]
        current = self
        while current.prev is not None:
            current = current.prev
            values.insert(0, current.obj)
        return values

    def get_values_with_index(self) -> list[tuple[Any, int]]:
        values_with_index = [(self.obj, self._index)]
        current = self
        while current.prev is not None:
            current = current.prev
            values_with_index.insert(0, (current.obj, current._index))
        return values_with_index

    ###########################################################
    # Setter Methods
    ###########################################################

    def set_error(self, error: str) -> None:
        self.error = error

    ###########################################################
    # State Methods
    ###########################################################

    def save_state(self) -> tuple[Any, 'Cascader', 'Cascader', int]:
        return (self.obj, self.prev, self.next, self._index)

    @classmethod
    def restore_state(cls, state) -> 'Cascader':
        obj, prev, next_cascader, index = state
        restored_cascader = cls(obj, prev, next_cascader, index)
        if prev is not None:
            prev.next = restored_cascader
        if next_cascader is not None:
            next_cascader.prev = restored_cascader
        return restored_cascader

    ###########################################################
    # Private Methods
    ###########################################################

    def _get_last_index(self) -> int:
        last_index = self._index
        current = self
        while current.prev is not None:
            last_index = max(last_index, current.prev._index)
            current = current.prev
        return last_index

    def _format_index(self, index: int) -> int:
        if index < 0:
            index = self._get_last_index() + index + 1
        if index < 0 or index > self._get_last_index():
            raise IndexError("Index out of range")
        return index

    def _update_index(self):
        current = self
        while current.next:
            current.next._index = current._index + 1
            current = current.next

    def _handle_index(self, index):
        if index < 0:
            index = self._get_last_index() + index + 1
        if index < 0 or index > self._get_last_index():
            raise IndexError("Index out of range")
        current = self
        while current is not None and current._index != index:
            current = current.prev
        if current is None:
            raise IndexError("Index out of range")
        return current.obj

    def _handle_slice(self, slice_obj):
        start, stop, step = slice_obj.indices(self._get_last_index() + 1)
        result = []
        current = self
        while current is not None and current._index >= start:
            if current._index < stop and (current._index - start) % step == 0:
                result.append(current.obj)
            current = current.prev
        return result[::-1]


    ###########################################################
    # Magic Methods
    ###########################################################

    def __str__(self):
        return str(self.obj)

    def __len__(self):
        return self._index + 1

    def __repr__(self):
        return f"Cascader(obj={self.obj}, index={self._index})"

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self._handle_slice(index)
        elif isinstance(index, int):
            return self._handle_index(index)
        else:
            raise TypeError("Indices must be integers or slices")

    def __iter__(self):
        current = self
        while current:
            yield current
            current = current.next

    def __next__(self):
        if self.next is not None:
            return self.next
        else:
            raise StopIteration

    def __reversed__(self):
        current = self
        while current:
            yield current.obj
            current = current.next


if __name__ == '__main__':
    obj = Cascader(1)
    print(obj.get_values_with_index())
    obj = obj.push(2)
    print(obj.get_values_with_index())
    obj = obj.push(3)
    print(obj.get_values_with_index())
    saved_state  = obj.save_state()
    # print(obj.pop().pop().pop())
    print("pop")
    # obj = obj.pop().pop().pop()
    print(obj.get_values_with_index())
    obj = obj.pop()
    print(obj.get_values_with_index())
    obj = obj.pop()
    print(obj.get_values_with_index())
    obj = obj.pop()
    print(obj.get_values_with_index())
    obj = obj.push(2)
    print(obj.get_values_with_index())
    obj = obj.push(3)
    print(obj.get_values_with_index())
    obj = obj.push(4)
    print(obj.get_values_with_index())
    obj = obj.push(5)
    print(obj.get_values_with_index())
    obj = obj.push(6)
    print(obj.get_values_with_index())
    obj = obj.push(7)
    print(obj.get_values_with_index())
    obj = obj.push(8)
    print(obj.get_values_with_index())
    obj = obj.push(9)
    print(obj.get_values_with_index())
    obj = obj.push(10)
    print(obj.get_values_with_index())
    # swap
    obj = obj.swap()
    print(obj.get_values_with_index())
    # dup
    obj = obj.dup()
    print(obj.get_values_with_index())
    # jump
    obj = obj.jump(1)
    print(obj.get_values_with_index())
    obj = obj.jump(10)
    print(obj.get_values_with_index())
    # pick
    print("pick")
    obj = obj.pick(1)
    print(obj.get_values_with_index())
    # remove
    obj = Cascader(1)
    obj = obj.push(2)
    obj = obj.push(3)
    obj = obj.push(4)
    obj = obj.push(5)
    print(obj.get_values_with_index())
    print("remove")
    obj = obj.remove(1)
    print(obj.get_values_with_index())
    # len
    print(len(obj))
    # reversed
    print("reversed")
    cascader = Cascader(1)
    cascader.push(2).push(3)
    for obj in reversed(cascader):
        print(obj)
    # index
    cascader = Cascader(1)
    cascader = cascader.push(2).push(3).push(4).push(5)
    print(cascader[0])  # 最初の要素
    print(cascader[-1]) # 最後の要素
    print(cascader[1:3]) # 1から2までの要素
    obj = Cascader(1)
    obj = obj.push(2).push(3).push(4).push(5)
    print(obj.get_values_with_index())
    # Cascader インスタンスの作成
    cascader = Cascader(1)
    cascader.push(2).push(3).push(4).push(5).push(6).push(7).push(8).push(9).push(10)
    # Cascader インスタンスをイテレータとして使用
    for element in cascader:
        print(element.obj)
    cascader = Cascader("first")
    cascader = cascader.push("second").push("third")

    # 初期状態
    c = Cascader("Start")
    # 条件分岐点
    if_cascade = c.push("If")
    # Case A の分岐
    ca = if_cascade.push("A")
    # Case B の分岐
    cb = if_cascade.dup().push("B")
    print(cb.get_values_with_index())