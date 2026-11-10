def get_currencies(currencies_ids_lst: list[str]) -> list[dict]:
    import requests
    from xml.etree import ElementTree as ET  # TODO 1: Исследовать самостоятельно есть ли более оптимальная библиотека для парсинга XML или

    # посмотреть есть ли возможность использовать у ЦБ другой API для получения json изначально

    cur_res_str = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
    result = []

    root = ET.fromstring(cur_res_str.content)
    valutes = root.findall(
        "Valute"
    )  # исследовать, есть ли отдельный метод получения валют с опреденным id
    # если да, упростить алгоритм ниже
    for _v in valutes:
        valute_id = _v.get('ID')
        valute = {}
        if (str(valute_id) in currencies_ids_lst):
            valute_cur_name, valute_cur_val = _v.find('Name').text, _v.find(
                'Value').text
            valute_charcode = _v.find('CharCode').text
            # новое: целая и дробная части курса — отдельно
            valute_int, valute_frac = valute_cur_val.split(',')
            # новое: номинал валюты (если не 1 — сохраняем)
            valute_nominal = _v.find('Nominal').text
            valute[valute_charcode] = (
                valute_cur_name, (valute_int, valute_frac), valute_nominal
            )
            result.append(valute)

    return result


class CurrenciesLst():

    def __init__(self, currencies_ids_lst=None):
        # новый атрибут для входных параметров
        self.__currencies_ids_lst = list(currencies_ids_lst or [])
        # значения хранятся отдельно: целая и дробная часть курса + номинал
        self.__cur_lst = [{
            'GBP': ('Фунт стерлингов Соединенного королевства', ('113', '2069'), '1')
        }, {
            'KZT': ('Казахстанских тенге', ('19', '8264'), '100')
        }, {
            'TRY': ('Турецких лир', ('33', '1224'), '10')
        }]

    def __del__(self):
        # деструктор для атрибутов (по требованию задания)
        print(f"[CurrenciesLst] уничтожен объект id={id(self)}")

    # ---------- геттер и сеттер входных параметров ----------
    @property
    def currencies_ids_lst(self):
        return self.__currencies_ids_lst

    @currencies_ids_lst.setter
    def currencies_ids_lst(self, value):
        if not isinstance(value, list):
            raise TypeError("currencies_ids_lst должен быть списком")
        self.__currencies_ids_lst = [str(x) for x in value]

    # ---------- геттер и сеттер результата ----------
    @property
    def cur_lst(self):
        return self.__cur_lst

    @cur_lst.setter
    def cur_lst(self, value):
        if not isinstance(value, list):
            raise TypeError("cur_lst должен быть списком")
        self.__cur_lst = value

    # ---------- метод получения валюты (использует исходную get_currencies) ----------
    def get_currencies(self):
        self.__cur_lst = get_currencies(self.__currencies_ids_lst)
        return self.__cur_lst

    def visualize_currencies(self):
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        currencies = []
        for el in self.__cur_lst:
            currencies.append(str(el.keys()))

        print(currencies)
        # fruits = ['apple', 'blueberry', 'cherry', 'orange']
        # counts = [40, 100, 30, 55]
        # bar_labels = ['red', 'blue', '_red', 'orange']
        # bar_colors = ['tab:red', 'tab:blue', 'tab:red', 'tab:orange']

        # ax.bar(fruits, counts, label=bar_labels, color=bar_colors)

        # ax.set_ylabel('fruit supply')
        # ax.set_title('Fruit supply by kind and color')
        # ax.legend(title='Fruit color')

        # plt.show()

        # обращается к атрибуту __cur_lst, преобразовывать значения курсов валют в нужный формат и выводить эти данные в файл

        # self.__cur_lst


if __name__ == '__main__':

    res = get_currencies(['R01035', 'R01335', 'R01700J'])
    if res:
        print(get_currencies(['R01035', 'R01335', 'R01700J']))