#!/usr/bin/python3
import os
import re
import csv
import argparse
from pprint import pprint

parser = argparse.ArgumentParser(
    prog='Google CSV to Markdown',
    description='Convert Google CSV to Markdown')

parser.add_argument('input_file_csv', metavar="input-file.csv")
parser.add_argument('-f', '--force-replace',
                    action="store_true", default=False, help="Force replace existing markdown files")
parser.add_argument('-o', '--output-dir', default=".",
                    help="The directory where you would like the markdown files to be saved.")

args = parser.parse_args()

columns = []


def find_column(name):
    if name in columns:
        return columns.index(name)
    else:
        return None


def format_type(type):
    parts = type.split(" ")
    if len(parts) == 2:
        return parts[1]
    else:
        return type


def row_to_page(row):
    page = ""

    tags = ["contact"]
    gm_idx = find_column("Group Membership")
    if gm_idx != None and row[gm_idx] != '':
        for membership in row[gm_idx].split(" ::: "):
            m = format_type(membership)
            if m != "myContacts":
                tags.append(m)

    tags_str = ", ".join([f'"{tag}"' for tag in tags])
    page += "---\ntags: [" + tags_str + "]\naliases: []\n---\n\n"

    for field in ['E-mail', 'Phone', 'Address', 'Organization']:
        for i in range(1, 10):
            v_idx = find_column(f'{field} {i} - Value')
            if v_idx != None and row[v_idx] != '':
                t_idx = find_column(f'{field} {i} - Type')
                if t_idx != None:
                    page += '**' + field + \
                        '** (' + format_type(row[t_idx]) + \
                        '): ' + row[v_idx] + "\n"
            n_idx = find_column(f'{field} {i} - Name')
            if n_idx != None and row[n_idx] != '':
                page += '**' + field + '**: ' + row[n_idx] + "\n"

    notes_idx = find_column('Notes')
    if notes_idx != None and row[notes_idx] != '':
        page += '\n## Notes\n\n' + row[notes_idx] + '\n'

    return page


def main():
    with open(args.input_file_csv, newline='') as csvfile:
        gc_reader = csv.reader(csvfile)
        header = next(gc_reader)

        for column in header:
            columns.append(column)

        for row in gc_reader:
            page = row_to_page(row)

            name_idx = find_column('Name')
            if name_idx != None and row[name_idx] != '':
                name = re.sub(r'[\:\/\\\'\"\.\?\|]', '', row[name_idx])
                filepath = f'{args.output_dir}/{name}.md'

                if (not os.path.exists(filepath) or args.force_replace):
                    # print('file', filepath)
                    # print(page)
                    with open(filepath, "w") as f:
                        f.write(page)


if __name__ == "__main__":
    main()
