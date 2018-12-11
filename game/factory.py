from abc import ABCMeta, abstractmethod

from game.stats import HP, Stamina, Mana

LEVEL_INCREASING_FACTOR = 0.05

BASE_CHARACTERISTICS = {
    'human': {
        'base_hit': 100,
        'base_heal': 100,
        'base_heal_cost': 100,
        'hp_multiplier': 1,
        'stamina_multiplier': 1,
        'mana_multiplier': 1
    },
    'elf': {
        'base_hit': 200,
        'base_heal': 150,
        'base_heal_cost': 100,
        'hp_multiplier': 0.8,
        'stamina_multiplier': 0.8,
        'mana_multiplier': 1.5,
        'hit_mana_cost': 150,
    }
}


class AbstractPerson(metaclass=ABCMeta):
    hp_multiplier = 1
    stamina_multiplier = 1
    mana_multiplier = 1

    @abstractmethod
    def __init__(self, level=1, *args, **kwargs):
        self.level = level
        self.hp = HP(self.hp_multiplier, self.level)
        self.stamina = Stamina(self.stamina_multiplier, self.level)
        self.mana = Mana(self.mana_multiplier, self.level)
        self.level_increasing_factor = (1 + LEVEL_INCREASING_FACTOR) ** (level - 1)

    @abstractmethod
    def hit(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def heal(self, *args, **kwargs):
        raise NotImplementedError


class Human(AbstractPerson):
    def __init__(self, level=1, *args, **kwargs):
        for key in BASE_CHARACTERISTICS['human'].keys():
            self.__dict__[key] = BASE_CHARACTERISTICS['human'][key]
        super().__init__(level=level, *args, **kwargs)
        self.base_hit = self.base_hit * self.level_increasing_factor
        self.base_heal = self.base_heal * self.level_increasing_factor
        self.base_heal_cost = self.base_heal_cost * self.level_increasing_factor

    def hit(self, *args, **kwargs):
        heal = 0.2 * self.base_heal
        self.hp.change(heal)
        return self.base_hit

    def heal(self):
        self.mana.change(-self.base_heal_cost)
        self.hp.change(self.base_heal)


class Elf(AbstractPerson):
    def __init__(self, level=1, *args, **kwargs):
        for key in BASE_CHARACTERISTICS['elf'].keys():
            self.__dict__[key] = BASE_CHARACTERISTICS['elf'][key]
        super().__init__(level=level, *args, **kwargs)
        self.base_hit = self.base_hit * self.level_increasing_factor
        self.base_heal = self.base_heal * self.level_increasing_factor
        self.base_heal_cost = self.base_heal_cost * self.level_increasing_factor
        self.hit_mana_cost = self.hit_mana_cost * self.level_increasing_factor

    def hit(self, *args, **kwargs):
        if self.mana.check_value(self.hit_mana_cost):
            self.mana.change(-self.hit_mana_cost)
            return self.base_hit
        self.mana.change(-self.hit_mana_cost)
        return self.base_hit * 0.3

    def heal(self):
        self.mana.change(-self.base_heal_cost)
        self.hp.change(self.base_heal)


class Orc(AbstractPerson):
    base_hit = 300
    base_heal = 150

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hp = BASE_HP * 1.4
        self.stamina = BASE_STAMINA * 1.2
        self.mana = BASE_MANA * 0

        self.hit_strenght = self.BASE_HIT_STRENGHT
        self.heal = self.BASE_HEAL
        self.food = 0

    def hit(self, *args, **kwargs):
        return self.base_hit

    def heal(self):
        if self.food:
            self.food -= 1
            new_hp = self.hp + self.heal
            self.hp = new_hp if new_hp <= BASE_HP else BASE_HP


class PersonFactory:
    __person_classes = {
        'human': Human,
        'elf': Elf,
        'orc': Orc
    }

    @staticmethod
    def get_person(name, *args, **kwargs):
        person = PersonFactory.__person_classes.get(name.lower(), None)

        if person:
            return person(*args, **kwargs)
        raise NotImplementedError(f"Personage {name} wasn't implemented")


if __name__ == '__main__':
    person = PersonFactory.get_person('human')
    print(person.hp)
    print(person.base_heal_cost)

    # elf = PersonFactory.get_person('elf')
    # print(elf.hp, elf.mana)
