import matplotlib.pyplot as plt
import main
from datetime import datetime
import export.excel as excel
import export.csv as csv
from export.gdrive import save_to_drive

# CONSTANTS
items_to_parse = {
    "milk": "Piim ",
    "eggs": "Munad",
    "wheat": "nisujahu",
    "tomatoes": "tomat ",
    "cucumber": "kurk ",
}
table = excel.Excel()
table.create_sheets(items_to_parse.keys())


def get_products():
    return main.get_prices(main.connect())[1]


def get_products_by_name(name):
    return main.get_prices(main.connect(), name)[1]


def datetime_to_epoch(datetimes: list) -> list:
    epochs = []
    for dt in datetimes:
        if dt == "initial_products":
            dt = "2022-03-06"
        epoch = datetime.fromisoformat(dt).timestamp()
        epochs.append(epoch)
    return epochs


def get_data() -> dict:
    pass


def get_normalized_price(data: list) -> list:
    new_data = list()
    for index, item in enumerate(data):
        if index != 0 and data[index] == None:
            new_data.append(new_data[index - 1])
        else:
            new_data.append(item)

    return new_data


def save_to_excel(dataset, sheet_name: str = "Sheet") -> None:
    tables = [i[0] for i in main.get_tables(main.connect())]
    tables.remove("initial_products")
    header = ["Product name", "Shop name", "2022-03-06"] + tables
    data = []

    for item in dataset:
        prices = get_normalized_price(
            [dataset[item]["prices"][value] for value in dataset[item]["prices"]]
        )
        value = [item, dataset[item]["shop"]] + prices
        data.append(value)

    table.append_header(header, sheet_name)
    table.put_data(data, sheet_name)


def save_to_csv(dataset) -> None:
    data = []

    tables = [i[0] for i in main.get_tables(main.connect())]
    tables.remove("initial_products")
    header = ["Product name", "Shop name", "2022-03-06"] + tables

    data.append(header)

    for item in dataset:
        prices = get_normalized_price(
            [dataset[item]["prices"][value] for value in dataset[item]["prices"]]
        )
        value = [item, dataset[item]["shop"]] + prices
        data.append(value)

    csv.write_to_csv("data.csv", data)


def plot() -> None:
    chosen_item = dataset["977184, Kihiline suitsukalasalat 500 g"]

    dates = [i for i in chosen_item]
    epochs = datetime_to_epoch(dates)

    values = [chosen_item[i] for i in chosen_item]

    plt.plot(epochs, values, "o")
    plt.show()


for item in items_to_parse:
    products = get_products_by_name(items_to_parse[item])
    save_to_excel(products, item)
    save_to_csv(products)

table.save()
save_to_drive("data.xlsx", "xlsx")
save_to_drive("data.csv", "csv")