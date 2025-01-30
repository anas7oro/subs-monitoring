# main.py

import argparse
from db import init_db
from targets import add_target, remove_target, list_targets
from scanner import run_tools
from storage import (
    save_subdomains, 
    get_subdomains, 
    search_subdomains, 
    add_subdomain, 
    remove_subdomain, 
    remove_subdomains_by_keyword
)
from scheduler import start_scheduler
import os

def add_domains_from_file(filepath):
    """
    Reads domains from a text file (one per line) and adds each to monitoring list.
    """
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r') as f:
        lines = f.readlines()

    for line in lines:
        domain = line.strip()
        if domain:
            add_target(domain)

def main():
    # Initialize the database (creates tables if they don't exist)
    init_db()

    parser = argparse.ArgumentParser(description="Subdomain Enumeration and Monitoring Tool (PostgreSQL Version)")

    # Existing CLI options
    parser.add_argument('-a', '--add', help='Add domain to monitoring list')
    parser.add_argument('-r', '--remove', help='Remove domain from monitoring list')
    parser.add_argument('-l', '--list', action='store_true', help='List monitored domains')
    parser.add_argument('-s', '--scan', help='Scan a domain or list of domains (comma-separated) one-time')
    parser.add_argument('-g', '--get', help='Get stored subdomains for a domain')
    parser.add_argument('-m', '--monitor', action='store_true', help='Start the monitoring scheduler')
    parser.add_argument('--save', action='store_true', help='Save subdomains to database during one-time scan')
    parser.add_argument('-f', '--find', help='Find subdomains containing a specific keyword')

    # New CLI options
    parser.add_argument('--remove-subdomain', help='Remove a specific subdomain from the database (format: domain:subdomain)')
    parser.add_argument('--add-subdomain', help='Add a specific subdomain to the database (format: domain:subdomain)')
    parser.add_argument('--remove-kw', help='Remove all subdomains containing the given keyword')
    parser.add_argument('--add-file', help='Add new domains from a text file (one domain per line)')

    args = parser.parse_args()

    # 1) Add a domain to the monitoring list
    if args.add:
        add_target(args.add)

    # 2) Remove a domain from the monitoring list
    elif args.remove:
        remove_target(args.remove)

    # 3) List monitored domains
    elif args.list:
        domains = list_targets()
        print("Monitored Domains:")
        for domain in domains:
            print(domain)

    # 4) Perform a one-time scan
    elif args.scan:
        domains = args.scan.split(',')
        for domain in domains:
            domain = domain.strip()
            subdomains = run_tools(domain)
            print(f"\nSubdomains for {domain}:")
            for subdomain in subdomains:
                print(subdomain)
            if args.save:
                new_subdomains = save_subdomains(domain, subdomains)
                print(f"\nSaved {len(new_subdomains)} new subdomains for {domain}.")

    # 5) Get stored subdomains for a domain
    elif args.get:
        subdomains = get_subdomains(args.get)
        print(f"\nStored Subdomains for {args.get}:")
        for subdomain in subdomains:
            print(subdomain)

    # 6) Find subdomains containing a specific keyword
    elif args.find:
        matching_subdomains = search_subdomains(args.find)
        print(f"\nSubdomains containing '{args.find}':")
        for subdomain in matching_subdomains:
            print(subdomain)

    # 7) Remove a specific subdomain
    elif args.remove_subdomain:
        # Expect format "domain:subdomain"
        if ':' not in args.remove_subdomain:
            print("Error: Please use the format --remove-subdomain domain:subdomain")
        else:
            domain, sub = args.remove_subdomain.split(':', 1)
            domain, sub = domain.strip(), sub.strip()
            deleted = remove_subdomain(domain, sub)
            if deleted:
                print(f"Successfully removed subdomain '{sub}' under '{domain}'.")
            else:
                print(f"No matching subdomain '{sub}' under '{domain}' found.")

    # 8) Add a specific subdomain
    elif args.add_subdomain:
        # Expect format "domain:subdomain"
        if ':' not in args.add_subdomain:
            print("Error: Please use the format --add-subdomain domain:subdomain")
        else:
            domain, sub = args.add_subdomain.split(':', 1)
            domain, sub = domain.strip(), sub.strip()
            inserted = add_subdomain(domain, sub)
            if inserted:
                print(f"Subdomain '{sub}' added under '{domain}'.")
            else:
                print(f"Subdomain '{sub}' under '{domain}' already exists or error occurred.")

    # 9) Remove subdomains containing a keyword
    elif args.remove_kw:
        count = remove_subdomains_by_keyword(args.remove_kw)
        print(f"Removed {count} subdomain(s) containing '{args.remove_kw}'.")

    # 10) Add new domains from a text file
    elif args.add_file:
        add_domains_from_file(args.add_file)

    # 11) Start the monitoring scheduler
    elif args.monitor:
        start_scheduler()

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
