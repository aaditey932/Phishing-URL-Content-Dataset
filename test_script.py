import unittest
import requests
import pandas as pd
from bs4 import BeautifulSoup
from script import (
    extract_link_density,
    extract_link_features,
    extract_ip_address,
    extract_iframes,
    extract_certificate,
    extract_if_https,
    extract_whois,
    create_dataset
)


class TestFeatureExtraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Setup HTML content and domain for testing by fetching from a live domain.
        """
        cls.domain = "duotriali.com"
        cls.url = f"http://{cls.domain}"  # Assuming the domain uses HTTP
        try:
            response = requests.get(cls.url, timeout=10)
            response.raise_for_status()
            cls.soup = BeautifulSoup(response.content, "html.parser")
        except requests.RequestException as e:
            cls.soup = None
            print(f"Failed to fetch HTML content from {cls.url}: {e}")

    def test_extract_link_density(self):
        if self.soup:
            result = extract_link_density(self.soup)
            self.assertIsInstance(result, float)
            self.assertGreaterEqual(result, 0)
        else:
            self.skipTest("HTML content could not be fetched for testing.")

    def test_extract_link_features(self):
        if self.soup:
            external_count, internal_count, ip_based_count, https_count, http_count, non_count = extract_link_features(
                self.soup, self.domain
            )
            self.assertIsInstance(external_count, int)
            self.assertIsInstance(internal_count, int)
            self.assertIsInstance(https_count, int)
            self.assertIsInstance(http_count, int)
        else:
            self.skipTest("HTML content could not be fetched for testing.")

    def test_extract_ip_address_valid(self):
        result = extract_ip_address(self.domain)
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "Error")

    def test_extract_ip_address_invalid(self):
        result = extract_ip_address("invalid_domain")
        self.assertEqual(result, "Error")

    def test_extract_iframes(self):
        if self.soup:
            external_iframes_count, hidden_iframes_count = extract_iframes(self.soup)
            self.assertIsInstance(external_iframes_count, int)
            self.assertIsInstance(hidden_iframes_count, int)
        else:
            self.skipTest("HTML content could not be fetched for testing.")

    def test_extract_certificate_valid(self):
        result = extract_certificate(self.domain)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 5)

    def test_extract_certificate_invalid(self):
        result = extract_certificate("invalid_domain")
        self.assertEqual(result, ("Error", "Error", "Error", "Error", "Error"))

    def test_extract_if_https(self):
        self.assertEqual(extract_if_https(f"https://{self.domain}"), 1)
        self.assertEqual(extract_if_https(f"http://{self.domain}"), 1)
        self.assertEqual(extract_if_https("ftp://example.com"), 0)

    def test_extract_whois_valid(self):
        result = extract_whois(self.domain)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)

    def test_extract_whois_invalid(self):
        result = extract_whois("invalid_domain")
        self.assertEqual(result, (None, None, None))

    def test_create_dataset(self):
        urls = ["google.com", "nonexistentdomain.test"]
        df = create_dataset(urls)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreaterEqual(len(df), 1)  # At least one valid domain should work


if __name__ == "__main__":
    unittest.main()
