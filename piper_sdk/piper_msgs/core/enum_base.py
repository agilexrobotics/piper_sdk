from enum import IntEnum, Enum

class IntEnumBase(IntEnum):
    def __str__(self):
        # return f"{self.__class__.__name__}.{self.name}(0x{self.value:X})"
        return f"{self.name}(0x{self.value:X})"
    def __repr__(self):
        # return f"{self.__class__.__name__}.{self.name}(0x{self.value:X})"
        return f"{self.name}(0x{self.value:X})"
    @classmethod
    def match_value(cls, val):
        if not isinstance(val, int):
            raise ValueError(f"{cls.__name__}: input value must be an integer, got {type(val).__name__}")
        try:
            return cls(val)
        except ValueError:
            if hasattr(cls, "UNKNOWN"):
                return cls.UNKNOWN
            else:
                raise ValueError(f"{cls.__name__}: invalid enum value 0x{val:X}, and no UNKNOWN defined")
    @classmethod
    def value_list(cls):
        return [e.value for e in cls]
    

class EnumBase(Enum):
    def __str__(self):
        return f"{self.name}({self.value})"
    def __repr__(self):
        return f"{self.name}({self.value})"
    @classmethod
    def match_value(cls, val):
        try:
            return cls(val)
        except ValueError:
            if hasattr(cls, "UNKNOWN"):
                return cls.UNKNOWN
            else:
                raise ValueError(f"{cls.__name__}: invalid enum value {val}, and no UNKNOWN defined")
    @classmethod
    def value_list(cls):
        return [e.value for e in cls]

class StrStruct:
    """
    轻量字符串枚举结构
    成员本质就是str，不是Enum对象
    """

    @classmethod
    def _member_map(cls):
        """获取所有成员"""
        result = {}
        for base in reversed(cls.__mro__):
            if base in (object, StrStruct):
                continue
            for k, v in base.__dict__.items():
                if k.startswith("_"):
                    continue
                if isinstance(v, (classmethod, staticmethod, property)):
                    continue
                if callable(v):
                    continue
                result[k] = v
        return result
    
    # @classmethod
    # def _member_map(cls):
    #     """获取所有成员"""
    #     result = {}
    #     for k, v in cls.__dict__.items():
    #         if k.startswith("_"):
    #             continue
    #         if callable(v):
    #             continue
    #         result[k] = v
    #     return result
    

    @classmethod
    def value_list(cls):
        """返回所有value"""
        return list(cls._member_map().values())

    @classmethod
    def match_value(cls, val):
        """根据value匹配"""
        for v in cls._member_map().values():
            if v == val:
                return v

        if hasattr(cls, "UNKNOWN"):
            return cls.UNKNOWN

        raise ValueError(f"{cls.__name__}: invalid value {val}")
