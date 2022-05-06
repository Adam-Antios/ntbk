import os
import sys
import subprocess

import time
from datetime import datetime

from pathlib import Path

import getpass

from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

# ==============================================================================
# 
# ==============================================================================


def add_new_note(extension):

    command = f"nvim {notes_directory_path}/{timestamp}."+extension
    subprocess.run(command, shell=True)

#
#

def search_all_notes(pattern):

    all_notes = os.listdir(notes_directory_path)

    if len(all_notes) == 0:
        print("\nThere are no notes in general.")

    else:
        notes_list = []

        for note in all_notes:
            note_path = Path(notes_directory_path, note)

            with open(note_path) as note:
                contents = note.read()

                if pattern.lower() in contents.lower():
                    notes_list.append(note_path)

        notes_list = sorted(notes_list, key=os.path.getmtime)

        if len(notes_list) == 0:
            print("\nThere are no notes matching your pattern.")

        return notes_list

#
#

def list_all_notes():

    all_notes = os.listdir(notes_directory_path)

    if len(all_notes) == 0:
        print("\nThere are no notes in general.")

    else:
        notes_list = []

        for note in all_notes:
            note_path = Path(notes_directory_path, note)
            notes_list.append(note_path)

        notes_list = sorted(notes_list, key=os.path.getmtime)

        return notes_list

#
#

def edit_note(note):

    command = f"nvim {note}"
    subprocess.run(command, shell=True)

#
#

def delete_notes(note):

    os.remove(note)

#
#

def render_notes_list(notes_list):

    if len(notes_list) != 0:

        console = Console()

        for index, note in enumerate(notes_list):

            table = Table(
                show_header=True,
                header_style="magenta",
                show_lines=False,
                box=False
            )

            table.add_column("No.", width=10)
            table.add_column("Note", width=85)
            table.add_column("Date", width=20)

            note_path = Path(notes_directory_path, note)

            note_date = os.path.getmtime(note_path)
            note_date = datetime.fromtimestamp(int(note_date))

            with open(note_path) as note:

                contents = note.read()
                contents = Markdown(contents)

                table.add_row(str(index), contents, str(note_date))

            print("\n")
            console.print(table)

#
#

def main():

    if len(sys.argv) == 1:
        print("\nGive an option.")

    else:
        option = sys.argv[1]

        if option == "new" or option == "n":

            if len(sys.argv) == 2:
                add_new_note("md")

            elif len(sys.argv) == 3:
                add_new_note(sys.argv[2])

        elif option == "find" or option == "f":

            if len(sys.argv) == 2:
                print("\nGive a search term.")

            elif len(sys.argv) == 3:

                pattern = sys.argv[2]

                notes_list = search_all_notes(pattern)
                render_notes_list(notes_list)

        elif option == "edit" or option == "e" or \
             option == "view" or option == "v":

            if len(sys.argv) == 2:
                print("\nGive a search term.")

            elif len(sys.argv) == 3:

                pattern = sys.argv[2]

                notes_list = search_all_notes(pattern)
                render_notes_list(notes_list)

                if len(notes_list) == 1:
                    note = notes_list[0]
                    edit_note(note)

                elif len(notes_list) > 1:

                    number = input("\nWhich note to edit/view? ")
                    
                    note = notes_list[int(number)]
                    edit_note(note)

        elif option == "list" or option == "l":

            if len(sys.argv) == 2:
                print("\nGive a correct option.")

            elif len(sys.argv) == 3:

                set = sys.argv[2]

                if set == "all" or set == "a":
                    notes_list = list_all_notes()
                    render_notes_list(notes_list)

                else:
                    print("\nGive a correct option.")

        elif option == "delete" or option == "d":

            if len(sys.argv) == 2:
                print("\nGive a search term.")

            elif len(sys.argv) == 3:

                pattern = sys.argv[2]

                notes_list = search_all_notes(pattern)
                render_notes_list(notes_list)

                if len(notes_list) != 0:

                    number = input("\nWhich note to delete? ")

                    note = notes_list[int(number)]
                    delete_notes(note)

        else:
            print("\nGive a correct option.")

# ==============================================================================
# 
# ==============================================================================

if __name__ == "__main__":

    timestamp = int(time.time())

    home_directory_path = str(Path.home())
    notes_directory_path = Path(home_directory_path, ".ntbk")

    is_notes_directory = os.path.exists(notes_directory_path)

    if not is_notes_directory:
        os.makedirs(notes_directory_path)
    
    #
    #

    os.system("clear")

    main()
