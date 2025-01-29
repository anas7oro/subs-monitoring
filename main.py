# main.py

import argparse
from db import init_db
from targets import add_target, remove_target, list_targets
from scanner import run_tools
from storage import save_subdomains, get_subdomains, search_subdomains
from scheduler import start_scheduler

def main():
    # Initialize the database (creates tables if they don't exist)
    init_db()

    parser = argparse.ArgumentParser(description="Subdomain Enumeration and Monitoring Tool (PostgreSQL Version)")
    parser.add_argument('-a', '--add', help='Add domain to monitoring list')
    parser.add_argument('-r', '--remove', help='Remove domain from monitoring list')
    parser.add_argument('-l', '--list', action='store_true', help='List monitored domains')
    parser.add_argument('-s', '--scan', help='Scan a domain or list of domains (comma-separated) one-time')
    parser.add_argument('-g', '--get', help='Get stored subdomains for a domain')
    parser.add_argument('-m', '--monitor', action='store_true', help='Start the monitoring scheduler')
    parser.add_argument('--save', action='store_true', help='Save subdomains to database during one-time scan')
    parser.add_argument('-f', '--find', help='Find subdomains containing a specific keyword')

    args = parser.parse_args()

    if args.add:
        add_target(args.add)
    elif args.remove:
        remove_target(args.remove)
    elif args.list:
        domains = list_targets()
        print("Monitored Domains:")
        for domain in domains:
            print(domain)
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
    elif args.get:
        subdomains = get_subdomains(args.get)
        print(f"\nStored Subdomains for {args.get}:")
        for subdomain in subdomains:
            print(subdomain)
    elif args.find:
        matching_subdomains = search_subdomains(args.find)
        print(f"\nSubdomains containing '{args.find}':")
        for subdomain in matching_subdomains:
            print(subdomain)
    elif args.monitor:
        start_scheduler()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
