from sqlalchemy import Column, Table, Integer, Boolean, DateTime, String, Text, ForeignKey, func


from .db import db


class AutoCategory(db.Model):
    __tablename__ = "rra_category"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)

    def __str__(self):
        return self.name


class CheckStatus(db.Model):
    __tablename__ = "rra_check_status"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)

    def __str__(self):
        return self.name


class RRA(db.Model):
    __tablename__ = "rra"
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('rra_category.id'), nullable=False)
    brand = Column(String(255))
    model = Column(String(255))
    year = Column(Integer)
    monitoring_check = Column(Integer, ForeignKey('rra_check_status.id'))
    safe_block_check = Column(Integer, ForeignKey('rra_check_status.id'))
    danger_block_check = Column(Integer, ForeignKey('rra_check_status.id'))
    CAN_check = Column(Integer, ForeignKey('rra_check_status.id'))
    default_fuel_sens_check = Column(Integer, ForeignKey('rra_check_status.id'))
    fuel_sens_check = Column(Integer, ForeignKey('rra_check_status.id'))
    temp_sens_check = Column(Integer, ForeignKey('rra_check_status.id'))
    reed_switch_check = Column(Integer, ForeignKey('rra_check_status.id'))
    angle_sens_check = Column(Integer, ForeignKey('rra_check_status.id'))
    first_tank_volume = Column(Integer)
    second_tank_volume = Column(Integer)
    third_tank_volume = Column(Integer)
    dismantling_tank_check = Column(Integer, ForeignKey('rra_check_status.id'))
    equipment = Column(String(255))
    mounting = Column(Boolean(), server_default='t')
    pyrus_link = Column(String(255))
    docs = Column(String(255))
    note = Column(Text)

    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), server_default=func.now(), onupdate=func.now())

    category = db.relationship('AutoCategory')
    monitoring = db.relationship('CheckStatus', foreign_keys=[monitoring_check])
    safe_block = db.relationship('CheckStatus', foreign_keys=[safe_block_check])
    danger_block = db.relationship('CheckStatus', foreign_keys=[danger_block_check])
    CAN = db.relationship('CheckStatus', foreign_keys=[CAN_check])
    default_fuel_sens = db.relationship('CheckStatus', foreign_keys=[default_fuel_sens_check])
    fuel_sens = db.relationship('CheckStatus', foreign_keys=[fuel_sens_check])
    temp_sens = db.relationship('CheckStatus', foreign_keys=[temp_sens_check])
    reed_switch = db.relationship('CheckStatus', foreign_keys=[reed_switch_check])
    angle_sens = db.relationship('CheckStatus', foreign_keys=[angle_sens_check])
    dismantling_tank = db.relationship('CheckStatus', foreign_keys=[dismantling_tank_check])

    relationship_filters = [("category", AutoCategory)]
    
    column_labels = dict(
        category="Категория авто",
        brand="Марка",
        model="Модель",
        year="Год выпуска",
        monitoring="Мониторинг",
        safe_block="Безопасная блокиовка",
        danger_block="Опасная блокировка",
        CAN="CAN",
        default_fuel_sens="Штатный ДУТ",
        fuel_sens="ДУТ",
        temp_sens="Датчик температуры",
        reed_switch="Геркон",
        angle_sens="Датчик угла наклона",
        first_tank_volume="Первый бак, л.",
        second_tank_volume="Второй бак, л.",
        third_tank_volume="Третий бак, л.",
        dismantling_tank="Демонтаж бака",
        equipment="Установленное борудование",
        mounting="Возможность установки",
        pyrus_link="Pyrus",
        docs="Материалы",
        note="Примечание",
        created_at="Дата создания",
        updated_at="Дата изменения"
    )
    column_labels.update(
        {
            "category.name": "Категория авто"
        }
    )

    def __str__(self):
        return f"{self.brand} {self.model} {self.year}"

