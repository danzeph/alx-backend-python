#!/usr/bin/env python3
"""test for client module."""

import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import Mock, PropertyMock, patch
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for GithubOrgClient.org"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """org returns the mocked JSON response"""

        payload = {"org": org_name}
        mock_get_json.return_value = payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """public_repos_url returns repos_url from org payload"""

        payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }

        with patch.object(
            GithubOrgClient,
            'org',
            new_callable=PropertyMock
        ) as mock_org:

            mock_org.return_value = payload

            client = GithubOrgClient("google")
            result = client._public_repos_url
            # print(result)
            self.assertEqual(
                result,
                payload["repos_url"]
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """GithubOrgClient.public_repos returns the known payload(repos)."""
        repos_payload = [
            {'name': 'episodes.dart'},
            {'name': 'cpp-netlib'},
            {'name': 'dagger'},
            {'name': 'ios-webkit-debug-proxy'},
        ]

        mock_get_json.return_value = repos_payload

        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock
        )as mock_public_repos_url:
            org_payload = {
                "repos_url": "https://api.github.com/orgs/google/repos"
            }
            mock_public_repos_url.return_value = org_payload["repos_url"]

            client = GithubOrgClient("google")
            result = client.public_repos()

            expected_repos = [
                'episodes.dart',
                'cpp-netlib',
                'dagger',
                'ios-webkit-debug-proxy'
                ]
            # ommitted some to show the public_repos was really called
            # uncomment to see assertion results
            # expected_repos = ['episodes.dart','ios-webkit-debug-proxy']

            self.assertEqual(result, expected_repos)
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(org_payload['repos_url'])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        has_license returns True only when license_key matches repo license
        """

        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(
    (
        "org_payload",
        "repos_payload",
        "expected_repos",
        "apache2_repos",
    ), [TEST_PAYLOAD[0]]

)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient."""

    @classmethod
    def setUpClass(cls):
        """Set up class fixtures and mock request.get"""

        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            """Return the appropriate mocked responsed based on URL"""
            mock_response = Mock()
            if url == "https://api.github.com/orgs/google":
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repos"""
        client = GithubOrgClient("google")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test filtered repos by Apache 2.0 license"""
        client = GithubOrgClient("google")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
