"""
detecr_rules.py
Detection Rules Engine - Defines suspicious behavior patterns
"""

from datetime import datetime

# ============================================================================
# DETECTION RULES CONFIGURATION
# ============================================================================

# Rule 1: Suspicious Parent-Child Process Relationships
# Office apps, browsers shouldn't spawn shells/scripts
SUSPICIOUS_PARENT_CHILD = {
    'winword.exe': ['powershell.exe', 'cmd.exe', 'wscript.exe', 'cscript.exe', 'mshta.exe', 'regsvr32.exe'],
    'excel.exe': ['powershell.exe', 'cmd.exe', 'wscript.exe', 'cscript.exe', 'mshta.exe', 'regsvr32.exe'],
    'outlook.exe': ['powershell.exe', 'cmd.exe', 'wscript.exe', 'cscript.exe', 'mshta.exe'],
    'acrord32.exe': ['powershell.exe', 'cmd.exe', 'wscript.exe'],  # Adobe Reader
    'chrome.exe': ['powershell.exe', 'wscript.exe', 'mshta.exe'],
    'firefox.exe': ['powershell.exe', 'wscript.exe', 'mshta.exe'],
    'iexplore.exe': ['powershell.exe', 'cmd.exe', 'wscript.exe'],
    'msedge.exe': ['powershell.exe', 'wscript.exe', 'mshta.exe'],
}

# Rule 2: Suspicious File Paths
# Processes shouldn't run from these locations
SUSPICIOUS_PATHS = [
    '\\Temp\\',
    '\\AppData\\Local\\Temp\\',
    '\\Users\\Public\\',
    'C:\\Windows\\Temp\\',
    '\\Downloads\\',
    'C:\\ProgramData\\',
    '\\AppData\\Roaming\\',
]

# Rule 3: High-Risk Process Names
# Known malware process names or suspicious patterns
SUSPICIOUS_PROCESS_NAMES = [
    'nc.exe',  # Netcat
    'ncat.exe',  # Ncat
    'mimikatz.exe',  # Credential dumper
    'psexec.exe',  # Remote execution
    'procdump.exe',  # Memory dumper
    'pwdump.exe',  # Password dumper
    'htran.exe',  # Proxy tool
    'plink.exe',  # SSH tunneling
]

# Rule 4: Legitimate System Processes
# These are safe and expected
LEGITIMATE_PROCESSES = [
    'System', 'smss.exe', 'csrss.exe', 'wininit.exe', 'services.exe',
    'lsass.exe', 'svchost.exe', 'explorer.exe', 'dwm.exe', 'winlogon.exe',
    'taskhost.exe', 'taskhostw.exe', 'RuntimeBroker.exe', 'dllhost.exe',
    'conhost.exe', 'fontdrvhost.exe', 'sihost.exe', 'ctfmon.exe',
]

# Rule 5: Suspicious Service Paths
# Services shouldn't be in these locations
SUSPICIOUS_SERVICE_PATHS = [
    '\\Temp\\',
    '\\AppData\\',
    '\\Users\\Public\\',
    '\\Downloads\\',
    'C:\\ProgramData\\',
]

# Rule 6: Known legitimate service paths
LEGITIMATE_SERVICE_PATHS = [
    'C:\\Windows\\System32\\',
    'C:\\Windows\\SysWOW64\\',
    'C:\\Program Files\\',
    'C:\\Program Files (x86)\\',
]


# ============================================================================
# DETECTION FUNCTIONS
# ============================================================================

def detect_suspicious_parent_child(process_tree, pid_to_process):
    """
    Detect anomalous parent-child process relationships
    Returns: List of alerts
    """
    alerts = []

    print("[*] Checking for suspicious parent-child relationships...")

    for parent_pid, children in process_tree.items():
        # Get parent process info
        parent_proc = pid_to_process.get(parent_pid)

        if not parent_proc:
            continue

        parent_name = parent_proc['name'].lower()

        # Check if parent is in our suspicious parent list
        if parent_name in SUSPICIOUS_PARENT_CHILD:
            suspicious_children = SUSPICIOUS_PARENT_CHILD[parent_name]

            for child in children:
                child_name = child['name'].lower()

                # Check if child matches suspicious pattern
                if child_name in suspicious_children:
                    alert = {
                        'severity': 'HIGH',
                        'type': 'Suspicious Parent-Child Relationship',
                        'parent_name': parent_proc['name'],
                        'parent_pid': parent_pid,
                        'child_name': child['name'],
                        'child_pid': child['pid'],
                        'child_path': child['path'],
                        'description': f"{parent_proc['name']} spawned {child['name']} - Potential malware execution",
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    alerts.append(alert)

    print(f"[+] Found {len(alerts)} suspicious parent-child relationships")
    return alerts


def detect_suspicious_paths(processes):
    """
    Detect processes running from suspicious/risky locations
    Returns: List of alerts
    """
    alerts = []

    print("[*] Checking for processes in suspicious paths...")

    for proc in processes:
        if not proc['path']:
            continue

        proc_path = proc['path'].lower()

        # Skip legitimate system processes
        if proc['name'] in LEGITIMATE_PROCESSES:
            continue

        # Check against suspicious paths
        for sus_path in SUSPICIOUS_PATHS:
            if sus_path.lower() in proc_path:
                alert = {
                    'severity': 'MEDIUM',
                    'type': 'Suspicious Process Path',
                    'process_name': proc['name'],
                    'pid': proc['pid'],
                    'path': proc['path'],
                    'description': f"Process running from risky location: {sus_path}",
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                alerts.append(alert)
                break  # Only alert once per process

    print(f"[+] Found {len(alerts)} processes in suspicious paths")
    return alerts


def detect_suspicious_process_names(processes):
    """
    Detect known malicious or high-risk process names
    Returns: List of alerts
    """
    alerts = []

    print("[*] Checking for suspicious process names...")

    for proc in processes:
        proc_name = proc['name'].lower()

        if proc_name in SUSPICIOUS_PROCESS_NAMES:
            alert = {
                'severity': 'CRITICAL',
                'type': 'High-Risk Process Detected',
                'process_name': proc['name'],
                'pid': proc['pid'],
                'path': proc['path'],
                'description': f"Known high-risk tool detected: {proc['name']}",
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            alerts.append(alert)

    print(f"[+] Found {len(alerts)} high-risk processes")
    return alerts


def detect_suspicious_services(services):
    """
    Detect services with suspicious configurations or paths
    Returns: List of alerts
    """
    alerts = []

    print("[*] Checking for suspicious service configurations...")

    for svc in services:
        if svc['path'] == 'N/A':
            continue

        svc_path = svc['path'].lower()
        is_suspicious = False
        sus_reason = ""

        # Check for suspicious service paths
        for sus_path in SUSPICIOUS_SERVICE_PATHS:
            if sus_path.lower() in svc_path:
                is_suspicious = True
                sus_reason = f"Service running from suspicious location: {sus_path}"
                break

        # Check if service is NOT in legitimate paths
        is_legitimate = any(leg_path.lower() in svc_path for leg_path in LEGITIMATE_SERVICE_PATHS)

        if is_suspicious or not is_legitimate:
            # Additional check: skip if it's from Program Files
            if 'program files' not in svc_path:
                alert = {
                    'severity': 'MEDIUM',
                    'type': 'Suspicious Service Configuration',
                    'service_name': svc['name'],
                    'display_name': svc['display_name'],
                    'path': svc['path'],
                    'state': svc['state'],
                    'startup_type': svc['startup_type'],
                    'description': sus_reason if sus_reason else "Service in unusual location",
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                alerts.append(alert)

    print(f"[+] Found {len(alerts)} suspicious services")
    return alerts


def run_all_detections(processes, process_tree, pid_to_process, services):
    """
    Run all detection rules and combine results
    Returns: Dictionary of all alerts categorized by type
    """
    print("\n" + "=" * 60)
    print("🔍 RUNNING ALL DETECTION RULES")
    print("=" * 60 + "\n")

    all_alerts = {
        'parent_child': detect_suspicious_parent_child(process_tree, pid_to_process),
        'suspicious_paths': detect_suspicious_paths(processes),
        'suspicious_names': detect_suspicious_process_names(processes),
        'suspicious_services': detect_suspicious_services(services)
    }

    total_alerts = sum(len(alerts) for alerts in all_alerts.values())

    print("\n" + "=" * 60)
    print(f"✅ DETECTION COMPLETE - {total_alerts} total alerts")
    print("=" * 60)

    return all_alerts


# Test function - Only runs when file is executed directly
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🧠 DETECTION RULES ENGINE - TEST MODE")
    print("=" * 60 + "\n")

    # Test data - simulating detections
    test_process = {
        'name': 'malware.exe',
        'pid': 9999,
        'path': 'C:\\Users\\Public\\malware.exe'
    }

    print("📋 LOADED DETECTION RULES:")
    print(f"   Suspicious Parent-Child Patterns: {len(SUSPICIOUS_PARENT_CHILD)}")
    print(f"   Suspicious Paths: {len(SUSPICIOUS_PATHS)}")
    print(f"   High-Risk Process Names: {len(SUSPICIOUS_PROCESS_NAMES)}")
    print(f"   Legitimate Processes Whitelist: {len(LEGITIMATE_PROCESSES)}")
    print(f"   Suspicious Service Paths: {len(SUSPICIOUS_SERVICE_PATHS)}")

    print("\n🎯 EXAMPLE DETECTION PATTERNS:")
    print("\n   Office Apps Shouldn't Spawn:")
    for parent, children in list(SUSPICIOUS_PARENT_CHILD.items())[:3]:
        print(f"      {parent} → {', '.join(children[:3])}")

    print("\n   Suspicious Locations:")
    for path in SUSPICIOUS_PATHS[:5]:
        print(f"      {path}")

    print("\n✅ Detection Engine Ready!\n")
# ```
#
# ---
#
# ## 🧪 **STEP 3: Test It!**
#
# ### **Run the file:**
#
# 1. ** Right - click
# on
# `detecr_rules.py` ** in PyCharm
# 2.
# Click ** "Run 'detecr_rules'" **
#
# ### **Expected Output:**
# ```
# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
# 🧠 DETECTION
# RULES
# ENGINE - TEST
# MODE
# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
#
# 📋 LOADED
# DETECTION
# RULES:
# Suspicious
# Parent - Child
# Patterns: 8
# Suspicious
# Paths: 7
# High - Risk
# Process
# Names: 8
# Legitimate
# Processes
# Whitelist: 18
# Suspicious
# Service
# Paths: 5
#
# 🎯 EXAMPLE
# DETECTION
# PATTERNS:
#
# Office
# Apps
# Shouldn
# 't Spawn:
# winword.exe → powershell.exe, cmd.exe, wscript.exe
# excel.exe → powershell.exe, cmd.exe, wscript.exe
# outlook.exe → powershell.exe, cmd.exe, wscript.exe
#
# Suspicious
# Locations:
# \Temp \
#     \AppData\Local\Temp \
#     \Users\Public \
#     C:\Windows\Temp \
#     \Downloads \
#  \
#     ✅ Detection
# Engine
# Ready!
# ```
#
# ---
#
# ## ✅ **Verification Checklist**
#
# - []
# File
# created: `detecr_rules.py`
# - []
# Code
# runs
# without
# errors
# - []
# Shows
# 8
# parent - child
# patterns
# - []
# Shows
# 7
# suspicious
# paths
# - []
# Shows
# detection
# rules
# loaded
#
# ---
#
# ## 🎉 **Progress Update**
# ```
# [████████████░░░░░░░░] 60 % Complete
#
# ✅ core_mon.py(Process
# Monitor)
# ✅ service_mon.py(Service
# Auditor)
# ✅ detecr_rules.py(Detection
# Engine) ← YOU
# ARE
# HERE
# ⬜ alert_sys.py(Alert
# System)
# ⬜ report_gen.py(Report
# Generator)
# ⬜ main.py(Main
# Orchestrator)