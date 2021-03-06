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

"""version_info added

Revision ID: 4f46e2c07565
Revises: 278885b460cd
Create Date: 2015-12-15 11:51:56.237567

"""

# revision identifiers, used by Alembic.
revision = '4f46e2c07565'
down_revision = '278885b460cd'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'oswl_stats',
        sa.Column('version_info', postgresql.JSON(), nullable=True)
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('oswl_stats', 'version_info')
    ### end Alembic commands ###
