import json
import os

# Имя файла, куда сохраняем все данные
DATA_FILE = "autopark.json"


# ====================== БАЗОВЫЙ КЛАСС ======================
# От него будет наследоваться Driver (водитель)
class Person:
    def __init__(self, name, phone):
        # Прячем поля через _ (инкапсуляция)
        self._name = name
        self._phone = phone

    # Геттеры и сеттеры через свойства (доступ к закрытым полям)
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = value

    # Метод info будет переопределяться у наследников (полиморфизм)
    def info(self):
        return f"Имя: {self._name}, Телефон: {self._phone}"


# ====================== ВОДИТЕЛЬ ======================
class Driver(Person):
    def __init__(self, driver_id, name, phone, license_category):
        # Вызываем конструктор родителя
        super().__init__(name, phone)
        self._driver_id = driver_id
        self._license_category = license_category  # категория прав (B, C и т.д.)

    @property
    def driver_id(self):
        return self._driver_id

    @property
    def license_category(self):
        return self._license_category

    # Переопределяем info (полиморфизм)
    def info(self):
        return (f"ID: {self._driver_id}, Имя: {self._name}, "
                f"Телефон: {self._phone}, Категория прав: {self._license_category}")

    # Превращаем объект в словарь, чтобы сохранить в JSON
    def to_dict(self):
        return {
            "driver_id": self._driver_id,
            "name": self._name,
            "phone": self._phone,
            "license_category": self._license_category
        }

    # Создаём объект Driver из словаря (при загрузке из файла)
    @staticmethod
    def from_dict(d):
        return Driver(d["driver_id"], d["name"], d["phone"], d["license_category"])


# ====================== АВТОМОБИЛЬ ======================
class Car:
    def __init__(self, number, brand, year):
        self._number = number  # гос. номер (используем как id)
        self._brand = brand
        self._year = year

    @property
    def number(self):
        return self._number

    @property
    def brand(self):
        return self._brand

    @property
    def year(self):
        return self._year

    def info(self):
        return f"Номер: {self._number}, Марка: {self._brand}, Год: {self._year}"

    def to_dict(self):
        return {
            "number": self._number,
            "brand": self._brand,
            "year": self._year
        }

    @staticmethod
    def from_dict(d):
        return Car(d["number"], d["brand"], d["year"])


# ====================== РЕЙС ======================
class Trip:
    def __init__(self, trip_id, driver_id, car_number, route, date):
        self._trip_id = trip_id
        self._driver_id = driver_id      # какой водитель
        self._car_number = car_number    # какая машина
        self._route = route              # маршрут
        self._date = date                # дата

    @property
    def trip_id(self):
        return self._trip_id

    @property
    def driver_id(self):
        return self._driver_id

    @property
    def car_number(self):
        return self._car_number

    def info(self):
        return (f"ID рейса: {self._trip_id}, Водитель(ID): {self._driver_id}, "
                f"Машина: {self._car_number}, Маршрут: {self._route}, Дата: {self._date}")

    def to_dict(self):
        return {
            "trip_id": self._trip_id,
            "driver_id": self._driver_id,
            "car_number": self._car_number,
            "route": self._route,
            "date": self._date
        }

    @staticmethod
    def from_dict(d):
        return Trip(d["trip_id"], d["driver_id"], d["car_number"], d["route"], d["date"])


# ====================== ТЕХОБСЛУЖИВАНИЕ ======================
class Maintenance:
    def __init__(self, maint_id, car_number, description, date, cost):
        self._maint_id = maint_id
        self._car_number = car_number    # какая машина
        self._description = description   # что делали
        self._date = date
        self._cost = cost                # стоимость

    @property
    def maint_id(self):
        return self._maint_id

    @property
    def car_number(self):
        return self._car_number

    @property
    def cost(self):
        return self._cost

    def info(self):
        return (f"ID ТО: {self._maint_id}, Машина: {self._car_number}, "
                f"Работы: {self._description}, Дата: {self._date}, Стоимость: {self._cost}")

    def to_dict(self):
        return {
            "maint_id": self._maint_id,
            "car_number": self._car_number,
            "description": self._description,
            "date": self._date,
            "cost": self._cost
        }

    @staticmethod
    def from_dict(d):
        return Maintenance(d["maint_id"], d["car_number"], d["description"], d["date"], d["cost"])


# ====================== ГЛАВНЫЙ КЛАСС АВТОПАРК ======================
class AutoPark:
    def __init__(self):
        # Списки всех объектов
        self._drivers = []
        self._cars = []
        self._trips = []
        self._maintenances = []

    # --------- РАБОТА С ФАЙЛОМ ---------
    def save(self):
        # Собираем все данные в один большой словарь
        data = {
            "drivers": [d.to_dict() for d in self._drivers],
            "cars": [c.to_dict() for c in self._cars],
            "trips": [t.to_dict() for t in self._trips],
            "maintenances": [m.to_dict() for m in self._maintenances]
        }
        # Записываем в JSON файл
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("Данные сохранены!")

    def load(self):
        # Если файла нет - ничего не загружаем
        if not os.path.exists(DATA_FILE):
            return
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Восстанавливаем объекты из словарей
        self._drivers = [Driver.from_dict(d) for d in data.get("drivers", [])]
        self._cars = [Car.from_dict(c) for c in data.get("cars", [])]
        self._trips = [Trip.from_dict(t) for t in data.get("trips", [])]
        self._maintenances = [Maintenance.from_dict(m) for m in data.get("maintenances", [])]

    # --------- ГЕНЕРАЦИЯ ID ---------
    # Берём максимальный id из списка и прибавляем 1
    def _next_driver_id(self):
        max_id = 0
        for d in self._drivers:
            if d.driver_id > max_id:
                max_id = d.driver_id
        return max_id + 1

    def _next_trip_id(self):
        max_id = 0
        for t in self._trips:
            if t.trip_id > max_id:
                max_id = t.trip_id
        return max_id + 1

    def _next_maint_id(self):
        max_id = 0
        for m in self._maintenances:
            if m.maint_id > max_id:
                max_id = m.maint_id
        return max_id + 1

    # --------- ДОБАВЛЕНИЕ ---------
    def add_driver(self):
        driver_id = self._next_driver_id()  # генерируем id сами
        name = input("Введите имя: ")
        phone = input("Введите телефон: ")
        category = input("Введите категорию прав: ")
        self._drivers.append(Driver(driver_id, name, phone, category))
        print(f"Водитель добавлен! Его ID: {driver_id}")

    def add_car(self):
        number = input("Введите гос. номер: ")
        # Гос. номер вводит пользователь, проверяем уникальность
        for c in self._cars:
            if c.number == number:
                print("Машина с таким номером уже есть!")
                return
        brand = input("Введите марку: ")
        # --- ВАЛИДАЦИЯ ГОДА ---
        year = input("Введите год выпуска: ")
        if not year.isdigit():
            print("Год должен быть числом! Машина не добавлена.")
            return
        self._cars.append(Car(number, brand, year))
        print("Машина добавлена!")

    def add_trip(self):
        driver_id_str = input("Введите ID водителя: ")
        # Проверяем, что ввели число
        if not driver_id_str.isdigit():
            print("ID должен быть числом!")
            return
        driver_id = int(driver_id_str)
        # Проверяем, что водитель существует
        if not self._find_driver(driver_id):
            print("Такого водителя нет! Сначала добавьте водителя.")
            return
        car_number = input("Введите номер машины: ")
        if not self._find_car(car_number):
            print("Такой машины нет! Сначала добавьте машину.")
            return
        route = input("Введите маршрут: ")
        date = input("Введите дату: ")
        trip_id = self._next_trip_id()  # генерируем id сами
        self._trips.append(Trip(trip_id, driver_id, car_number, route, date))
        print(f"Рейс добавлен! Его ID: {trip_id}")

    def add_maintenance(self):
        car_number = input("Введите номер машины: ")
        if not self._find_car(car_number):
            print("Такой машины нет!")
            return
        description = input("Введите описание работ: ")
        date = input("Введите дату: ")
        # --- ВАЛИДАЦИЯ СТОИМОСТИ ---
        cost_str = input("Введите стоимость: ")
        try:
            cost = float(cost_str)  # сразу превращаем в число
        except ValueError:
            print("Стоимость должна быть числом! ТО не добавлено.")
            return
        maint_id = self._next_maint_id()  # генерируем id сами
        self._maintenances.append(Maintenance(maint_id, car_number, description, date, cost))
        print(f"Техобслуживание добавлено! Его ID: {maint_id}")

    # --------- ВСПОМОГАТЕЛЬНЫЕ ПОИСКИ ---------
    def _find_driver(self, driver_id):
        for d in self._drivers:
            if d.driver_id == driver_id:
                return d
        return None

    def _find_car(self, number):
        for c in self._cars:
            if c.number == number:
                return c
        return None

    # --------- ВЫВОД СПИСКОВ ---------
    def show_drivers(self):
        if not self._drivers:
            print("Водителей нет.")
            return
        print("--- Список водителей ---")
        for d in self._drivers:
            print(d.info())

    def show_cars(self):
        if not self._cars:
            print("Машин нет.")
            return
        print("--- Список машин ---")
        for c in self._cars:
            print(c.info())

    def show_trips(self):
        if not self._trips:
            print("Рейсов нет.")
            return
        print("--- Список рейсов ---")
        for t in self._trips:
            print(t.info())

    def show_maintenances(self):
        if not self._maintenances:
            print("Записей о ТО нет.")
            return
        print("--- Список техобслуживания ---")
        for m in self._maintenances:
            print(m.info())

    # --------- УДАЛЕНИЕ ---------
    def delete_driver(self):
        driver_id_str = input("Введите ID водителя для удаления: ")
        if not driver_id_str.isdigit():
            print("ID должен быть числом!")
            return
        driver = self._find_driver(int(driver_id_str))
        if driver:
            self._drivers.remove(driver)
            print("Водитель удалён.")
        else:
            print("Водитель не найден.")

    def delete_car(self):
        number = input("Введите номер машины для удаления: ")
        car = self._find_car(number)
        if car:
            self._cars.remove(car)
            print("Машина удалена.")
        else:
            print("Машина не найдена.")

    def delete_trip(self):
        trip_id_str = input("Введите ID рейса для удаления: ")
        if not trip_id_str.isdigit():
            print("ID должен быть числом!")
            return
        trip_id = int(trip_id_str)
        for t in self._trips:
            if t.trip_id == trip_id:
                self._trips.remove(t)
                print("Рейс удалён.")
                return
        print("Рейс не найден.")

    def delete_maintenance(self):
        maint_id_str = input("Введите ID ТО для удаления: ")
        if not maint_id_str.isdigit():
            print("ID должен быть числом!")
            return
        maint_id = int(maint_id_str)
        for m in self._maintenances:
            if m.maint_id == maint_id:
                self._maintenances.remove(m)
                print("Запись о ТО удалена.")
                return
        print("Запись не найдена.")

    # --------- СТАТИСТИКА / ИНФОРМАЦИЯ ---------
    def driver_stats(self):
        driver_id_str = input("Введите ID водителя: ")
        if not driver_id_str.isdigit():
            print("ID должен быть числом!")
            return
        driver_id = int(driver_id_str)
        driver = self._find_driver(driver_id)
        if not driver:
            print("Водитель не найден.")
            return
        print(driver.info())
        # Считаем рейсы этого водителя
        count = 0
        cars_used = []   # на каких машинах ездил
        for t in self._trips:
            if t.driver_id == driver_id:
                count += 1
                if t.car_number not in cars_used:
                    cars_used.append(t.car_number)
        print(f"Количество рейсов: {count}")
        if cars_used:
            print("Машины, на которых ездил:", ", ".join(cars_used))
        else:
            print("Машин пока нет (рейсов не было).")

    def car_stats(self):
        number = input("Введите номер машины: ")
        car = self._find_car(number)
        if not car:
            print("Машина не найдена.")
            return
        print(car.info())
        # Считаем рейсы машины
        trips_count = 0
        for t in self._trips:
            if t.car_number == number:
                trips_count += 1
        # Считаем ТО и сумму затрат
        maint_count = 0
        total_cost = 0
        for m in self._maintenances:
            if m.car_number == number:
                maint_count += 1
                # пытаемся прибавить стоимость (вдруг введено число)
                try:
                    total_cost += float(m.cost)
                except ValueError:
                    pass
        print(f"Количество рейсов: {trips_count}")
        print(f"Количество ТО: {maint_count}")
        print(f"Общие затраты на ТО: {total_cost}")


# ====================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ИНТЕРФЕЙСА ======================
def line():
    # Печатает разделитель
    print("=" * 40)


def pause():
    # Пауза, чтобы пользователь успел прочитать результат
    input("\nНажмите Enter, чтобы продолжить...")


# ====================== ПОДМЕНЮ ======================
def drivers_menu(park):
    while True:
        line()
        print("--- ВОДИТЕЛИ ---")
        print("1. Добавить")
        print("2. Показать всех")
        print("3. Удалить")
        print("4. Статистика по водителю")
        print("0. Назад")
        line()
        choice = input("Выберите пункт: ")

        if choice == "1":
            park.add_driver()
            pause()
        elif choice == "2":
            park.show_drivers()
            pause()
        elif choice == "3":
            park.delete_driver()
            pause()
        elif choice == "4":
            park.driver_stats()
            pause()
        elif choice == "0":
            break
        else:
            print("Нет такого пункта.")
            pause()


def cars_menu(park):
    while True:
        line()
        print("--- АВТОМОБИЛИ ---")
        print("1. Добавить")
        print("2. Показать все")
        print("3. Удалить")
        print("4. Статистика по машине")
        print("0. Назад")
        line()
        choice = input("Выберите пункт: ")

        if choice == "1":
            park.add_car()
            pause()
        elif choice == "2":
            park.show_cars()
            pause()
        elif choice == "3":
            park.delete_car()
            pause()
        elif choice == "4":
            park.car_stats()
            pause()
        elif choice == "0":
            break
        else:
            print("Нет такого пункта.")
            pause()


def trips_menu(park):
    while True:
        line()
        print("--- РЕЙСЫ ---")
        print("1. Добавить")
        print("2. Показать все")
        print("3. Удалить")
        print("0. Назад")
        line()
        choice = input("Выберите пункт: ")

        if choice == "1":
            park.add_trip()
            pause()
        elif choice == "2":
            park.show_trips()
            pause()
        elif choice == "3":
            park.delete_trip()
            pause()
        elif choice == "0":
            break
        else:
            print("Нет такого пункта.")
            pause()


def maintenance_menu(park):
    while True:
        line()
        print("--- ТЕХОБСЛУЖИВАНИЕ ---")
        print("1. Добавить")
        print("2. Показать все")
        print("3. Удалить")
        print("0. Назад")
        line()
        choice = input("Выберите пункт: ")

        if choice == "1":
            park.add_maintenance()
            pause()
        elif choice == "2":
            park.show_maintenances()
            pause()
        elif choice == "3":
            park.delete_maintenance()
            pause()
        elif choice == "0":
            break
        else:
            print("Нет такого пункта.")
            pause()


# ====================== ГЛАВНОЕ МЕНЮ ======================
def main():
    park = AutoPark()
    park.load()  # загружаем данные при запуске

    while True:
        line()
        print("===== УЧЁТ АВТОПАРКА =====")
        print("1. Водители")
        print("2. Автомобили")
        print("3. Рейсы")
        print("4. Техобслуживание")
        print("0. Сохранить и выйти")
        line()
        choice = input("Выберите раздел: ")

        if choice == "1":
            drivers_menu(park)
        elif choice == "2":
            cars_menu(park)
        elif choice == "3":
            trips_menu(park)
        elif choice == "4":
            maintenance_menu(park)
        elif choice == "0":
            park.save()  # сохраняем перед выходом
            print("До свидания!")
            break
        else:
            print("Нет такого раздела, попробуйте ещё раз.")
            pause()


# Запуск программы
if __name__ == "__main__":
    main()