#!/usr/bin/env python
# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging

from django.utils.translation import ugettext as _

from desktop.conf import CONNECTORS_BLACKLIST, CONNECTORS_WHITELIST


LOG = logging.getLogger(__name__)


CONNECTOR_TYPES = [
  {
    'id': 'hive',
    'dialect': 'hive',
    'nice_name': 'Hive',
    'description': '',
    'category': 'editor',
    'interface': 'hiveserver2',
    'settings': [
      {'name': 'server_host', 'value': ''},
      {'name': 'server_port', 'value': ''},
    ],
    'properties': {
      'is_sql': True,
      'sql_identifier_quote': '`',
      'sql_identifier_comment_single': '--',
      'has_catalog': True,
      'has_database': True,
      'has_table': True,
      'has_live_queries': False,
      'has_optimizer_risks': True,
      'has_optimizer_values': True,
      'has_auto_limit': False,
    }
  },
  {
    'nice_name': "Impala",
    'dialect': 'impala',
    'interface': 'hiveserver2',
    'settings': [{'name': 'server_host', 'value': ''}, {'name': 'server_port', 'value': ''},],
    'category': 'editor',
    'description': '',
    'properties': {
      'is_sql': True
    }
  },
  {
    'nice_name': "Hive Tez",
    'dialect': 'hive-tez',
    'interface': 'hiveserver2',
    'settings': [{'name': 'server_host', 'value': ''}, {'name': 'server_port', 'value': ''},],
    'category': 'editor',
    'description': '',
    'properties': {'is_sql': True}
  },
  {'nice_name': "Hive LLAP", 'dialect': 'hive-llap', 'interface': 'hiveserver2', 'settings': [{'name': 'server_host', 'value': ''}, {'name': 'server_port', 'value': ''},], 'category': 'editor', 'description': '', 'properties': {'is_sql': True}},
  {'nice_name': "Druid", 'dialect': 'sql-druid', 'interface': 'sqlalchemy', 'settings': [{'name': 'url', 'value': 'druid://druid-host.com:8082/druid/v2/sql/'}], 'category': 'editor', 'description': '', 'properties': {'is_sql': True}},
  {'nice_name': "Kafka SQL", 'dialect': 'ksql', 'interface': 'ksql', 'settings': [], 'category': 'editor', 'description': '', 'properties': {'is_sql': True}},
  {'nice_name': "Flink SQL", 'dialect': 'flink', 'interface': 'flink', 'settings': [{'name': 'api_url', 'value': 'http://flink:10000'}], 'category': 'editor', 'description': '', 'properties': {'is_sql': True}},
  {'nice_name': "SparkSQL", 'dialect': 'spark-sql', 'interface': 'sqlalchemy', 'settings': [], 'category': 'editor', 'description': '', 'properties': {'is_sql': True}},
  {
    'nice_name': "MySQL",
    'dialect': 'mysql',
    'interface': 'sqlalchemy',
    'settings': [{'name': 'url', 'value': 'mysql://username:password@mysq-host:3306/hue'}],
    'category': 'editor',
    'description': '',
    'properties': {
      'is_sql': True,
      'sql_identifier_quote': '`',
      'sql_identifier_comment_single': '--',
      'has_catalog': True,
      'has_database': True,
      'has_table': True,
      'has_live_queries': False,
      'has_optimizer_risks': False,
      'has_optimizer_values': False,
      'has_auto_limit': False,
    }
  },
  {
    'nice_name': "PostgreSQL",
    'dialect': 'postgresql',
    'interface': 'sqlalchemy',
    'settings': [{'name': 'url', 'value': 'postgresql://username:password@host:5432/hue'}],
    'category': 'editor',
    'description': '',
    'properties': {
      'is_sql': True,
      'sql_identifier_quote': '"',
      'sql_identifier_comment_single': '--',
      'has_catalog': True,
      'has_database': True,
      'has_table': True,
      'has_live_queries': False,
      'has_optimizer_risks': False,
      'has_optimizer_values': False,
      'has_auto_limit': False,
    }
  },
  {'nice_name': "Presto", 'dialect': 'presto', 'interface': 'sqlalchemy', 'settings': [], 'category': 'editor', 'description': '', 'properties': {'is_sql': True}},
  {'nice_name': "Athena", 'dialect': 'athena', 'interface': 'sqlalchemy', 'settings': [], 'category': 'editor', 'description': '', 'properties': {'is_sql': True}},
  {'nice_name': "Redshift", 'dialect': 'redshift', 'interface': 'sqlalchemy', 'settings': [], 'category': 'editor', 'description': '', 'properties': {'is_sql': True}},
  {'nice_name': "Big Query", 'dialect': 'bigquery', 'interface': 'sqlalchemy', 'settings': [], 'category': 'editor', 'description': '', 'properties': {'is_sql': True}},
  {'nice_name': "Oracle", 'dialect': 'oracle', 'interface': 'sqlalchemy', 'settings': [], 'category': 'editor', 'description': '', 'properties': {'is_sql': True}},
  {'nice_name': "SQL Database", 'dialect': 'sql-alchemy', 'interface': 'sqlalchemy', 'settings': [], 'category': 'editor', 'description': '', 'properties': {'is_sql': True}},
  {'nice_name': "SQL Database (JDBC)", 'dialect': 'sql-jdbc', 'interface': 'sqlalchemy', 'settings': [], 'category': 'editor', 'description': 'Deprecated: older way to connect to any database.', 'properties': {'is_sql': True}},
  # solr
  # hbase
  # kafka

  {'nice_name': "PySpark", 'dialect': 'pyspark', 'settings': [], 'category': 'editor', 'description': '', 'properties': {}},
  {'nice_name': "Spark", 'dialect': 'spark', 'settings': [], 'category': 'editor', 'description': '', 'properties': {}},
  {'nice_name': "Pig", 'dialect': 'pig', 'settings': [], 'category': 'editor', 'description': '', 'properties': {}},
  {'nice_name': "Java", 'dialect': 'java', 'settings': [], 'category': 'editor', 'description': '', 'properties': {}},

  {'nice_name': "HDFS", 'dialect': 'hdfs', 'interface': 'rest', 'settings': [{'name': 'server_url', 'value': 'http://localhost:9870/webhdfs/v1'}, {'name': 'default_fs', 'value': 'fs_defaultfs=hdfs://localhost:8020'}], 'category': 'browsers', 'description': '', 'properties': {}},
  {'nice_name': "YARN", 'dialect': 'yarn', 'settings': [], 'category': 'browsers', 'description': '', 'properties': {}},
  {'nice_name': "S3", 'dialect': 's3', 'settings': [], 'category': 'browsers', 'description': '', 'properties': {}},
  {'nice_name': "ADLS", 'dialect': 'adls-v1', 'settings': [], 'category': 'browsers', 'description': '', 'properties': {}},

  {
    'nice_name': "Hive Metastore",
    'dialect': 'hms',
    'interface': 'hiveserver2',
    'settings': [{'name': 'server_host', 'value': ''}, {'name': 'server_port', 'value': ''},],
    'category': 'catalogs',
    'description': '',
    'properties': {}
  },
  {'nice_name': "Atlas", 'dialect': 'atlas', 'interface': 'rest', 'settings': [], 'category': 'catalogs', 'description': '', 'properties': {}},
  {'nice_name': "Navigator", 'dialect': 'navigator', 'interface': 'rest', 'settings': [], 'category': 'catalogs', 'description': '', 'properties': {}},

  {'nice_name': "Optimizer", 'dialect': 'optimizer', 'settings': [], 'category': 'optimizers', 'description': '', 'properties': {}},

  {'nice_name': "Oozie", 'dialect': 'oozie', 'settings': [], 'category': 'schedulers', 'description': '', 'properties': {}},
  {'nice_name': "Celery", 'dialect': 'celery', 'settings': [], 'category': 'schedulers', 'description': '', 'properties': {}},
]

CONNECTOR_TYPES = [connector for connector in CONNECTOR_TYPES if connector['dialect'] not in CONNECTORS_BLACKLIST.get()]

if CONNECTORS_WHITELIST.get():
  CONNECTOR_TYPES = [connector for connector in CONNECTOR_TYPES if connector['dialect'] in CONNECTORS_WHITELIST.get()]


CATEGORIES = [
  {"name": "Editor", 'type': 'editor', 'description': ''},
  {"name": "Browsers", 'type': 'browsers', 'description': ''},
  {"name": "Catalogs", 'type': 'catalogs', 'description': ''},
  {"name": "Optimizers", 'type': 'optimizers', 'description': ''},
  {"name": "Schedulers", 'type': 'schedulers', 'description': ''},
  {"name": "Plugins", 'type': 'plugins', 'description': ''},
]
