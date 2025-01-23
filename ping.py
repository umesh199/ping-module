import ipaddress
import subprocess
import argparse

def ping_ip(ip):
    """
    Pings an IP address to check its availability.
    Returns True if the IP responds, False otherwise.
    """
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1", str(ip)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error pinging {ip}: {e}")
        return False

def scan_vlan(vlan_range, output_file):
    """
    Scans the given VLAN range for responsive IPs.
    Writes responsive IPs to an output file.
    """
    responsive_ips = []
    try:
        network = ipaddress.ip_network(vlan_range, strict=False)
        print(f"Scanning VLAN range: {vlan_range}")
        
        with open(output_file, "w") as file:
            file.write(f"Responsive IPs in VLAN range {vlan_range}:\n")
            
            for ip in network.hosts():
                if ping_ip(ip):
                    print(f"{ip} is responsive")
                    responsive_ips.append(str(ip))
                    file.write(f"{ip}\n")
                else:
                    print(f"{ip} is not responsive")

    except ValueError as e:
        print(f"Invalid VLAN range: {e}")
    
    return responsive_ips

def main():
    parser = argparse.ArgumentParser(description="Scan a VLAN range for responsive IPs.")
    parser.add_argument(
        "vlan_range",
        type=str,
        help="The VLAN range in CIDR notation (e.g., 192.168.1.0/24)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="responsive_ips.txt",
        help="File to save the list of responsive IPs (default: responsive_ips.txt)"
    )
    args = parser.parse_args()

    vlan_range = args.vlan_range
    output_file = args.output
    responsive_ips = scan_vlan(vlan_range, output_file)

    print("\nScan complete. Responsive IPs saved to:", output_file)

if __name__ == "__main__":
    main()
