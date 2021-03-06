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

"""Indexes on action_logs.body

Revision ID: 278885b460cd
Revises: 567ac5955ca3
Create Date: 2015-08-24 14:45:03.193144

"""

# revision identifiers, used by Alembic.
revision = '278885b460cd'
down_revision = '567ac5955ca3'

from alembic import op


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE INDEX action_logs_body_action_type ON "
               "action_logs ((body->>'action_type'))")
    op.execute("CREATE INDEX action_logs_body_action_name ON "
               "action_logs ((body->>'action_name'))")
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.execute("DROP INDEX action_logs_body_action_name")
    op.execute("DROP INDEX action_logs_body_action_type")
    ### end Alembic commands ###
