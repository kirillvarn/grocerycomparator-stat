from openpyxl import Workbook


class Excel:
    def __init__(self, filename="data"):
        self.filename = filename
        self.workbook = Workbook()

    def append_header(self, header: list, sheet_name: str = "Sheet"):
        ws = self.workbook[sheet_name]
        ws.append(header)

    def create_sheets(self, sheet_names):
        del self.workbook["Sheet"]
        for name in sheet_names:
            self.workbook.create_sheet(name)

    def put_data(self, data: list, sheet_name: str = "Sheet"):
        ws = self.workbook[sheet_name]
        for values in data:
            ws.append(values)

    def save(self):
        self.workbook.save(f"{self.filename}.xlsx")
