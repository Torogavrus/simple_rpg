from abc import ABCMeta, abstractmethod


BASE_HP = 1000
HP_LEVEL_INCREASING = 5
HP_LOW_LEVEL = 10

BASE_STAMINA = 1000
STAMINA_LEVEL_INCREASING = 8

BASE_MANA = 1000
MANA_LEVEL_INCREASING = 10
MANA_LOW_LEVEL = 10


class BaseStats(metaclass=ABCMeta):
    normal_value = 0
    _value = 0

    @property
    def stat_value(self):
        raise NotImplementedError

    def get_normal_value(self,
                         base_value: int =1000,
                         level_increasing: float =1.0,
                         race_multiplier: float =1,
                         level: int =1):
        return int(base_value * race_multiplier * (1 + level_increasing / 100) ** (level - 1))

    def change(self, amount, percent=None):
        if percent:
            self._value = int(self._value + self.normal_value * amount / 100)
        else:
            self._value = int(self._value + amount)

        if self._value > self.normal_value:
            self._value = self.normal_value
        if self._value < 0:
            self._value = 0

        return self._value


class HP(BaseStats):
    def __init__(self, race_multiplier, level):
        self.normal_value = self.get_normal_value(BASE_HP, HP_LEVEL_INCREASING, race_multiplier, level)
        self._value = self.normal_value

    @property
    def stat_value(self):
        if self._value == 0:
            system_print('Person is dead')
        elif self._value < int(self.normal_value * HP_LOW_LEVEL / 100):
            system_print(f'HP level is less then {HP_LOW_LEVEL}%')
        return self._value

    def __str__(self):
        hp_percent = self._value / self.normal_value * 100
        if hp_percent > 0 and hp_percent < 0.01:
            hp_percent = 0.01
        else:
            hp_percent = round(hp_percent, 2)
        return f'Current HP: {self._value} ({hp_percent}%)'


class Stamina(BaseStats):
    def __init__(self, race_multiplier, level):
        self.normal_value = self.get_normal_value(BASE_STAMINA, STAMINA_LEVEL_INCREASING, race_multiplier, level)

    @property
    def stat_value(self):
        return self.normal_value

    def __str__(self):
        return f'Stamina: {self.normal_value}'


class Mana(BaseStats):
    def __init__(self, race_multiplier, level):
        self.normal_value = self.get_normal_value(BASE_MANA, MANA_LEVEL_INCREASING, race_multiplier, level)
        self._value = self.normal_value

    @property
    def stat_value(self):
        if self._value == 0:
            system_print('Your mana is )')
        elif self._value < int(self.normal_value * MANA_LOW_LEVEL / 100):
            system_print('Mana level is less then 10%')
        return self._value

    def check_value(self, needed_mana):
        if needed_mana <= self._value:
            return True
        else:
            system_print('You dont have enougth mana')
            return False

    def __str__(self):
        mana_percent = self._value / self.normal_value * 100
        if mana_percent > 0 and mana_percent < 0.01:
            mana_percent = 0.01
        else:
            mana_percent = round(mana_percent, 2)
        return f'Current Mana: {self._value} ({mana_percent}%)'


def system_print(msg):
    # temporary implementation
    print(msg)
