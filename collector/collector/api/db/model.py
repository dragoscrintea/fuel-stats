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

from sqlalchemy.dialects.postgresql import JSON

from collector.api.app import db
from collector.api.common import consts


class ActionLog(db.Model):
    __tablename__ = 'action_logs'
    __table_args__ = (
        db.UniqueConstraint('master_node_uid', 'external_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    master_node_uid = db.Column(db.String, nullable=False)
    external_id = db.Column(db.Integer, nullable=False)
    body = db.Column(db.Text, nullable=False)
    action_type = db.Column(db.Text)
    action_name = db.Column(db.Text)
    db.Index('ix_action_logs_action_name_action_type',
             'action_name', 'action_type')


class InstallationStructure(db.Model):
    __tablename__ = 'installation_structures'

    id = db.Column(db.Integer, primary_key=True)
    master_node_uid = db.Column(db.String, nullable=False, unique=True)
    structure = db.Column(JSON, nullable=False)
    creation_date = db.Column(db.DateTime)
    modification_date = db.Column(db.DateTime)
    is_filtered = db.Column(db.Boolean, default=False, index=True)
    release = db.Column(db.Text, index=True)


class OpenStackWorkloadStats(db.Model):
    __tablename__ = 'oswl_stats'
    __table_args__ = (
        db.UniqueConstraint('master_node_uid', 'external_id',
                            'resource_type'),
    )

    id = db.Column(db.Integer, primary_key=True)
    master_node_uid = db.Column(db.Text, nullable=False, index=True)
    external_id = db.Column(db.Integer, nullable=False, index=True)
    cluster_id = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.Date, nullable=False, index=True)
    updated_time = db.Column(db.Time, nullable=False)
    resource_type = db.Column(
        db.Enum(*consts.OSWL_RESOURCE_TYPES, name='oswl_resource_type'),
        nullable=False,
        index=True
    )
    resource_data = db.Column(JSON, nullable=True)
    resource_checksum = db.Column(db.Text, nullable=False)
    version_info = db.Column(JSON, nullable=True)
