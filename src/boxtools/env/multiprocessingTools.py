#!/usr/bin/env python3

from multiprocessing import Pool
from time import sleep
from boxtools.Logs import LogDisplay

DELAY_BETWEEN_LOGS = 3


# data: array of execute_build_command args
def multithread_starmap(data, method, subprocess=False):
    log_display: LogDisplay = LogDisplay().get_log_display()
    pool_size = len(data)
    log_display.show_debug_log(' - data to process: ' + str(data))
    if not subprocess:
        log_display.show_debug_log(' - Creating processes pool')
    process_pool = Pool(pool_size)
    if not subprocess:
        log_display.show_info_log(" - Starting build threads.")
    process_pool.starmap(method, data)
    first = True
    for data_row in data:
        mp_dto = data_row[2]
        if first:
            first = False
        elif not subprocess:
            print(
                " - Printing " + mp_dto.process_name + " build output in " + str(DELAY_BETWEEN_LOGS) + " seconds...\n")
            sleep(DELAY_BETWEEN_LOGS)
        if not subprocess:
            log_display.show_info_color_log(" - " + mp_dto.process_name + " build output:")
        with open(mp_dto.output_path, 'r') as db_fin:
            log_display.show_log(db_fin.read())
        if not subprocess:
            log_display.show_info_color_log(' -> Log file available: ' + str(mp_dto.output_path))
            # Spacer
            log_display.show_info_log(" ")
