# -*- coding: utf-8 -*-

#    Copyright 2015 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import csv
from datetime import datetime
import mock
import six
import types

from fuel_analytics.test.api.resources.utils.inst_structure_test import \
    InstStructureTest
from fuel_analytics.test.base import DbTest

from fuel_analytics.api.app import app
from fuel_analytics.api.app import db
from fuel_analytics.api.db.model import ActionLog
from fuel_analytics.api.resources.csv_exporter import get_action_logs
from fuel_analytics.api.resources.csv_exporter import get_inst_structures
from fuel_analytics.api.resources.utils import export_utils
from fuel_analytics.api.resources.utils.stats_to_csv import StatsToCsv


class StatsToCsvExportTest(InstStructureTest, DbTest):

    def test_get_cluster_keys_paths(self):
        exporter = StatsToCsv()
        _, _, csv_keys_paths = exporter.get_cluster_keys_paths()
        self.assertIn(['attributes', 'heat'], csv_keys_paths)
        self.assertIn(['attributes', 'auto_assign_floating_ip'],
                      csv_keys_paths)
        self.assertIn(['attributes', 'corosync_verified'], csv_keys_paths)
        self.assertIn(['attributes', 'external_mongo_replset'], csv_keys_paths)
        self.assertIn(['attributes', 'external_ntp_list'], csv_keys_paths)
        self.assertIn(['attributes', 'mongo'], csv_keys_paths)
        self.assertIn(['attributes', 'nova_quota'], csv_keys_paths)
        self.assertIn(['attributes', 'repos'], csv_keys_paths)
        self.assertIn(['attributes', 'resume_guests_state_on_host_boot'],
                      csv_keys_paths)
        self.assertIn(['attributes', 'workloads_collector_enabled'],
                      csv_keys_paths)
        self.assertIn(['attributes', 'ironic'], csv_keys_paths)
        self.assertIn(['attributes', 'murano-cfapi'], csv_keys_paths)
        self.assertIn(['attributes', 'murano_glance_artifacts_plugin'],
                      csv_keys_paths)
        self.assertIn(['attributes', 'neutron_dvr'], csv_keys_paths)
        self.assertIn(['attributes', 'neutron_l2_pop'], csv_keys_paths)
        self.assertIn(['attributes', 'neutron_l3_ha'], csv_keys_paths)
        self.assertIn(['attributes', 'neutron_qos'], csv_keys_paths)
        self.assertIn(['attributes', 'public_ssl_cert_source'], csv_keys_paths)
        self.assertIn(['attributes', 'public_ssl_horizon'], csv_keys_paths)
        self.assertIn(['attributes', 'public_ssl_services'], csv_keys_paths)
        self.assertIn(['attributes', 'puppet_debug'], csv_keys_paths)
        self.assertIn(['attributes', 'task_deploy'], csv_keys_paths)

        self.assertIn(['vmware_attributes', 'vmware_az_cinder_enable'],
                      csv_keys_paths)
        self.assertIn(['vmware_attributes', 'vmware_az_nova_computes_num'],
                      csv_keys_paths)
        self.assertIn(['structure', 'fuel_packages', 0], csv_keys_paths)
        self.assertNotIn(['structure', 'clusters'], csv_keys_paths)
        self.assertNotIn(['installed_plugins'], csv_keys_paths)

    def test_get_flatten_clusters(self):
        installations_num = 200
        inst_structures = self.get_saved_inst_structures(
            installations_num=installations_num)
        exporter = StatsToCsv()
        structure_paths, cluster_paths, csv_paths = \
            exporter.get_cluster_keys_paths()
        flatten_clusters = exporter.get_flatten_clusters(
            structure_paths, cluster_paths, inst_structures, [])
        self.assertIsInstance(flatten_clusters, types.GeneratorType)
        for flatten_cluster in flatten_clusters:
            self.assertEqual(len(csv_paths), len(flatten_cluster))

    def test_flatten_data_as_csv(self):
        installations_num = 100
        inst_structures = self.get_saved_inst_structures(
            installations_num=installations_num)

        exporter = StatsToCsv()
        structure_paths, cluster_paths, csv_paths = \
            exporter.get_cluster_keys_paths()
        flatten_clusters = exporter.get_flatten_clusters(
            structure_paths, cluster_paths, inst_structures, [])
        self.assertIsInstance(flatten_clusters, types.GeneratorType)
        result = export_utils.flatten_data_as_csv(csv_paths, flatten_clusters)
        self.assertIsInstance(result, types.GeneratorType)
        output = six.StringIO(list(result))
        reader = csv.reader(output)
        # Pop columns names from reader
        _ = reader.next()

        # Checking reading result CSV
        for _ in reader:
            pass

    def test_unicode_as_csv(self):
        installations_num = 10
        inst_structures = self.get_saved_inst_structures(
            installations_num=installations_num)

        exporter = StatsToCsv()
        structure_paths, cluster_paths, csv_paths = \
            exporter.get_cluster_keys_paths()
        flatten_clusters = exporter.get_flatten_clusters(
            structure_paths, cluster_paths, inst_structures, [])
        flatten_clusters = list(flatten_clusters)
        flatten_clusters[1][0] = u'эюя'
        list(export_utils.flatten_data_as_csv(csv_paths, flatten_clusters))

    def test_export_clusters(self):
        installations_num = 100
        inst_structures = self.get_saved_inst_structures(
            installations_num=installations_num)
        exporter = StatsToCsv()
        result = exporter.export_clusters(inst_structures, [])
        self.assertIsInstance(result, types.GeneratorType)

    def test_filter_by_date(self):
        exporter = StatsToCsv()
        num = 10
        with app.test_request_context('/?from_date=2015-02-01'):

            # Creating installation structures
            inst_structures = self.get_saved_inst_structures(
                installations_num=num)
            # Filtering installation structures
            result = exporter.export_clusters(inst_structures, [])
            self.assertIsInstance(result, types.GeneratorType)
            output = six.StringIO(list(result))
            reader = csv.reader(output)
            for _ in reader:
                pass

    def test_network_verification_status(self):
        num = 2
        inst_structures = self.get_saved_inst_structures(
            installations_num=num, clusters_num_range=(2, 2))
        inst_structure = inst_structures[0]
        clusters = inst_structure.structure['clusters']
        exporter = StatsToCsv()
        expected_als = [
            ActionLog(
                master_node_uid=inst_structure.master_node_uid,
                external_id=1,
                action_type='nailgun_task',
                action_name=exporter.NETWORK_VERIFICATION_ACTION,
                body={'cluster_id': clusters[0]['id'],
                      'end_timestamp': datetime.utcnow().isoformat(),
                      'action_type': 'nailgun_task',
                      'action_name': exporter.NETWORK_VERIFICATION_ACTION,
                      'additional_info': {'ended_with_status': 'error'}}
            ),
            ActionLog(
                master_node_uid=inst_structure.master_node_uid,
                external_id=2,
                action_type='nailgun_task',
                action_name=exporter.NETWORK_VERIFICATION_ACTION,
                body={'cluster_id': clusters[1]['id'],
                      'end_timestamp': datetime.utcnow().isoformat(),
                      'action_type': 'nailgun_task',
                      'action_name': exporter.NETWORK_VERIFICATION_ACTION,
                      'additional_info': {'ended_with_status': 'ready'}}
            )
        ]

        with app.test_request_context():
            for action_log in expected_als:
                db.session.add(action_log)
            db.session.commit()

            action_logs = get_action_logs()
            inst_structures = get_inst_structures()
            structure_keys_paths, cluster_keys_paths, csv_keys_paths = \
                exporter.get_cluster_keys_paths()
            flatten_clusters = list(exporter.get_flatten_clusters(
                structure_keys_paths, cluster_keys_paths,
                inst_structures, action_logs))
            self.assertIn([exporter.NETWORK_VERIFICATION_COLUMN],
                          csv_keys_paths)
            nv_column_pos = csv_keys_paths.index(
                [exporter.NETWORK_VERIFICATION_COLUMN])

            # Checking cluster network verification statuses
            for al_pos, expected_al in enumerate(expected_als):
                self.assertEqual(
                    expected_al.body['additional_info']['ended_with_status'],
                    flatten_clusters[al_pos][nv_column_pos]
                )
            # Checking empty network verification status
            for flatten_cluster in flatten_clusters[2:]:
                self.assertIsNone(flatten_cluster[nv_column_pos])

    def test_vmware_attributes(self):
        exporter = StatsToCsv()
        inst_structures = self.generate_inst_structures(
            clusters_num_range=(1, 1))
        result = exporter.export_clusters(inst_structures, [])
        for _ in result:
            pass

    def test_cluster_invalid_data(self):
        exporter = StatsToCsv()
        num = 10
        inst_structures = self.get_saved_inst_structures(
            installations_num=num, clusters_num_range=(1, 1))

        with app.test_request_context():
            # get_flatten_data 2 times called inside get_flatten_plugins
            side_effect = [[]] * num * 2
            side_effect[num / 2] = Exception
            with mock.patch('fuel_analytics.api.resources.utils.'
                            'export_utils.get_flatten_data',
                            side_effect=side_effect):
                structure_paths, cluster_paths, csv_paths = \
                    exporter.get_cluster_keys_paths()
                flatten_clusters = exporter.get_flatten_clusters(
                    structure_paths, cluster_paths, inst_structures, [])
                self.assertEqual(num - 1, len(list(flatten_clusters)))
