from enum import Enum


class Roles(Enum):
    ADMIN = 'Админ'
    EDITOR = 'Редактор'


class CheckStatusList(Enum):
    PROBABLY_YES = "Возможно да"
    PROBABLY_NO = "Возможно нет"
    YES = "Да"
    NO = "Нет"


class AutoCategoryList(Enum):
    TRACK = "грузовой"
    AUTO = "легковой"
    CYCKE = "мотоцикл"
