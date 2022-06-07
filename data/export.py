
import csv
import xlwings

from argparse import ArgumentParser
from re import compile as regex
from tabulate import tabulate

NONE_VAL = "–"

db_name = regex(r"Database v\d+.\d+")
readme_name = regex(r"v\d+.\d+ Readme")

def main():
    readme, header, rows = get_data()

    ap = ArgumentParser()
    ap.add_argument("--export", action="store_true", help="export readme PDF and database CSV")
    ap.add_argument("--usage", action="store_true", help="print column usage table")
    args = ap.parse_args()

    # export if no args given
    if args.export or not any(vars(args).values()):
        export(readme, header, rows)
    if args.usage:
        col_usage(header, rows)


def get_data():
    wb = xlwings.Book("aisc-shapes-database-v15.0.xlsx")

    db = None
    readme = None
    for sheet in wb.sheets:
        if db_name.match(sheet.name):
            db = sheet
        elif readme_name.match(sheet.name):
            readme = sheet

    assert all((db, readme)), "Readme and/or Database sheets not found. Maybe their names changed."

    header, *rows = sheet.range("A1").expand().value

    # replace AISC none values
    # replace non-csv encodable values (i.e. α)
    for r, row in enumerate(rows):
        for c, col in enumerate(row):
            if col == NONE_VAL:
                rows[r][c] = None

    return readme, header, rows


def export(readme_sheet, header, rows):
    # export readme as PDF
    readme_sheet.to_pdf()

    # export data as csv
    with open("aisc-shapes-db.csv", 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(rows)


def col_usage(header, rows):
    ALL_CHAR = '*'
    SOME_CHAR = 'o'

    print("\n\nColumn has data per shape:")
    print("\t{}: all".format(ALL_CHAR))
    print("\t{}: some".format(SOME_CHAR))
    print("")

    shapes = sorted(set(r[0] for r in rows))
    matrix = [['', *shapes]]
    for c, col in enumerate(header[3:], start=3):
        # stop if starting metric section
        if col == 'EDI_Std_Nomenclature':
            break

        # add new row for column
        matrix.append([col, *[None] * len(shapes)])

        for s, shape in enumerate(shapes, start=1):
            has_val = [r[c] is not None for r in rows if r[0] == shape]
            if all(has_val):
                matrix[-1][s] = ALL_CHAR
            elif any(has_val):
                matrix[-1][s] = SOME_CHAR

    # aggregate all shapes
    matrix[0].append("ALL")
    for i, row in enumerate(matrix[1:], start=1):
        for_all = None
        if all([x == ALL_CHAR for x in row[1:]]):
            for_all = ALL_CHAR

        matrix[i].append(for_all)

    # print table
    table_args = dict(
        headers="firstrow",
        tablefmt="psql",
        colalign=("right", *["center"] * (len(shapes) + 1))
    )
    print(tabulate(matrix, **table_args))


if __name__ == '__main__':
    main()
