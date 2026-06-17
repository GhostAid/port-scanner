import socket

# Dictionary of common port names
PORT_NAMES = {
    20: "FTP-DATA",
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    465: "SMTPS",
    587: "SMTP",
    993: "IMAPS",
    995: "POP3S",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    8080: "HTTP-Alt"
}

target = input("Enter IP or domain: ")
print(f"\n Scanning {target} ...\n")

for port in range(1, 1025):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((target, port))
    
    if result == 0:
        name = PORT_NAMES.get(port, "Unknown")
        print(f" Port {port} is OPEN ({name})")
    
    sock.close()

print("\n Scan complete!")
