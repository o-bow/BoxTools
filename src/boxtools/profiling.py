#!/usr/bin/env python3

import time

start = time.time()
print(' *** cmd start -- ', start)
#pip3 install line_profiler
import line_profiler
import atexit

profile = line_profiler.LineProfiler()
atexit.register(profile.print_stats)

@profile
def profiled_function():
    pass

    #from module.core.Error import GitException, CoreException, UnreachableException
    #from module.core.cdtFileAccess import get_resources_path, get_box_lib_path


    #from module.core.common import show_log, show_info_log, show_critical_log, show_help_log, call_legacy_zsh, \
    #    show_debug_color_log, show_input_feedback_log, handle_core_error, show_info_color_log

    #from module.core.settings.CdtSettings import UserSettings, AppSettings
    #from module.core.vpn import start_vpn

profiled_function()

end = time.time()
print(' *** cmd end : ', end)
print(' *** cmd duration : ', end - start)

# OBO -> This is a profiling sample. Run this to know what takes time & how long. Benched code is the content of profiled_function