#!/usr/bin/env python3
"""Test client Module"""

import unittest
from unittest.mock import patch, PropertyMock, call, Mock
from parameterized import parameterized, parameterized_class
from urllib.error import HTTPError

GithubOrgClient = __import__('client').GithubOrgClient
TEST_PAYLOAD = __import__('fixtures').TEST_PAYLOAD


GithubOrgClient = __import__("client").GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Github Org Client Test Class"""

    @parameterized.expand(["google", "abc"])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test Org"""
        test_class = GithubOrgClient(org_name)
        test_class.org()
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test Public Repos URL property"""

        mock_payload = {
            "repos_url": "https://api.github.com/orgs/test_org/repos"
        }

        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_property:
            mock_property.return_value = mock_payload
            test_class = GithubOrgClient("test_org")
            self.assertEqual(
                test_class._public_repos_url, mock_payload["repos_url"]
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test  GithubOrgClient.public_repos method."""

        mock_repos_payload = [
            {"name": "repo1", "license": {"key": "my-license"}},
            {"name": "repo2", "license": {"key": "other-license"}},
            {"name": "repo3", "license": {"key": "my-license"}},
        ]

        mock_repos_url = "https://api.github.com/orgs/sample_org/repos"

        mock_get_json.return_value = mock_repos_payload

        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = mock_repos_url

            github_org_client = GithubOrgClient("sample_org")

            repos = github_org_client.public_repos("my-license")
            self.assertListEqual(repos, ["repo1", "repo3"])
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(mock_repos_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected_value):
        """Test GithubOrgClient.has_license method."""

        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_value)


@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Integration test for github org client """

    @classmethod
    def setUpClass(cls):
        """Set up resources for testing."""
        org = TEST_PAYLOAD[0][0]
        repos = TEST_PAYLOAD[0][1]
        org_mock = Mock()
        org_mock.json = Mock(return_value=org)
        cls.org_mock = org_mock
        repos_mock = Mock()
        repos_mock.json = Mock(return_value=repos)
        cls.repos_mock = repos_mock

        cls.get_patcher = patch('requests.get')
        cls.get = cls.get_patcher.start()

        options = {cls.org_payload["repos_url"]: repos_mock}
        cls.get.side_effect = lambda y: options.get(y, org_mock)

    @classmethod
    def tearDownClass(cls):
        """Tear down resources after testing."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test for public repositories."""
        y = GithubOrgClient("x")
        self.assertEqual(y.org, self.org_payload)
        self.assertEqual(y.repos_payload, self.repos_payload)
        self.assertEqual(y.public_repos(), self.expected_repos)
        self.assertEqual(y.public_repos("NONEXISTENT"), [])
        self.get.assert_has_calls([call("https://api.github.com/orgs/x"),
                                   call(self.org_payload["repos_url"])])

    def test_public_repos_with_license(self):
        """Test for public repositories with a specific license."""
        client_instance = GithubOrgClient("x")
        self.assertEqual(client_instance.org, self.org_payload)
        self.assertEqual(client_instance.repos_payload, self.repos_payload)
        self.assertEqual(client_instance.public_repos(), self.expected_repos)
        self.assertEqual(client_instance.public_repos("NONEXISTENT"), [])
        self.assertEqual(
            client_instance.public_repos("apache-2.0"), self.apache2_repos
        )
        self.get.assert_has_calls([call("https://api.github.com/orgs/x"),
                                   call(self.org_payload["repos_url"])])
