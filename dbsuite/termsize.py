# vim: set et sw=4 sts=4:

# Copyright 2012 Dave Hughes.
#
# This file is part of dbsuite.
#
# dbsuite is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# dbsuite is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# dbsuite.  If not, see <http://www.gnu.org/licenses/>.

"""Contains a cross-platform terminal size querying routine"""

from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
    )

import sys
import struct

__all__ = ['terminal_size']

if sys.platform.startswith('win'):
    # ctypes query_console_size() adapted from
    # http://code.activestate.com/recipes/440694/
    import ctypes

    def terminal_size():
        "Returns the size (cols, rows) of the console"

        def get_handle_size(handle):
            "Subroutine for querying terminal size from std handle"
            handle = ctypes.windll.kernel32.GetStdHandle(handle)
            if handle:
                buf = ctypes.create_string_buffer(22)
                if ctypes.windll.kernel32.GetConsoleScreenBufferInfo(
                        handle, buf):
                    (left, top, right, bottom) = struct.unpack(
                        str('hhhhHhhhhhh'), buf.raw)[5:9]
                    return (right - left + 1, bottom - top + 1)
            return None

        stdin, stdout, stderr = -10, -11, -12
        return (
            get_handle_size(stderr) or
            get_handle_size(stdout) or
            get_handle_size(stdin) or
            # Default
            (80, 25)
        )

else:
    import fcntl
    import termios
    import os

    def terminal_size():
        "Returns the size (cols, rows) of the console"

        def get_handle_size(handle):
            "Subroutine for querying terminal size from std handle"
            try:
                buf = fcntl.ioctl(handle, termios.TIOCGWINSZ, '12345678')
                row, col = struct.unpack(str('hhhh'), buf)[0:2]
                return (col, row)
            except IOError:
                return None

        stdin, stdout, stderr = 0, 1, 2
        # Try stderr first as it's the least likely to be redirected
        result = (
            get_handle_size(stderr) or
            get_handle_size(stdout) or
            get_handle_size(stdin)
        )
        if not result:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            try:
                result = get_handle_size(fd)
            finally:
                os.close(fd)
        if not result:
            try:
                result = (os.environ['COLUMNS'], os.environ['LINES'])
            except KeyError:
                # Default
                result = (80, 24)
        return result
