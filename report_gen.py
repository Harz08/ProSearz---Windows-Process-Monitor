"""
report_gen.py
Report Generation Module - Creates detailed HTML security reports
"""

from datetime import datetime


class ReportGenerator:
    """
    Generates professional HTML reports from security alerts
    """

    def __init__(self, alert_manager):
        self.alert_manager = alert_manager
        self.alerts = alert_manager.alerts
        self.summary = alert_manager.get_summary()
        self.timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    def generate_html_report(self, filename=None):
        """
        Generate comprehensive HTML report
        Returns: Filename of generated report
        """
        if filename is None:
            filename = f'security_report_{self.timestamp}.html'

        html_content = self._build_html()

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f"[+] HTML report generated: {filename}")
            return filename
        except Exception as e:
            print(f"[!] Error generating HTML report: {e}")
            return None

    def _build_html(self):
        """
        Build the complete HTML report structure
        """
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Monitoring Report - {self.timestamp}</title>
    <style>
        {self._get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        {self._build_header()}
        {self._build_summary_section()}
        {self._build_severity_breakdown()}
        {self._build_alerts_section()}
        {self._build_footer()}
    </div>
</body>
</html>"""
        return html

    def _get_css_styles(self):
        """
        CSS styling for the report
        """
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }

        .content {
            padding: 30px;
        }

        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }

        .summary-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .summary-card h3 {
            font-size: 2em;
            margin-bottom: 5px;
            color: #1e3c72;
        }

        .summary-card p {
            color: #666;
            font-size: 0.9em;
        }

        .severity-section {
            margin: 30px 0;
        }

        .severity-bars {
            margin: 20px 0;
        }

        .severity-bar {
            margin: 15px 0;
        }

        .severity-label {
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
            font-weight: bold;
        }

        .bar-container {
            background: #f0f0f0;
            border-radius: 10px;
            overflow: hidden;
            height: 25px;
        }

        .bar-fill {
            height: 100%;
            transition: width 0.3s ease;
            display: flex;
            align-items: center;
            padding-left: 10px;
            color: white;
            font-weight: bold;
        }

        .bar-critical { background: linear-gradient(90deg, #ff4444 0%, #cc0000 100%); }
        .bar-high { background: linear-gradient(90deg, #ffaa00 0%, #ff8800 100%); }
        .bar-medium { background: linear-gradient(90deg, #4444ff 0%, #0000cc 100%); }
        .bar-low { background: linear-gradient(90deg, #44ff44 0%, #00cc00 100%); }

        .alerts-section {
            margin: 30px 0;
        }

        .alert-card {
            background: white;
            border-left: 5px solid;
            margin: 15px 0;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .alert-critical { border-color: #ff4444; background: #fff5f5; }
        .alert-high { border-color: #ffaa00; background: #fffbf0; }
        .alert-medium { border-color: #4444ff; background: #f5f5ff; }
        .alert-low { border-color: #44ff44; background: #f5fff5; }

        .alert-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        .alert-title {
            font-size: 1.2em;
            font-weight: bold;
        }

        .alert-severity {
            padding: 5px 15px;
            border-radius: 20px;
            color: white;
            font-weight: bold;
            font-size: 0.9em;
        }

        .severity-critical { background: #ff4444; }
        .severity-high { background: #ffaa00; }
        .severity-medium { background: #4444ff; }
        .severity-low { background: #44ff44; }

        .alert-description {
            color: #666;
            margin: 10px 0;
            line-height: 1.6;
        }

        .alert-details {
            background: rgba(0,0,0,0.03);
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }

        .alert-details div {
            margin: 5px 0;
        }

        .detail-label {
            font-weight: bold;
            color: #1e3c72;
        }

        .footer {
            background: #f5f5f5;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 2px solid #e0e0e0;
        }

        h2 {
            color: #1e3c72;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }

        .no-alerts {
            text-align: center;
            padding: 40px;
            color: #44ff44;
            font-size: 1.3em;
        }
        """

    def _build_header(self):
        """
        Build report header
        """
        return f"""
        <div class="header">
            <h1>🔒 Windows Security Monitoring Report</h1>
            <p>Generated: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}</p>
        </div>
        """

    def _build_summary_section(self):
        """
        Build summary statistics section
        """
        total = self.summary['total_alerts']
        critical = self.summary['by_severity']['CRITICAL']
        high = self.summary['by_severity']['HIGH']
        medium = self.summary['by_severity']['MEDIUM']
        low = self.summary['by_severity']['LOW']

        return f"""
        <div class="content">
            <h2>📊 Executive Summary</h2>
            <div class="summary-grid">
                <div class="summary-card">
                    <h3>{total}</h3>
                    <p>Total Alerts</p>
                </div>
                <div class="summary-card">
                    <h3>{critical}</h3>
                    <p>Critical</p>
                </div>
                <div class="summary-card">
                    <h3>{high}</h3>
                    <p>High</p>
                </div>
                <div class="summary-card">
                    <h3>{medium}</h3>
                    <p>Medium</p>
                </div>
                <div class="summary-card">
                    <h3>{low}</h3>
                    <p>Low</p>
                </div>
            </div>
        </div>
        """

    def _build_severity_breakdown(self):
        """
        Build severity breakdown with progress bars
        """
        total = self.summary['total_alerts']
        if total == 0:
            total = 1  # Avoid division by zero

        severities = [
            ('CRITICAL', 'critical', self.summary['by_severity']['CRITICAL']),
            ('HIGH', 'high', self.summary['by_severity']['HIGH']),
            ('MEDIUM', 'medium', self.summary['by_severity']['MEDIUM']),
            ('LOW', 'low', self.summary['by_severity']['LOW'])
        ]

        bars_html = ""
        for label, css_class, count in severities:
            percentage = (count / total) * 100
            bars_html += f"""
            <div class="severity-bar">
                <div class="severity-label">
                    <span>{label}</span>
                    <span>{count} alerts</span>
                </div>
                <div class="bar-container">
                    <div class="bar-fill bar-{css_class}" style="width: {percentage}%;">
                        {percentage:.1f}%
                    </div>
                </div>
            </div>
            """

        return f"""
        <div class="content">
            <div class="severity-section">
                <h2>📈 Severity Breakdown</h2>
                <div class="severity-bars">
                    {bars_html}
                </div>
            </div>
        </div>
        """

    def _build_alerts_section(self):
        """
        Build detailed alerts section
        """
        if not self.alerts:
            return """
            <div class="content">
                <h2>🔍 Detailed Alerts</h2>
                <div class="no-alerts">
                    ✅ No security alerts detected. System appears clean!
                </div>
            </div>
            """

        # Sort alerts by severity
        severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        sorted_alerts = sorted(self.alerts,
                               key=lambda x: severity_order.get(x.get('severity', 'LOW'), 4))

        alerts_html = ""
        for idx, alert in enumerate(sorted_alerts, 1):
            severity = alert.get('severity', 'LOW').lower()
            alerts_html += f"""
            <div class="alert-card alert-{severity}">
                <div class="alert-header">
                    <div class="alert-title">Alert #{idx}: {alert.get('type', 'Unknown Alert')}</div>
                    <div class="alert-severity severity-{severity}">{alert.get('severity', 'LOW')}</div>
                </div>
                <div class="alert-description">
                    {alert.get('description', 'No description available')}
                </div>
                <div class="alert-details">
                    {self._build_alert_details(alert)}
                </div>
            </div>
            """

        return f"""
        <div class="content">
            <div class="alerts-section">
                <h2>🔍 Detailed Alerts ({len(self.alerts)} total)</h2>
                {alerts_html}
            </div>
        </div>
        """

    def _build_alert_details(self, alert):
        """
        Build detailed information for each alert
        """
        details = []

        # Common fields
        if 'timestamp' in alert:
            details.append(f'<div><span class="detail-label">Timestamp:</span> {alert["timestamp"]}</div>')

        # Process-specific fields
        if 'process_name' in alert:
            details.append(f'<div><span class="detail-label">Process:</span> {alert["process_name"]}</div>')
        if 'pid' in alert:
            details.append(f'<div><span class="detail-label">PID:</span> {alert["pid"]}</div>')
        if 'path' in alert and alert['path']:
            details.append(f'<div><span class="detail-label">Path:</span> {alert["path"]}</div>')

        # Parent-child specific
        if 'parent_name' in alert:
            details.append(
                f'<div><span class="detail-label">Parent Process:</span> {alert["parent_name"]} (PID: {alert.get("parent_pid", "N/A")})</div>')
        if 'child_name' in alert:
            details.append(
                f'<div><span class="detail-label">Child Process:</span> {alert["child_name"]} (PID: {alert.get("child_pid", "N/A")})</div>')

        # Service-specific
        if 'service_name' in alert:
            details.append(f'<div><span class="detail-label">Service Name:</span> {alert["service_name"]}</div>')
        if 'display_name' in alert:
            details.append(f'<div><span class="detail-label">Display Name:</span> {alert["display_name"]}</div>')
        if 'state' in alert:
            details.append(f'<div><span class="detail-label">State:</span> {alert["state"]}</div>')
        if 'startup_type' in alert:
            details.append(f'<div><span class="detail-label">Startup Type:</span> {alert["startup_type"]}</div>')

        return '\n'.join(details) if details else '<div>No additional details available</div>'

    def _build_footer(self):
        """
        Build report footer
        """
        return f"""
        <div class="footer">
            <p><strong>Windows Security Monitoring Agent</strong></p>
            <p>Report generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}</p>
            <p>This is an automated security report. Please review all alerts carefully.</p>
        </div>
        """


# Test function - Only runs when file is executed directly
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("📊 REPORT GENERATOR - TEST MODE")
    print("=" * 60 + "\n")

    # Import alert manager for testing
    from alert_sys import AlertManager

    # Create test alert manager with sample data
    alert_mgr = AlertManager()

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
        }
    ]

    print("[*] Creating test alerts...")
    for alert in test_alerts:
        alert_mgr.add_alert(alert)

    print("\n[*] Generating HTML report...")
    report_gen = ReportGenerator(alert_mgr)
    filename = report_gen.generate_html_report('test_security_report.html')

    if filename:
        print(f"\n✅ Test report generated successfully!")
        print(f"📄 Open '{filename}' in your web browser to view the report")

    print("\n✅ Report Generator Test Complete!\n")

    
# ```
#
# ---
#
# ## 🧪 **STEP 5: Test It!**
#
# ### **Run the file:**
#
# 1. ** Right - click
# on
# `report_gen.py` ** in PyCharm
# 2.
# Click ** "Run 'report_gen'" **
#
# ### **Expected Output:**
# ```
# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
# 📊 REPORT
# GENERATOR - TEST
# MODE
# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
#
# [*]
# Creating
# test
# alerts...
# [CRITICAL]
# High - Risk
# Process
# Detected
# [HIGH]
# Suspicious
# Parent - Child
# Relationship
# [MEDIUM]
# Suspicious
# Process
# Path
#
# [*]
# Generating
# HTML
# report...
# [+]
# HTML
# report
# generated: test_security_report.html
#
# ✅ Test
# report
# generated
# successfully!
# 📄 Open
# 'test_security_report.html' in your
# web
# browser
# to
# view
# the
# report
#
# ✅ Report
# Generator
# Test
# Complete!
# ```
#
# ---
#
# ## 🌐 **IMPORTANT: View Your Report!**
#
# 1. ** Find
# the
# file ** `test_security_report.html` in your
# project
# folder
# 2. ** Right - click
# it ** → Open
# with → Chrome / Firefox / Edge
# 3. ** You
# should
# see
# a
# beautiful
# HTML
# report **
# with:
#     - Blue
#     gradient
#     header
#     - Summary
#     cards
#     - Colored
#     progress
#     bars
#     - Detailed
#     alert
#     cards
#
# ---
#
# ## ✅ **Verification Checklist**
#
# - []
# File
# created: `report_gen.py`
# - []
# Code
# runs
# without
# errors
# - []
# HTML
# file
# created: `test_security_report.html`
# - []
# Report
# opens in browser and looks
# good
# - []
# Shows
# 3
# test
# alerts
# with colors
#
# ---
#
# ## 🎉 **Progress Update**
# ```
# [████████████████████] 90 % Complete!
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
# Generator) ← YOU
# ARE
# HERE
# ⬜ main.py(Main
# Orchestrator) ← LAST
# STEP!