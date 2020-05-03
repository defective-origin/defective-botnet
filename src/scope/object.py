
# TODO: work with dict, object and other, json
# parse json becouse of json response
class Object(dict):
    def __setitem__(self, attr: str, value: Any) -> None:
        self.__setattr__(attr, value)
    
    def __getitem__(self, attr: str) -> Any:
        return self.__getattr__(attr)

    def __delitem__(self, attr: str) -> None:
        self.__delattr__(attr)

    def __setattr__(self, attr: str, value: Any) -> None:
        self[attr] = value

    def __getattr__(self, attr: str) -> Any:
        return self.get(attr) 

    def __delattr__(self, attr: str) -> None:
        if attr in self:
            del self[attr]
