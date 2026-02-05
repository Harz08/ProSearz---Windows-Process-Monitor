"""
alert_sys.py
Alert Management System - Handles, displays, and exports security alerts
"""

import json
from datetime import datetime


class AlertManager:
    """
    Manages security alerts with severity levels and categorization
    """

    def __init__(self):
        self.alerts = []
        self.severity_counts = {
            'CRITICAL': 0,
            'HIGH': 0,
            'MEDIUM': 0,
            'LOW': 0
        }

    def add_alert(self, alert):
        """
        Add a new alert to the system
        """
        # Ensure alert has timestamp
        if 'timestamp' not in alert:
            alert['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Add to alerts list
        self.alerts.append(alert)

        # Update severity count
        severity = alert.get('severity', 'LOW')
        if severity in self.severity_counts:
            self.severity_counts[severity] += 1

        # Print alert to console
        self._print_alert(alert)

    def add_multiple_alerts(self, alerts_list):
        """
        Add multiple alerts at once
        """
        for alert in alerts_list:
            self.add_alert(alert)

    def _print_alert(self, alert):
        """
        Print colored alert to console based on severity
        """
        # ANSI color codes
        colors = {
            'CRITICAL': '\033[91m',  # Bright Red
            'HIGH': '\033[93m',  # Yellow
            'MEDIUM': '\033[94m',  # Blue
            'LOW': '\033[92m',  # Green
            'RESET': '\033[0m'
        }

        severity = alert.get('severity', 'LOW')
        color = colors.get(severity, colors['RESET'])
        reset = colors['RESET']

        # Print formatted alert
        print(f"{color}[{severity}] {alert.get('type', 'Alert')}{reset}")
        print(f"  └─ {alert.get('description', 'No description')}")

        # Print relevant details based on alert type
        if 'process_name' in alert:
            print(f"     Process: {alert['process_name']} (PID: {alert.get('pid', 'N/A')})")
        if 'parent_name' in alert and 'child_name' in alert:
            print(f"     Chain: {alert['parent_name']} → {alert['child_name']}")
        if 'path' in alert and alert['path']:
            print(f"     Path: {alert['path'][:80]}...")
        if 'service_name' in alert:
            print(f"     Service: {alert['display_name']} ({alert['service_name']})")

        print()  # Blank line for readability

    def get_summary(self):
        """
        Get summary statistics of all alerts
        Returns: Dictionary with alert statistics
        """
        summary = {
            'total_alerts': len(self.alerts),
            'by_severity': self.severity_counts.copy(),
            'by_type': {}
        }

        # Count alerts by type
        for alert in self.alerts:
            alert_type = alert.get('type', 'Unknown')
            summary['by_type'][alert_type] = summary['by_type'].get(alert_type, 0) + 1

        return summary

    def get_alerts_by_severity(self, severity):
        """
        Get all alerts of a specific severity level
        """
        return [alert for alert in self.alerts if alert.get('severity') == severity]

    def get_alerts_by_type(self, alert_type):
        """
        Get all alerts of a specific type
        """
        return [alert for alert in self.alerts if alert.get('type') == alert_type]

    def export_json(self, filename='alerts.json'):
        """
        Export all alerts to JSON file
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'total_alerts': len(self.alerts),
                    'summary': self.get_summary(),
                    'alerts': self.alerts
                }, f, indent=4, ensure_ascii=False)

            print(f"[+] Alerts exported to {filename}")
            return True
        except Exception as e:
            print(f"[!] Error exporting alerts: {e}")
            return False

    def export_csv(self, filename='alerts.csv'):
        """
        Export alerts to CSV format
        """
        try:
            import csv

            if not self.alerts:
                print("[!] No alerts to export")
                return False

            # Get all unique keys from alerts
            fieldnames = set()
            for alert in self.alerts:
                fieldnames.update(alert.keys())

            fieldnames = sorted(list(fieldnames))

            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.alerts)

            print(f"[+] Alerts exported to {filename}")
            return True
        except Exception as e:
            print(f"[!] Error exporting CSV: {e}")
            return False

    def print_summary(self):
        """
        Print formatted summary to console
        """
        summary = self.get_summary()

        print("\n" + "=" * 60)
        print("📊 ALERT SUMMARY")
        print("=" * 60)
        print(f"\nTotal Alerts: {summary['total_alerts']}")

        if summary['total_alerts'] > 0:
            print("\nBy Severity:")
            for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
                count = summary['by_severity'][severity]
                if count > 0:
                    print(f"  {severity:12} : {count}")

            print("\nBy Type:")
            for alert_type, count in sorted(summary['by_type'].items()):
                print(f"  {alert_type[:45]:45} : {count}")

        print("=" * 60 + "\n")

    def clear_alerts(self):
        """
        Clear all alerts (useful for testing)
        """
        self.alerts = []
        self.severity_counts = {
            'CRITICAL': 0,
            'HIGH': 0,
            'MEDIUM': 0,
            'LOW': 0
        }
        print("[*] All alerts cleared")


# Test function - Only runs when file is executed directly
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🚨 ALERT SYSTEM - TEST MODE")
    print("=" * 60 + "\n")

    # Create alert manager
    alert_mgr = AlertManager()

    # Test alerts with different severities
    test_alerts = [
        {
            'severity': 'CRITICAL',
            'type': 'High-Risk Process Detected',
            'process_name': 'mimikatz.exe',
            'pid': 1234,
            'path': 'C:\\Users\\Public\\mimikatz.exe',
            'description': 'Known credential dumping tool detected'
        },
        {
            'severity': 'HIGH',
            'type': 'Suspicious Parent-Child Relationship',
            'parent_name': 'winword.exe',
            'parent_pid': 5678,
            'child_name': 'powershell.exe',
            'child_pid': 9012,
            'description': 'Microsoft Word spawned PowerShell - Potential macro malware'
        },
        {
            'severity': 'MEDIUM',
            'type': 'Suspicious Process Path',
            'process_name': 'update.exe',
            'pid': 3456,
            'path': 'C:\\Windows\\Temp\\update.exe',
            'description': 'Process running from temporary directory'
        },
        {
            'severity': 'MEDIUM',
            'type': 'Suspicious Service Configuration',
            'service_name': 'MysteryService',
            'display_name': 'Mystery Background Service',
            'path': 'C:\\ProgramData\\unknown\\service.exe',
            'description': 'Service running from unusual location'
        }
    ]

    print("📝 Adding test alerts...\n")
    for alert in test_alerts:
        alert_mgr.add_alert(alert)

    # Print summary
    alert_mgr.print_summary()

    # Export to JSON
    alert_mgr.export_json('test_alerts.json')

    # Test getting alerts by severity
    critical_alerts = alert_mgr.get_alerts_by_severity('CRITICAL')
    print(f"\n🔴 Critical Alerts: {len(critical_alerts)}")

    high_alerts = alert_mgr.get_alerts_by_severity('HIGH')
    print(f"🟡 High Alerts: {len(high_alerts)}")

    print("\n✅ Alert System Test Complete!\n")