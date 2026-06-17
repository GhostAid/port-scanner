import socket
import threading
from datetime import datetime
import time

# Port names dictionary
PORT_NAMES = {
    20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "TELNET",
    25: "SMTP", 53: "DNS", 80: "HTTP", 110: "POP3",
    143: "IMAP", 443: "HTTPS", 465: "SMTPS", 587: "SMTP",
    993: "IMAPS", 995: "POP3S", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 5900: "VNC", 8080: "HTTP-Alt"
}

# List to store results
all_results = []

def scan_port(target, port):
    """Scan a single port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target, port))
        
        if result == 0:
            name = PORT_NAMES.get(port, "Unknown")
            output = f"Port {port} is OPEN ({name})"
            all_results.append(output)
            print(f"✅ {output}")
        
        sock.close()
    except:
        pass

def scan_target(target, start_port=1, end_port=1024):
    """Scan a single target with threading"""
    print(f"\n{'='*50}")
    print(f"🔍 Scanning: {target}")
    print(f"📊 Port range: {start_port}-{end_port}")
    print(f"⏰ Started: {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*50}\n")
    
    # Create threads
    threads = []
    semaphore = threading.Semaphore(100)  # Limit to 100 threads at once
    
    def scan_with_limit(port):
        with semaphore:
            scan_port(target, port)
    
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_with_limit, args=(port,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads
    for thread in threads:
        thread.join()
    
    return all_results

def scan_ip_range(ip_range):
    """Scan multiple IPs in a range"""
    # Parse IP range (e.g., 192.168.1.1-10 or 192.168.1.1/24 or just single IP)
    if '-' in ip_range:
        base = ip_range.split('-')[0].rsplit('.', 1)[0] + '.'
        start = int(ip_range.split('-')[0].split('.')[-1])
        end = int(ip_range.split('-')[1])
        return [f"{base}{i}" for i in range(start, end + 1)]
    elif '/' in ip_range:
        # Simple CIDR (only /24 supported for simplicity)
        base = ip_range.rsplit('.', 1)[0] + '.'
        return [f"{base}{i}" for i in range(1, 255)]
    else:
        return [ip_range]

def save_results(target, results):
    """Save results to a file"""
    filename = f"scan_{target.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(filename, 'w') as f:
        f.write("="*50 + "\n")
        f.write(f"PORT SCAN RESULTS\n")
        f.write(f"Target: {target}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*50 + "\n\n")
        
        if results:
            for result in results:
                f.write(result + "\n")
            f.write(f"\nTotal open ports: {len(results)}\n")
        else:
            f.write("No open ports found.\n")
        
        f.write("\n" + "="*50 + "\n")
    
    return filename

def main():
    """Main program"""
    print("\n" + "="*50)
    print("🔥 ULTIMATE PORT SCANNER 🔥")
    print("="*50 + "\n")
    
    # Get target
    target_input = input("Enter IP, domain, or range (e.g., 192.168.1.1-10): ")
    
    # Parse IPs
    targets = scan_ip_range(target_input)
    
    # Get port range
    port_start = input("Enter start port (default 1): ") or "1"
    port_end = input("Enter end port (default 1024): ") or "1024"
    
    try:
        port_start = int(port_start)
        port_end = int(port_end)
    except:
        print("Invalid port range. Using default 1-1024")
        port_start, port_end = 1, 1024
    
    # Scan all targets
    all_results_combined = []
    
    for target in targets:
        results = scan_target(target, port_start, port_end)
        all_results_combined.extend(results)
        
        if len(targets) > 1:
            print(f"\n✅ {target} scan complete!")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"🎯 SCAN COMPLETE!")
    print(f"📊 Total open ports found: {len(all_results_combined)}")
    print(f"{'='*50}")
    
    if all_results_combined:
        # Save results
        filename = save_results(target_input, all_results_combined)
        print(f"\n💾 Results saved to: {filename}")
    
    print("\n✅ Done!")

if __name__ == "__main__":
    main()
