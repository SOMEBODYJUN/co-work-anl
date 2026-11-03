"""Credential routing and resource operations tested without starting cloud jobs."""
from io import BytesIO
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock
import urllib.error
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import github_resources as github


class GitHubResourceTests(unittest.TestCase):
    def client(self):
        client = object.__new__(github.Client)
        client.repository = 'OWNER/research'
        client._token = 'test credential sentinel'
        client.request = mock.Mock()
        return client

    def test_status_performs_only_repository_reads_and_separates_missing_permissions(self):
        client = self.client()
        client.request.side_effect = [{'full_name': 'OWNER/research', 'default_branch': 'main', 'permissions': {'push': True}}, {'workflows': [], 'total_count': 0}, github.APIError(403, 'Codespaces permission absent')]
        result = client.status()
        self.assertEqual(result['mutations_performed'], 0)
        self.assertEqual(result['resource_operations']['codespaces']['http_status'], 403)
        self.assertTrue(all(call.args[0] == 'GET' for call in client.request.call_args_list))
        self.assertNotEqual(result['student_verification'], True)

    def test_authentication_failure_stops_followup_requests(self):
        client = self.client(); client.request.side_effect = github.APIError(401, 'Bad credentials')
        with self.assertRaises(github.APIError): client.status()
        self.assertEqual(client.request.call_count, 1)

    def test_dispatch_uses_an_explicit_known_workflow_and_does_not_claim_pass(self):
        client = self.client(); client.request.return_value = {'http_status': 204}
        result = client.dispatch('research-compute.yml', 'rebuild/research-v2', {'experiment': 'runtime-smoke'})
        self.assertEqual(result['status'], 'dispatch-request-accepted')
        self.assertEqual(client.request.call_args.args[0], 'POST')
        self.assertEqual(client.request.call_args.args[2]['ref'], 'rebuild/research-v2')
        with self.assertRaises(ValueError): client.dispatch('other.yml', 'main', {})

    def test_codespace_creation_requires_an_actual_available_machine(self):
        client = self.client(); client.machines = mock.Mock(return_value={'machines': [{'name': 'two-core', 'cpus': 2}]})
        with self.assertRaises(ValueError): client.create('main', 'invented-machine')
        self.assertEqual(client.request.call_count, 0)
        client.request.return_value = {'name': 'created-space', 'state': 'Starting'}
        self.assertEqual(client.create('main', 'two-core')['name'], 'created-space')

    def test_stop_refuses_another_repositories_codespace(self):
        client = self.client(); client.request.return_value = {'repository': {'full_name': 'OTHER/private'}}
        with self.assertRaisesRegex(ValueError, 'another repository'): client.stop('space-name')
        self.assertEqual(client.request.call_count, 1)

    def test_redirect_does_not_forward_authorization(self):
        with self.assertRaises(github.APIError): github.NoRedirect().redirect_request(None, None, 302, 'Redirect', {}, 'https://another.example/')

    def test_api_error_redacts_exact_credential(self):
        client = self.client()
        del client.request
        client._opener = mock.Mock()
        client._opener.open.side_effect = urllib.error.HTTPError('https://api.github.com/repos/OWNER/research', 401, 'denied', {}, BytesIO(json.dumps({'message': client._token}).encode()))
        with self.assertRaises(github.APIError) as context: client.request('GET', '/repos/OWNER/research')
        self.assertNotIn(client._token, str(context.exception))
        self.assertIn('[REDACTED]', str(context.exception))


if __name__ == '__main__': unittest.main()
