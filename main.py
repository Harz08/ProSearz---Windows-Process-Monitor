"""
main.py
Windows Service & Process Monitoring Agent - Main Application
Orchestrates all monitoring, detection, and reporting components
"""

# import sys
# from datetime import datetime
#
# # Import all our modules
# from core_mon import get_all_processes, build_process_tree
# from service_mon import enumerate_services
# from detect_rules import run_all_detections
# from alert_sys import AlertManager
# from report_gen import ReportGenerator

#
# def print_banner():
#     """
#     Display application banner
#     """
#     banner = """
#     ╔══════════════════════════════════════════════════════════════╗
#     ║                                                              ║
#     ║     🔒 Windows Service & Process Monitoring Agent 🔒         ║
#     ║                                                              ║
#     ║            Malware Detection & Security Analysis             ║
#     ║                                                              ║
#     ╚══════════════════════════════════════════════════════════════╝
#     """
#     print(banner)
#     print(f"    Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
#     print("    " + "=" * 62 + "\n")
#
#
# def print_section_header(title):
#     """
#     Print formatted section header
#     """
#     print("\n" + "=" * 60)
#     print(f"  {title}")
#     print("=" * 60 + "\n")
#
#
# def main():
#     """
#     Main application workflow
#     """
#     # Display banner
#     print_banner()
#
#     # Initialize alert manager
#     alert_manager = AlertManager()
#
#     try:
#         # ================================================================
#         # STEP 1: ENUMERATE PROCESSES
#         # ================================================================
#         print_section_header("📋 STEP 1: Enumerating System Processes")
#
#         processes = get_all_processes()
#
#         if not processes:
#             print("[!] Failed to enumerate processes. Exiting.")
#             return
#
#         print(f"[✓] Successfully enumerated {len(processes)} processes\n")
#
#         # ================================================================
#         # STEP 2: BUILD PROCESS TREE
#         # ================================================================
#         print_section_header("🌳 STEP 2: Building Process Hierarchy Tree")
#
#         process_tree, pid_to_process = build_process_tree(processes)
#
#         print(f"[✓] Process tree built with {len(process_tree)} parent processes\n")
#
#         # ================================================================
#         # STEP 3: ENUMERATE SERVICES
#         # ================================================================
#         print_section_header("⚙️  STEP 3: Enumerating Windows Services")
#
#         services = enumerate_services()
#
#         if not services:
#             print("[!] Warning: Failed to enumerate services")
#             print("[!] Try running as Administrator for full service access")
#             services = []
#         else:
#             print(f"[✓] Successfully enumerated {len(services)} services\n")
#
#         # ================================================================
#         # STEP 4: RUN DETECTIONS
#         # ================================================================
#         print_section_header("🔍 STEP 4: Running Security Detections")
#
#         # Run all detection rules
#         all_alerts = run_all_detections(processes, process_tree, pid_to_process, services)
#
#         # Add all alerts to alert manager
#         for alert_type, alerts_list in all_alerts.items():
#             for alert in alerts_list:
#                 alert_manager.add_alert(alert)
#
#         # ================================================================
#         # STEP 5: DISPLAY SUMMARY
#         # ================================================================
#         print_section_header("📊 STEP 5: Analysis Summary")
#
#         alert_manager.print_summary()
#
#         # ================================================================
#         # STEP 6: GENERATE REPORTS
#         # ================================================================
#         print_section_header("📝 STEP 6: Generating Reports")
#
#         # Export JSON report
#         print("[*] Exporting JSON report...")
#         alert_manager.export_json('security_alerts.json')
#
#         # Generate HTML report
#         print("[*] Generating HTML report...")
#         report_gen = ReportGenerator(alert_manager)
#         html_filename = report_gen.generate_html_report()
#
#         # ================================================================
#         # FINAL SUMMARY
#         # ================================================================
#         print_section_header("✅ MONITORING COMPLETE")
#
#         summary = alert_manager.get_summary()
#
#         print("📈 Final Statistics:")
#         print(f"   • Total Processes Scanned: {len(processes)}")
#         print(f"   • Total Services Scanned: {len(services)}")
#         print(f"   • Total Alerts Generated: {summary['total_alerts']}")
#         print(f"   • Critical Alerts: {summary['by_severity']['CRITICAL']}")
#         print(f"   • High Alerts: {summary['by_severity']['HIGH']}")
#         print(f"   • Medium Alerts: {summary['by_severity']['MEDIUM']}")
#         print(f"   • Low Alerts: {summary['by_severity']['LOW']}")
#
#         print("\n📄 Generated Files:")
#         print(f"   • JSON Report: security_alerts.json")
#         print(f"   • HTML Report: {html_filename}")
#
#         print("\n" + "=" * 60)
#
#         # Provide recommendations based on findings
#         if summary['by_severity']['CRITICAL'] > 0:
#             print("\n⚠️  CRITICAL ALERTS DETECTED!")
#             print("   Immediate action required. Review critical alerts in the report.")
#         elif summary['by_severity']['HIGH'] > 0:
#             print("\n⚠️  High-priority alerts detected.")
#             print("   Please review the report and investigate suspicious activity.")
#         elif summary['total_alerts'] > 0:
#             print("\n✓ Minor security findings detected.")
#             print("   Review the report for potential improvements.")
#         else:
#             print("\n✓ No security threats detected!")
#             print("   System appears clean. Continue monitoring regularly.")
#
#         print("\n" + "=" * 60)
#         print(f"\n🎉 Monitoring session completed at {datetime.now().strftime('%H:%M:%S')}")
#         print(f"💡 Tip: Open '{html_filename}' in your browser for detailed analysis\n")
#
#     except KeyboardInterrupt:
#         print("\n\n[!] Monitoring interrupted by user")
#         print("[*] Partial results may have been saved")
#         sys.exit(1)
#
#     except Exception as e:
#         print(f"\n[!] Error during monitoring: {e}")
#         import traceback
#         traceback.print_exc()
#         sys.exit(1)
#
#
# if __name__ == "__main__":
#     # Check if running on Windows
#     if sys.platform != 'win32':
#         print("[!] This tool is designed for Windows systems only")
#         sys.exit(1)
#
#     # Run main application
#     main()
# ```
#
# ---
#
# ## 🧪 **FINAL TEST: Run main.py!**
#
# ### **This is the BIG moment! 🎉**
#
# 1. ** Right - click
# on
# `main.py` ** in PyCharm
# 2.
# Click ** "Run 'main'" **
# 3. ** Watch
# the
# magic
# happen! **
#
# ### **Expected Output (Full System Run):**
# ```
# ╔══════════════════════════════════════════════════════════════╗
# ║                                                              ║
# ║     🔒 Windows
# Service & Process
# Monitoring
# Agent 🔒         ║
# ║                                                              ║
# ║            Malware
# Detection & Security
# Analysis             ║
# ║                                                              ║
# ╚══════════════════════════════════════════════════════════════╝
# Started: 2026 - 01 - 21
# 01: 15:30
# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
#
# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
# 📋 STEP
# 1: Enumerating
# System
# Processes
# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
#
# [*]
# Scanning
# running
# processes...
# [+]
# Found
# 246
# processes
# [✓] Successfully
# enumerated
# 246
# processes
#
# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
# 🌳 STEP
# 2: Building
# Process
# Hierarchy
# Tree
# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
#
# [*]
# Building
# process
# tree...
# [+]
# Process
# tree
# built
# with 50 parent processes
# [✓] Process
# tree
# built
# with 50 parent processes
#
# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
# ⚙️
# STEP
# 3: Enumerating
# Windows
# Services
# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
#
# [*]
# Scanning
# Windows
# services...
# [+]
# Found
# 315
# services
# [✓] Successfully
# enumerated
# 315
# services
#
# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
# 🔍 STEP
# 4: Running
# Security
# Detections
# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
#
# [*]
# Checking
# for suspicious parent - child relationships...
# [+]
# Found
# X
# suspicious
# parent - child
# relationships
# [*]
# Checking
# for processes in suspicious paths...
# [+]
# Found
# X
# processes in suspicious
# paths
# [*]
# Checking
# for suspicious process names...
# [+]
# Found
# X
# high - risk
# processes
# [*]
# Checking
# for suspicious service configurations...
# [+]
# Found
# X
# suspicious
# services
#
# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
# 📊 STEP
# 5: Analysis
# Summary
# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
#
# Total
# Alerts: X
#
# By
# Severity:
# CRITICAL: X
# HIGH: X
# MEDIUM: X
#
# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
# 📝 STEP
# 6: Generating
# Reports
# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
#
# [*]
# Exporting
# JSON
# report...
# [+]
# Alerts
# exported
# to
# security_alerts.json
# [*]
# Generating
# HTML
# report...
# [+]
# HTML
# report
# generated: security_report_2026 - 01 - 21_01 - 15 - 35.
# html
#
# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
# ✅ MONITORING
# COMPLETE
# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
#
# 📈 Final
# Statistics:
# • Total
# Processes
# Scanned: 246
# • Total
# Services
# Scanned: 315
# • Total
# Alerts
# Generated: X
# • Critical
# Alerts: X
# • High
# Alerts: X
# • Medium
# Alerts: X
# • Low
# Alerts: X
#
# 📄 Generated
# Files:
# • JSON
# Report: security_alerts.json
# • HTML
# Report: security_report_2026 - 01 - 21_01 - 15 - 35.
# html
#
# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
#
# ✓ No
# security
# threats
# detected! (or your actual results)
# System
# appears
# clean.Continue
# monitoring
# regularly.
#
# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
#
# 🎉 Monitoring
# session
# completed
# at
# 01: 15:35
# 💡 Tip: Open
# 'security_report_2026-01-21_01-15-35.html' in your
# browser
# for detailed analysis
#     ```
#
# ---
#
# ## 🎊 **YOU'RE DONE! PROJECT 100% COMPLETE!**
# ```
# [████████████████████] 100 % COMPLETE! 🎉
#
# ✅ core_mon.py(Process
# Monitor)
# ✅ service_mon.py(Service
# Auditor)
# ✅ detecr_rules.py(Detection
# Engine)
# ✅ alert_sys.py(Alert
# System)
# ✅ report_gen.py(Report
# Generator)
# ✅ main.py(Main
# Orchestrator)


"""
main.py
Windows Service & Process Monitoring Agent - Web Dashboard Version
"""

import sys
from web_interface import run_web_dashboard


def main():
    """
    Launch web-based security monitoring dashboard
    """
    print("\n" + "=" * 60)
    print("  🔒 Windows Security Monitoring Agent")
    print("  Web Dashboard Mode")
    print("=" * 60 + "\n")

    # Check if running on Windows
    if sys.platform != 'win32':
        print("[!] This tool is designed for Windows systems only")
        sys.exit(1)

    # Run web dashboard
    run_web_dashboard()


if __name__ == "__main__":
    main()