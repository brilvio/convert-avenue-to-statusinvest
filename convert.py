import sys

import tabula

from consts import SYMBOLS
from models import AvenueOperation, TypeAvenueOperation


def convert(pdf_name: str):
    tabula.convert_into(pdf_name, "output.csv", output_format="csv", pages="all")
    import csv

    with open("output.csv", newline="") as csvfile:
        operations = []
        spamreader = csv.reader(csvfile, delimiter=",", quotechar="|")

        for row in spamreader:
            if len(row) > 6:
                continue
            if "BUY" in row[0]:
                continue
            if "DI" in row[0]:
                continue
            operations.append(row)

    avenue_operations = build_avenue_operations(operations)
    print(avenue_operations)


def build_avenue_operations(operations) -> list[AvenueOperation]:
    output: list[AvenueOperation] = []
    for idx, operation in enumerate(operations):
        if len(operation[0].split()) > 2:
            op, date, _ = operation[0].split()
            if op in [TypeAvenueOperation.BOUGHT.value, TypeAvenueOperation.SOLD.value]:
                description = operation[1]

                if SYMBOLS.get(description, None) is None:
                    description = operations[idx + 1][1]

                quantity = float(operation[2])
                price = float(operation[3])

                output.append(
                    AvenueOperation.build_operation(
                        type_operation=TypeAvenueOperation[op],
                        date=date,
                        description=description,
                        quantity=quantity,
                        price=price,
                    )
                )
        else:
            continue
    return output


if len(sys.argv) == 1:
    print("Please inform the pdf name!")
else:
    convert(sys.argv[1])
