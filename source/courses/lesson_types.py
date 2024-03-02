from enum import Enum

class LESSON_TYPES(Enum):
    free = ('free', 'Free')
    paid = ('paid', 'Paid')

    @classmethod
    def get_value(cls, type):
        return cls[type].value[0]
    



