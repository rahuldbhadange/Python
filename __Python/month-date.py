"""In the previous exercise we saved information about famous scientists’ names and birthdays to disk.
In this exercise, load that JSON file from disk, extract the months of all the birthdays,
and count how many scientists have a birthday in each month.
"""

import json
from collections import Counter
from pprint import pprint

with open("birthdays.json", "r") as f:
    birthdays = json.load(f)
    pprint(birthdays)

num_to_string = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

months = []
for name, birthday_string in birthdays.items():
    month = int(birthday_string.split("/")[0])
    months.append(num_to_string[month])

print(months)
print(Counter(months))
