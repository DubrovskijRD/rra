from enum import Enum


class Roles(Enum):
    ADMIN = 'admin'
    EDITOR = 'editor'


class CheckStatusList(Enum):
    PROBABLY_YES = "Возможно да"
    PROBABLY_NO = "Возможно нет"
    YES = "Да"
    NO = "Нет"


class AutoCategoryList(Enum):
    TRACK = "грузовой"
