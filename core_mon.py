"""
core_monitor.py
Process Monitoring Module - Enumerates and analyzes Windows processes
"""

import psutil
from datetime import datetime


def get_all_processes():
    """
    Enumerate all running processes on the system
    Returns: List of dictionaries containing process information
    """
    processes = []

    print("[*] Scanning running processes...")

    for proc in psutil.process_iter(['pid', 'name', 'ppid', 'exe', 'username', 'create_time']):
        try:
            proc_info = {
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'ppid': proc.info['ppid'],  # Parent Process ID
                'path': proc.info['exe'],
                'user': proc.info['username'],
                'create_time': datetime.fromtimestamp(proc.info['create_time']).strftime('%Y-%m-%d %H:%M:%S'),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            processes.append(proc_info)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Some system processes can't be accessed - skip them
            continue

    print(f"[+] Found {len(processes)} processes")
    return processes


def build_process_tree(processes):
    """
    Build parent-child relationship tree from process list
    Returns: Dictionary mapping parent PID to list of child processes
    """
    print("[*] Building process tree...")

    # Create a mapping of PID to process info for quick lookup
    pid_to_process = {proc['pid']: proc for proc in processes}

    # Build the tree structure
    process_tree = {}

    for proc in processes:
        parent_pid = proc['ppid']

        # Initialize parent entry if not exists
        if parent_pid not in process_tree:
            process_tree[parent_pid] = []

        # Add this process as a child of its parent
        process_tree[parent_pid].append(proc)

    print(f"[+] Process tree built with {len(process_tree)} parent processes")
    return process_tree, pid_to_process


def get_process_by_name(processes, name):
    """
    Find all processes matching a specific name
    Returns: List of matching processes
    """
    return [proc for proc in processes if proc['name'].lower() == name.lower()]


def get_children_of_process(process_tree, parent_pid):
    """
    Get all direct children of a specific process
    Returns: List of child processes
    """
    return process_tree.get(parent_pid, [])


def display_process_info(process):
    """
    Pretty print process information
    """
    print("\n" + "=" * 60)
    print(f"Process Name: {process['name']}")
    print(f"PID: {process['pid']}")
    print(f"Parent PID: {process['ppid']}")
    print(f"Path: {process['path']}")
    print(f"User: {process['user']}")
    print(f"Created: {process['create_time']}")
    print("=" * 60)


# Test function - Only runs when file is executed directly
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🔍 PROCESS MONITOR - TEST MODE")
    print("=" * 60 + "\n")

    # Get all processes
    all_processes = get_all_processes()

    # Build process tree
    tree, pid_map = build_process_tree(all_processes)

    # Display some statistics
    print("\n📊 STATISTICS:")
    print(f"   Total Processes: {len(all_processes)}")
    print(f"   Parent Processes: {len(tree)}")

    # Show sample process (first one)
    if all_processes:
        print("\n📋 SAMPLE PROCESS INFO:")
        display_process_info(all_processes[0])

    # Find all Chrome processes (example)
    chrome_procs = get_process_by_name(all_processes, 'chrome.exe')
    if chrome_procs:
        print(f"\n🌐 Found {len(chrome_procs)} Chrome processes")

    print("\n✅ Test Complete!\n")
