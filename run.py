# -*- coding: UTF-8 -*-

from hostloc.hostloc import start


def main_handler(event, context):
    return start(log_to_file=False)

if __name__ == "__main__":
    start()
