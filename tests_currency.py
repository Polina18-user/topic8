"""Тесты для get_currencies на unittest."""
import unittest

from currency_fetcher import get_currencies  # подставьте имя своего модуля


class TestGetCurrencies(unittest.TestCase):
    """Тесты функции get_currencies."""

    # ---------- тест на неправильный ID ----------
    def test_invalid_id_returns_none(self):
        """Несуществующий ID 'R9999' -> [{'R9999': None}]."""
        result = get_currencies(['R9999'])
        self.assertEqual(result, [{'R9999': None}])

    # ---------- корректный ID: GBP ----------
    def test_valid_gbp_name_and_value_range(self):
        """GBP: русскоязычное название и курс в диапазоне (0, 999)."""
        result = get_currencies(['R01035'])  # GBP
        self.assertEqual(len(result), 1)

        item = result[0]
        self.assertIn('GBP', item)

        name, (int_part, frac_part), nominal = item['GBP']
        # 1) название русскоязычное — содержит «Фунт»
        self.assertIn('Фунт', name)
        # 2) курс в диапазоне 0..999
        value = float(f'{int_part}.{frac_part}')
        self.assertGreater(value, 0)
        self.assertLess(value, 999)

    # ---------- корректный ID: KZT ----------
    def test_valid_kzt_name_and_value_range(self):
        """KZT: русскоязычное название и курс в диапазоне (0, 999)."""
        result = get_currencies(['R01335'])  # KZT
        self.assertEqual(len(result), 1)

        item = result[0]
        self.assertIn('KZT', item)

        name, (int_part, frac_part), nominal = item['KZT']
        self.assertIn('тенге', name.lower())
        value = float(f'{int_part}.{frac_part}')
        self.assertGreater(value, 0)
        self.assertLess(value, 999)


if __name__ == '__main__':
    unittest.main()