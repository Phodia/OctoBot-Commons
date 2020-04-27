#  Drakkar-Software OctoBot
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.


import sys
import os
import platform

from octobot_commons.constants import PLATFORM_DATA_SEPARATOR
from octobot_commons.enums import OctoBotTypes, PlatformsName


def get_current_platform():
    """
    Return the current platform details
    Return examples
    For Windows :
    >>> 'Windows:10:AMD64'
    For Linux :
    >>> 'Linux:4.15.0-46-generic:x86_64'
    For Raspberry :
    >>> 'Linux:4.14.98-v7+:armv7l'
    :return: the current platform details
    """
    return (
        f"{platform.system()}{PLATFORM_DATA_SEPARATOR}{platform.release()}{PLATFORM_DATA_SEPARATOR}"
        f"{platform.machine()}"
    )


def get_octobot_type():
    """
    Return OctoBot running type from OctoBotTypes
    :return: the OctoBot running type
    """
    try:
        execution_arg = sys.argv[0]
        # sys.argv[0] is always the name of the python script called when using a command "python xyz.py"
        if execution_arg.endswith(".py"):
            if _is_on_docker():
                return OctoBotTypes.DOCKER.value
            return OctoBotTypes.PYTHON.value
        # sys.argv[0] is the name of the binary when using a binary version: ends with nothing or .exe"
        return OctoBotTypes.BINARY.value
    except IndexError:
        return OctoBotTypes.BINARY.value


def get_os():
    """
    Return the OS name
    :return: the OS name
    """
    return PlatformsName(os.name)


def _is_on_docker():
    """
    Check if the current platform is docker
    :return: True if OctoBot is running with docker
    """
    file_to_check = "/proc/self/cgroup"
    try:
        return os.path.exists("/.dockerenv") or (
            os.path.isfile(file_to_check)
            and any("docker" in line for line in open(file_to_check))
        )
    except FileNotFoundError:
        return False
