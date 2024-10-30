import os.path
from collections import OrderedDict

from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale


class ModelIndex:
    def __init__(self, model_id: int, position_in_data_file: int):
        self.model_id = model_id
        self.position_in_data_file = position_in_data_file


class CarIndex:
    def __init__(self, car_id: str, position_in_data_file: int):
        self.car_id = car_id
        self.position_in_data_file = position_in_data_file


class SaleIndex:
    def __init__(self, sale_id: str, position_in_data_file: int):
        self.sale_id = sale_id
        self.position_in_data_file = position_in_data_file


class CarService:
    def _format_path(self, filename: str) -> str:
        return os.path.join(self.root_dir, filename)

    def _read_file(self, filename: str) -> list[list[str]]:
        if not os.path.exists(self._format_path(filename)):
            return []

        with open(self._format_path(filename), "r") as f:
            lines = f.readlines()
            split_lines = [l.strip().split(",") for l in lines]
            return split_lines

    def update_car_status(self, car_position: int, status: CarStatus) -> Car:
        with open(self._format_path("cars_update.txt"), "a") as f_upd:
            with open(self._format_path("cars.txt"), "r") as f:
                for i, v in enumerate(f):
                    if i != car_position:
                        f_upd.write(v)
                    else:
                        car_info = v.strip().split(",")
                        str_car = f"{car_info[0]},{car_info[1]},{car_info[2]},{car_info[3]},{status}".ljust(500)
                        f_upd.write(str_car + "\n")

                        car = Car(
                            vin=car_info[0],
                            model=car_info[1],
                            price=car_info[2],
                            date_start=car_info[3],
                            status=status
                        )

        os.remove(self._format_path("cars.txt"))
        os.rename(self._format_path("cars_update.txt"), self._format_path("cars.txt"))

        return car

    # Задание 1. Сохранение автомобилей и моделей
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.model_index: list[ModelIndex] = []
        self.car_index: list[CarIndex] = []
        self.sale_index: list[SaleIndex] = []

        split_model_lines = self._read_file("models_index.txt")
        self.model_index = [ModelIndex(int(l[0]), int(l[1])) for l in split_model_lines]

        split_car_lines = self._read_file("cars_index.txt")
        self.car_index = [CarIndex(l[0], int(l[1])) for l in split_car_lines]

        split_sale_index = self._read_file("sales_index.txt")
        self.sale_index = [SaleIndex(l[0], int(l[1])) for l in split_sale_index]

    def add_model(self, model: Model) -> Model:
        with open(self._format_path("models.txt"), "a") as f:
            str_model = f"{model.id},{model.name},{model.brand}".ljust(500)
            f.write(str_model + "\n")

        new_mi = ModelIndex(model.id, len(self.model_index))

        self.model_index.append(new_mi)
        self.model_index.sort(key=lambda x: x.model_id)

        with open(self._format_path("models_index.txt"), "w") as f:
            for current_mi in self.model_index:
                str_model = f"{current_mi.model_id},{current_mi.position_in_data_file}".ljust(50)
                f.write(str_model + "\n")

        return model

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        with open(self._format_path("cars.txt"), "a") as f:
            str_car = f"{car.vin},{car.model},{car.price},{car.date_start},{car.status}".ljust(500)
            f.write(str_car + "\n")

        new_ci = CarIndex(car.vin, len(self.car_index))

        self.car_index.append(new_ci)
        self.car_index.sort(key=lambda x: x.car_id)

        with open(self._format_path("cars_index.txt"), "w") as f:
            for current_ci in self.car_index:
                str_car = f"{current_ci.car_id},{current_ci.position_in_data_file}".ljust(50)
                f.write(str_car + "\n")

        return car

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        car_position = None

        with open(self._format_path("sales.txt"), "a") as f:
            str_sale = f"{sale.sales_number},{sale.car_vin},{sale.sales_date},{sale.cost}".ljust(500)
            f.write(str_sale + "\n")

        new_si = SaleIndex(sale.sales_number, len(self.sale_index))

        self.sale_index.append(new_si)
        self.sale_index.sort(key=lambda x: x.sale_id)

        with open(self._format_path("sales_index.txt"), "w") as f:
            for current_si in self.sale_index:
                str_sale = f"{current_si.sale_id},{current_si.position_in_data_file}".ljust(50)
                f.write(str_sale + "\n")

        for i in self.car_index:
            if i.car_id == sale.car_vin:
                car_position = i.position_in_data_file
                break

        with open(self._format_path("cars_update.txt"), "a") as f_upd:
            with open(self._format_path("cars.txt"), "r") as f:
                for i, v in enumerate(f):
                    if i != car_position:
                        f_upd.write(v)
                    else:
                        car_info = v.strip().split(",")
                        str_car = f"{car_info[0]},{car_info[1]},{car_info[2]},{car_info[3]},{CarStatus.sold}".ljust(500)
                        f_upd.write(str_car + "\n")

                        car = Car(
                            vin=car_info[0],
                            model=car_info[1],
                            price=car_info[2],
                            date_start=car_info[3],
                            status=CarStatus.sold
                        )

        os.remove(self._format_path("cars.txt"))
        os.rename(self._format_path("cars_update.txt"), self._format_path("cars.txt"))

        return car

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        cars_list = []

        with open(self._format_path("cars.txt"), "r") as f:
            for line in f:
                car_info = line.strip().split(",")

                if car_info[4] == status:
                    car = Car(
                        vin=car_info[0],
                        model=car_info[1],
                        price=car_info[2],
                        date_start=car_info[3],
                        status=car_info[4]
                    )
                    cars_list.append(car)

        # cars_list.sort(key=lambda car: car.vin)
        return cars_list

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        car_position = None
        model_position = None
        sale_position = None
        sales_date = None
        sales_cost = None

        for i in self.car_index:
            if i.car_id == vin:
                car_position = i.position_in_data_file
                break

        if car_position is None:
            return None

        with open(self._format_path("cars.txt"), "r") as f:
            f.seek(501 * car_position)
            car_info = f.readline().strip().split(",")

        car = Car(
            vin=car_info[0],
            model=car_info[1],
            price=car_info[2],
            date_start=car_info[3],
            status=car_info[4]
        )

        for i in self.model_index:
            if i.model_id == car.model:
                model_position = i.position_in_data_file
                break

        with open(self._format_path("models.txt"), "r") as f:
            f.seek(501 * model_position)
            model_info = f.readline().strip().split(",")

        model = Model(
            id=model_info[0],
            name=model_info[1],
            brand=model_info[2]
        )

        if car.status == CarStatus.sold:
            for i in self.sale_index:
                if i.sale_id.split("#")[-1] == car.vin:
                    sale_position = i.position_in_data_file
                    break

            with open(self._format_path("sales.txt"), "r") as f:
                f.seek(501 * sale_position)
                sale_info = f.readline().strip().split(",")

            sales_date, sales_cost = sale_info[2], sale_info[3]

        car_full_info = CarFullInfo(
            vin=car.vin,
            car_model_name=model.name,
            car_model_brand=model.brand,
            price=car.price,
            date_start=car.date_start,
            status=car.status,
            sales_date=sales_date,
            sales_cost=sales_cost
        )

        if car_full_info is not None:
            return car_full_info
        else:
            return None


    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
        car_position = None

        for i in self.car_index:
            if i.car_id == vin:
                car_position = i.position_in_data_file
                break

        self.car_index: list[CarIndex] = []

        with open(self._format_path("cars_update.txt"), "a") as f_upd:
            with open(self._format_path("cars.txt"), "r") as f:
                for i, v in enumerate(f):
                    if i != car_position:
                        f_upd.write(v)
                        car_vin = v.strip().split(",")[0]
                    else:
                        car_info = v.strip().split(",")
                        str_car = f"{new_vin},{car_info[1]},{car_info[2]},{car_info[3]},{car_info[4]}".ljust(500)
                        car_vin = new_vin
                        f_upd.write(str_car + "\n")

                        car = Car(
                            vin=new_vin,
                            model=car_info[1],
                            price=car_info[2],
                            date_start=car_info[3],
                            status=car_info[4]
                        )

                    new_ci = CarIndex(car_vin, len(self.car_index))
                    self.car_index.append(new_ci)
                    self.car_index.sort(key=lambda x: x.car_id)

        with open(self._format_path("cars_index_update.txt"), "a") as fi_upd:
            for current_ci in self.car_index:
                str_car = f"{current_ci.car_id},{current_ci.position_in_data_file}".ljust(50)
                fi_upd.write(str_car + "\n")

        os.remove(self._format_path("cars.txt"))
        os.rename(self._format_path("cars_update.txt"), self._format_path("cars.txt"))

        os.remove(self._format_path("cars_index.txt"))
        os.rename(self._format_path("cars_index_update.txt"), self._format_path("cars_index.txt"))

        return car

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        sale_position = None
        car_position = None

        for i in self.sale_index:
            if i.sale_id == sales_number:
                sale_position = i.position_in_data_file
                break

        self.sale_index: list[SaleIndex] = []

        with open(self._format_path("sales_update.txt"), "a") as f_upd:
            with open(self._format_path("sales.txt"), "r") as f:
                for i, v in enumerate(f):
                    if i != sale_position:
                        f_upd.write(v)
                        sale_id = v.strip().split(",")[0]
                        new_si = SaleIndex(sale_id, len(self.sale_index))
                        self.sale_index.append(new_si)
                        self.sale_index.sort(key=lambda x: x.sale_id)
                    else:
                        vin = v.strip().split(",")[1]

        with open(self._format_path("sales_index_update.txt"), "a") as fi_upd:
            for current_si in self.sale_index:
                str_sale = f"{current_si.sale_id},{current_si.position_in_data_file}".ljust(50)
                fi_upd.write(str_sale + "\n")

        for i in self.car_index:
            if i.car_id == vin:
                car_position = i.position_in_data_file
                break

        car = self.update_car_status(car_position, CarStatus.available)

        os.remove(self._format_path("sales.txt"))
        os.rename(self._format_path("sales_update.txt"), self._format_path("sales.txt"))

        os.remove(self._format_path("sales_index.txt"))
        os.rename(self._format_path("sales_index_update.txt"), self._format_path("sales_index.txt"))

        return car

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        sales_dict = dict()
        car_position = None
        stats_list = []

        with open(self._format_path("sales.txt"), "r") as f:
            for line in f:
                vin = line.strip().split(",")[1]

                for i in self.car_index:
                    if i.car_id == vin:
                        car_position = i.position_in_data_file
                        break

                with open(self._format_path("cars.txt"), "r") as f:
                    f.seek(501 * car_position)
                    car_info = f.readline().strip().split(",")

                if not sales_dict.get(car_info[1]):
                    sales_dict[car_info[1]] = 1
                else:
                    sales_dict[car_info[1]] += 1

            sales_dict = sorted(sales_dict.items(), key=lambda item: item[1], reverse=True)

            top_3_sales = OrderedDict()
            for k, v in sales_dict:
                if k not in top_3_sales:
                    top_3_sales[k] = v
                    if len(top_3_sales) == 3:
                        break

            for model_item in list(top_3_sales.items()):
                for index_item in self.model_index:
                    if index_item.model_id == int(model_item[0]):
                        model_position = index_item.position_in_data_file

                        with open(self._format_path("models.txt"), "r") as f:
                            f.seek(501 * model_position)
                            model_info = f.readline().strip().split(",")

                        model_sales_stats = ModelSaleStats(
                            car_model_name=model_info[1],
                            brand=model_info[2],
                            sales_number=model_item[1]
                        )
                        stats_list.append(model_sales_stats)
                        break

        return stats_list
