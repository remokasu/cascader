
from typing import Any

class InvalidOffsetError(Exception):
    pass

class EmptyStackError(Exception):
    pass

class InvalidOperationError(Exception):
    pass

class DataIntegrityError(Exception):
    pass

class Cascader:
    def __init__(self, obj, prev=None, next=None):
        self.obj = obj
        self.prev = prev
        self.next = next
        self.error = None

    ###########################################################
    # Properties
    ###########################################################

    @property
    def value(self) -> Any:
        return self.obj

    ###########################################################
    # Stack Methods
    ###########################################################

    def push(self, obj) -> 'Cascader':
        new_cascader = Cascader(obj, prev=self, next=None)
        if self.next is not None:
            self.next.prev = new_cascader
            new_cascader.next = self.next
        self.next = new_cascader
        return new_cascader

    def pop(self) -> 'Cascader':
        if self.prev is None:
            # raise EmptyStackError("Error: Stack is empty")
            return Cascader(None, None, None)
        if self.next is not None:
            self.next.prev = self.prev
        self.prev.next = self.next
        return self.prev

    def swap(self) -> 'Cascader':
        '''
        Swap the current two elements
        '''
        if self.prev is None:
            raise InvalidOperationError("Error: No more objects to swap")
        self.obj, self.prev.obj = self.prev.obj, self.obj
        return self

    def dup(self) -> 'Cascader':
        '''
        Duplicate the top element
        '''
        return self.push(self.obj)


    def head(self) -> 'Cascader':
        '''
        Jump to the head
        '''
        target = self
        while target.next is not None:
            target = target.next
        return target

    def tail(self) -> 'Cascader':
        '''
        Jump to the tail
        '''
        target = self
        while target.prev is not None:
            target = target.prev
        return target

    def jump(self, offset: int) -> 'Cascader':
        '''
        Jump to the specified offset
        '''
        if offset == 0:
            return self
        elif offset > 0:
            target = self._jump_to_next_ofst(offset)
        else:
            target = self._jump_to_prev_ofst(-offset)
        return target

    def _jump_to_prev_ofst(self, offset: int) -> 'Cascader':
        target = self
        for i in range(offset):
            target = target.prev
            if target is None:
                raise InvalidOffsetError("Error: Offset out of range")
        return target

    def _jump_to_next_ofst(self, offset: int) -> 'Cascader':
        target = self
        for i in range(offset):
            target = target.next
            if target is None:
                raise InvalidOffsetError("Error: Offset out of range")
        return target

    def pick(self, offset: int) -> 'Cascader':
        '''
        Return a new Cascader with the element at the specified offset
        '''
        target = self.jump(offset)
        new_cascader = Cascader(target.obj, None, None)
        return new_cascader

    def pluck(self, offset: int) -> 'Cascader':
        '''
        Remove the element at the specified offset and push it to the current
        '''
        if offset == 0:
            return self
        target = self.jump(offset)
        if target.prev is not None:
            target.prev.next = target.next
        if target.next is not None:
            target.next.prev = target.prev
        return self.push(target.obj)

    def clone(self, offset: int) -> 'Cascader':
        '''
        Copy the element at the specified offset to the current
        '''
        target = self.jump(offset)
        return self.push(target.obj)

    def remove(self, offset: int) -> 'Cascader':
        return self.pluck(offset).pop()

    def insert(self, offset: int, obj: Any) -> 'Cascader':
        target = self.jump(offset)
        new_cascader = Cascader(obj, None, None)
        if target.prev is not None:
            target.prev.next = new_cascader
            new_cascader.prev = target.prev
        target.prev = new_cascader
        new_cascader.next = target
        return self

    def current(self) -> 'Cascader':
        return self

    ###########################################################
    # Head Methods
    ###########################################################

    def pushH(self, obj) -> 'Cascader':
        if self.is_head() is False:
            raise InvalidOperationError("Error: Cannot pushH on a non-head")
        return self.push(obj)

    def popH(self) -> 'Cascader':
        if self.is_head() is False:
            raise InvalidOperationError("Error: Cannot popH on a non-head")
        return self.pop()

    def swapH(self) -> 'Cascader':
        if self.is_head() is False:
            raise InvalidOperationError("Error: Cannot swapH on a non-head")
        return self.swap()

    def dupH(self) -> 'Cascader':
        if self.is_head() is False:
            raise InvalidOperationError("Error: Cannot dupH on a non-head")
        return self.dup()

    def pluckH(self, offset: int) -> 'Cascader':
        if self.is_head() is False:
            raise InvalidOperationError("Error: Cannot pluckH on a non-head")
        return self.pluck(offset)

    def cloneH(self, offset: int) -> 'Cascader':
        if self.is_head() is False:
            raise InvalidOperationError("Error: Cannot cloneH on a non-head")
        return self.clone(offset)

    ###########################################################
    # Conditional Methods
    ###########################################################

    def if_(self, offset: int) -> 'Cascader':
        if self.obj is True:
            return self.jump(offset)
        return self

    def ifnot(self, offset: int) -> 'Cascader':
        if self.obj is False:
            return self.jump(offset)
        return self

    def ifelse(self, offset_true: int, offset_false: int) -> 'Cascader':
        if self.obj is True:
            return self.jump(offset_true)
        return self.jump(offset_false)

    ###########################################################
    # Other Methods
    ###########################################################

    def reset(self) -> 'Cascader':
        tail = self.tail()
        while tail.is_head() is False:
            tail = tail.pop()
        return tail

    ###########################################################
    # List Methods
    ###########################################################

    def reverse(self) -> 'Cascader':
        current = self
        while current.next is not None:
            current = current.next
        new_cascader = Cascader(current.obj, None, None)
        current = current.prev
        while current is not None:
            new_cascader = new_cascader.push(current.obj)
            current = current.prev
        return new_cascader

    ###########################################################
    # Boolean Methods
    ###########################################################

    def is_head(self) -> bool:
        return self.next is None

    def is_tail(self) -> bool:
        return self.prev is None

    ###########################################################
    # Object Methods
    ###########################################################

    def update(self, offset: int, obj: Any) -> None:
        target = self.jump(offset)
        target.set_value(obj)

    ###########################################################
    # Getter Methods
    ###########################################################

    def get_values(self) -> list[Any]:
        current = self.tail()
        values = []
        while current.is_head() is False:
            values.append(current.obj)
            current = current.next
        values.append(current.obj)
        return values

    ###########################################################
    # Setter Methods
    ###########################################################

    def set_value(self, obj: Any) -> None:
        self.obj = obj

    def set_error(self, error) -> None:
        self.error = error

    ###########################################################
    # State Methods
    ###########################################################

    def save_state(self) -> tuple[Any, 'Cascader', 'Cascader']:
        return (self.obj, self.prev, self.next)

    @classmethod
    def restore_state(cls, state) -> 'Cascader':
        obj, prev, next_cascader = state
        restored_cascader = cls(obj, prev, next_cascader)
        if prev is not None:
            prev.next = restored_cascader
        if next_cascader is not None:
            next_cascader.prev = restored_cascader
        return restored_cascader


    ###########################################################
    # Magic Methods
    ###########################################################

    def __str__(self):
        return str(self.obj)

    def __repr__(self):
        return f"Cascader(obj={self.obj})"

    def __len__(self):
        return len(self.head().get_values())
