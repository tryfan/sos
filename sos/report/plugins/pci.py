# This file is part of the sos project: https://github.com/sosreport/sos
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# version 2 of the GNU General Public License.
#
# See the LICENSE file in the source distribution for further information.

from sos.report.plugins import Plugin, RedHatPlugin, UbuntuPlugin, DebianPlugin
import os


class Pci(Plugin, RedHatPlugin, UbuntuPlugin, DebianPlugin):

    short_desc = 'PCI devices'

    plugin_name = "pci"
    profiles = ('hardware', 'system')

    def setup(self):
        self.add_copy_spec([
            "/proc/ioports",
            "/proc/iomem",
            "/proc/bus/pci"
        ])

        if os.path.isdir("/proc/bus/pci/00"):
            self.add_cmd_output("lspci -nnvv", root_symlink="lspci")
            self.add_cmd_output("lspci -tv")

# vim: set et ts=4 sw=4 :
