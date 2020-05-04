from sos.plugins import Plugin, RedHatPlugin, DebianPlugin, UbuntuPlugin
import re
import os
import yaml


class MorpheusElastic(Plugin, RedHatPlugin, DebianPlugin, UbuntuPlugin):

    short_desc = 'Morpheus ElasticSearch Service'
    plugin_name = 'morpheus_elastic'
    profiles = ('services', )

    es_embedded = True
    es_config_file = ""
    morpheus_application_yml = "/opt/morpheus/conf/application.yml"

    def check_es_embedded(self):
        es_status_local = self.collect_cmd_output("morpheus-ctl status elasticsearch")
        if not es_status_local['output']:
            self.es_embedded = False

    def get_remote_hostnames_ports(self):
        if os.path.isfile(self.morpheus_application_yml):
            with open(self.morpheus_application_yml) as appyml:
                appyml_data = yaml.load(appyml, Loader=yaml.FullLoader)

        es_hosts = []
        es_config = appyml_data['environments']['production']['elasticSearch']
        es_host_detail = es_config['client']['hosts']
        return es_host_detail

    def get_local_hostname_port(self):
        if os.path.isfile(self.morpheus_application_yml):
            with open(self.morpheus_application_yml) as appyml:
                appyml_data = yaml.load(appyml, Loader=yaml.FullLoader)

        es_config = appyml_data['environments']['production']['elasticSearch']
        hostname = es_config['client']['hosts'][0]['host']
        port = es_config['client']['hosts'][0]['port']
        return str(hostname), str(port)

    def setup(self):
        self.check_es_embedded()
        if self.es_embedded:
            es_config_file = "/opt/morpheus/embedded/elasticsearch/config/elasticsearch.yml"
            self.add_copy_spec(es_config_file)

            log_base_dir = "/var/log/morpheus/elasticsearch/"
            self.add_copy_spec(log_base_dir + "morpheus_*.log")
            self.add_copy_spec(log_base_dir + "morpheus.log")
            self.add_copy_spec(log_base_dir + "current")

            host, port = self.get_local_hostname_port()

            endpoint = host + ":" + port
            self.add_cmd_output([
                "curl -X GET '%s/_cluster/settings?pretty'" % endpoint,
                "curl -X GET '%s/_cluster/health?pretty'" % endpoint,
                "curl -X GET '%s/_cluster/stats?pretty'" % endpoint,
                "curl -X GET '%s/_cat/nodes?v'" % endpoint,
            ])
        else:
            es_hosts = self.get_remote_hostnames_ports()
            for hp in es_hosts:
                endpoint = str(hp['host']) + ":" + str(hp['port'])
                self.add_cmd_output([
                    "curl -X GET '%s/_cluster/settings?pretty'" % endpoint,
                    "curl -X GET '%s/_cluster/health?pretty'" % endpoint,
                    "curl -X GET '%s/_cluster/stats?pretty'" % endpoint,
                    "curl -X GET '%s/_cat/nodes?v'" % endpoint,
                ])
