import unittest
from unittest.mock import patch

from game.factory import BASE_CHARACTERISTICS, LEVEL_INCREASING_FACTOR, AbstractPerson, Human, Elf, Orc
from .mocked_tests import MockedHP, MockedStamina, MockedMana


class AbstractPersonTest(unittest.TestCase):
    @patch('game.factory.Mana')
    @patch('game.factory.Stamina')
    @patch('game.factory.HP')
    @patch.multiple(AbstractPerson, __abstractmethods__=set())
    def setUp(self, mocked_hp, mocked_stamina, mocked_mana):
        mocked_hp.return_value = 'hp'
        mocked_stamina.return_value = 'stamina'
        mocked_mana.return_value = 'mana'
        self.abstract_person = AbstractPerson(2)

    def test_init(self):
        self.assertEqual(self.abstract_person.hp, 'hp')
        self.assertEqual(self.abstract_person.stamina, 'stamina')
        self.assertEqual(self.abstract_person.mana, 'mana')
        self.assertEqual(self.abstract_person.level_increasing_factor, 1.05)

    def test_hit(self):
        with self.assertRaises(NotImplementedError):
            self.abstract_person.hit()

    def test_heal(self):
        with self.assertRaises(NotImplementedError):
            self.abstract_person.heal()


class HumanTest(unittest.TestCase):
    @patch.multiple(AbstractPerson, __abstractmethods__=set())
    def setUp(self):
        self.human_1_level = Human()
        self.human_3_level = Human(3)

    def test_init(self):
        self.assertEqual(self.human_1_level.base_hit, BASE_CHARACTERISTICS['human']['base_hit'])
        self.assertEqual(self.human_1_level.base_heal, BASE_CHARACTERISTICS['human']['base_heal'])
        self.assertEqual(self.human_1_level.base_heal_cost, BASE_CHARACTERISTICS['human']['base_heal_cost'])
        self.assertEqual(self.human_1_level.hp_multiplier, BASE_CHARACTERISTICS['human']['hp_multiplier'])
        self.assertEqual(self.human_1_level.stamina_multiplier, BASE_CHARACTERISTICS['human']['stamina_multiplier'])
        self.assertEqual(self.human_1_level.mana_multiplier, BASE_CHARACTERISTICS['human']['mana_multiplier'])
        self.assertEqual(self.human_1_level.hp.stat_value, 1000)
        self.assertEqual(self.human_1_level.stamina.stat_value, 1000)
        self.assertEqual(self.human_1_level.mana.stat_value, 1000)

        self.assertEqual(self.human_3_level.base_hit, BASE_CHARACTERISTICS['human']['base_hit'] *
                         (1 + LEVEL_INCREASING_FACTOR) ** 2)
        self.assertEqual(self.human_3_level.base_heal, BASE_CHARACTERISTICS['human']['base_heal']*
                         (1 + LEVEL_INCREASING_FACTOR) ** 2)
        self.assertEqual(self.human_3_level.base_heal_cost, BASE_CHARACTERISTICS['human']['base_heal_cost']*
                         (1 + LEVEL_INCREASING_FACTOR) ** 2)
        self.assertEqual(self.human_3_level.hp_multiplier, BASE_CHARACTERISTICS['human']['hp_multiplier'])
        self.assertEqual(self.human_3_level.stamina_multiplier, BASE_CHARACTERISTICS['human']['stamina_multiplier'])
        self.assertEqual(self.human_3_level.mana_multiplier, BASE_CHARACTERISTICS['human']['mana_multiplier'])
        self.assertEqual(self.human_3_level.hp.stat_value, 1102)
        self.assertEqual(self.human_3_level.stamina.stat_value, 1166)
        self.assertEqual(self.human_3_level.mana.stat_value, 1210)

    def test_hit(self):
        hit_1 = self.human_1_level.hit()
        self.assertEqual(hit_1, 100)
        self.assertEqual(self.human_1_level.hp.stat_value, 1000)

        hit_3 = self.human_3_level.hit()
        self.assertEqual(hit_3, 110.25)
        self.assertEqual(self.human_3_level.hp.stat_value, 1102)

        self.human_1_level.hp.change(-50, True)
        hit_1 = self.human_1_level.hit()
        self.assertEqual(hit_1, 100)
        self.assertEqual(self.human_1_level.hp.stat_value, 520)

    def test_heal(self):
        self.assertEqual(self.human_1_level.hp.stat_value, 1000)

        self.human_1_level.hp.change(-150)
        self.human_1_level.heal()
        self.assertEqual(self.human_1_level.hp.stat_value, 950)
        self.assertEqual(self.human_1_level.mana.stat_value, 900)

        self.human_1_level.heal()
        self.assertEqual(self.human_1_level.hp.stat_value, 1000)
        self.assertEqual(self.human_1_level.mana.stat_value, 800)

        self.assertEqual(self.human_3_level.hp.stat_value, 1102)
        self.human_3_level.hp.change(-602)
        self.human_3_level.heal()
        self.assertEqual(self.human_3_level.hp.stat_value, 610)
        self.assertEqual(self.human_3_level.mana.stat_value, 1099)


class ElfTest(unittest.TestCase):
    @patch.multiple(AbstractPerson, __abstractmethods__=set())
    def setUp(self):
        self.elf_1_level = Elf()
        self.elf_3_level = Elf(3)

    def test_init(self):
        self.assertEqual(self.elf_1_level.base_hit, BASE_CHARACTERISTICS['elf']['base_hit'])
        self.assertEqual(self.elf_1_level.base_heal, BASE_CHARACTERISTICS['elf']['base_heal'])
        self.assertEqual(self.elf_1_level.base_heal_cost, BASE_CHARACTERISTICS['elf']['base_heal_cost'])
        self.assertEqual(self.elf_1_level.hit_mana_cost, BASE_CHARACTERISTICS['elf']['hit_mana_cost'])
        self.assertEqual(self.elf_1_level.hp_multiplier, BASE_CHARACTERISTICS['elf']['hp_multiplier'])
        self.assertEqual(self.elf_1_level.stamina_multiplier, BASE_CHARACTERISTICS['elf']['stamina_multiplier'])
        self.assertEqual(self.elf_1_level.mana_multiplier, BASE_CHARACTERISTICS['elf']['mana_multiplier'])
        self.assertEqual(self.elf_1_level.hp.stat_value, 800)
        self.assertEqual(self.elf_1_level.stamina.stat_value, 800)
        self.assertEqual(self.elf_1_level.mana.stat_value, 1500)

        self.assertEqual(self.elf_3_level.base_hit, BASE_CHARACTERISTICS['elf']['base_hit'] *
                         (1 + LEVEL_INCREASING_FACTOR) ** 2)
        self.assertEqual(self.elf_3_level.base_heal, BASE_CHARACTERISTICS['elf']['base_heal'] *
                         (1 + LEVEL_INCREASING_FACTOR) ** 2)
        self.assertEqual(self.elf_3_level.base_heal_cost, BASE_CHARACTERISTICS['elf']['base_heal_cost'] *
                         (1 + LEVEL_INCREASING_FACTOR) ** 2)
        self.assertEqual(self.elf_3_level.hit_mana_cost, BASE_CHARACTERISTICS['elf']['hit_mana_cost'] *
                         (1 + LEVEL_INCREASING_FACTOR) ** 2)
        self.assertEqual(self.elf_3_level.hp_multiplier, BASE_CHARACTERISTICS['elf']['hp_multiplier'])
        self.assertEqual(self.elf_3_level.stamina_multiplier, BASE_CHARACTERISTICS['elf']['stamina_multiplier'])
        self.assertEqual(self.elf_3_level.mana_multiplier, BASE_CHARACTERISTICS['elf']['mana_multiplier'])
        self.assertEqual(self.elf_3_level.hp.stat_value, 882)
        self.assertEqual(self.elf_3_level.stamina.stat_value, 933)
        self.assertEqual(self.elf_3_level.mana.stat_value, 1815)

    def test_hit(self):
        hit_1 = self.elf_1_level.hit()
        self.assertEqual(hit_1, 200.0)
        self.assertEqual(self.elf_1_level.hp.stat_value, 800)

        hit_3 = self.elf_3_level.hit()
        self.assertEqual(hit_3, 220.5)
        self.assertEqual(self.elf_3_level.hp.stat_value, 882)

        self.elf_1_level.hp.change(-50, True)
        hit_1 = self.elf_1_level.hit()
        self.assertEqual(hit_1, 200.0)
        self.assertEqual(self.elf_1_level.hp.stat_value, 400)

    def test_heal(self):
        self.assertEqual(self.elf_1_level.hp.stat_value, 800)
        self.assertEqual(self.elf_1_level.mana.stat_value, 1500)

        self.elf_1_level.hp.change(-250)
        self.elf_1_level.heal()
        self.assertEqual(self.elf_1_level.hp.stat_value, 700)
        self.assertEqual(self.elf_1_level.mana.stat_value, 1400)

        self.elf_1_level.heal()
        self.assertEqual(self.elf_1_level.hp.stat_value, 800)
        self.assertEqual(self.elf_1_level.mana.stat_value, 1300)

        self.assertEqual(self.elf_3_level.hp.stat_value, 882)
        self.elf_3_level.hp.change(-482)
        self.elf_3_level.heal()
        self.assertEqual(self.elf_3_level.hp.stat_value, 565)
        self.assertEqual(self.elf_3_level.mana.stat_value, 1704)
