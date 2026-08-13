import csv
import os


def initialize_file(filename, headers):
    if not os.path.exists(filename):
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)


def add_record(filename, record):
    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(record)


def read_records(filename):
    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def write_records(filename, records, headers):
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(records)