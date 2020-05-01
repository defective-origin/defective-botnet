
# TODO: work with dict, object and other, json
# parse json becouse of json response
# TODO: subscribe
class Object: # TODO: inherit from Dict
    __data = {}

    def __setitem__(self, attr: str, value: Any) -> None:
        self.__setattr__(attr, value)
    
    def __getitem__(self, attr: str) -> Any:
        return self.__getattr__(attr)

    def __delitem__(self, attr: str) -> None:
        self.__delattr__(attr)

    def __setattr__(self, attr: str, value: Any) -> None:
        self.__data[attr] = value

    def __getattr__(self, attr: str) -> Any:
        return self.__data.get(attr) 

    def __delattr__(self, attr: str) -> None:
        if attr in self:
            del self.__data[attr]

    def __contains__(self, attr: str) -> bool:
        return attr in self.__data

    def __iter__(self) -> iterator:
        return iter(self.__data)

    def __str__(self) -> str:
        return str(self.__data)

    def __len__(self) -> int:
        return len(self.__data)

    # def assign(self): pass
    # def is(self): pass
    # def isExtensible(self): pass
    # def isFrozen(self): pass
    # def isSealed(self): pass
    # def observe(self): pass
    # def preventExtensions(self): pass
    # def unwatch(self): pass
    # def watch(self): pass
    # def freeze(self): pass
    # def seal(self): pass
    # def clone(self, deep = True): pass
    # def items(self): pass
    # def values(self): pass
    # def keys(self): pass
    # TODO: и другие свойства и методы js and python
