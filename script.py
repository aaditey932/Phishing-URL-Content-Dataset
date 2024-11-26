import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import socket
import ssl
import certifi
import whois
import pandas as pd

######################################################################################################################################################
# Helper Functions for Feature Extraction
######################################################################################################################################################

def extract_link_density(soup):
    """
    Calculates the link density of a webpage.
    
    Args:
        soup (BeautifulSoup): Parsed HTML content of the webpage.
        
    Returns:
        float or str: Link density as a float or 'Error' in case of exceptions.
    """
    try:

        link_count = len(soup.find_all('a'))
        text = soup.get_text(separator=" ")
        word_count = len(text.split())
        link_density = link_count / word_count if word_count > 0 else 0
        
        return link_density
    
    except Exception:
        return 'Error'
    
def extract_link_features(soup, domain):
    """
    Extracts link-related features from a webpage.
    
    Args:
        soup (BeautifulSoup): Parsed HTML content of the webpage.
        domain (str): Domain of the webpage being analyzed.
        
    Returns:
        tuple: (external_count, internal_count, ip_based_count, https_count, http_count, non_count)
        or tuple of 'Error' in case of exceptions.
    """
    try:
        # Extract all links from the webpage
        links = [a['href'] for a in soup.find_all('a', href=True)]

        # Initialize counters
        external_count = 0
        internal_count = 0
        ip_based_count = 0
        https_count = 0
        http_count = 0
        non_count = 0

        # Iterate through each link and compute statistics
        for link in links:
            parsed_url = urlparse(link)

            # External links
            if parsed_url.netloc and domain not in parsed_url.netloc:
                external_count += 1
            
            # Internal links
            if parsed_url.netloc and domain in parsed_url.netloc:
                internal_count += 1
            
            # IP-based links
            if parsed_url.hostname and parsed_url.hostname.replace('.', '').isdigit():
                ip_based_count += 1
            
            # Protocol-specific links
            if parsed_url.scheme == 'https':
                https_count += 1
            elif parsed_url.scheme == 'http':
                http_count += 1
            else:
                non_count += 1

        return external_count, internal_count, ip_based_count, https_count, http_count, non_count

    except Exception:
        return 'Error', 'Error', 'Error', 'Error', 'Error', 'Error'


def extract_ip_address(domain):
    """
    Retrieves the IP address of a domain.

    Args:
        domain (str): Domain name to resolve.

    Returns:
        str: IP address or 'Error' in case of exceptions.
    """
    try:

        ip_address = socket.gethostbyname(domain)

        return ip_address
    
    except Exception:
        return 'Error'

######################################################################################################################################################

def extract_iframes(soup):
    """
    Counts external and hidden iframes on a webpage.
    
    Args:
        soup (BeautifulSoup): Parsed HTML content of the webpage.

    Returns:
        tuple: (external_iframes_count, hidden_iframes_count) or ('Error', 'Error') in case of exceptions.
    """
    try:

        external_iframes_count = 0
        hidden_iframes_count = 0

        for iframe in soup.find_all('iframe'):
            src = iframe.get('src', '')
        
            # Check if iframe is external
            if urlparse(src).netloc and "your-website-domain.com" not in src:
                external_iframes_count += 1
        
            # Check if iframe is hidden (width or height == 0)
            if iframe.get('width') == '0' or iframe.get('height') == '0':
                hidden_iframes_count += 1
        
        return external_iframes_count, hidden_iframes_count

    except Exception:
        return 'Error', 'Error'

######################################################################################################################################################

def extract_certificate(domain):
    """
    Extracts SSL certificate details for a domain.

    Args:
        domain (str): Domain name to query.

    Returns:
        tuple: (country, org, certificatee, notBefore, notAfter)
        or ('Error', ...) in case of exceptions.
    """
    try:

        # Create an SSL context that uses the certifi CA bundle
        context = ssl.create_default_context(cafile=certifi.where())
        
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                certificate = ssock.getpeercert()
                country = certificate['issuer'][0][0][1]
                org = certificate['issuer'][1][0][1]
                certificatee = certificate['issuer'][2][0][1]
                notBefore = certificate['notBefore']
                notAfter = certificate['notAfter']

        return country, org, certificatee, notBefore, notAfter
    
    except Exception:
        return 'Error', 'Error', 'Error', 'Error', 'Error'

######################################################################################################################################################

def extract_if_https(url):
    """
    Checks if a URL uses HTTPS.

    Args:
        url (str): URL to check.

    Returns:
        int: 1 if HTTPS, 0 otherwise, or 'Error' in case of exceptions.
    """
    try:
        if url.startswith(('https', 'http')):
            response = 1
        else:
            response = 0

        return response
    
    except Exception:
        return 'Error'


######################################################################################################################################################

def extract_whois(domain):
    """
    Retrieves WHOIS information for a domain.

    Args:
        domain (str): Domain name to query.

    Returns:
        tuple: (whois_country, whois_creation_date, whois_expiration_date)
        or ('Error', ...) in case of exceptions.
    """
    try:
        whois_info = whois.whois(domain)
        whois_country = whois_info['country']
        whois_creation_date = whois_info['creation_date']
        whois_expiration_date = whois_info['expiration_date']
        return whois_country, whois_creation_date, whois_expiration_date
    
    except Exception:
        return 'Error', 'Error', 'Error'
    
######################################################################################################################################################
# Dataset Creation Functions
######################################################################################################################################################

def get_row(url, http_url):
    """
    Extracts all features for a given URL.

    Args:
        url (str): Original URL.
        http_url (str): URL with the HTTP scheme added if missing.

    Returns:
        dict: Row of extracted features.
    """
    page = requests.get(http_url, timeout=120)
    soup = BeautifulSoup(page.content, 'html.parser')
    parsed_url = urlparse(http_url)
    domain = parsed_url.netloc
    ip_address = extract_ip_address(domain)

    link_density = extract_link_density(soup)
    external_links_count, internal_links_count, external_ip_count, https_count, http_count, non_count = extract_link_features(soup, domain)
    external_iframes_count, hidden_iframes_count = extract_iframes(soup)
    country, org, certificate, notBefore, notAfter = extract_certificate(domain)
    if_https = extract_if_https(url)
    whois_country, whois_creation_date, whois_expiration_date = extract_whois(domain)

    row = {
        "URL": url,
        "Domain": domain,
        "IP Address": ip_address,
        "Link Density": link_density,
        "External Links Count": external_links_count,
        "Internal Links Count": internal_links_count,
        "External IP Count": external_ip_count,
        "HTTP Count": http_count,
        "HTTPS Count": https_count,
        "Non Count": non_count,
        "External Iframes Count": external_iframes_count,
        "Hidden Iframes Count": hidden_iframes_count,
        "Country": country,
        "Organization": org,
        "Certificate": certificate,
        "Certificate Not Before": notBefore,
        "Certificate Not After": notAfter,
        "If HTTPS": if_https,
        "Whois_country": whois_country,
        "whois_creation_date" : whois_creation_date,
        "whois_expiration_date" : whois_expiration_date
    }
    return row
    
def create_dataset(urls):
    """
    Creates a dataset by extracting features for a list of URLs.

    Args:
        urls (list): List of URLs to process.

    Returns:
        DataFrame: Dataset containing features for each URL.
    """
    df = pd.DataFrame()

    for url in urls:

        if not urlparse(url).scheme:
            http_url = f"http://{url}"
        
        try:
            row = get_row(url, http_url)  
            row_df = pd.DataFrame([row]) 
            df = pd.concat([df, row_df], ignore_index=True) 
            print("Successfully Added: ", url)
        except requests.exceptions.Timeout:
            print(f"Timeout: {url} took too long to respond.")
            continue 

        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch {url}: {e}")
            continue

    return df

######################################################################################################################################################
# Main Execution
######################################################################################################################################################

def main():
    """
    Main function to process malicious and benign URLs and save the dataset.
    """
    mal_urls = pd.read_csv("malicious_phish.csv", encoding='latin1')
    mal_urls = mal_urls.rename(columns={'url': 'URL'})

    df_phishing = mal_urls[mal_urls['type'] == 'phishing']
    df_benign = mal_urls[mal_urls['type'] == 'benign']

    phish_urls = df_phishing['URL'].head(2000).unique()
    benign_urls = df_benign['URL'].head(1000).unique()

    phishing_data = create_dataset(phish_urls)
    benign_data = create_dataset(benign_urls)

    phishing_data = pd.merge(phishing_data, df_phishing, on='URL', how='left')
    benign_data = pd.merge(benign_data, df_benign, on='URL', how='left')

    phishing_data = phishing_data.head(400)
    phishing_data = phishing_data.head(400)

    final_df = pd.concat([phishing_data, benign_data])
    final_df = final_df.sample(frac=1, random_state=0)

    final_df.to_csv('phishing_url_datasett.csv', index=False)
    print('Successfully created dataset and saved it in "phishing_url_dataset.csv"')

if __name__ == "__main__":
    main()