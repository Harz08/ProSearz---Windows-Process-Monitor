"""
service_mon.py
Service Monitoring Module - Enumerates and analyzes Windows services
"""

import win32service
import win32serviceutil
from datetime import datetime


def enumerate_services():
    """
    Enumerate all Windows services on the system
    Returns: List of dictionaries containing service information
    """
    services = []

    print("[*] Scanning Windows services...")

    try:
        # Open Service Control Manager
        accessSCM = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ENUMERATE_SERVICE)

        # Define service types and states to enumerate
        typeFilter = win32service.SERVICE_WIN32
        stateFilter = win32service.SERVICE_STATE_ALL

        # Get all services
        service_list = win32service.EnumServicesStatus(accessSCM, typeFilter, stateFilter)

        for service in service_list:
            service_name = service[0]
            display_name = service[1]
            service_status = service[2]

            # Get service state
            state = service_status[1]
            state_str = get_service_state_string(state)

            # Try to get service configuration (path, startup type)
            service_config = None
            service_path = "N/A"
            startup_type = "N/A"

            try:
                service_handle = win32service.OpenService(
                    accessSCM,
                    service_name,
                    win32service.SERVICE_QUERY_CONFIG
                )
                service_config = win32service.QueryServiceConfig(service_handle)
                service_path = service_config[3]  # Binary path
                startup_type = get_startup_type_string(service_config[1])
                win32service.CloseServiceHandle(service_handle)
            except Exception:
                # Some services might not allow config query
                pass

            service_info = {
                'name': service_name,
                'display_name': display_name,
                'state': state_str,
                'path': service_path,
                'startup_type': startup_type,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            services.append(service_info)

        # Close Service Control Manager
        win32service.CloseServiceHandle(accessSCM)

        print(f"[+] Found {len(services)} services")

    except Exception as e:
        print(f"[!] Error enumerating services: {e}")
        return []

    return services


def get_service_state_string(state):
    """
    Convert service state code to readable string
    """
    states = {
        win32service.SERVICE_STOPPED: 'STOPPED',
        win32service.SERVICE_START_PENDING: 'START_PENDING',
        win32service.SERVICE_STOP_PENDING: 'STOP_PENDING',
        win32service.SERVICE_RUNNING: 'RUNNING',
        win32service.SERVICE_CONTINUE_PENDING: 'CONTINUE_PENDING',
        win32service.SERVICE_PAUSE_PENDING: 'PAUSE_PENDING',
        win32service.SERVICE_PAUSED: 'PAUSED'
    }
    return states.get(state, 'UNKNOWN')


def get_startup_type_string(startup_type):
    """
    Convert startup type code to readable string
    """
    types = {
        win32service.SERVICE_AUTO_START: 'AUTO',
        win32service.SERVICE_BOOT_START: 'BOOT',
        win32service.SERVICE_DEMAND_START: 'MANUAL',
        win32service.SERVICE_DISABLED: 'DISABLED',
        win32service.SERVICE_SYSTEM_START: 'SYSTEM'
    }
    return types.get(startup_type, 'UNKNOWN')


def get_running_services(services):
    """
    Filter to get only running services
    Returns: List of running services
    """
    return [svc for svc in services if svc['state'] == 'RUNNING']


def get_auto_start_services(services):
    """
    Filter to get services that auto-start
    Returns: List of auto-start services
    """
    return [svc for svc in services if svc['startup_type'] == 'AUTO']


def find_service_by_name(services, name):
    """
    Find services matching a specific name (partial match)
    Returns: List of matching services
    """
    name_lower = name.lower()
    return [svc for svc in services if name_lower in svc['name'].lower() or
            name_lower in svc['display_name'].lower()]


def display_service_info(service):
    """
    Pretty print service information
    """
    print("\n" + "=" * 60)
    print(f"Service Name: {service['name']}")
    print(f"Display Name: {service['display_name']}")
    print(f"State: {service['state']}")
    print(f"Startup Type: {service['startup_type']}")
    print(f"Path: {service['path']}")
    print("=" * 60)


# Test function - Only runs when file is executed directly
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🔧 SERVICE MONITOR - TEST MODE")
    print("=" * 60 + "\n")

    # Get all services
    all_services = enumerate_services()

    if all_services:
        # Get running services
        running = get_running_services(all_services)
        auto_start = get_auto_start_services(all_services)

        # Display statistics
        print("\n📊 STATISTICS:")
        print(f"   Total Services: {len(all_services)}")
        print(f"   Running Services: {len(running)}")
        print(f"   Auto-Start Services: {len(auto_start)}")

        # Show sample service (first running service)
        if running:
            print("\n📋 SAMPLE RUNNING SERVICE:")
            display_service_info(running[0])

        # Find Windows Defender (example)
        defender = find_service_by_name(all_services, 'Defender')
        if defender:
            print(f"\n🛡️ Found {len(defender)} Windows Defender related services")

        print("\n✅ Test Complete!\n")
    else:
        print("\n❌ Failed to enumerate services. Try running as Administrator.\n")


'''

## 🧪 **STEP 2: Test It!**

### **Run the file:**

1. ** Right - click
on
`service_mon.py` ** in PyCharm
2.
Click ** "Run 'service_mon'" **

### **Expected Output:**
```
== == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
🔧 SERVICE
MONITOR - TEST
MODE
== == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==

[*]
Scanning
Windows
services...
[+]
Found
350
services

📊 STATISTICS:
Total
Services: 350
Running
Services: 120
Auto - Start
Services: 85

📋 SAMPLE
RUNNING
SERVICE:

== == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
Service
Name: eventlog
Display
Name: Windows
Event
Log
State: RUNNING
Startup
Type: AUTO
Path: C:\Windows\System32\svchost.exe - k
LocalServiceNetworkRestricted
== == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==

🛡️
Found
3
Windows
Defender
related
services

✅ Test
Complete!
```

---

## ⚠️ **IMPORTANT NOTE**

If
you
get ** "Access Denied" ** or ** fewer
services
than
expected **:

### **Run PyCharm as Administrator:**

1. ** Close
PyCharm
completely **
2. ** Right - click
PyCharm
icon ** on
desktop / start
menu
3. ** Select
"Run as administrator" **
4. ** Open
your
project
again **
5. ** Run
`service_mon.py`
again **

This is normal - Windows
services
require
elevated
privileges
to
query!

---

## ✅ **Verification Checklist**

- []
File
created: `service_mon.py`
- []
Code
runs
without
errors
- []
You
see
200 + services(typical
Windows)
- []
You
see
running
services
count
- []
Sample
service
displayed
with path

---

## 🎉 **Progress Update**
```
[████████░░░░░░░░░░░░] 40 % Complete

✅ core_mon.py(Process
Monitor)
✅ service_mon.py(Service
Auditor)
⬜ detecr_rules.py(Detection
Engine)
⬜ alert_sys.py(Alert
System)
⬜ report_gen.py(Report
Generator)
⬜ main.py(Main
Orchestrator)
'''