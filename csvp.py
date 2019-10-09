import csv

""" CSV+ - Just a simple class within function to find element/s """
class csvp:
    def __init__(self, _csv):
        self._csv = _csv

    def findElements(self, column, value):
        with open(self._csv, encoding="utf-8") as csv_open:
            _csv = csv.DictReader(csv_open, delimiter=",")
            elements = []
            for row in _csv:
                if value.lower() in row[column].lower():
                    elements.append(row)
            return elements

    def findElement(self, column, value):
        with open(self._csv, encoding="utf-8") as csv_open:
            _csv = csv.DictReader(csv_open, delimiter=",")
            for row in _csv:
                if value.lower() == row[column].lower():
                    return row
