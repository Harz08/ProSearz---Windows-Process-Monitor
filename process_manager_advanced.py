"""
process_manager.py
Advanced Process Management & Control
Provides process termination, whitelisting, and detailed analysis
"""

import psutil
import hashlib
import os
from datetime import datetime


class ProcessManager:
    """Advanced process management and control"""
    
    def __init__(self):
        self.whitelist = self.load_whitelist()
        self.process_cache = {}
    
    def load_whitelist(self):
        """Load whitelisted processes from file"""
        whitelist_file = 'process_whitelist.txt'
        if os.path.exists(whitelist_file):
            with open(whitelist_file, 'r') as f:
                return set(line.strip().lower() for line in f if line.strip())
        return set()
    
    def save_whitelist(self):
        """Save whitelist to file"""
        with open('process_whitelist.txt', 'w') as f:
            for process in sorted(self.whitelist):
                f.write(f"{process}\n")
    
    def add_to_whitelist(self, process_name):
        """Add process to whitelist"""
        self.whitelist.add(process_name.lower())
        self.save_whitelist()
        return True
    
    def remove_from_whitelist(self, process_name):
        """Remove process from whitelist"""
        self.whitelist.discard(process_name.lower())
        self.save_whitelist()
        return True
    
    def is_whitelisted(self, process_name):
        """Check if process is whitelisted"""
        return process_name.lower() in self.whitelist
    
    def get_process_details(self, pid):
        """Get detailed information about a process"""
        try:
            proc = psutil.Process(pid)
            
            # Get CPU and memory usage
            cpu_percent = proc.cpu_percent(interval=0.1)
            memory_info = proc.memory_info()
            
            # Get threads and connections
            num_threads = proc.num_threads()
            
            try:
                connections = len(proc.connections())
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                connections = 0
            
            # Get file hash if executable exists
            exe_path = proc.exe()
            file_hash = self.calculate_file_hash(exe_path) if exe_path else None
            
            details = {
                'pid': pid,
                'name': proc.name(),
                'exe': exe_path,
                'status': proc.status(),
                'cpu_percent': round(cpu_percent, 2),
                'memory_mb': round(memory_info.rss / 1024 / 1024, 2),
                'num_threads': num_threads,
                'num_connections': connections,
                'file_hash_sha256': file_hash,
                'create_time': datetime.fromtimestamp(proc.create_time()).strftime('%Y-%m-%d %H:%M:%S'),
                'username': proc.username() if proc.username() else 'N/A',
                'cmdline': ' '.join(proc.cmdline()) if proc.cmdline() else 'N/A'
            }
            
            # Check if whitelisted
            details['is_whitelisted'] = self.is_whitelisted(proc.name())
            
            # Calculate risk score
            details['risk_score'] = self.calculate_risk_score(details)
            
            return details
            
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            return {'error': f'Cannot access process: {str(e)}'}
    
    def calculate_file_hash(self, file_path):
        """Calculate SHA-256 hash of file"""
        try:
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                # Read in chunks to handle large files
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception:
            return None
    
    def calculate_risk_score(self, details):
        """Calculate risk score (0-100) based on process characteristics"""
        score = 0
        
        # Base score starts at 20
        score = 20
        
        # High CPU usage (>50%) adds risk
        if details.get('cpu_percent', 0) > 50:
            score += 15
        
        # High memory usage (>500MB) adds risk
        if details.get('memory_mb', 0) > 500:
            score += 10
        
        # Many threads (>20) can indicate complex/suspicious behavior
        if details.get('num_threads', 0) > 20:
            score += 10
        
        # Network connections add risk
        if details.get('num_connections', 0) > 10:
            score += 15
        
        # Running from suspicious paths
        exe = details.get('exe', '').lower()
        suspicious_paths = ['temp', 'appdata\\local\\temp', 'downloads', 'public']
        if any(path in exe for path in suspicious_paths):
            score += 20
        
        # No hash available (protected/hidden)
        if not details.get('file_hash_sha256'):
            score += 10
        
        # Whitelisted processes reduce score
        if details.get('is_whitelisted'):
            score = max(0, score - 40)
        
        # Cap at 100
        return min(100, score)
    
    def terminate_process(self, pid, force=False):
        """Terminate a process by PID"""
        try:
            proc = psutil.Process(pid)
            process_name = proc.name()
            
            if force:
                proc.kill()  # Force kill
                method = "killed (forced)"
            else:
                proc.terminate()  # Graceful termination
                method = "terminated (graceful)"
            
            return {
                'success': True,
                'message': f'Process {process_name} (PID: {pid}) {method}',
                'process_name': process_name,
                'pid': pid
            }
            
        except psutil.NoSuchProcess:
            return {
                'success': False,
                'message': f'Process with PID {pid} not found',
                'error': 'NoSuchProcess'
            }
        except psutil.AccessDenied:
            return {
                'success': False,
                'message': f'Access denied. Try running as Administrator.',
                'error': 'AccessDenied'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error terminating process: {str(e)}',
                'error': str(e)
            }
    
    def suspend_process(self, pid):
        """Suspend a process"""
        try:
            proc = psutil.Process(pid)
            proc.suspend()
            return {
                'success': True,
                'message': f'Process {proc.name()} (PID: {pid}) suspended'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error suspending process: {str(e)}'
            }
    
    def resume_process(self, pid):
        """Resume a suspended process"""
        try:
            proc = psutil.Process(pid)
            proc.resume()
            return {
                'success': True,
                'message': f'Process {proc.name()} (PID: {pid}) resumed'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error resuming process: {str(e)}'
            }
    
    def get_process_network_info(self, pid):
        """Get network connections for a process"""
        try:
            proc = psutil.Process(pid)
            connections = proc.connections()
            
            conn_list = []
            for conn in connections:
                conn_list.append({
                    'local_address': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else 'N/A',
                    'remote_address': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else 'N/A',
                    'status': conn.status,
                    'type': 'TCP' if conn.type == 1 else 'UDP'
                })
            
            return {
                'success': True,
                'connections': conn_list,
                'total': len(conn_list)
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error getting network info: {str(e)}',
                'connections': []
            }
    
    def check_virustotal(self, file_hash):
        """
        Check file hash against VirusTotal
        NOTE: Requires VirusTotal API key (not included for security)
        This is a placeholder - users can add their own API key
        """
        # Placeholder for VirusTotal integration
        return {
            'scanned': False,
            'message': 'VirusTotal integration requires API key. Add your key in settings.',
            'virustotal_url': f'https://www.virustotal.com/gui/file/{file_hash}'
        }


# Test function
if __name__ == "__main__":
    print("Testing Process Manager...")
    
    pm = ProcessManager()
    
    # Get all processes
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            pid = proc.info['pid']
            name = proc.info['name']
            
            # Test on first Chrome process found
            if 'chrome' in name.lower():
                print(f"\nTesting with {name} (PID: {pid})")
                details = pm.get_process_details(pid)
                
                print(f"CPU: {details.get('cpu_percent')}%")
                print(f"Memory: {details.get('memory_mb')} MB")
                print(f"Risk Score: {details.get('risk_score')}/100")
                print(f"Whitelisted: {details.get('is_whitelisted')}")
                break
        except:
            continue
    
    print("\n✅ Process Manager Test Complete")
