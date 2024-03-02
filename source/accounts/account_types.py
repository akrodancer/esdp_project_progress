from enum import Enum

class ACCOUNT_TYPES(Enum):
    teacher = ('teacher', 'Teacher')
    user = ('user', 'User')

    @classmethod
    def get_value(cls, type):
        return cls[type].value[0]
    