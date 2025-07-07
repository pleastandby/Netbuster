import subprocess

#created by pleastandby

network_range = "192.168.1.0/24"
common_web_ports = [80, 443, 8080, 8000, 8443]

def scan_network(subnet):
    print(f"[*] Scanning network: {subnet} ...")
    result = subprocess.check_output(["nmap", "-p", ",".join(map(str, common_web_ports)), "--open", subnet], encoding="utf-8")
    return result

def parse_hosts(nmap_output):
    hosts = []
    current_ip = None
    for line in nmap_output.splitlines():
        if "Nmap scan report for" in line:
            current_ip = line.split()[-1]
        elif any(f"{port}/tcp open" in line for port in map(str, common_web_ports)) and current_ip:
            port = int(line.split("/")[0])
            hosts.append((current_ip, port))
    return hosts

def run_dirb(ip, port):
    protocol = "https" if port in [443, 8443] else "http"
    url = f"{protocol}://{ip}:{port}/"
    print(f"[+] Running dirb on {url}")
    subprocess.call(["dirb", url])

if __name__ == "__main__":
    try:
        nmap_output = scan_network(network_range)
        targets = parse_hosts(nmap_output)
        if not targets:
            print("[-] No HTTP services found.")
        else:
            print(f"[+] Found {len(targets)} HTTP services.")
            for ip, port in targets:
                run_dirb(ip, port)
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
    except Exception as e:
        print(f"[!] Error: {e}")
