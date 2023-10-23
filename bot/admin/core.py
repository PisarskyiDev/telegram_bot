from __future__ import annotations

from typing import List

from bot.admin import command


def list_commands(default: bool = True) -> List[str] | List[object]:
    command_list = []
    for function in command.variables.items():
        function_name = function[0]
        function_object = function[1]

        if function_name[0] != "_":
            if default:
                command_list.append(function_name)
            else:
                command_list.append(function_object)
    return command_list


def find_command(name: str) -> object:
    command_list = list_commands(default=False)
    for function in command_list:
        if function.__name__ == name:
            return function
