from sos.plugins import Plugin, RedHatPlugin, DebianPlugin, UbuntuPlugin


class Morpheus(Plugin, RedHatPlugin, DebianPlugin, UbuntuPlugin):

    short_desc = "Morpheus UI"
    plugin_name = "morpheus"
    profiles = ('services', )

    def setup(self):
        self.add_copy_spec("/etc/morpheus/*")
        self.add_copy_spec("/opt/morpheus/version-manifest.json")
        self.add_copy_spec("/opt/morpheus/conf/application.yml")
        self.add_forbidden_path("/etc/morpheus/ssl/*")
        self.add_cmd_output([
            'morpheus-ctl status'
        ])
