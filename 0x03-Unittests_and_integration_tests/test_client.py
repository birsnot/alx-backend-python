#!/usr/bin/env python3
"""Unit tests for client.py"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient class"""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected_response, mock_get_json):
        """Test that GithubOrgClient.org returns correct org info"""
        mock_get_json.return_value = expected_response
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected_response)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns expected URL from mocked org"""
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock
        ) as mock_org:
            expected_url = "https://api.github.com/orgs/test-org/repos"
            mock_org.return_value = {"repos_url": expected_url}

            client = GithubOrgClient("test-org")
            self.assertEqual(client._public_repos_url, expected_url)
