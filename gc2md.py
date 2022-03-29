#!/usr/bin/python3
import os
from pprint import pprint

notes_path = "/home/user/Notes/Contacts"
contacts_path = "/home/user/Downloads/contacts.csv"
force_update = False # setting to true will force previously made contacts to be replaced with the new export

def main():
    with open(contacts_path, "r") as f:
        contacts = f.readlines()

    thead = contacts[0].split(",")
    contacts.pop(0)  # remove header

    for contact in contacts:
        fields = contact.split(",")

        if (
            not os.path.exists(f"{notes_path}{fields[0].replace(' ','_')}.md")
            or force_update
        ):
            with open(f"{notes_path}{fields[0].replace(' ','_')}.md", "w") as f:
                content = ""
                header = """---
tags: ["contact"]
aliases: []
---

"""
                content += header

                for i in range(len(fields) - 1):
                    if i == 0:
                        content += f"# {fields[i]}\n"
                        content += "\n-----------\n"

                    if len(fields[i]) > 1:
                        content += f"**{thead[i]}:** {fields[i]}\n"
                content += "\n-----------\n"
                content += "\n## Relationships\n"
                content += "\n## Places\n"
                content += "\n## Notes\n"

                print(content + "\n\n")
                f.write(content)


if __name__ == "__main__":
    main()
