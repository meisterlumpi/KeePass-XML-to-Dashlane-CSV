import xml.etree.ElementTree as ET
import csv
import click


class Entry:
    name = ""
    login = ""
    password = ""
    website = ""
    category = ""
    note = ""


def process_group(grp, is_root_grp, grp_path=""):
    if is_root_grp:
        grp_path = ""
    else:
        if grp_path == "":
            grp_path = grp.find("Name").text
        else:
            grp_path = '/'.join([grp_path, grp.find("Name").text])

    for child in grp:
        if child.tag == "Entry":
            strings = child.findall("String")

            e = Entry()
            e.category = grp_path

            for string in strings:
                key = string.find("Key").text
                value = string.find("Value").text

                if key == "Notes":
                    e.note = value
                elif key == "Password":
                    e.password = value
                elif key == "Title":
                    e.name = value
                elif key == "URL":
                    e.website = value
                elif key == "UserName":
                    e.login = value

            entries.append(e)

        elif child.tag == "Group":
            process_group(child, False, grp_path)


entries = []


@click.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.File('w', encoding='UTF8'))
def main(input, output):
    print(input)
    root = ET.parse(input).getroot()

    root_grp = root.find("Root/Group")

    root_grp_name = root_grp.find("Name").text

    print(f"Dumping data base '{root_grp_name}'")

    process_group(root_grp, True)

    writer = csv.writer(output)

    header = ['name', 'website', 'login', 'password', 'category', 'note']
    writer.writerow(header)

    for e in entries:
        row = [e.name, e.website, e.login, e.password, e.category, e.note]
        writer.writerow(row)


if __name__ == "__main__":
    main()
