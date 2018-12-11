import unittest
from unittest.mock import patch

from game.stats import BaseStats, HP, Stamina, Mana


class BaseStatsTest(unittest.TestCase):
    def test_value(self):
        base_stats = BaseStats()
        with self.assertRaises(NotImplementedError):
            base_stats.stat_value()

    def test_get_normal_value(self):
        base_stats = BaseStats()

        result = base_stats.get_normal_value()
        self.assertEqual(result, 1000)

        result = base_stats.get_normal_value(1000, 1, 1.1, 1)
        self.assertEqual(result, 1100)

        result = base_stats.get_normal_value(1000, 1, 1.1, 2)
        self.assertEqual(result, 1111)

        with self.assertRaises(TypeError):
            base_stats.get_normal_value('1000', 1, 1.1, 2)

        with self.assertRaises(TypeError):
            base_stats.get_normal_value(1000, '1', 1.1, 2)

        with self.assertRaises(TypeError):
            base_stats.get_normal_value(1000, 1, '1.1', 2)

        with self.assertRaises(TypeError):
            base_stats.get_normal_value(1000, 1, 1.1, '2')

        result = base_stats.get_normal_value(1000.2, 1, 1.1, 2)
        self.assertEqual(result, 1111)

    def test_cahnge(self):
        base_stats = BaseStats()
        base_stats.normal_value = 100
        base_stats._value = 100

        r = base_stats.change(-10)
        self.assertEqual(r, 90)

        r = base_stats.change(-10, True)
        self.assertEqual(r, 80)

        r = base_stats.change(30, True)
        self.assertEqual(r, 100)

        base_stats.normal_value = 200
        base_stats._value = 15
        r = base_stats.change(7, True)
        self.assertEqual(r, 29)

        r = base_stats.change(-15, True)
        self.assertEqual(r, 0)


class HPTest(unittest.TestCase):
    @patch('game.stats.HP.get_normal_value')
    def test_init(self, mocked_normal_value):
        mocked_normal_value.return_value = 2000
        hp = HP(1.1, 1)
        self.assertEqual(hp.normal_value, 2000)
        self.assertEqual(hp._value, 2000)

    @patch('game.stats.HP.get_normal_value')
    def test_value(self, mocked_normal_value):
        mocked_normal_value.return_value = 2000
        hp = HP(1.1, 1)
        self.assertEqual(hp.stat_value, 2000)

    @patch('game.stats.HP.get_normal_value')
    def test_str(self, mocked_normal_value):
        mocked_normal_value.return_value = 2000
        hp = HP(1.1, 1)
        self.assertEqual(str(hp), 'Current HP: 2000 (100.0%)')

        hp._value = 1010
        self.assertEqual(str(hp), 'Current HP: 1010 (50.5%)')

        hp._value = 123
        self.assertEqual(str(hp), 'Current HP: 123 (6.15%)')

        hp._value = 0
        self.assertEqual(str(hp), 'Current HP: 0 (0.0%)')

        mocked_normal_value.return_value = 3000
        hp = HP(1.1, 1)
        hp._value = 1010
        self.assertEqual(str(hp), 'Current HP: 1010 (33.67%)')

        hp._value = 1
        self.assertEqual(str(hp), 'Current HP: 1 (0.03%)')

        mocked_normal_value.return_value = 30000
        hp = HP(1.1, 1)
        hp._value = 1
        self.assertEqual(str(hp), 'Current HP: 1 (0.01%)')


class TestStamina(unittest.TestCase):
    @patch('game.stats.Stamina.get_normal_value')
    def test_init(self, mocked_normal_value):
        mocked_normal_value.return_value = 2000
        stamina = Stamina(1.1, 1)
        self.assertEqual(stamina.normal_value, 2000)
        self.assertEqual(stamina.stat_value, 2000)
        self.assertEqual(str(stamina), 'Stamina: 2000')


class ManaTest(unittest.TestCase):
    @patch('game.stats.Mana.get_normal_value')
    def test_init(self, mocked_normal_value):
        mocked_normal_value.return_value = 2000
        mana = Mana(1.1, 1)
        self.assertEqual(mana.normal_value, 2000)
        self.assertEqual(mana._value, 2000)

    @patch('game.stats.Mana.get_normal_value')
    def test_value(self, mocked_normal_value):
        mocked_normal_value.return_value = 2000
        mana = Mana(1.1, 1)
        self.assertEqual(mana.stat_value, 2000)

    @patch('game.stats.Mana.get_normal_value')
    def test_check_value(self, mocked_normal_value):
        mocked_normal_value.return_value = 2000
        mana = Mana(1.1, 1)
        mana._value = 150

        result = mana.check_value(100)
        self.assertTrue(result)

        result = mana.check_value(200)
        self.assertFalse(result)

    @patch('game.stats.Mana.get_normal_value')
    def test_str(self, mocked_normal_value):
        mocked_normal_value.return_value = 2000
        mana = Mana(1.1, 1)
        self.assertEqual(str(mana), 'Current Mana: 2000 (100.0%)')

        mana._value = 1010
        self.assertEqual(str(mana), 'Current Mana: 1010 (50.5%)')

        mana._value = 123
        self.assertEqual(str(mana), 'Current Mana: 123 (6.15%)')

        mana._value = 0
        self.assertEqual(str(mana), 'Current Mana: 0 (0.0%)')

        mocked_normal_value.return_value = 3000
        mana = Mana(1.1, 1)
        mana._value = 1010
        self.assertEqual(str(mana), 'Current Mana: 1010 (33.67%)')

        mana._value = 1
        self.assertEqual(str(mana), 'Current Mana: 1 (0.03%)')

        mocked_normal_value.return_value = 30000
        mana = Mana(1.1, 1)
        mana._value = 1
        self.assertEqual(str(mana), 'Current Mana: 1 (0.01%)')

