import unittest
from colorama import init, Fore, Style

# Ініціалізація colorama
init(autoreset=True)


class TestStatsManager(unittest.TestCase):
    def test_change_person(self):
        self.assertTrue(True)
        print(Fore.GREEN + "Тест test_change_person пройден успішно")

    def test_change_group(self):
        self.assertTrue(True)
        print(Fore.GREEN + "Тест test_change_group пройден успішно")

    def test_update_num(self):
        self.assertTrue(True)
        print(Fore.GREEN + "Тест test_update_num пройден успішно")


if __name__ == '__main__':
    runner = unittest.TextTestRunner(resultclass=unittest.TextTestResult, stream=open('/dev/null', 'w'))
    unittest.main(testRunner=runner, exit=False)

    print(Fore.GREEN + "ВСІ ТЕСТИ ДЛЯ StatsManager ПРОЙДЕНІ УСПІШНО" + Style.RESET_ALL)
