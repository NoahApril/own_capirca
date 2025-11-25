"""Tests for MigrationAPIClient integration helper."""

from __future__ import annotations

import json
from unittest import mock

import pytest

from capirca.utils import migration


class FakeResponse:
  def __init__(self, payload=None, status_code=200):
    self._payload = payload or {}
    self.status_code = status_code
    self.text = json.dumps(self._payload)

  def json(self):
    return self._payload


def test_persist_migration_output_calls_api():
  session = mock.Mock()
  session.post.side_effect = [
      FakeResponse({'id': 10, 'name': 'NET_GROUP'}),
      FakeResponse({'id': 11, 'name': 'SVC_TCP_80'}),
      FakeResponse({'id': 12, 'name': 'policy'}),
      FakeResponse({'is_valid': True, 'errors': []}),
  ]

  client = migration.MigrationAPIClient('http://localhost:8000/api', session=session)
  net_objects = {'NET_GROUP': ['10.0.0.0/8']}
  svc_objects = {
      'SVC_TCP_80': migration.ServiceDef(
          name='SVC_TCP_80', ports=['80'], protocols=['tcp'])
  }

  result = client.persist_migration_output(
      policy_content='term allow { action:: accept }',
      policy_name='demo-policy',
      network_objects=net_objects,
      service_objects=svc_objects,
  )

  assert result['policy']['id'] == 12
  assert result['validation']['is_valid']
  assert session.post.call_args_list[0][0][0] == 'http://localhost:8000/api/network-objects'
  assert session.post.call_args_list[1][0][0] == 'http://localhost:8000/api/service-objects'
  assert session.post.call_args_list[2][0][0] == 'http://localhost:8000/api/policies'
  assert session.post.call_args_list[3][0][0].endswith('/validate')


def test_api_client_raises_on_error():
  session = mock.Mock()
  session.post.return_value = FakeResponse({'detail': 'error'}, status_code=400)

  client = migration.MigrationAPIClient('http://localhost:8000/api', session=session)

  with pytest.raises(migration.MigrationAPIError):
    client.persist_policy('demo', 'content')
