from sos.report.plugins import Plugin, RedHatPlugin, DebianPlugin, UbuntuPlugin
import os
from sos import utilities


class Morpheus_RabbitMQ(Plugin, RedHatPlugin, DebianPlugin, UbuntuPlugin):

    short_desc = 'Morpheus RabbitMQ Service'
    plugin_name = 'morpheus_rabbitmq'
    profiles = ('services',)

    rmq_embedded = True
    rmq_config_file = ""
    morpheus_application_yml = "/opt/morpheus/conf/application.yml"

    def check_rmq_embedded(self):
        rmq_status_local = self.collect_cmd_output("morpheus-ctl status rabbitmq")
        if not rmq_status_local['output']:
            self.rmq_embedded = False

    def setup(self):

        if self.rmq_embedded:
            original_env = os.environ
            envopts = {
                # 'HOME': '/opt/morpheus/embedded/rabbitmq',
                'PREPATH': '/opt/morpheus/bin:/opt/morpheus/embedded/bin:/opt/morpheus/embedded/sbin',
                'ERL_EPMD_ADDRESS': '127.0.0.1',
                'RABBITMQ_CONF_ENV_FILE': '/opt/morpheus/embedded/rabbitmq/etc/rabbitmq-env.conf',
                'RABBITMQ_SYS_PREFIX': '/opt/morpheus/embedded/rabbitmq',
                'RABBITMQ_CONFIG_FILE': '/opt/morpheus/embedded/rabbitmq/etc/rabbit',
                'RABBITMQ_MNESIA_BASE': '/var/opt/morpheus/rabbitmq/db',
                'RABBITMQ_SCHEMA_DIR': '/opt/morpheus/embedded/rabbitmq/priv/schema',
                'RABBITMQ_ENABLED_PLUGINS_FILE': '/opt/morpheus/embedded/rabbitmq/etc/enabled_plugins',
                'RABBITMQ_LOG_BASE': '/var/log/morpheus/rabbitmq',
                'RABBITMQ_NODE_IP_ADDRESS': '127.0.0.1',
                'RABBITMQ_NODE_PORT': '5672',
                'RABBITMQ_PID_FILE': '/var/run/morpheus/rabbitmq/rabbit@localhost.pid',
                'RABBITMQ_NODENAME': 'rabbit@localhost'
            }
            envopts['PATH'] = envopts['PREPATH'] + ":" + os.environ['PATH']
            os.environ.update(envopts)
            #envopts = {'HOME': '/opt/morpheus/embedded/rabbitmq'}
            #self.add_cmd_output("rabbitmqctl report")
            out = utilities.sos_get_command_output("rabbitmqctl report")
            self.add_string_as_file(out['output'], "rabbitmqctl_report_out")
            os.environ = original_env

            self.add_copy_spec([
                "/opt/morpheus/embedded/rabbitmq/etc/*",
                "/opt/morpheus/embedded/rabbitmq/etc/*",
                "/etc/security/limits.d/",
                "/etc/systemd/"
            ])
            self.add_copy_spec([
                "/var/log/morpheus/rabbitmq/*",
            ])
