import time


def get_currencies(currencies_ids_lst: list) -> list:
    import requests
    from xml.etree import ElementTree as ET

    cur_res_str = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
    result = []

    root = ET.fromstring(cur_res_str.content)
    valutes = root.findall("Valute")

    found_ids = set()

    for _v in valutes:
        valute_id = _v.get('ID')
        valute = {}
        if (str(valute_id) in currencies_ids_lst):
            valute_cur_name, valute_cur_val = _v.find('Name').text, _v.find(
                'Value').text
            valute_charcode = _v.find('CharCode').text
            valute_int, valute_frac = valute_cur_val.split(',')
            valute_nominal = _v.find('Nominal').text
            valute[valute_charcode] = (
                valute_cur_name, (valute_int, valute_frac), valute_nominal
            )
            result.append(valute)
            found_ids.add(str(valute_id))

    for cid in currencies_ids_lst:
        if str(cid) not in found_ids:
            result.append({str(cid): None})

    return result


class CurrenciesLst():

    def __init__(self, currencies_ids_lst=None, min_interval_sec=1.0):
        self.__currencies_ids_lst = list(currencies_ids_lst or [])
        self.__min_interval_sec = float(min_interval_sec)
        self.__last_request_time = None
        self.__cur_lst = [{
            'GBP': ('Фунт стерлингов Соединенного королевства', ('113', '2069'), '1')
        }, {
            'KZT': ('Казахстанских тенге', ('19', '8264'), '100')
        }, {
            'TRY': ('Турецких лир', ('33', '1224'), '10')
        }]

    def __del__(self):
        print(f"[CurrenciesLst] уничтожен объект id={id(self)}")

    @property
    def currencies_ids_lst(self):
        return self.__currencies_ids_lst

    @currencies_ids_lst.setter
    def currencies_ids_lst(self, value):
        if not isinstance(value, list):
            raise TypeError("currencies_ids_lst должен быть списком")
        self.__currencies_ids_lst = [str(x) for x in value]

    @property
    def cur_lst(self):
        return self.__cur_lst

    @cur_lst.setter
    def cur_lst(self, value):
        if not isinstance(value, list):
            raise TypeError("cur_lst должен быть списком")
        self.__cur_lst = value

    @property
    def min_interval_sec(self):
        return self.__min_interval_sec

    @min_interval_sec.setter
    def min_interval_sec(self, value):
        value = float(value)
        if value < 0:
            raise ValueError("min_interval_sec не может быть отрицательным")
        self.__min_interval_sec = value

    def get_currencies(self):
        now = time.monotonic()
        if (self.__last_request_time is not None
                and now - self.__last_request_time < self.__min_interval_sec):
            print(f"[CurrenciesLst] слишком часто: прошло "
                  f"{now - self.__last_request_time:.3f} с, "
                  f"нужно {self.__min_interval_sec} с — возвращаю кеш")
            return self.__cur_lst

        self.__cur_lst = get_currencies(self.__currencies_ids_lst)
        self.__last_request_time = time.monotonic()
        return self.__cur_lst

    def visualize_currencies(self, filename='currencies.jpg'):
        """Получает курсы валют (если их нет) и строит график в filename."""
        if not self.__cur_lst:
            self.get_currencies()

        labels = []
        values = []
        for item in self.__cur_lst:
            for code, data in item.items():
                if data is None:
                    continue
                name, (int_part, frac_part), nominal = data
                rate = float(f'{int_part}.{frac_part}') / float(nominal)
                labels.append(code)
                values.append(rate)

        if not labels:
            print('Нет данных для визуализации — сначала вызовите get_currencies()')
            return None

        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(labels, values, color='steelblue')
        ax.set_xlabel('Валюта')
        ax.set_ylabel('Курс, руб. за 1 единицу')
        ax.set_title('Курсы валют ЦБ РФ')
        ax.bar_label(bars, fmt='%.2f', padding=3)
        fig.tight_layout()

        fig.savefig(filename, dpi=150)
        plt.close(fig)
        print(f'График сохранён в {filename}')
        return filename


if __name__ == '__main__':

    res = get_currencies(['R01035', 'R01335', 'R01700J'])
    if res:
        print(get_currencies(['R01035', 'R01335', 'R01700J']))

    print(get_currencies(['R9999']))
    print(get_currencies(['R01035', 'R9999']))

    cl = CurrenciesLst(['R01035'], min_interval_sec=1.0)
    print(cl.get_currencies())
    print(cl.get_currencies())
    time.sleep(1.1)
    print(cl.get_currencies())

    cl_viz = CurrenciesLst(['R01035', 'R01335', 'R01700J'])
    cl_viz.visualize_currencies('currencies.jpg')