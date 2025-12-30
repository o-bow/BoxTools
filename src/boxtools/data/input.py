#!/usr/bin/env python3

from boxtools.Logs import LogDisplay


def ask_for_value(value_name: str, desc: str = None, log: LogDisplay=None):
    if log is None:
        log = LogDisplay().get_log_display()
    value = input('Please write down your ' + value_name + ' (+ Enter' + ((' - ex: ' + desc) if desc is not None else '') + '): ')
    log.show_info_input_feedback_log(' -> Your ' + value_name.split('(')[0] + ': {1}', value)
    return value

# default choice must be the first element in choices_array; first letter of each choice MUST differ
def ask_for_choice(text, choices_array, log: LogDisplay=None):
    if log is None:
        log = LogDisplay().get_log_display()
    keys = [w[0] for w in choices_array]
    if len(keys) > 2:
        keys_prompt = '\n'.join(map(lambda c: ' - (' + c[0] + ')' + c[1:], choices_array))
        prompt_str = text + ' Available choices: \n' + keys_prompt + '\n'
    else:
        keys_prompt = '/'.join(map(lambda c: '(' + c[0] + ')' + c[1:], choices_array))
        prompt_str = text + ' ' + keys_prompt + ': '
    log.show_debug_log(' - keys: ' + '/'.join(keys))
    choice = input(prompt_str)
    log.show_debug_log(' - choice: ' + choice)
    for idx, value in enumerate(keys):
        #show_debug_log(' - loop: ' + str(idx) + ' ' + value + ' ' + choice)
        # Default value
        if not choice and idx == 0:
            return choices_array[0]
        # Matching choice
        elif choice in [value.lower(), value.upper(), choices_array[idx]]:
            return choices_array[idx]
    log.show_debug_log('  - choice not found')
    return None