import time
import os
import platform
import sys
import urllib3
import argparse
import requests
import random
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# ANSI Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Clear screen based on the platform
def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

clear_screen()

# Banner
BANNER = f'''
{BLUE}{BOLD}█▀█ ▄▀█ █▄░█ █▀▀ █░░ █▀▀ █▀█ ▀▄▀  {YELLOW}Github: {RESET}ameeshaheshan
█▀▀ █▀█ █░▀█ ██▄ █▄▄ █▀░ █▄█ █░█  {YELLOW}Version: {RESET}2.0
{GREEN}════════════════════════════════
{YELLOW}{BOLD}The Hidden Admin Panel Finder 🦊
{GREEN}════════════════════════════════{RESET}
'''

def animated_banner(text, delay=0.008):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print("\n")

animated_banner(BANNER)

# Logging setup
logging.basicConfig(
    filename='admin_finder.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Hidden Admin Panel Finder Tool")
    parser.add_argument('-u', '--url', type=str, required=True, help="Target URL (e.g. http://example.com)")
    parser.add_argument('-w', '--word-list', type=str, required=True, help="Wordlist file containing admin paths")
    parser.add_argument('-t', '--threads', type=int, choices=range(1, 11), default=1, help="Number of threads (1-10)")
    parser.add_argument('-X', '--method', type=str, default='GET', choices=['GET', 'POST', 'HEAD', 'PUT', 'DELETE'], help="HTTP method to use")
    parser.add_argument('-H', '--header', action='append', help="Add custom headers (e.g. 'X-API-Key: 12345')")
    parser.add_argument('--cookie', type=str, help="Add cookies (e.g. 'session_id=abc123; token=xyz')")
    parser.add_argument('--delay', type=float, help="Add random delay between requests (seconds)")
    parser.add_argument('--show-headers', action='store_true', help="Display response headers for found pages")
    parser.add_argument('-l', '--log', action='store_true', help="Enable logging of requests")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose mode")
    parser.add_argument('-p', '--proxy', type=str, help="Proxy list file")
    parser.add_argument('-o', '--output', type=str, help="Save results to a file")
    parser.add_argument('-I', '--ignore-ssl', action='store_true', help="Ignore SSL certificate warnings")
    parser.add_argument('--user-agent', type=str, help="User-Agent list file")
    parser.add_argument('--save-responses', action='store_true', help="Save HTTP responses for analysis")
    parser.add_argument('--status-code-filter', type=int, help="Filter results by HTTP status code")
    
    '''
    # Custom help handling
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                        help="Show this help message and exit") '''
    
    # If no arguments provided
    if len(sys.argv) == 1:
        print(f"{RED}{BOLD}Error:{RESET}{GREEN}{BOLD} Required arguments missing!\n")
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()
    return args

def load_wordlist(wordlist_path):
    try:
        with open(wordlist_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(f"{RED}{BOLD}Error:{RESET} Unable to load wordlist: {e}")
        sys.exit(1)

def load_list_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(f"{RED}{BOLD}Error:{RESET} Unable to load file {filename}: {e}")
        return None

def parse_headers(headers):
    header_dict = {}
    if headers:
        for header in headers:
            if ':' not in header:
                print(f"{RED}Invalid header format: {header}{RESET}")
                continue
            key, value = header.split(':', 1)
            header_dict[key.strip()] = value.strip()
    return header_dict

def parse_cookies(cookie_string):
    cookies = {}
    if cookie_string:
        for cookie in cookie_string.split(';'):
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                cookies[key.strip()] = value.strip()
    return cookies

def get_status_color(status_code):
    if 200 <= status_code < 300:
        return GREEN
    elif 300 <= status_code < 400:
        return YELLOW
    elif 400 <= status_code < 500:
        return RED
    else:
        return RESET

def check_admin_panel(url, path, session, args, baseline_data):
    target = f"{url.rstrip('/')}/{path.lstrip('/')}"
    
    # Build request components
    headers = {'User-Agent': random.choice(args.user_agents) if args.user_agents else "Mozilla/5.0"}
    headers.update(args.custom_headers)
    proxies = {"http": random.choice(args.proxies), "https": random.choice(args.proxies)} if args.proxies else None
    
    # Add random delay
    if args.delay:
        time.sleep(args.delay * random.uniform(0.8, 1.2))
    
    try:
        response = session.request(
            method=args.method,
            url=target,
            headers=headers,
            proxies=proxies,
            verify=not args.ignore_ssl,
            timeout=10,
            allow_redirects=False
        )
        
        # Skip filtered status codes
        if args.status_code_filter and response.status_code != args.status_code_filter:
            return None
        
        # Detect false positives
        content_length = len(response.text)
        if (content_length == baseline_data['length'] and 
            response.text == baseline_data['content']):
            return None
        if any(keyword in response.text.lower() for keyword in ["404", "not found", "error"]):
            return None
        
        # Prepare result
        color = get_status_color(response.status_code)
        result = f"{color}[{response.status_code}]{RESET} Found: {target}"
        
        # Add redirect info for 30x codes
        if response.status_code in [301, 302]:
            location = response.headers.get('Location', 'Unknown')
            result += f"\n{YELLOW}└── Redirects to: {location}{RESET}"
        
        # Add content length info
        result += f"\n{CYAN}└── Content Length: {content_length}{RESET}"
        
        # Show headers if requested
        if args.show_headers or args.verbose:
            result += f"\n{BLUE}└── Headers:{RESET}"
            for key, value in response.headers.items():
                result += f"\n    {key}: {value}"
        
        return result
        
    except Exception as e:
        if args.verbose:
            return f"{RED}[Error]{RESET} {target}: {str(e)}"
        return None

def main():
    args = parse_arguments()
    
    # Load resources
    args.admin_paths = load_wordlist(args.word_list)
    args.proxies = load_list_from_file(args.proxy) if args.proxy else None
    args.user_agents = load_list_from_file(args.user_agent) if args.user_agent else None
    args.custom_headers = parse_headers(args.header)
    
    # Set up session
    session = requests.Session()
    if args.cookie:
        session.cookies.update(parse_cookies(args.cookie))
    
    # Get baseline 404 data
    baseline_url = f"{args.url}/this-path-should-not-exist-{random.randint(10000,99999)}"
    try:
        baseline_response = session.get(baseline_url, verify=not args.ignore_ssl)
        baseline_data = {
            'content': baseline_response.text,
            'length': len(baseline_response.text)
        }
    except Exception as e:
        baseline_data = {'content': '', 'length': 0}

    print(f"{BLUE}{BOLD}[*]{RESET} Scanning {args.url} with {len(args.admin_paths)} paths...\n")
    
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [
            executor.submit(
                check_admin_panel,
                args.url,
                path,
                session,
                args,
                baseline_data
            ) for path in args.admin_paths
        ]
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                print(f"\n{result}")
                if args.log:
                    logging.info(result.split('\n')[0])  # Log basic info
                if args.output:
                    with open(args.output, 'a', encoding='utf-8') as f:
                        f.write(result + "\n\n")

    print(f"\n{GREEN}{BOLD}[✔]{RESET} Scan completed!")

if __name__ == "__main__":
    main()