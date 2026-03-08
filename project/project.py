from cs50 import SQL
import argparse
import re
import sys
from tabulate import tabulate

db = SQL("sqlite:///list.db") # database connection

BOXMARK = '\u2610'
CHECKMARK = '\u2714'

# argparse argument setting
parser = argparse.ArgumentParser()
parser.add_argument("-ov", help="view whole to-do list", action="store_true")
parser.add_argument("-v", help="view day to-do list", type=str)
parser.add_argument("-a", help="add to list", action="store_true")
parser.add_argument("-r", help="remove from list", action="store_true")
parser.add_argument("-c", help="mark as complete", action="store_true")
args = parser.parse_args()

def main():
    if not (args.ov or args.v or args.a or args.r or args.c):
        parser.print_help()
    if args.ov:
        overview()
    elif args.v:
        view(args.v)
    elif args.a:
        add()
    elif args.r:
        remove()
    elif args.c:
        complete()

def overview():
    days = db.execute("SELECT * FROM week") # getting days of the week
    for day in days:
        print("\n")
        print(day["day"])
        rows = db.execute("SELECT id, time, task, status FROM tasks WHERE day=? ORDER BY time", day["day"]) # sql inquiry for tasks per day for all days
        print(tabulate(rows, headers="keys", tablefmt="grid"))

def view(day):
    print(day)
    rows = db.execute("SELECT id, time, task, status FROM tasks WHERE day=? ORDER BY time", day) # sql inquiry for tasks on chosen day
    print(tabulate(rows, headers="keys", tablefmt="grid"))

def add():
    while True:
        add_into = input("Task: ").strip()
        if add_into == "done": # break out of loop if done
            break
        else:
            day = input("Day: ").strip().lower()
            day_check = validate_day(day)
            if day_check == True:
                day == day
            else:
                sys.exit("Invalid day")
            time = input("Time: ").strip()
            timing_check = validate_time(time)
            if timing_check == True:
                timing = f"{int(time):04d}"
            elif timing_check == False:
                sys.exit("Invalid time")
            if day == "all": # check if task is for specific day or all days
                days = db.execute("SELECT * FROM week")
                for a_day in days:
                    db.execute("INSERT INTO tasks (day, time, task, status) VALUES (?, ?, ?, ?)", a_day["day"], timing, add_into, BOXMARK) # sql inquiry for adding task to all days
            else:
                db.execute("INSERT INTO tasks (day, time, task, status) VALUES (?, ?, ?, ?)", day, timing, add_into, BOXMARK) # sql inquiry for adding task to chosen day
    overview()

def remove():
    take_away = input("Task id: ").strip()
    id_test = validate_id(take_away)
    if id_test == True:
        take_away == take_away
    else:
        sys.exit("Invalid ID")
    day_of = db.execute("SELECT day FROM tasks WHERE id=?", take_away)
    db.execute("DELETE FROM tasks WHERE id=?", take_away)
    view(day_of[0]['day'])


def complete():
    finish = input("Task id: ").strip()
    id_test = validate_id(finish)
    if id_test == True:
        finish == finish
    else:
        sys.exit("Invalid ID")
    day_of = db.execute("SELECT day FROM tasks WHERE id=?", finish)
    db.execute("UPDATE tasks SET status=? WHERE id=?", CHECKMARK, finish)
    view(day_of[0]['day'])


# VALIDATION FUNCTIONS

def validate_day(day):
    day_check = re.fullmatch(r"(?:mon|tue|wed|thu|fri|sat|sun|all)", day)
    if day_check:
        return True
    else:
        return False


def validate_time(timing):
    timing_check = re.search(r"[012][0-9][012345][0-9]", timing)
    if timing_check:
        timing = int(timing)
        if 0000 <= timing <= 2359:
            return True
    return False

def validate_id(id):
    try:
        id = int(id)
    except ValueError:
        sys.exit("Invalid id")
    available_id = db.execute("SELECT id FROM tasks")
    id_list = []
    for option in available_id:
        id_list.append(option['id'])
    if id in id_list:
        return True
    else:
        return False

if __name__ == "__main__":
    main()