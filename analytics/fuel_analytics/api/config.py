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

import logging
import os


class Production(object):
    DEBUG = False
    LOG_FILE = '/var/log/fuel-stats/analytics.log'
    LOG_LEVEL = logging.ERROR
    LOG_ROTATION = False
    LOGGER_NAME = 'analytics'
    ELASTIC_HOST = 'product-stats.mirantis.com'
    ELASTIC_PORT = 443
    ELASTIC_USE_SSL = True
    ELASTIC_INDEX_FUEL = 'fuel'
    ELASTIC_DOC_TYPE_STRUCTURE = 'structure'


class Testing(Production):
    DEBUG = False
    LOG_FILE = os.path.realpath(os.path.join(
        os.path.dirname(__file__), '..', 'test', 'logs', 'analytics.log'))
    LOG_LEVEL = logging.DEBUG
    LOG_ROTATION = True
    LOG_FILE_SIZE = 2048000
    LOG_FILES_COUNT = 5
    ELASTIC_HOST = 'localhost'
    ELASTIC_PORT = 9200
    ELASTIC_USE_SSL = False