#!/usr/bin/python3
# This file is part of the sos project: https://github.com/sosreport/sos
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# version 2 of the GNU General Public License.
#
# See the LICENSE file in the source distribution for further information.

import sys
import os

try:
    sys.path.insert(0, os.getcwd())
    from sos import SoS
except KeyboardInterrupt:
    raise SystemExit()


if __name__ == '__main__':
    sos = SoS(sys.argv[1:])
    sos.execute()