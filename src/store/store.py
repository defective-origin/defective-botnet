from .object import Object
from .constants import Operation
from ..event.event_emitter import EventEmitter
from uuid import uuid4

# class Store(Object, EventEmmiter):
#     def __setitem__(self, attr: str, value: Any) -> None:
#         self.__setattr__(attr, value)

#     def __delitem__(self, attr: str) -> None:
#         self.__delattr__(attr)

#     def __setattr__(self, attr: str, value: Any) -> None:
#         self.emit(attr, self[attr], value, Operation.SET)
#         super().__setattr__(attr, value)

#     def __delattr__(self, attr: str) -> None:
#         self.emit(attr, self[attr], None, Operation.DELETE)
#         super().__delattr__(attr)
# # TODO add subscription
# TODO: as NGXS
class Store(Object): # TODO: change name?
    NAME = uuid4()
    DEFAULT = None

    def __chanched__(self, prev: Store, curr: Store): pass
    # add also look at changing of a field a.field.on('change')

    def bind(self, space: Space): pass

    @selector([a,b,c])
    def simple_selector(self, a,b,c):
        pass

    @action([a,b,c])
    def simple_action(self, a,b,c):
        pass

# if field is simple we can subscribe with it a.field.subscribe()
# TODO add subscription
# TODO: subscribe

    # def observe(self): pass #TODO: looking for object
    # def unobserve(self): pass

    # def unwatch(self): pass #TODO: looking for props
    # def watch(self): pass # TODO close()

    # TODO: и другие свойства и методы js and python