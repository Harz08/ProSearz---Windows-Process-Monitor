# """
# web_interface.py
# Web-based Dashboard Interface for Security Monitoring
# """
#
# from flask import Flask, render_template_string, jsonify, send_file
# import threading
# import webbrowser
# import time
# import json
# from datetime import datetime
# import os
#
# # Import our modules
# from core_mon import get_all_processes, build_process_tree
# from service_mon import enumerate_services
# from detect_rules import run_all_detections
# from alert_sys import AlertManager
# from report_gen import ReportGenerator
#
#
# class WebDashboard:
#     def __init__(self):
#         self.app = Flask(__name__)
#         self.scan_complete = False
#         self.scan_progress = 0
#         self.current_step = "Initializing..."
#         self.alert_manager = None
#         self.processes_count = 0
#         self.services_count = 0
#         self.setup_routes()
#
#     def setup_routes(self):
#         """Setup Flask routes"""
#
#         @self.app.route('/')
#         def dashboard():
#             return render_template_string(self.get_html_template())
#
#         @self.app.route('/api/status')
#         def get_status():
#             """API endpoint for scan status"""
#             if self.alert_manager:
#                 summary = self.alert_manager.get_summary()
#             else:
#                 summary = {'total_alerts': 0, 'by_severity': {}}
#
#             return jsonify({
#                 'scan_complete': self.scan_complete,
#                 'progress': self.scan_progress,
#                 'current_step': self.current_step,
#                 'processes_count': self.processes_count,
#                 'services_count': self.services_count,
#                 'summary': summary
#             })
#
#         @self.app.route('/api/alerts')
#         def get_alerts():
#             """API endpoint for alerts data"""
#             if self.alert_manager:
#                 return jsonify({
#                     'alerts': self.alert_manager.alerts,
#                     'summary': self.alert_manager.get_summary()
#                 })
#             return jsonify({'alerts': [], 'summary': {}})
#
#         @self.app.route('/download/pdf')
#         def download_pdf():
#             """Generate and download PDF report"""
#             if self.alert_manager:
#                 # Generate HTML report first
#                 report_gen = ReportGenerator(self.alert_manager)
#                 html_file = report_gen.generate_html_report()
#
#                 # For now, return the HTML (PDF conversion requires additional library)
#                 return send_file(html_file, as_attachment=True,
#                                  download_name=f'security_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
#             return "No data available", 404
#
#         @self.app.route('/download/json')
#         def download_json():
#             """Download JSON report"""
#             if self.alert_manager:
#                 filename = 'security_alerts.json'
#                 self.alert_manager.export_json(filename)
#                 return send_file(filename, as_attachment=True)
#             return "No data available", 404
#
#     def run_scan_async(self):
#         """Run security scan in background"""
#         try:
#             # Step 1: Enumerate processes
#             self.current_step = "🔍 Scanning processes..."
#             self.scan_progress = 20
#             processes = get_all_processes()
#             self.processes_count = len(processes)
#             time.sleep(0.5)
#
#             # Step 2: Build process tree
#             self.current_step = "🌳 Building process tree..."
#             self.scan_progress = 40
#             process_tree, pid_to_process = build_process_tree(processes)
#             time.sleep(0.5)
#
#             # Step 3: Enumerate services
#             self.current_step = "⚙️ Scanning services..."
#             self.scan_progress = 60
#             services = enumerate_services()
#             self.services_count = len(services)
#             time.sleep(0.5)
#
#             # Step 4: Run detections
#             self.current_step = "🔍 Running security detections..."
#             self.scan_progress = 80
#             self.alert_manager = AlertManager()
#             all_alerts = run_all_detections(processes, process_tree, pid_to_process, services)
#
#             # Add alerts
#             for alert_type, alerts_list in all_alerts.items():
#                 for alert in alerts_list:
#                     self.alert_manager.add_alert(alert)
#
#             time.sleep(0.5)
#
#             # Step 5: Complete
#             self.current_step = "✅ Scan complete!"
#             self.scan_progress = 100
#             self.scan_complete = True
#
#         except Exception as e:
#             self.current_step = f"❌ Error: {str(e)}"
#             self.scan_complete = True
#
#     def start_scan(self):
#         """Start background scan"""
#         scan_thread = threading.Thread(target=self.run_scan_async, daemon=True)
#         scan_thread.start()
#
#     def run_server(self, port=5000):
#         """Run Flask server and open browser"""
#         # Start scan
#         self.start_scan()
#
#         # Open browser after short delay
#         def open_browser():
#             time.sleep(1.5)
#             webbrowser.open(f'http://127.0.0.1:{port}')
#
#         browser_thread = threading.Thread(target=open_browser, daemon=True)
#         browser_thread.start()
#
#         # Run Flask
#         print(f"\n🌐 Starting web dashboard on http://127.0.0.1:{port}")
#         print("🚀 Opening browser automatically...")
#         print("⌨️  Press Ctrl+C to stop the server\n")
#
#         self.app.run(port=port, debug=False, use_reloader=False)
#
#     def get_html_template(self):
#         """HTML template for dashboard"""
#         return '''
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Security Monitoring Dashboard</title>
#     <style>
#         * {
#             margin: 0;
#             padding: 0;
#             box-sizing: border-box;
#         }
#
#         body {
#             font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#             background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#             min-height: 100vh;
#             padding: 20px;
#         }
#
#         .container {
#             max-width: 1400px;
#             margin: 0 auto;
#         }
#
#         .header {
#             background: white;
#             padding: 30px;
#             border-radius: 15px;
#             box-shadow: 0 10px 40px rgba(0,0,0,0.2);
#             margin-bottom: 20px;
#             text-align: center;
#         }
#
#         .header h1 {
#             color: #1e3c72;
#             font-size: 2.5em;
#             margin-bottom: 10px;
#         }
#
#         .header p {
#             color: #666;
#             font-size: 1.1em;
#         }
#
#         .progress-section {
#             background: white;
#             padding: 30px;
#             border-radius: 15px;
#             box-shadow: 0 10px 40px rgba(0,0,0,0.2);
#             margin-bottom: 20px;
#         }
#
#         .progress-bar {
#             background: #f0f0f0;
#             border-radius: 25px;
#             height: 40px;
#             overflow: hidden;
#             margin: 20px 0;
#         }
#
#         .progress-fill {
#             background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
#             height: 100%;
#             transition: width 0.3s ease;
#             display: flex;
#             align-items: center;
#             justify-content: center;
#             color: white;
#             font-weight: bold;
#         }
#
#         .stats-grid {
#             display: grid;
#             grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
#             gap: 20px;
#             margin: 20px 0;
#         }
#
#         .stat-card {
#             background: white;
#             padding: 25px;
#             border-radius: 15px;
#             box-shadow: 0 5px 20px rgba(0,0,0,0.1);
#             text-align: center;
#         }
#
#         .stat-card h2 {
#             font-size: 3em;
#             margin-bottom: 10px;
#         }
#
#         .stat-card p {
#             color: #666;
#             font-size: 1em;
#         }
#
#         .critical { color: #ff4444; }
#         .high { color: #ffaa00; }
#         .medium { color: #4444ff; }
#         .low { color: #44ff44; }
#         .info { color: #1e3c72; }
#
#         .alerts-section {
#             background: white;
#             padding: 30px;
#             border-radius: 15px;
#             box-shadow: 0 10px 40px rgba(0,0,0,0.2);
#             margin-bottom: 20px;
#         }
#
#         .alert-item {
#             background: #f8f9fa;
#             border-left: 5px solid;
#             padding: 20px;
#             margin: 15px 0;
#             border-radius: 5px;
#         }
#
#         .alert-critical { border-color: #ff4444; background: #fff5f5; }
#         .alert-high { border-color: #ffaa00; background: #fffbf0; }
#         .alert-medium { border-color: #4444ff; background: #f5f5ff; }
#         .alert-low { border-color: #44ff44; background: #f5fff5; }
#
#         .alert-header {
#             display: flex;
#             justify-content: space-between;
#             margin-bottom: 10px;
#         }
#
#         .alert-title {
#             font-weight: bold;
#             font-size: 1.1em;
#         }
#
#         .alert-badge {
#             padding: 5px 15px;
#             border-radius: 20px;
#             color: white;
#             font-weight: bold;
#             font-size: 0.9em;
#         }
#
#         .badge-critical { background: #ff4444; }
#         .badge-high { background: #ffaa00; }
#         .badge-medium { background: #4444ff; }
#         .badge-low { background: #44ff44; }
#
#         .download-buttons {
#             display: flex;
#             gap: 15px;
#             justify-content: center;
#             margin-top: 30px;
#         }
#
#         .btn {
#             padding: 15px 40px;
#             border: none;
#             border-radius: 25px;
#             font-size: 1.1em;
#             font-weight: bold;
#             cursor: pointer;
#             transition: transform 0.2s;
#             text-decoration: none;
#             display: inline-block;
#         }
#
#         .btn:hover {
#             transform: scale(1.05);
#         }
#
#         .btn-primary {
#             background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#             color: white;
#         }
#
#         .btn-success {
#             background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
#             color: white;
#         }
#
#         .loading {
#             text-align: center;
#             padding: 40px;
#             font-size: 1.2em;
#             color: #666;
#         }
#
#         .spinner {
#             border: 4px solid #f3f3f3;
#             border-top: 4px solid #667eea;
#             border-radius: 50%;
#             width: 50px;
#             height: 50px;
#             animation: spin 1s linear infinite;
#             margin: 20px auto;
#         }
#
#         @keyframes spin {
#             0% { transform: rotate(0deg); }
#             100% { transform: rotate(360deg); }
#         }
#
#         .hidden {
#             display: none;
#         }
#     </style>
# </head>
# <body>
#     <div class="container">
#         <!-- Header -->
#         <div class="header">
#             <h1>🔒 Security Monitoring Dashboard</h1>
#             <p id="timestamp">Loading...</p>
#         </div>
#
#         <!-- Progress Section -->
#         <div class="progress-section" id="progressSection">
#             <h2 style="color: #1e3c72; margin-bottom: 20px;">Scan Progress</h2>
#             <div class="progress-bar">
#                 <div class="progress-fill" id="progressBar">0%</div>
#             </div>
#             <p id="currentStep" style="text-align: center; font-size: 1.2em; color: #666;">
#                 Initializing...
#             </p>
#         </div>
#
#         <!-- Statistics Grid -->
#         <div class="stats-grid" id="statsGrid">
#             <div class="stat-card">
#                 <h2 class="info" id="processCount">-</h2>
#                 <p>Processes Scanned</p>
#             </div>
#             <div class="stat-card">
#                 <h2 class="info" id="serviceCount">-</h2>
#                 <p>Services Scanned</p>
#             </div>
#             <div class="stat-card">
#                 <h2 class="info" id="totalAlerts">-</h2>
#                 <p>Total Alerts</p>
#             </div>
#             <div class="stat-card">
#                 <h2 class="critical" id="criticalCount">-</h2>
#                 <p>Critical</p>
#             </div>
#             <div class="stat-card">
#                 <h2 class="high" id="highCount">-</h2>
#                 <p>High</p>
#             </div>
#             <div class="stat-card">
#                 <h2 class="medium" id="mediumCount">-</h2>
#                 <p>Medium</p>
#             </div>
#         </div>
#
#         <!-- Alerts Section -->
#         <div class="alerts-section hidden" id="alertsSection">
#             <h2 style="color: #1e3c72; margin-bottom: 20px;">Security Alerts</h2>
#             <div id="alertsList"></div>
#
#             <!-- Download Buttons -->
#             <div class="download-buttons">
#                 <a href="/download/pdf" class="btn btn-primary">📄 Download Report (HTML)</a>
#                 <a href="/download/json" class="btn btn-success">📊 Download JSON</a>
#             </div>
#         </div>
#     </div>
#
#     <script>
#         // Update timestamp
#         document.getElementById('timestamp').textContent =
#             'Started: ' + new Date().toLocaleString();
#
#         // Poll for updates
#         function updateDashboard() {
#             fetch('/api/status')
#                 .then(response => response.json())
#                 .then(data => {
#                     // Update progress
#                     document.getElementById('progressBar').style.width = data.progress + '%';
#                     document.getElementById('progressBar').textContent = data.progress + '%';
#                     document.getElementById('currentStep').textContent = data.current_step;
#
#                     // Update stats
#                     document.getElementById('processCount').textContent = data.processes_count || '-';
#                     document.getElementById('serviceCount').textContent = data.services_count || '-';
#                     document.getElementById('totalAlerts').textContent = data.summary.total_alerts || '0';
#                     document.getElementById('criticalCount').textContent =
#                         (data.summary.by_severity && data.summary.by_severity.CRITICAL) || '0';
#                     document.getElementById('highCount').textContent =
#                         (data.summary.by_severity && data.summary.by_severity.HIGH) || '0';
#                     document.getElementById('mediumCount').textContent =
#                         (data.summary.by_severity && data.summary.by_severity.MEDIUM) || '0';
#
#                     // If scan complete, show alerts
#                     if (data.scan_complete) {
#                         loadAlerts();
#                     }
#                 });
#         }
#
#         function loadAlerts() {
#             fetch('/api/alerts')
#                 .then(response => response.json())
#                 .then(data => {
#                     const alertsList = document.getElementById('alertsList');
#                     const alertsSection = document.getElementById('alertsSection');
#
#                     if (data.alerts.length === 0) {
#                         alertsList.innerHTML = '<div class="loading">✅ No security threats detected! System appears clean.</div>';
#                     } else {
#                         alertsList.innerHTML = data.alerts.map((alert, idx) => `
#                             <div class="alert-item alert-${alert.severity.toLowerCase()}">
#                                 <div class="alert-header">
#                                     <div class="alert-title">Alert #${idx + 1}: ${alert.type}</div>
#                                     <div class="alert-badge badge-${alert.severity.toLowerCase()}">${alert.severity}</div>
#                                 </div>
#                                 <p>${alert.description}</p>
#                                 ${alert.process_name ? `<p style="margin-top: 10px;"><strong>Process:</strong> ${alert.process_name} (PID: ${alert.pid})</p>` : ''}
#                                 ${alert.path ? `<p><strong>Path:</strong> ${alert.path}</p>` : ''}
#                             </div>
#                         `).join('');
#                     }
#
#                     alertsSection.classList.remove('hidden');
#                 });
#         }
#
#         // Update every 1 second
#         setInterval(updateDashboard, 1000);
#         updateDashboard();
#     </script>
# </body>
# </html>
#         '''
#
#
# def run_web_dashboard():
#     """Main function to run the web dashboard"""
#     dashboard = WebDashboard()
#     dashboard.run_server(port=5000)
#
#
# if __name__ == "__main__":
#     run_web_dashboard()




























































































#
# """
# web_interface.py
# Enhanced Web-based Dashboard Interface with Full Alert Details
# """
#
# from flask import Flask, render_template_string, jsonify, send_file
# import threading
# import webbrowser
# import time
# import json
# from datetime import datetime
# import os
#
# # Import our modules
# from core_mon import get_all_processes, build_process_tree
# from service_mon import enumerate_services
# from detect_rules import run_all_detections
# from alert_sys import AlertManager
# from report_gen import ReportGenerator
#
#
# class WebDashboard:
#     def __init__(self):
#         self.app = Flask(__name__)
#         self.scan_complete = False
#         self.scan_progress = 0
#         self.current_step = "Initializing..."
#         self.alert_manager = None
#         self.processes_count = 0
#         self.services_count = 0
#         self.processes_data = []
#         self.services_data = []
#         self.setup_routes()
#
#     def setup_routes(self):
#         """Setup Flask routes"""
#
#         @self.app.route('/')
#         def dashboard():
#             return render_template_string(self.get_html_template())
#
#         @self.app.route('/api/status')
#         def get_status():
#             """API endpoint for scan status"""
#             if self.alert_manager:
#                 summary = self.alert_manager.get_summary()
#             else:
#                 summary = {'total_alerts': 0, 'by_severity': {}}
#
#             return jsonify({
#                 'scan_complete': self.scan_complete,
#                 'progress': self.scan_progress,
#                 'current_step': self.current_step,
#                 'processes_count': self.processes_count,
#                 'services_count': self.services_count,
#                 'summary': summary
#             })
#
#         @self.app.route('/api/alerts')
#         def get_alerts():
#             """API endpoint for full alerts data"""
#             if self.alert_manager:
#                 return jsonify({
#                     'alerts': self.alert_manager.alerts,
#                     'summary': self.alert_manager.get_summary()
#                 })
#             return jsonify({'alerts': [], 'summary': {}})
#
#         @self.app.route('/api/full-data')
#         def get_full_data():
#             """API endpoint for complete scan data"""
#             if self.alert_manager:
#                 return jsonify({
#                     'alerts': self.alert_manager.alerts,
#                     'summary': self.alert_manager.get_summary(),
#                     'processes_sample': self.processes_data[:20],  # First 20 processes
#                     'total_processes': len(self.processes_data),
#                     'services_sample': self.services_data[:20],  # First 20 services
#                     'total_services': len(self.services_data)
#                 })
#             return jsonify({})
#
#         @self.app.route('/download/pdf')
#         def download_pdf():
#             """Generate and download HTML report"""
#             if self.alert_manager:
#                 report_gen = ReportGenerator(self.alert_manager)
#                 html_file = report_gen.generate_html_report()
#                 return send_file(html_file, as_attachment=True,
#                                  download_name=f'security_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
#             return "No data available", 404
#
#         @self.app.route('/download/json')
#         def download_json():
#             """Download JSON report"""
#             if self.alert_manager:
#                 filename = 'security_alerts.json'
#                 self.alert_manager.export_json(filename)
#                 return send_file(filename, as_attachment=True)
#             return "No data available", 404
#
#     def run_scan_async(self):
#         """Run security scan in background"""
#         try:
#             # Step 1: Enumerate processes
#             self.current_step = "🔍 Scanning processes..."
#             self.scan_progress = 20
#             processes = get_all_processes()
#             self.processes_count = len(processes)
#             self.processes_data = processes
#             time.sleep(0.5)
#
#             # Step 2: Build process tree
#             self.current_step = "🌳 Building process tree..."
#             self.scan_progress = 40
#             process_tree, pid_to_process = build_process_tree(processes)
#             time.sleep(0.5)
#
#             # Step 3: Enumerate services
#             self.current_step = "⚙️ Scanning services..."
#             self.scan_progress = 60
#             services = enumerate_services()
#             self.services_count = len(services)
#             self.services_data = services
#             time.sleep(0.5)
#
#             # Step 4: Run detections
#             self.current_step = "🔍 Running security detections..."
#             self.scan_progress = 80
#             self.alert_manager = AlertManager()
#             all_alerts = run_all_detections(processes, process_tree, pid_to_process, services)
#
#             # Add alerts
#             for alert_type, alerts_list in all_alerts.items():
#                 for alert in alerts_list:
#                     self.alert_manager.add_alert(alert)
#
#             time.sleep(0.5)
#
#             # Step 5: Complete
#             self.current_step = "✅ Scan complete!"
#             self.scan_progress = 100
#             self.scan_complete = True
#
#         except Exception as e:
#             self.current_step = f"❌ Error: {str(e)}"
#             self.scan_complete = True
#
#     def start_scan(self):
#         """Start background scan"""
#         scan_thread = threading.Thread(target=self.run_scan_async, daemon=True)
#         scan_thread.start()
#
#     def run_server(self, port=5000):
#         """Run Flask server and open browser"""
#         self.start_scan()
#
#         def open_browser():
#             time.sleep(1.5)
#             webbrowser.open(f'http://127.0.0.1:{port}')
#
#         browser_thread = threading.Thread(target=open_browser, daemon=True)
#         browser_thread.start()
#
#         print(f"\n🌐 Starting web dashboard on http://127.0.0.1:{port}")
#         print("🚀 Opening browser automatically...")
#         print("⌨️  Press Ctrl+C to stop the server\n")
#
#         self.app.run(port=port, debug=False, use_reloader=False)
#
#     def get_html_template(self):
#         """Enhanced HTML template with full details"""
#         return '''
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Security Monitoring Dashboard</title>
#     <style>
#         * {
#             margin: 0;
#             padding: 0;
#             box-sizing: border-box;
#         }
#
#         body {
#             font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#             background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#             min-height: 100vh;
#             padding: 20px;
#         }
#
#         .container {
#             max-width: 1400px;
#             margin: 0 auto;
#         }
#
#         .header {
#             background: white;
#             padding: 30px;
#             border-radius: 15px;
#             box-shadow: 0 10px 40px rgba(0,0,0,0.2);
#             margin-bottom: 20px;
#             text-align: center;
#         }
#
#         .header h1 {
#             color: #1e3c72;
#             font-size: 2.5em;
#             margin-bottom: 10px;
#         }
#
#         .header p {
#             color: #666;
#             font-size: 1.1em;
#         }
#
#         .progress-section {
#             background: white;
#             padding: 30px;
#             border-radius: 15px;
#             box-shadow: 0 10px 40px rgba(0,0,0,0.2);
#             margin-bottom: 20px;
#         }
#
#         .progress-bar {
#             background: #f0f0f0;
#             border-radius: 25px;
#             height: 40px;
#             overflow: hidden;
#             margin: 20px 0;
#         }
#
#         .progress-fill {
#             background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
#             height: 100%;
#             transition: width 0.3s ease;
#             display: flex;
#             align-items: center;
#             justify-content: center;
#             color: white;
#             font-weight: bold;
#         }
#
#         .stats-grid {
#             display: grid;
#             grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
#             gap: 20px;
#             margin: 20px 0;
#         }
#
#         .stat-card {
#             background: white;
#             padding: 25px;
#             border-radius: 15px;
#             box-shadow: 0 5px 20px rgba(0,0,0,0.1);
#             text-align: center;
#         }
#
#         .stat-card h2 {
#             font-size: 3em;
#             margin-bottom: 10px;
#         }
#
#         .stat-card p {
#             color: #666;
#             font-size: 1em;
#         }
#
#         .critical { color: #ff4444; }
#         .high { color: #ffaa00; }
#         .medium { color: #4444ff; }
#         .low { color: #44ff44; }
#         .info { color: #1e3c72; }
#
#         .alerts-section {
#             background: white;
#             padding: 30px;
#             border-radius: 15px;
#             box-shadow: 0 10px 40px rgba(0,0,0,0.2);
#             margin-bottom: 20px;
#         }
#
#         .alert-item {
#             background: #f8f9fa;
#             border-left: 5px solid;
#             padding: 20px;
#             margin: 15px 0;
#             border-radius: 5px;
#         }
#
#         .alert-critical { border-color: #ff4444; background: #fff5f5; }
#         .alert-high { border-color: #ffaa00; background: #fffbf0; }
#         .alert-medium { border-color: #4444ff; background: #f5f5ff; }
#         .alert-low { border-color: #44ff44; background: #f5fff5; }
#
#         .alert-header {
#             display: flex;
#             justify-content: space-between;
#             margin-bottom: 15px;
#             align-items: center;
#         }
#
#         .alert-title {
#             font-weight: bold;
#             font-size: 1.2em;
#         }
#
#         .alert-badge {
#             padding: 5px 15px;
#             border-radius: 20px;
#             color: white;
#             font-weight: bold;
#             font-size: 0.9em;
#         }
#
#         .badge-critical { background: #ff4444; }
#         .badge-high { background: #ffaa00; }
#         .badge-medium { background: #4444ff; }
#         .badge-low { background: #44ff44; }
#
#         .alert-description {
#             color: #555;
#             font-size: 1em;
#             line-height: 1.6;
#             margin-bottom: 15px;
#         }
#
#         .alert-details {
#             background: rgba(0,0,0,0.03);
#             padding: 15px;
#             border-radius: 8px;
#             font-family: 'Courier New', monospace;
#             font-size: 0.9em;
#         }
#
#         .alert-details div {
#             margin: 8px 0;
#             display: flex;
#         }
#
#         .detail-label {
#             font-weight: bold;
#             color: #1e3c72;
#             min-width: 150px;
#         }
#
#         .detail-value {
#             color: #333;
#             word-break: break-all;
#         }
#
#         .download-buttons {
#             display: flex;
#             gap: 15px;
#             justify-content: center;
#             margin-top: 30px;
#             flex-wrap: wrap;
#         }
#
#         .btn {
#             padding: 15px 40px;
#             border: none;
#             border-radius: 25px;
#             font-size: 1.1em;
#             font-weight: bold;
#             cursor: pointer;
#             transition: transform 0.2s;
#             text-decoration: none;
#             display: inline-block;
#         }
#
#         .btn:hover {
#             transform: scale(1.05);
#         }
#
#         .btn-primary {
#             background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#             color: white;
#         }
#
#         .btn-success {
#             background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
#             color: white;
#         }
#
#         .loading {
#             text-align: center;
#             padding: 40px;
#             font-size: 1.2em;
#             color: #666;
#         }
#
#         .hidden {
#             display: none;
#         }
#
#         .section-title {
#             color: #1e3c72;
#             border-bottom: 3px solid #667eea;
#             padding-bottom: 10px;
#             margin-bottom: 20px;
#             font-size: 1.5em;
#         }
#
#         .no-alerts {
#             background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
#             color: white;
#             padding: 40px;
#             border-radius: 15px;
#             text-align: center;
#             font-size: 1.3em;
#             margin: 20px 0;
#         }
#
#         .severity-breakdown {
#             background: white;
#             padding: 30px;
#             border-radius: 15px;
#             box-shadow: 0 10px 40px rgba(0,0,0,0.2);
#             margin-bottom: 20px;
#         }
#
#         .severity-bar-container {
#             margin: 20px 0;
#         }
#
#         .severity-label {
#             display: flex;
#             justify-content: space-between;
#             margin-bottom: 8px;
#             font-weight: bold;
#         }
#
#         .bar-bg {
#             background: #f0f0f0;
#             border-radius: 10px;
#             overflow: hidden;
#             height: 30px;
#         }
#
#         .bar-fill-critical {
#             background: linear-gradient(90deg, #ff4444 0%, #cc0000 100%);
#             height: 100%;
#             display: flex;
#             align-items: center;
#             padding-left: 15px;
#             color: white;
#             font-weight: bold;
#             transition: width 0.5s ease;
#         }
#
#         .bar-fill-high {
#             background: linear-gradient(90deg, #ffaa00 0%, #ff8800 100%);
#             height: 100%;
#             display: flex;
#             align-items: center;
#             padding-left: 15px;
#             color: white;
#             font-weight: bold;
#             transition: width 0.5s ease;
#         }
#
#         .bar-fill-medium {
#             background: linear-gradient(90deg, #4444ff 0%, #0000cc 100%);
#             height: 100%;
#             display: flex;
#             align-items: center;
#             padding-left: 15px;
#             color: white;
#             font-weight: bold;
#             transition: width 0.5s ease;
#         }
#
#         .bar-fill-low {
#             background: linear-gradient(90deg, #44ff44 0%, #00cc00 100%);
#             height: 100%;
#             display: flex;
#             align-items: center;
#             padding-left: 15px;
#             color: white;
#             font-weight: bold;
#             transition: width 0.5s ease;
#         }
#     </style>
# </head>
# <body>
#     <div class="container">
#         <!-- Header -->
#         <div class="header">
#             <h1>🔒 Security Monitoring Dashboard</h1>
#             <p id="timestamp">Loading...</p>
#         </div>
#
#         <!-- Progress Section -->
#         <div class="progress-section" id="progressSection">
#             <h2 class="section-title">Scan Progress</h2>
#             <div class="progress-bar">
#                 <div class="progress-fill" id="progressBar">0%</div>
#             </div>
#             <p id="currentStep" style="text-align: center; font-size: 1.2em; color: #666;">
#                 Initializing...
#             </p>
#         </div>
#
#         <!-- Statistics Grid -->
#         <div class="stats-grid" id="statsGrid">
#             <div class="stat-card">
#                 <h2 class="info" id="processCount">-</h2>
#                 <p>Processes Scanned</p>
#             </div>
#             <div class="stat-card">
#                 <h2 class="info" id="serviceCount">-</h2>
#                 <p>Services Scanned</p>
#             </div>
#             <div class="stat-card">
#                 <h2 class="info" id="totalAlerts">-</h2>
#                 <p>Total Alerts</p>
#             </div>
#             <div class="stat-card">
#                 <h2 class="critical" id="criticalCount">-</h2>
#                 <p>Critical</p>
#             </div>
#             <div class="stat-card">
#                 <h2 class="high" id="highCount">-</h2>
#                 <p>High</p>
#             </div>
#             <div class="stat-card">
#                 <h2 class="medium" id="mediumCount">-</h2>
#                 <p>Medium</p>
#             </div>
#         </div>
#
#         <!-- Severity Breakdown -->
#         <div class="severity-breakdown hidden" id="severitySection">
#             <h2 class="section-title">📈 Severity Breakdown</h2>
#             <div class="severity-bar-container">
#                 <div class="severity-label">
#                     <span>CRITICAL</span>
#                     <span id="criticalCountText">0 alerts</span>
#                 </div>
#                 <div class="bar-bg">
#                     <div class="bar-fill-critical" id="barCritical" style="width: 0%;">0%</div>
#                 </div>
#             </div>
#             <div class="severity-bar-container">
#                 <div class="severity-label">
#                     <span>HIGH</span>
#                     <span id="highCountText">0 alerts</span>
#                 </div>
#                 <div class="bar-bg">
#                     <div class="bar-fill-high" id="barHigh" style="width: 0%;">0%</div>
#                 </div>
#             </div>
#             <div class="severity-bar-container">
#                 <div class="severity-label">
#                     <span>MEDIUM</span>
#                     <span id="mediumCountText">0 alerts</span>
#                 </div>
#                 <div class="bar-bg">
#                     <div class="bar-fill-medium" id="barMedium" style="width: 0%;">0%</div>
#                 </div>
#             </div>
#             <div class="severity-bar-container">
#                 <div class="severity-label">
#                     <span>LOW</span>
#                     <span id="lowCountText">0 alerts</span>
#                 </div>
#                 <div class="bar-bg">
#                     <div class="bar-fill-low" id="barLow" style="width: 0%;">0%</div>
#                 </div>
#             </div>
#         </div>
#
#         <!-- Alerts Section -->
#         <div class="alerts-section hidden" id="alertsSection">
#             <h2 class="section-title">🔍 Detailed Security Alerts (<span id="alertCount">0</span>)</h2>
#             <div id="alertsList"></div>
#
#             <!-- Download Buttons -->
#             <div class="download-buttons">
#                 <a href="/download/pdf" class="btn btn-primary">📄 Download Full Report (HTML)</a>
#                 <a href="/download/json" class="btn btn-success">📊 Download Data (JSON)</a>
#             </div>
#         </div>
#     </div>
#
#     <script>
#         document.getElementById('timestamp').textContent =
#             'Started: ' + new Date().toLocaleString();
#
#         function updateDashboard() {
#             fetch('/api/status')
#                 .then(response => response.json())
#                 .then(data => {
#                     // Update progress
#                     document.getElementById('progressBar').style.width = data.progress + '%';
#                     document.getElementById('progressBar').textContent = data.progress + '%';
#                     document.getElementById('currentStep').textContent = data.current_step;
#
#                     // Update stats
#                     document.getElementById('processCount').textContent = data.processes_count || '-';
#                     document.getElementById('serviceCount').textContent = data.services_count || '-';
#                     document.getElementById('totalAlerts').textContent = data.summary.total_alerts || '0';
#                     document.getElementById('criticalCount').textContent =
#                         (data.summary.by_severity && data.summary.by_severity.CRITICAL) || '0';
#                     document.getElementById('highCount').textContent =
#                         (data.summary.by_severity && data.summary.by_severity.HIGH) || '0';
#                     document.getElementById('mediumCount').textContent =
#                         (data.summary.by_severity && data.summary.by_severity.MEDIUM) || '0';
#
#                     // If scan complete, show full details
#                     if (data.scan_complete) {
#                         loadFullDetails();
#                     }
#                 });
#         }
#
#         function loadFullDetails() {
#             fetch('/api/alerts')
#                 .then(response => response.json())
#                 .then(data => {
#                     const alertsList = document.getElementById('alertsList');
#                     const alertsSection = document.getElementById('alertsSection');
#                     const severitySection = document.getElementById('severitySection');
#
#                     // Show severity breakdown
#                     severitySection.classList.remove('hidden');
#                     updateSeverityBars(data.summary);
#
#                     // Update alert count
#                     document.getElementById('alertCount').textContent = data.alerts.length;
#
#                     if (data.alerts.length === 0) {
#                         alertsList.innerHTML = '<div class="no-alerts">✅ No security threats detected! Your system appears clean.</div>';
#                     } else {
#                         // Sort alerts by severity
#                         const severityOrder = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3};
#                         data.alerts.sort((a, b) => severityOrder[a.severity] - severityOrder[b.severity]);
#
#                         alertsList.innerHTML = data.alerts.map((alert, idx) => {
#                             let details = '';
#
#                             // Build detailed information
#                             if (alert.timestamp) {
#                                 details += `<div><span class="detail-label">Timestamp:</span><span class="detail-value">${alert.timestamp}</span></div>`;
#                             }
#                             if (alert.process_name) {
#                                 details += `<div><span class="detail-label">Process Name:</span><span class="detail-value">${alert.process_name}</span></div>`;
#                             }
#                             if (alert.pid) {
#                                 details += `<div><span class="detail-label">Process ID (PID):</span><span class="detail-value">${alert.pid}</span></div>`;
#                             }
#                             if (alert.path) {
#                                 details += `<div><span class="detail-label">File Path:</span><span class="detail-value">${alert.path}</span></div>`;
#                             }
#                             if (alert.parent_name) {
#                                 details += `<div><span class="detail-label">Parent Process:</span><span class="detail-value">${alert.parent_name} (PID: ${alert.parent_pid || 'N/A'})</span></div>`;
#                             }
#                             if (alert.child_name) {
#                                 details += `<div><span class="detail-label">Child Process:</span><span class="detail-value">${alert.child_name} (PID: ${alert.child_pid || 'N/A'})</span></div>`;
#                             }
#                             if (alert.child_path) {
#                                 details += `<div><span class="detail-label">Child Path:</span><span class="detail-value">${alert.child_path}</span></div>`;
#                             }
#                             if (alert.service_name) {
#                                 details += `<div><span class="detail-label">Service Name:</span><span class="detail-value">${alert.service_name}</span></div>`;
#                             }
#                             if (alert.display_name) {
#                                 details += `<div><span class="detail-label">Display Name:</span><span class="detail-value">${alert.display_name}</span></div>`;
#                             }
#                             if (alert.state) {
#                                 details += `<div><span class="detail-label">Service State:</span><span class="detail-value">${alert.state}</span></div>`;
#                             }
#                             if (alert.startup_type) {
#                                 details += `<div><span class="detail-label">Startup Type:</span><span class="detail-value">${alert.startup_type}</span></div>`;
#                             }
#
#                             return `
#                                 <div class="alert-item alert-${alert.severity.toLowerCase()}">
#                                     <div class="alert-header">
#                                         <div class="alert-title">Alert #${idx + 1}: ${alert.type}</div>
#                                         <div class="alert-badge badge-${alert.severity.toLowerCase()}">${alert.severity}</div>
#                                     </div>
#                                     <div class="alert-description">${alert.description}</div>
#                                     <div class="alert-details">
#                                         ${details}
#                                     </div>
#                                 </div>
#                             `;
#                         }).join('');
#                     }
#
#                     alertsSection.classList.remove('hidden');
#                 });
#         }
#
#         function updateSeverityBars(summary) {
#             const total = summary.total_alerts || 1;
#             const critical = summary.by_severity?.CRITICAL || 0;
#             const high = summary.by_severity?.HIGH || 0;
#             const medium = summary.by_severity?.MEDIUM || 0;
#             const low = summary.by_severity?.LOW || 0;
#
#             const criticalPct = (critical / total * 100).toFixed(1);
#             const highPct = (high / total * 100).toFixed(1);
#             const mediumPct = (medium / total * 100).toFixed(1);
#             const lowPct = (low / total * 100).toFixed(1);
#
#             document.getElementById('barCritical').style.width = criticalPct + '%';
#             document.getElementById('barCritical').textContent = criticalPct + '%';
#             document.getElementById('criticalCountText').textContent = critical + ' alerts';
#
#             document.getElementById('barHigh').style.width = highPct + '%';
#             document.getElementById('barHigh').textContent = highPct + '%';
#             document.getElementById('highCountText').textContent = high + ' alerts';
#
#             document.getElementById('barMedium').style.width = mediumPct + '%';
#             document.getElementById('barMedium').textContent = mediumPct + '%';
#             document.getElementById('mediumCountText').textContent = medium + ' alerts';
#
#             document.getElementById('barLow').style.width = lowPct + '%';
#             document.getElementById('barLow').textContent = lowPct + '%';
#             document.getElementById('lowCountText').textContent = low + ' alerts';
#         }
#
#         // Update every 1 second
#         setInterval(updateDashboard, 1000);
#         updateDashboard();
#     </script>
# </body>
# </html>
#         '''
#
#
# def run_web_dashboard():
#     """Main function to run the web dashboard"""
#     dashboard = WebDashboard()
#     dashboard.run_server(port=5000)
#
#
# if __name__ == "__main__":
#     run_web_dashboard()

#
# """
# web_interface.py
# Enhanced Web Dashboard with Process Tree & Warning Banner
# Complete working version - Just copy and save!
# """
#
# from flask import Flask, render_template_string, jsonify, send_file
# import threading
# import webbrowser
# import time
# from datetime import datetime
#
# from core_mon import get_all_processes, build_process_tree
# from service_mon import enumerate_services
# from detect_rules import run_all_detections
# from alert_sys import AlertManager
# from report_gen import ReportGenerator
# from threat_intel import ThreatIntelligence
#
# class WebDashboard:
#     def __init__(self):
#         self.app = Flask(__name__)
#         self.scan_complete = False
#         self.scan_progress = 0
#         self.current_step = "Initializing..."
#         self.alert_manager = None
#         self.processes_count = 0
#         self.services_count = 0
#         self.processes_data = []
#         self.services_data = []
#         self.process_tree = {}
#         self.pid_to_process = {}
#         self.setup_routes()
#
#     def setup_routes(self):
#         @self.app.route('/')
#         def dashboard():
#             return render_template_string(HTML_TEMPLATE)
#
#         @self.app.route('/api/status')
#         def get_status():
#             if self.alert_manager:
#                 summary = self.alert_manager.get_summary()
#             else:
#                 summary = {'total_alerts': 0, 'by_severity': {}}
#             return jsonify({
#                 'scan_complete': self.scan_complete,
#                 'progress': self.scan_progress,
#                 'current_step': self.current_step,
#                 'processes_count': self.processes_count,
#                 'services_count': self.services_count,
#                 'summary': summary
#             })
#
#         @self.app.route('/api/alerts')
#         def get_alerts():
#             if self.alert_manager:
#                 return jsonify({
#                     'alerts': self.alert_manager.alerts,
#                     'summary': self.alert_manager.get_summary()
#                 })
#             return jsonify({'alerts': [], 'summary': {}})
#
#         @self.app.route('/api/process-tree')
#         def get_process_tree():
#             if self.scan_complete:
#                 tree_data = []
#                 for parent_pid, children in self.process_tree.items():
#                     parent_info = self.pid_to_process.get(parent_pid, {
#                         'pid': parent_pid, 'name': 'Unknown', 'path': 'N/A'
#                     })
#                     tree_data.append({
#                         'parent': {
#                             'pid': parent_info.get('pid', parent_pid),
#                             'name': parent_info.get('name', 'Unknown'),
#                             'path': parent_info.get('path', 'N/A'),
#                             'user': parent_info.get('user', 'N/A')
#                         },
#                         'children': [{'pid': c.get('pid'), 'name': c.get('name'),
#                                       'path': c.get('path', 'N/A'), 'user': c.get('user', 'N/A')}
#                                      for c in children],
#                         'child_count': len(children)
#                     })
#                 tree_data.sort(key=lambda x: x['child_count'], reverse=True)
#                 return jsonify({'tree': tree_data[:50], 'total_parents': len(self.process_tree)})
#             return jsonify({'tree': [], 'total_parents': 0})
#
#         @self.app.route('/download/pdf')
#         def download_pdf():
#             if self.alert_manager:
#                 report_gen = ReportGenerator(self.alert_manager)
#                 html_file = report_gen.generate_html_report()
#                 return send_file(html_file, as_attachment=True,
#                                  download_name=f'security_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
#             return "No data available", 404
#
#         @self.app.route('/download/json')
#         def download_json():
#             if self.alert_manager:
#                 filename = 'security_alerts.json'
#                 self.alert_manager.export_json(filename)
#                 return send_file(filename, as_attachment=True)
#             return "No data available", 404
#
#     def run_scan_async(self):
#         try:
#             self.current_step = "🔍 Scanning processes..."
#             self.scan_progress = 20
#             processes = get_all_processes()
#             self.processes_count = len(processes)
#             self.processes_data = processes
#             time.sleep(0.5)
#
#             self.current_step = "🌳 Building process tree..."
#             self.scan_progress = 40
#             process_tree, pid_to_process = build_process_tree(processes)
#             self.process_tree = process_tree
#             self.pid_to_process = pid_to_process
#             time.sleep(0.5)
#
#             self.current_step = "⚙️ Scanning services..."
#             self.scan_progress = 60
#             services = enumerate_services()
#             self.services_count = len(services)
#             self.services_data = services
#             time.sleep(0.5)
#
#             self.current_step = "🔍 Running security detections..."
#             self.scan_progress = 80
#             self.alert_manager = AlertManager()
#             all_alerts = run_all_detections(processes, process_tree, pid_to_process, services)
#
#             for alert_type, alerts_list in all_alerts.items():
#                 for alert in alerts_list:
#                     self.alert_manager.add_alert(alert)
#             time.sleep(0.5)
#
#             self.current_step = "✅ Scan complete!"
#             self.scan_progress = 100
#             self.scan_complete = True
#         except Exception as e:
#             self.current_step = f"❌ Error: {str(e)}"
#             self.scan_complete = True
#
#     def start_scan(self):
#         threading.Thread(target=self.run_scan_async, daemon=True).start()
#
#     def run_server(self, port=5000):
#         self.start_scan()
#
#         def open_browser():
#             time.sleep(1.5)
#             webbrowser.open(f'http://127.0.0.1:{port}')
#
#         threading.Thread(target=open_browser, daemon=True).start()
#
#         print(f"\n🌐 Starting web dashboard on http://127.0.0.1:{port}")
#         print("🚀 Opening browser automatically...")
#         print("⌨️  Press Ctrl+C to stop\n")
#         self.app.run(port=port, debug=False, use_reloader=False)
#
#
# HTML_TEMPLATE = open('web_template.html', 'r').read() if False else '''
# <!DOCTYPE html>
# <html><head><meta charset="UTF-8"><title>Security Dashboard</title>
# <style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Segoe UI',sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;padding:20px}.container{max-width:1400px;margin:0 auto}.header{background:#fff;padding:30px;border-radius:15px;box-shadow:0 10px 40px rgba(0,0,0,.2);margin-bottom:20px;text-align:center}.header h1{color:#1e3c72;font-size:2.5em;margin-bottom:10px}.header p{color:#666;font-size:1.1em}.warning-banner{background:linear-gradient(135deg,#f44 0%,#c00 100%);color:#fff;padding:20px;border-radius:15px;box-shadow:0 10px 40px rgba(0,0,0,.2);margin-bottom:20px;display:none;animation:pulse 2s infinite}.warning-banner.show{display:block}@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.02)}}.warning-banner h2{font-size:1.5em;margin-bottom:10px}.progress-section{background:#fff;padding:30px;border-radius:15px;box-shadow:0 10px 40px rgba(0,0,0,.2);margin-bottom:20px}.progress-bar{background:#f0f0f0;border-radius:25px;height:40px;overflow:hidden;margin:20px 0}.progress-fill{background:linear-gradient(90deg,#667eea 0%,#764ba2 100%);height:100%;transition:width .3s ease;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700}.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px;margin:20px 0}.stat-card{background:#fff;padding:25px;border-radius:15px;box-shadow:0 5px 20px rgba(0,0,0,.1);text-align:center}.stat-card h2{font-size:3em;margin-bottom:10px}.stat-card p{color:#666}.critical{color:#f44}.high{color:#fa0}.medium{color:#44f}.info{color:#1e3c72}.process-tree-section,.alerts-section,.severity-breakdown{background:#fff;padding:30px;border-radius:15px;box-shadow:0 10px 40px rgba(0,0,0,.2);margin-bottom:20px}.tree-item{border:2px solid #e0e0e0;border-radius:10px;padding:15px;margin:15px 0;background:#f8f9fa}.tree-parent{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:#fff;padding:15px;border-radius:8px;margin-bottom:10px;font-weight:700}.tree-parent-info{display:flex;justify-content:space-between;align-items:center}.tree-children{margin-left:30px;margin-top:10px}.tree-child{background:#fff;border-left:3px solid #667eea;padding:10px;margin:8px 0;border-radius:5px;font-size:.9em}.child-badge{background:#667eea;color:#fff;padding:3px 10px;border-radius:15px;font-size:.8em}.alert-item{background:#f8f9fa;border-left:5px solid;padding:20px;margin:15px 0;border-radius:5px}.alert-critical{border-color:#f44;background:#fff5f5}.alert-high{border-color:#fa0;background:#fffbf0}.alert-medium{border-color:#44f;background:#f5f5ff}.alert-header{display:flex;justify-content:space-between;margin-bottom:15px;align-items:center}.alert-title{font-weight:700;font-size:1.2em}.alert-badge{padding:5px 15px;border-radius:20px;color:#fff;font-weight:700;font-size:.9em}.badge-critical{background:#f44}.badge-high{background:#fa0}.badge-medium{background:#44f}.alert-description{color:#555;line-height:1.6;margin-bottom:15px}.alert-details{background:rgba(0,0,0,.03);padding:15px;border-radius:8px;font-family:'Courier New',monospace;font-size:.9em}.alert-details div{margin:8px 0;display:flex}.detail-label{font-weight:700;color:#1e3c72;min-width:150px}.detail-value{color:#333;word-break:break-all}.download-buttons{display:flex;gap:15px;justify-content:center;margin-top:30px;flex-wrap:wrap}.btn{padding:15px 40px;border:0;border-radius:25px;font-size:1.1em;font-weight:700;cursor:pointer;transition:transform .2s;text-decoration:none;display:inline-block}.btn:hover{transform:scale(1.05)}.btn-primary{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:#fff}.btn-success{background:linear-gradient(135deg,#56ab2f 0%,#a8e063 100%);color:#fff}.hidden{display:none}.section-title{color:#1e3c72;border-bottom:3px solid #667eea;padding-bottom:10px;margin-bottom:20px;font-size:1.5em}.no-alerts{background:linear-gradient(135deg,#56ab2f 0%,#a8e063 100%);color:#fff;padding:40px;border-radius:15px;text-align:center;font-size:1.3em;margin:20px 0}.severity-bar-container{margin:20px 0}.severity-label{display:flex;justify-content:space-between;margin-bottom:8px;font-weight:700}.bar-bg{background:#f0f0f0;border-radius:10px;overflow:hidden;height:30px}.bar-fill-critical,.bar-fill-high,.bar-fill-medium,.bar-fill-low{height:100%;display:flex;align-items:center;padding-left:15px;color:#fff;font-weight:700;transition:width .5s ease}.bar-fill-critical{background:linear-gradient(90deg,#f44 0%,#c00 100%)}.bar-fill-high{background:linear-gradient(90deg,#fa0 0%,#f80 100%)}.bar-fill-medium{background:linear-gradient(90deg,#44f 0%,#00c 100%)}.bar-fill-low{background:linear-gradient(90deg,#4f4 0%,#0c0 100%)}</style>
# </head><body><div class="container">
# <div class="header"><h1>🔒 Security Monitoring Dashboard</h1><p id="timestamp">Loading...</p></div>
# <div class="warning-banner" id="warningBanner"><h2>⚠️ SECURITY THREATS DETECTED!</h2><p id="warningMessage">Critical security issues found.</p></div>
# <div class="progress-section"><h2 class="section-title">Scan Progress</h2><div class="progress-bar"><div class="progress-fill" id="progressBar">0%</div></div><p id="currentStep" style="text-align:center;font-size:1.2em;color:#666">Initializing...</p></div>
# <div class="stats-grid">
# <div class="stat-card"><h2 class="info" id="processCount">-</h2><p>Processes Scanned</p></div>
# <div class="stat-card"><h2 class="info" id="serviceCount">-</h2><p>Services Scanned</p></div>
# <div class="stat-card"><h2 class="info" id="totalAlerts">-</h2><p>Total Alerts</p></div>
# <div class="stat-card"><h2 class="critical" id="criticalCount">-</h2><p>Critical</p></div>
# <div class="stat-card"><h2 class="high" id="highCount">-</h2><p>High</p></div>
# <div class="stat-card"><h2 class="medium" id="mediumCount">-</h2><p>Medium</p></div>
# </div>
# <div class="process-tree-section hidden" id="processTreeSection">
# <h2 class="section-title">🌳 Parent-Child Process Relationships (Top 20)</h2>
# <p style="color:#666;margin-bottom:20px">Showing processes and their child processes. Suspicious relationships are flagged in alerts.</p>
# <div id="processTreeList"></div></div>
# <div class="severity-breakdown hidden" id="severitySection"><h2 class="section-title">📈 Severity Breakdown</h2>
# <div class="severity-bar-container"><div class="severity-label"><span>CRITICAL</span><span id="criticalCountText">0 alerts</span></div><div class="bar-bg"><div class="bar-fill-critical" id="barCritical" style="width:0%">0%</div></div></div>
# <div class="severity-bar-container"><div class="severity-label"><span>HIGH</span><span id="highCountText">0 alerts</span></div><div class="bar-bg"><div class="bar-fill-high" id="barHigh" style="width:0%">0%</div></div></div>
# <div class="severity-bar-container"><div class="severity-label"><span>MEDIUM</span><span id="mediumCountText">0 alerts</span></div><div class="bar-bg"><div class="bar-fill-medium" id="barMedium" style="width:0%">0%</div></div></div>
# <div class="severity-bar-container"><div class="severity-label"><span>LOW</span><span id="lowCountText">0 alerts</span></div><div class="bar-bg"><div class="bar-fill-low" id="barLow" style="width:0%">0%</div></div></div>
# </div>
# <div class="alerts-section hidden" id="alertsSection"><h2 class="section-title">🔍 Detailed Security Alerts (<span id="alertCount">0</span>)</h2><div id="alertsList"></div>
# <div class="download-buttons"><a href="/download/pdf" class="btn btn-primary">📄 Download Full Report (HTML)</a><a href="/download/json" class="btn btn-success">📊 Download Data (JSON)</a></div></div>
# </div>
# <script>document.getElementById('timestamp').textContent='Started: '+new Date().toLocaleString();function updateDashboard(){fetch('/api/status').then(r=>r.json()).then(d=>{document.getElementById('progressBar').style.width=d.progress+'%';document.getElementById('progressBar').textContent=d.progress+'%';document.getElementById('currentStep').textContent=d.current_step;document.getElementById('processCount').textContent=d.processes_count||'-';document.getElementById('serviceCount').textContent=d.services_count||'-';document.getElementById('totalAlerts').textContent=d.summary.total_alerts||'0';const c=(d.summary.by_severity&&d.summary.by_severity.CRITICAL)||0;const h=(d.summary.by_severity&&d.summary.by_severity.HIGH)||0;document.getElementById('criticalCount').textContent=c;document.getElementById('highCount').textContent=h;document.getElementById('mediumCount').textContent=(d.summary.by_severity&&d.summary.by_severity.MEDIUM)||'0';if(d.scan_complete&&(c>0||h>0)){const m=c>0?`⚠️ ${c} CRITICAL threat(s) detected! Immediate action required.`:`⚠️ ${h} HIGH priority alert(s) detected. Please review immediately.`;document.getElementById('warningMessage').textContent=m;document.getElementById('warningBanner').classList.add('show')}if(d.scan_complete){loadFullDetails();loadProcessTree()}})}function loadProcessTree(){fetch('/api/process-tree').then(r=>r.json()).then(d=>{const l=document.getElementById('processTreeList');const s=document.getElementById('processTreeSection');if(d.tree&&d.tree.length>0){l.innerHTML=d.tree.slice(0,20).map(i=>`<div class="tree-item"><div class="tree-parent"><div class="tree-parent-info"><span><strong>Parent:</strong> ${i.parent.name} (PID: ${i.parent.pid})</span><span class="child-badge">${i.child_count} children</span></div><div style="font-size:0.85em;margin-top:5px;opacity:0.9">Path: ${i.parent.path||'N/A'}</div></div><div class="tree-children">${i.children.slice(0,10).map(c=>`<div class="tree-child"><strong>→ ${c.name}</strong> (PID: ${c.pid})<br><span style="color:#666;font-size:0.85em">Path: ${c.path||'N/A'}</span></div>`).join('')}${i.child_count>10?`<div class="tree-child" style="text-align:center;color:#667eea">... and ${i.child_count-10} more children</div>`:''}</div></div>`).join('');s.classList.remove('hidden')}})}function loadFullDetails(){fetch('/api/alerts').then(r=>r.json()).then(d=>{document.getElementById('severitySection').classList.remove('hidden');updateSeverityBars(d.summary);document.getElementById('alertCount').textContent=d.alerts.length;const l=document.getElementById('alertsList');if(d.alerts.length===0){l.innerHTML='<div class="no-alerts">✅ No security threats detected! Your system appears clean.</div>'}else{const o={'CRITICAL':0,'HIGH':1,'MEDIUM':2,'LOW':3};d.alerts.sort((a,b)=>o[a.severity]-o[b.severity]);l.innerHTML=d.alerts.map((a,i)=>{let dt='';if(a.timestamp)dt+=`<div><span class="detail-label">Timestamp:</span><span class="detail-value">${a.timestamp}</span></div>`;if(a.process_name)dt+=`<div><span class="detail-label">Process Name:</span><span class="detail-value">${a.process_name}</span></div>`;if(a.pid)dt+=`<div><span class="detail-label">Process ID (PID):</span><span class="detail-value">${a.pid}</span></div>`;if(a.path)dt+=`<div><span class="detail-label">File Path:</span><span class="detail-value">${a.path}</span></div>`;if(a.parent_name)dt+=`<div><span class="detail-label">Parent Process:</span><span class="detail-value">${a.parent_name} (PID: ${a.parent_pid||'N/A'})</span></div>`;if(a.child_name)dt+=`<div><span class="detail-label">Child Process:</span><span class="detail-value">${a.child_name} (PID: ${a.child_pid||'N/A'})</span></div>`;if(a.child_path)dt+=`<div><span class="detail-label">Child Path:</span><span class="detail-value">${a.child_path}</span></div>`;if(a.service_name)dt+=`<div><span class="detail-label">Service Name:</span><span class="detail-value">${a.service_name}</span></div>`;if(a.display_name)dt+=`<div><span class="detail-label">Display Name:</span><span class="detail-value">${a.display_name}</span></div>`;if(a.state)dt+=`<div><span class="detail-label">Service State:</span><span class="detail-value">${a.state}</span></div>`;if(a.startup_type)dt+=`<div><span class="detail-label">Startup Type:</span><span class="detail-value">${a.startup_type}</span></div>`;return`<div class="alert-item alert-${a.severity.toLowerCase()}"><div class="alert-header"><div class="alert-title">Alert #${i+1}: ${a.type}</div><div class="alert-badge badge-${a.severity.toLowerCase()}">${a.severity}</div></div><div class="alert-description">${a.description}</div><div class="alert-details">${dt}</div></div>`}).join('')}document.getElementById('alertsSection').classList.remove('hidden')})}function updateSeverityBars(s){const t=s.total_alerts||1;const c=s.by_severity?.CRITICAL||0;const h=s.by_severity?.HIGH||0;const m=s.by_severity?.MEDIUM||0;const l=s.by_severity?.LOW||0;const cp=(c/t*100).toFixed(1);const hp=(h/t*100).toFixed(1);const mp=(m/t*100).toFixed(1);const lp=(l/t*100).toFixed(1);document.getElementById('barCritical').style.width=cp+'%';document.getElementById('barCritical').textContent=cp+'%';document.getElementById('criticalCountText').textContent=c+' alerts';document.getElementById('barHigh').style.width=hp+'%';document.getElementById('barHigh').textContent=hp+'%';document.getElementById('highCountText').textContent=h+' alerts';document.getElementById('barMedium').style.width=mp+'%';document.getElementById('barMedium').textContent=mp+'%';document.getElementById('mediumCountText').textContent=m+' alerts';document.getElementById('barLow').style.width=lp+'%';document.getElementById('barLow').textContent=lp+'%';document.getElementById('lowCountText').textContent=l+' alerts'}setInterval(updateDashboard,1000);updateDashboard()</script>
# </body></html>
# '''
#
#
# def run_web_dashboard():
#     dashboard = WebDashboard()
#     dashboard.run_server(port=5000)
#
#
# if __name__ == "__main__":
#     run_web_dashboard()


# """
# web_interface.py - PART 1 (Python Code)
# Copy this entire file, then add PART 2 (HTML) at the bottom
# """
#
# from flask import Flask, render_template_string, jsonify, send_file, request
# import threading
# import webbrowser
# import time
# from datetime import datetime
#
# from core_mon import get_all_processes, build_process_tree
# from service_mon import enumerate_services
# from detect_rules import run_all_detections
# from alert_sys import AlertManager
# from report_gen import ReportGenerator
# from process_manager_advanced import ProcessManager
# from threat_intel import ThreatIntelligence
#
#
# class WebDashboard:
#     def __init__(self):
#         self.app = Flask(__name__)
#         self.scan_complete = False
#         self.scan_progress = 0
#         self.current_step = "Initializing..."
#         self.alert_manager = None
#         self.process_manager = ProcessManager()
#         self.threat_intel = ThreatIntelligence()
#         self.processes_count = 0
#         self.services_count = 0
#         self.processes_data = []
#         self.services_data = []
#         self.process_tree = {}
#         self.pid_to_process = {}
#         self.setup_routes()
#
#     def setup_routes(self):
#         @self.app.route('/')
#         def dashboard():
#             return render_template_string(DASHBOARD_HTML)
#
#         @self.app.route('/api/status')
#         def get_status():
#             summary = self.alert_manager.get_summary() if self.alert_manager else {'total_alerts': 0, 'by_severity': {}}
#             return jsonify({
#                 'scan_complete': self.scan_complete,
#                 'progress': self.scan_progress,
#                 'current_step': self.current_step,
#                 'processes_count': self.processes_count,
#                 'services_count': self.services_count,
#                 'summary': summary
#             })
#
#         @self.app.route('/api/alerts')
#         def get_alerts():
#             if self.alert_manager:
#                 return jsonify({'alerts': self.alert_manager.alerts, 'summary': self.alert_manager.get_summary()})
#             return jsonify({'alerts': [], 'summary': {}})
#
#         @self.app.route('/api/process-tree')
#         def get_process_tree():
#             if self.scan_complete:
#                 tree_data = []
#                 for parent_pid, children in self.process_tree.items():
#                     parent_info = self.pid_to_process.get(parent_pid,
#                                                           {'pid': parent_pid, 'name': 'Unknown', 'path': 'N/A'})
#                     tree_data.append({
#                         'parent': {'pid': parent_info.get('pid'), 'name': parent_info.get('name'),
#                                    'path': parent_info.get('path'), 'user': parent_info.get('user', 'N/A')},
#                         'children': [{'pid': c.get('pid'), 'name': c.get('name'), 'path': c.get('path'),
#                                       'user': c.get('user', 'N/A')} for c in children],
#                         'child_count': len(children)
#                     })
#                 tree_data.sort(key=lambda x: x['child_count'], reverse=True)
#                 return jsonify({'tree': tree_data[:50], 'total_parents': len(self.process_tree)})
#             return jsonify({'tree': [], 'total_parents': 0})
#
#         @self.app.route('/api/process-details/<int:pid>')
#         def get_process_details(pid):
#             details = self.process_manager.get_process_details(pid)
#             if 'error' not in details:
#                 details['threat_assessment'] = self.threat_intel.assess_threat(details)
#             return jsonify(details)
#
#         @self.app.route('/api/terminate-process/<int:pid>', methods=['POST'])
#         def terminate_process(pid):
#             force = request.json.get('force', False) if request.json else False
#             result = self.process_manager.terminate_process(pid, force)
#             return jsonify(result)
#
#         @self.app.route('/api/whitelist-process', methods=['POST'])
#         def whitelist_process():
#             data = request.json
#             process_name = data.get('process_name')
#             if process_name:
#                 self.process_manager.add_to_whitelist(process_name)
#                 return jsonify({'success': True, 'message': f'{process_name} added to whitelist'})
#             return jsonify({'success': False, 'message': 'No process name provided'})
#
#         @self.app.route('/download/pdf')
#         def download_pdf():
#             if self.alert_manager:
#                 report_gen = ReportGenerator(self.alert_manager)
#                 html_file = report_gen.generate_html_report()
#                 return send_file(html_file, as_attachment=True,
#                                  download_name=f'security_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
#             return "No data available", 404
#
#         @self.app.route('/download/json')
#         def download_json():
#             if self.alert_manager:
#                 filename = 'security_alerts.json'
#                 self.alert_manager.export_json(filename)
#                 return send_file(filename, as_attachment=True)
#             return "No data available", 404
#
#     def run_scan_async(self):
#         try:
#             self.current_step = "🔍 Scanning processes..."
#             self.scan_progress = 20
#             processes = get_all_processes()
#             self.processes_count = len(processes)
#             self.processes_data = processes
#             time.sleep(0.5)
#
#             self.current_step = "🌳 Building process tree..."
#             self.scan_progress = 40
#             process_tree, pid_to_process = build_process_tree(processes)
#             self.process_tree = process_tree
#             self.pid_to_process = pid_to_process
#             time.sleep(0.5)
#
#             self.current_step = "⚙️ Scanning services..."
#             self.scan_progress = 60
#             services = enumerate_services()
#             self.services_count = len(services)
#             self.services_data = services
#             time.sleep(0.5)
#
#             self.current_step = "🔍 Running security detections..."
#             self.scan_progress = 80
#             self.alert_manager = AlertManager()
#             all_alerts = run_all_detections(processes, process_tree, pid_to_process, services)
#
#             for alert_type, alerts_list in all_alerts.items():
#                 for alert in alerts_list:
#                     self.alert_manager.add_alert(alert)
#             time.sleep(0.5)
#
#             self.current_step = "✅ Scan complete!"
#             self.scan_progress = 100
#             self.scan_complete = True
#         except Exception as e:
#             self.current_step = f"❌ Error: {str(e)}"
#             self.scan_complete = True
#
#     def start_scan(self):
#         threading.Thread(target=self.run_scan_async, daemon=True).start()
#
#     def run_server(self, port=5000):
#         self.start_scan()
#
#         def open_browser():
#             time.sleep(1.5)
#             webbrowser.open(f'http://127.0.0.1:{port}')
#
#         threading.Thread(target=open_browser, daemon=True).start()
#
#         print(f"\n🌐 Web dashboard: http://127.0.0.1:{port}")
#         print("🚀 Browser opening...")
#         print("⌨️  Press Ctrl+C to stop\n")
#         self.app.run(port=port, debug=False, use_reloader=False)
#
#
# def run_web_dashboard():
#     dashboard = WebDashboard()
#     dashboard.run_server(port=5000)
#
#
# if __name__ == "__main__":
#     run_web_dashboard()
#
#
#
#
#
# DASHBOARD_HTML = '''<!DOCTYPE html>
# <html><head><meta charset="UTF-8"><title>Security Monitor Pro</title>
# <style>
# *{margin:0;padding:0;box-sizing:border-box}
# body{font-family:'Segoe UI',sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);min-height:100vh;padding:20px}
# .container{max-width:1600px;margin:0 auto}
# .header{background:#fff;padding:30px;border-radius:15px;box-shadow:0 10px 40px rgba(0,0,0,.2);margin-bottom:20px;text-align:center}
# .header h1{color:#1e3c72;font-size:2.5em;margin-bottom:10px}
# .warning-banner{background:linear-gradient(135deg,#f44,#c00);color:#fff;padding:20px;border-radius:15px;margin-bottom:20px;display:none;animation:pulse 2s infinite}
# .warning-banner.show{display:block}
# @keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.02)}}
# .progress-section{background:#fff;padding:30px;border-radius:15px;box-shadow:0 10px 40px rgba(0,0,0,.2);margin-bottom:20px}
# .progress-bar{background:#f0f0f0;border-radius:25px;height:40px;overflow:hidden;margin:20px 0}
# .progress-fill{background:linear-gradient(90deg,#667eea,#764ba2);height:100%;transition:width .3s;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700}
# .stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px;margin:20px 0}
# .stat-card{background:#fff;padding:25px;border-radius:15px;box-shadow:0 5px 20px rgba(0,0,0,.1);text-align:center;transition:transform .2s}
# .stat-card:hover{transform:translateY(-5px)}
# .stat-card h2{font-size:3em;margin-bottom:10px}
# .critical{color:#f44}.high{color:#fa0}.medium{color:#44f}.info{color:#1e3c72}
# .process-tree-section,.alerts-section,.severity-breakdown{background:#fff;padding:30px;border-radius:15px;box-shadow:0 10px 40px rgba(0,0,0,.2);margin-bottom:20px}
# .tree-item{border:2px solid #e0e0e0;border-radius:10px;padding:15px;margin:15px 0;background:#f8f9fa;transition:all .3s}
# .tree-item:hover{border-color:#667eea;box-shadow:0 5px 15px rgba(102,126,234,.3)}
# .tree-parent{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:15px;border-radius:8px;margin-bottom:10px;font-weight:700}
# .tree-children{margin-left:30px;margin-top:10px}
# .tree-child{background:#fff;border-left:3px solid #667eea;padding:10px;margin:8px 0;border-radius:5px;cursor:pointer;transition:all .2s}
# .tree-child:hover{background:#f0f4ff;border-left-width:5px}
# .alert-item{background:#f8f9fa;border-left:5px solid;padding:20px;margin:15px 0;border-radius:5px}
# .alert-critical{border-color:#f44;background:#fff5f5}
# .alert-high{border-color:#fa0;background:#fffbf0}
# .alert-medium{border-color:#44f;background:#f5f5ff}
# .alert-header{display:flex;justify-content:space-between;margin-bottom:15px}
# .alert-badge{padding:5px 15px;border-radius:20px;color:#fff;font-weight:700}
# .badge-critical{background:#f44}.badge-high{background:#fa0}.badge-medium{background:#44f}
# .alert-details{background:rgba(0,0,0,.03);padding:15px;border-radius:8px;font-family:'Courier New',monospace;font-size:.9em}
# .alert-details div{margin:8px 0;display:flex}
# .detail-label{font-weight:700;color:#1e3c72;min-width:150px}
# .btn{padding:15px 40px;border:0;border-radius:25px;font-size:1.1em;font-weight:700;cursor:pointer;transition:all .2s;text-decoration:none;display:inline-block}
# .btn:hover{transform:scale(1.05)}
# .btn-primary{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff}
# .btn-success{background:linear-gradient(135deg,#56ab2f,#a8e063);color:#fff}
# .btn-danger{background:linear-gradient(135deg,#f44,#c00);color:#fff}
# .btn-small{padding:8px 20px;font-size:.9em}
# .hidden{display:none}
# .modal{display:none;position:fixed;z-index:1000;left:0;top:0;width:100%;height:100%;background:rgba(0,0,0,.7)}
# .modal.show{display:flex;align-items:center;justify-content:center}
# .modal-content{background:#fff;padding:30px;border-radius:15px;max-width:600px;width:90%;max-height:80vh;overflow-y:auto}
# .modal-header{display:flex;justify-content:space-between;margin-bottom:20px}
# .close-modal{background:none;border:0;font-size:2em;cursor:pointer;color:#666}
# .risk-score{font-size:3em;font-weight:700;margin:20px 0}
# .risk-low{color:#4f4}.risk-medium{color:#fa0}.risk-high{color:#f44}
# .help-btn{position:fixed;bottom:30px;right:30px;width:60px;height:60px;border-radius:50%;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;border:0;font-size:1.5em;cursor:pointer;box-shadow:0 5px 20px rgba(0,0,0,.3);z-index:999}
# </style></head><body><div class="container">
# <div class="header"><h1>🔒 Security Monitor Pro</h1><p id="timestamp">Loading...</p></div>
# <div class="warning-banner" id="warningBanner"><h2>⚠️ SECURITY THREATS!</h2><p id="warningMessage">Critical issues found.</p></div>
# <div class="progress-section"><h2 style="color:#1e3c72;border-bottom:3px solid #667eea;padding-bottom:10px">Scan Progress</h2>
# <div class="progress-bar"><div class="progress-fill" id="progressBar">0%</div></div>
# <p id="currentStep" style="text-align:center;font-size:1.2em;color:#666">Initializing...</p></div>
# <div class="stats-grid">
# <div class="stat-card"><h2 class="info" id="processCount">-</h2><p>Processes</p></div>
# <div class="stat-card"><h2 class="info" id="serviceCount">-</h2><p>Services</p></div>
# <div class="stat-card"><h2 class="info" id="totalAlerts">-</h2><p>Alerts</p></div>
# <div class="stat-card"><h2 class="critical" id="criticalCount">-</h2><p>Critical</p></div>
# <div class="stat-card"><h2 class="high" id="highCount">-</h2><p>High</p></div>
# <div class="stat-card"><h2 class="medium" id="mediumCount">-</h2><p>Medium</p></div>
# </div>
# <div class="process-tree-section hidden" id="processTreeSection">
# <h2 style="color:#1e3c72;border-bottom:3px solid #667eea;padding-bottom:10px">🌳 Process Tree (Top 20)</h2>
# <p style="color:#666;margin:20px 0">Click any process for details</p>
# <div id="processTreeList"></div></div>
# <div class="severity-breakdown hidden" id="severitySection">
# <h2 style="color:#1e3c72;border-bottom:3px solid #667eea;padding-bottom:10px">📈 Severity</h2>
# <div style="margin:20px 0">
# <div style="display:flex;justify-content:space-between;margin-bottom:8px;font-weight:700"><span>CRITICAL</span><span id="criticalCountText">0</span></div>
# <div style="background:#f0f0f0;border-radius:10px;height:30px"><div style="background:linear-gradient(90deg,#f44,#c00);height:100%;display:flex;align-items:center;padding-left:15px;color:#fff;font-weight:700;transition:width .5s" id="barCritical">0%</div></div></div>
# <div style="margin:20px 0">
# <div style="display:flex;justify-content:space-between;margin-bottom:8px;font-weight:700"><span>HIGH</span><span id="highCountText">0</span></div>
# <div style="background:#f0f0f0;border-radius:10px;height:30px"><div style="background:linear-gradient(90deg,#fa0,#f80);height:100%;display:flex;align-items:center;padding-left:15px;color:#fff;font-weight:700;transition:width .5s" id="barHigh">0%</div></div></div>
# <div style="margin:20px 0">
# <div style="display:flex;justify-content:space-between;margin-bottom:8px;font-weight:700"><span>MEDIUM</span><span id="mediumCountText">0</span></div>
# <div style="background:#f0f0f0;border-radius:10px;height:30px"><div style="background:linear-gradient(90deg,#44f,#00c);height:100%;display:flex;align-items:center;padding-left:15px;color:#fff;font-weight:700;transition:width .5s" id="barMedium">0%</div></div></div>
# </div>
# <div class="alerts-section hidden" id="alertsSection">
# <h2 style="color:#1e3c72;border-bottom:3px solid #667eea;padding-bottom:10px">🔍 Alerts (<span id="alertCount">0</span>)</h2>
# <div id="alertsList"></div>
# <div style="display:flex;gap:15px;justify-content:center;margin-top:30px">
# <a href="/download/pdf" class="btn btn-primary">📄 Download HTML</a>
# <a href="/download/json" class="btn btn-success">📊 Download JSON</a>
# </div></div></div>
# <button class="help-btn" onclick="showHelp()">?</button>
# <div class="modal" id="processModal">
# <div class="modal-content">
# <div class="modal-header"><h2>Process Details</h2><button class="close-modal" onclick="closeModal()">&times;</button></div>
# <div id="processDetailsContent"></div></div></div>
# <div class="modal" id="helpModal">
# <div class="modal-content">
# <div class="modal-header"><h2>📚 Help</h2><button class="close-modal" onclick="closeHelpModal()">&times;</button></div>
# <div style="line-height:1.8">
# <h3>What This Does</h3><p>Monitors Windows processes for threats</p>
# <h3>How to Use</h3><ul><li>Wait for scan</li><li>Review alerts</li><li>Click processes for details</li><li>Download reports</li></ul>
# <h3>Warning Levels</h3><p><strong style="color:#f44">CRITICAL:</strong> Act now<br><strong style="color:#fa0">HIGH:</strong> Investigate<br><strong style="color:#44f">MEDIUM:</strong> Review</p>
# </div></div></div>
# <script>
# document.getElementById('timestamp').textContent='Started: '+new Date().toLocaleString();
# function updateDashboard(){fetch('/api/status').then(r=>r.json()).then(d=>{document.getElementById('progressBar').style.width=d.progress+'%';document.getElementById('progressBar').textContent=d.progress+'%';document.getElementById('currentStep').textContent=d.current_step;document.getElementById('processCount').textContent=d.processes_count||'-';document.getElementById('serviceCount').textContent=d.services_count||'-';document.getElementById('totalAlerts').textContent=d.summary.total_alerts||'0';const c=(d.summary.by_severity&&d.summary.by_severity.CRITICAL)||0;const h=(d.summary.by_severity&&d.summary.by_severity.HIGH)||0;document.getElementById('criticalCount').textContent=c;document.getElementById('highCount').textContent=h;document.getElementById('mediumCount').textContent=(d.summary.by_severity&&d.summary.by_severity.MEDIUM)||'0';if(d.scan_complete&&(c>0||h>0)){document.getElementById('warningMessage').textContent=c>0?`${c} CRITICAL!`:`${h} HIGH alerts`;document.getElementById('warningBanner').classList.add('show')}if(d.scan_complete){loadFullDetails();loadProcessTree()}})}
# function loadProcessTree(){fetch('/api/process-tree').then(r=>r.json()).then(d=>{if(d.tree&&d.tree.length>0){document.getElementById('processTreeList').innerHTML=d.tree.slice(0,20).map(i=>`<div class="tree-item"><div class="tree-parent"><div style="display:flex;justify-content:space-between"><span>Parent: ${i.parent.name} (${i.parent.pid})</span><span style="background:#667eea;color:#fff;padding:3px 10px;border-radius:15px">${i.child_count} children</span></div><div style="font-size:0.85em;margin-top:5px;opacity:0.9">Path: ${i.parent.path||'N/A'}</div></div><div class="tree-children">${i.children.slice(0,10).map(c=>`<div class="tree-child" onclick="showProcessDetails(${c.pid})"><strong>→ ${c.name}</strong> (${c.pid})<br><span style="color:#666;font-size:0.85em">${c.path||'N/A'}</span></div>`).join('')}${i.child_count>10?`<div class="tree-child" style="text-align:center;color:#667eea">+${i.child_count-10} more</div>`:''}</div></div>`).join('');document.getElementById('processTreeSection').classList.remove('hidden')}})}
# function showProcessDetails(pid){fetch(`/api/process-details/${pid}`).then(r=>r.json()).then(d=>{if(d.error){alert(d.error);return}const risk=d.risk_score||0;const riskClass=risk>70?'risk-high':risk>40?'risk-medium':'risk-low';const content=`<div style="text-align:center"><div class="risk-score ${riskClass}">${risk}</div><p>Risk Score</p></div><div style="margin-top:20px"><strong>Process:</strong> ${d.name}<br><strong>PID:</strong> ${d.pid}<br><strong>Path:</strong> ${d.exe||'N/A'}<br><strong>CPU:</strong> ${d.cpu_percent}%<br><strong>Memory:</strong> ${d.memory_mb} MB<br><strong>Threads:</strong> ${d.num_threads}<br><strong>Connections:</strong> ${d.num_connections}</div><div style="margin-top:20px;display:flex;gap:10px"><button class="btn btn-danger btn-small" onclick="terminateProcess(${pid})">🛑 Terminate</button><button class="btn btn-success btn-small" onclick="whitelistProcess('${d.name}')">✅ Whitelist</button></div>`;document.getElementById('processDetailsContent').innerHTML=content;document.getElementById('processModal').classList.add('show')})}
# function terminateProcess(pid){if(confirm('Terminate this process?')){fetch(`/api/terminate-process/${pid}`,{method:'POST',headers:{'Content-Type':'application/json'}}).then(r=>r.json()).then(d=>{alert(d.message);closeModal();updateDashboard()})}}
# function whitelistProcess(name){fetch('/api/whitelist-process',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({process_name:name})}).then(r=>r.json()).then(d=>{alert(d.message);closeModal()})}
# function closeModal(){document.getElementById('processModal').classList.remove('show')}
# function showHelp(){document.getElementById('helpModal').classList.add('show')}
# function closeHelpModal(){document.getElementById('helpModal').classList.remove('show')}
# function loadFullDetails(){fetch('/api/alerts').then(r=>r.json()).then(d=>{document.getElementById('severitySection').classList.remove('hidden');updateSeverityBars(d.summary);document.getElementById('alertCount').textContent=d.alerts.length;const l=document.getElementById('alertsList');if(d.alerts.length===0){l.innerHTML='<div style="background:linear-gradient(135deg,#56ab2f,#a8e063);color:#fff;padding:40px;border-radius:15px;text-align:center;font-size:1.3em">✅ No threats!</div>'}else{const o={'CRITICAL':0,'HIGH':1,'MEDIUM':2};d.alerts.sort((a,b)=>o[a.severity]-o[b.severity]);l.innerHTML=d.alerts.map((a,i)=>{let dt='';if(a.timestamp)dt+=`<div><span class="detail-label">Time:</span>${a.timestamp}</div>`;if(a.process_name)dt+=`<div><span class="detail-label">Process:</span>${a.process_name}</div>`;if(a.pid)dt+=`<div><span class="detail-label">PID:</span>${a.pid}</div>`;if(a.path)dt+=`<div><span class="detail-label">Path:</span>${a.path}</div>`;if(a.parent_name)dt+=`<div><span class="detail-label">Parent:</span>${a.parent_name} (${a.parent_pid})</div>`;if(a.child_name)dt+=`<div><span class="detail-label">Child:</span>${a.child_name} (${a.child_pid})</div>`;if(a.service_name)dt+=`<div><span class="detail-label">Service:</span>${a.service_name}</div>`;return`<div class="alert-item alert-${a.severity.toLowerCase()}"><div class="alert-header"><div style="font-weight:700;font-size:1.2em">Alert #${i+1}: ${a.type}</div><div class="alert-badge badge-${a.severity.toLowerCase()}">${a.severity}</div></div><div style="color:#555;line-height:1.6;margin-bottom:15px">${a.description}</div><div class="alert-details">${dt}</div></div>`}).join('')}document.getElementById('alertsSection').classList.remove('hidden')})}
# function updateSeverityBars(s){const t=s.total_alerts||1;const c=s.by_severity?.CRITICAL||0;const h=s.by_severity?.HIGH||0;const m=s.by_severity?.MEDIUM||0;const cp=(c/t*100).toFixed(1);const hp=(h/t*100).toFixed(1);const mp=(m/t*100).toFixed(1);document.getElementById('barCritical').style.width=cp+'%';document.getElementById('barCritical').textContent=cp+'%';document.getElementById('criticalCountText').textContent=c+' alerts';document.getElementById('barHigh').style.width=hp+'%';document.getElementById('barHigh').textContent=hp+'%';document.getElementById('highCountText').textContent=h+' alerts';document.getElementById('barMedium').style.width=mp+'%';document.getElementById('barMedium').textContent=mp+'%';document.getElementById('mediumCountText').textContent=m+' alerts'}
# setInterval(updateDashboard,1000);updateDashboard();
# </script>
# </body></html>'''


from flask import Flask, render_template_string, jsonify, send_file, request
import threading
import webbrowser
import time
from datetime import datetime

from core_mon import get_all_processes, build_process_tree
from service_mon import enumerate_services
from detect_rules import run_all_detections
from alert_sys import AlertManager
from report_gen import ReportGenerator
from process_manager_advanced import ProcessManager
from threat_intel import ThreatIntelligence


class WebDashboard:
    def __init__(self):
        self.app = Flask(__name__)
        self.scan_complete = False
        self.scan_progress = 0
        self.current_step = "Initializing..."
        self.alert_manager = None
        self.process_manager = ProcessManager()
        self.threat_intel = ThreatIntelligence()
        self.processes_count = 0
        self.services_count = 0
        self.processes_data = []
        self.services_data = []
        self.process_tree = {}
        self.pid_to_process = {}
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def dashboard():
            return render_template_string(DASHBOARD_HTML)

        @self.app.route('/api/status')
        def get_status():
            summary = self.alert_manager.get_summary() if self.alert_manager else {'total_alerts': 0, 'by_severity': {}}
            return jsonify({
                'scan_complete': self.scan_complete,
                'progress': self.scan_progress,
                'current_step': self.current_step,
                'processes_count': self.processes_count,
                'services_count': self.services_count,
                'summary': summary
            })

        @self.app.route('/api/alerts')
        def get_alerts():
            if self.alert_manager:
                return jsonify({'alerts': self.alert_manager.alerts, 'summary': self.alert_manager.get_summary()})
            return jsonify({'alerts': [], 'summary': {}})

        @self.app.route('/api/process-tree')
        def get_process_tree():
            if self.scan_complete:
                tree_data = []
                for parent_pid, children in self.process_tree.items():
                    parent_info = self.pid_to_process.get(parent_pid,
                                                          {'pid': parent_pid, 'name': 'Unknown', 'path': 'N/A'})
                    tree_data.append({
                        'parent': {
                            'pid': parent_info.get('pid', parent_pid),
                            'name': parent_info.get('name', 'Unknown'),
                            'path': parent_info.get('path', 'N/A'),
                            'user': parent_info.get('user', 'N/A')
                        },
                        'children': [
                            {
                                'pid': c.get('pid'),
                                'name': c.get('name'),
                                'path': c.get('path', 'N/A'),
                                'user': c.get('user', 'N/A')
                            }
                            for c in children
                        ],
                        'child_count': len(children)
                    })
                tree_data.sort(key=lambda x: x['child_count'], reverse=True)
                return jsonify({'tree': tree_data[:50], 'total_parents': len(self.process_tree)})
            return jsonify({'tree': [], 'total_parents': 0})

        @self.app.route('/api/process-details/<int:pid>')
        def get_process_details(pid):
            details = self.process_manager.get_process_details(pid)
            if 'error' not in details:
                details['threat_assessment'] = self.threat_intel.assess_threat(details)
            return jsonify(details)

        @self.app.route('/api/terminate-process/<int:pid>', methods=['POST'])
        def terminate_process(pid):
            force = request.json.get('force', False) if request.json else False
            result = self.process_manager.terminate_process(pid, force)
            return jsonify(result)

        @self.app.route('/api/whitelist-process', methods=['POST'])
        def whitelist_process():
            data = request.json
            process_name = data.get('process_name')
            if process_name:
                self.process_manager.add_to_whitelist(process_name)
                return jsonify({'success': True, 'message': f'{process_name} added to whitelist'})
            return jsonify({'success': False, 'message': 'No process name provided'})

        @self.app.route('/download/pdf')
        def download_pdf():
            if self.alert_manager:
                report_gen = ReportGenerator(self.alert_manager)
                html_file = report_gen.generate_html_report()
                return send_file(html_file, as_attachment=True,
                                 download_name=f'security_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
            return "No data available", 404

        @self.app.route('/download/json')
        def download_json():
            if self.alert_manager:
                filename = 'security_alerts.json'
                self.alert_manager.export_json(filename)
                return send_file(filename, as_attachment=True)
            return "No data available", 404

    def run_scan_async(self):
        try:
            self.current_step = "🔍 Scanning processes..."
            self.scan_progress = 20
            processes = get_all_processes()
            self.processes_count = len(processes)
            self.processes_data = processes
            time.sleep(0.5)

            self.current_step = "🌳 Building process tree..."
            self.scan_progress = 40
            process_tree, pid_to_process = build_process_tree(processes)
            self.process_tree = process_tree
            self.pid_to_process = pid_to_process
            time.sleep(0.5)

            self.current_step = "⚙️ Scanning services..."
            self.scan_progress = 60
            services = enumerate_services()
            self.services_count = len(services)
            self.services_data = services
            time.sleep(0.5)

            self.current_step = "🔍 Running security detections..."
            self.scan_progress = 80
            self.alert_manager = AlertManager()
            all_alerts = run_all_detections(processes, process_tree, pid_to_process, services)

            for alert_type, alerts_list in all_alerts.items():
                for alert in alerts_list:
                    self.alert_manager.add_alert(alert)
            time.sleep(0.5)

            self.current_step = "✅ Scan complete!"
            self.scan_progress = 100
            self.scan_complete = True
        except Exception as e:
            self.current_step = f"❌ Error: {str(e)}"
            self.scan_complete = True

    def start_scan(self):
        threading.Thread(target=self.run_scan_async, daemon=True).start()

    def run_server(self, port=5000):
        self.start_scan()

        def open_browser():
            time.sleep(1.5)
            webbrowser.open(f'http://127.0.0.1:{port}')

        threading.Thread(target=open_browser, daemon=True).start()

        print(f"\n🌐 Web dashboard: http://127.0.0.1:{port}")
        print("🚀 Browser opening...")
        print("⌨️  Press Ctrl+C to stop\n")
        self.app.run(port=port, debug=False, use_reloader=False)


def run_web_dashboard():
    dashboard = WebDashboard()
    dashboard.run_server(port=5000)


if __name__ == "__main__":
    run_web_dashboard()

DASHBOARD_HTML = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Security Monitor Pro</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);min-height:100vh;padding:20px}
.container{max-width:1600px;margin:0 auto}
.header{background:#fff;padding:30px;border-radius:15px;box-shadow:0 10px 40px rgba(0,0,0,.2);margin-bottom:20px;text-align:center}
.header h1{color:#1e3c72;font-size:2.5em;margin-bottom:10px}
.warning-banner{background:linear-gradient(135deg,#f44,#c00);color:#fff;padding:20px;border-radius:15px;margin-bottom:20px;display:none;animation:pulse 2s infinite}
.warning-banner.show{display:block}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.02)}}
.progress-section{background:#fff;padding:30px;border-radius:15px;box-shadow:0 10px 40px rgba(0,0,0,.2);margin-bottom:20px}
.progress-bar{background:#f0f0f0;border-radius:25px;height:40px;overflow:hidden;margin:20px 0}
.progress-fill{background:linear-gradient(90deg,#667eea,#764ba2);height:100%;transition:width .3s;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700}
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px;margin:20px 0}
.stat-card{background:#fff;padding:25px;border-radius:15px;box-shadow:0 5px 20px rgba(0,0,0,.1);text-align:center;transition:transform .2s}
.stat-card:hover{transform:translateY(-5px)}
.stat-card h2{font-size:3em;margin-bottom:10px}
.critical{color:#f44}.high{color:#fa0}.medium{color:#44f}.info{color:#1e3c72}
.severity-breakdown,.alerts-section,.process-tree-section{background:#fff;padding:30px;border-radius:15px;box-shadow:0 10px 40px rgba(0,0,0,.2);margin-bottom:20px}
.section-title{color:#1e3c72;border-bottom:3px solid #667eea;padding-bottom:10px;margin-bottom:20px;font-size:1.5em}
.tree-item{border:2px solid #e0e0e0;border-radius:10px;padding:15px;margin:15px 0;background:#f8f9fa;transition:all .3s}
.tree-item:hover{border-color:#667eea;box-shadow:0 5px 15px rgba(102,126,234,.3)}
.tree-parent{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:15px;border-radius:8px;margin-bottom:10px;font-weight:700;cursor:pointer}
.tree-parent:hover{opacity:0.9}
.tree-children{margin-left:30px;margin-top:10px;display:none}
.tree-children.expanded{display:block}
.tree-child{background:#fff;border-left:3px solid #667eea;padding:10px;margin:8px 0;border-radius:5px;cursor:pointer;transition:all .2s}
.tree-child:hover{background:#f0f4ff;border-left-width:5px;transform:translateX(3px)}
.expand-btn{background:#667eea;color:#fff;border:0;padding:8px 20px;border-radius:20px;cursor:pointer;margin-top:10px;font-size:0.9em;transition:all .2s}
.expand-btn:hover{background:#5568d3;transform:scale(1.05)}
.alert-item{background:#f8f9fa;border-left:5px solid;padding:20px;margin:15px 0;border-radius:5px;transition:all .2s}
.alert-item:hover{transform:translateX(5px)}
.alert-critical{border-color:#f44;background:#fff5f5}
.alert-high{border-color:#fa0;background:#fffbf0}
.alert-medium{border-color:#44f;background:#f5f5ff}
.alert-header{display:flex;justify-content:space-between;margin-bottom:15px}
.alert-title{font-weight:700;font-size:1.2em}
.alert-badge{padding:5px 15px;border-radius:20px;color:#fff;font-weight:700}
.badge-critical{background:#f44}.badge-high{background:#fa0}.badge-medium{background:#44f}
.alert-details{background:rgba(0,0,0,.03);padding:15px;border-radius:8px;font-family:'Courier New',monospace;font-size:.9em;margin-top:10px}
.alert-details div{margin:8px 0;display:flex}
.detail-label{font-weight:700;color:#1e3c72;min-width:150px}
.btn{padding:15px 40px;border:0;border-radius:25px;font-size:1.1em;font-weight:700;cursor:pointer;transition:all .2s;text-decoration:none;display:inline-block}
.btn:hover{transform:scale(1.05)}
.btn-primary{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff}
.btn-success{background:linear-gradient(135deg,#56ab2f,#a8e063);color:#fff}
.btn-danger{background:linear-gradient(135deg,#f44,#c00);color:#fff}
.btn-small{padding:8px 20px;font-size:.9em}
.hidden{display:none}
.modal{display:none;position:fixed;z-index:1000;left:0;top:0;width:100%;height:100%;background:rgba(0,0,0,.7)}
.modal.show{display:flex;align-items:center;justify-content:center}
.modal-content{background:#fff;padding:30px;border-radius:15px;max-width:600px;width:90%;max-height:80vh;overflow-y:auto}
.modal-header{display:flex;justify-content:space-between;margin-bottom:20px;align-items:center}
.modal-header h2{color:#1e3c72}
.close-modal{background:none;border:0;font-size:2em;cursor:pointer;color:#666;line-height:1}
.close-modal:hover{color:#f44}
.risk-score{font-size:3em;font-weight:700;margin:20px 0;text-align:center}
.risk-low{color:#4f4}.risk-medium{color:#fa0}.risk-high{color:#f44}
.process-info{background:#f8f9fa;padding:15px;border-radius:8px;margin:15px 0}
.process-info div{margin:8px 0;display:flex;justify-content:space-between;border-bottom:1px solid #e0e0e0;padding-bottom:8px}
.process-info div:last-child{border-bottom:none}
.info-label{font-weight:700;color:#1e3c72}
.info-value{color:#333}
.help-btn{position:fixed;bottom:30px;right:30px;width:60px;height:60px;border-radius:50%;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;border:0;font-size:1.5em;cursor:pointer;box-shadow:0 5px 20px rgba(0,0,0,.3);z-index:999;transition:transform .2s}
.help-btn:hover{transform:scale(1.1)}
</style></head><body><div class="container">
<div class="header"><h1>🔒 Security Monitor Pro</h1><p id="timestamp">Loading...</p></div>
<div class="warning-banner" id="warningBanner"><h2>⚠️ SECURITY THREATS!</h2><p id="warningMessage"></p></div>
<div class="progress-section"><h2 class="section-title">Scan Progress</h2>
<div class="progress-bar"><div class="progress-fill" id="progressBar">0%</div></div>
<p id="currentStep" style="text-align:center;font-size:1.2em;color:#666">Initializing...</p></div>
<div class="stats-grid">
<div class="stat-card"><h2 class="info" id="processCount">-</h2><p>Processes</p></div>
<div class="stat-card"><h2 class="info" id="serviceCount">-</h2><p>Services</p></div>
<div class="stat-card"><h2 class="info" id="totalAlerts">-</h2><p>Alerts</p></div>
<div class="stat-card"><h2 class="critical" id="criticalCount">-</h2><p>Critical</p></div>
<div class="stat-card"><h2 class="high" id="highCount">-</h2><p>High</p></div>
<div class="stat-card"><h2 class="medium" id="mediumCount">-</h2><p>Medium</p></div>
</div>
<div class="severity-breakdown hidden" id="severitySection">
<h2 class="section-title">📈 Severity Breakdown</h2>
<div style="margin:20px 0">
<div style="display:flex;justify-content:space-between;margin-bottom:8px;font-weight:700"><span>CRITICAL</span><span id="criticalCountText">0</span></div>
<div style="background:#f0f0f0;border-radius:10px;height:30px"><div style="background:linear-gradient(90deg,#f44,#c00);height:100%;display:flex;align-items:center;padding-left:15px;color:#fff;font-weight:700;transition:width .5s" id="barCritical">0%</div></div></div>
<div style="margin:20px 0">
<div style="display:flex;justify-content:space-between;margin-bottom:8px;font-weight:700"><span>HIGH</span><span id="highCountText">0</span></div>
<div style="background:#f0f0f0;border-radius:10px;height:30px"><div style="background:linear-gradient(90deg,#fa0,#f80);height:100%;display:flex;align-items:center;padding-left:15px;color:#fff;font-weight:700;transition:width .5s" id="barHigh">0%</div></div></div>
<div style="margin:20px 0">
<div style="display:flex;justify-content:space-between;margin-bottom:8px;font-weight:700"><span>MEDIUM</span><span id="mediumCountText">0</span></div>
<div style="background:#f0f0f0;border-radius:10px;height:30px"><div style="background:linear-gradient(90deg,#44f,#00c);height:100%;display:flex;align-items:center;padding-left:15px;color:#fff;font-weight:700;transition:width .5s" id="barMedium">0%</div></div></div>
</div>
<div class="alerts-section hidden" id="alertsSection">
<h2 class="section-title">🔍 Security Alerts (<span id="alertCount">0</span>)</h2>
<div id="alertsList"></div>
<div style="display:flex;gap:15px;justify-content:center;margin-top:30px;flex-wrap:wrap">
<a href="/download/pdf" class="btn btn-primary">📄 Download HTML</a>
<a href="/download/json" class="btn btn-success">📊 Download JSON</a>
</div></div>
<div class="process-tree-section hidden" id="processTreeSection">
<h2 class="section-title">🌳 Parent-Child Process Tree</h2>
<p style="color:#666;margin-bottom:20px"><strong>Click parent process name or any child process to view detailed information</strong></p>
<div id="processTreeList"></div></div>
</div>
<button class="help-btn" onclick="showHelp()">?</button>
<div class="modal" id="processModal">
<div class="modal-content">
<div class="modal-header"><h2>Process Details</h2><button class="close-modal" onclick="closeModal()">&times;</button></div>
<div id="processDetailsContent"></div></div></div>
<div class="modal" id="helpModal">
<div class="modal-content">
<div class="modal-header"><h2>📚 Help Guide</h2><button class="close-modal" onclick="closeHelpModal()">&times;</button></div>
<div style="line-height:1.8;color:#333">
<h3 style="color:#667eea;margin-top:15px">🔍 What This Tool Does</h3>
<p>Monitors Windows processes and services for suspicious activity and security threats.</p>
<h3 style="color:#667eea;margin-top:15px">🎯 How to Use</h3>
<ul style="margin-left:20px"><li>Wait for scan to complete</li><li>Review severity breakdown</li><li>Check security alerts</li><li><strong>Click any process</strong> in the tree to view details</li><li>Terminate suspicious processes</li><li>Download reports</li></ul>
<h3 style="color:#667eea;margin-top:15px">⚠️ Warning Levels</h3>
<p><strong style="color:#f44">CRITICAL:</strong> Immediate action required<br><strong style="color:#fa0">HIGH:</strong> Investigate now<br><strong style="color:#44f">MEDIUM:</strong> Review carefully</p>
<h3 style="color:#667eea;margin-top:15px">🖱️ Process Tree Navigation</h3>
<p><strong>Click parent process name</strong> to view its details<br><strong>Click any child process</strong> to view its details<br><strong>Click +N more</strong> to expand full list</p>
</div></div></div>
<script>
document.getElementById('timestamp').textContent='Started: '+new Date().toLocaleString();
function updateDashboard(){fetch('/api/status').then(r=>r.json()).then(d=>{document.getElementById('progressBar').style.width=d.progress+'%';document.getElementById('progressBar').textContent=d.progress+'%';document.getElementById('currentStep').textContent=d.current_step;document.getElementById('processCount').textContent=d.processes_count||'-';document.getElementById('serviceCount').textContent=d.services_count||'-';document.getElementById('totalAlerts').textContent=d.summary.total_alerts||'0';const c=(d.summary.by_severity&&d.summary.by_severity.CRITICAL)||0;const h=(d.summary.by_severity&&d.summary.by_severity.HIGH)||0;document.getElementById('criticalCount').textContent=c;document.getElementById('highCount').textContent=h;document.getElementById('mediumCount').textContent=(d.summary.by_severity&&d.summary.by_severity.MEDIUM)||'0';if(d.scan_complete&&(c>0||h>0)){document.getElementById('warningMessage').textContent=c>0?`${c} CRITICAL threat(s) detected! Immediate action required.`:`${h} HIGH priority alert(s) detected.`;document.getElementById('warningBanner').classList.add('show')}if(d.scan_complete){loadFullDetails();loadProcessTree()}})}
function loadProcessTree(){fetch('/api/process-tree').then(r=>r.json()).then(d=>{if(d.tree&&d.tree.length>0){const list=document.getElementById('processTreeList');list.innerHTML=d.tree.slice(0,20).map((item,idx)=>{const showCount=5;const hasMore=item.child_count>showCount;const visibleChildren=item.children.slice(0,showCount);const hiddenCount=item.child_count-showCount;return`<div class="tree-item"><div class="tree-parent" onclick="showProcessDetails(${item.parent.pid})" title="Click to view details"><div style="display:flex;justify-content:space-between;align-items:center"><span><strong>Parent:</strong> ${item.parent.name} (PID: ${item.parent.pid})</span><span style="background:rgba(255,255,255,0.3);padding:3px 10px;border-radius:15px;font-size:0.85em">${item.child_count} children</span></div><div style="font-size:0.85em;margin-top:5px;opacity:0.9">Path: ${item.parent.path||'N/A'}</div></div><div class="tree-children expanded" id="children-${idx}">${visibleChildren.map(c=>`<div class="tree-child" onclick="showProcessDetails(${c.pid})" title="Click to view details"><strong>→ ${c.name}</strong> (PID: ${c.pid})<br><span style="color:#666;font-size:0.85em">Path: ${c.path||'N/A'}</span></div>`).join('')}${hasMore?`<button class="expand-btn" onclick="expandChildren(${idx},${item.child_count},event)">+${hiddenCount} more processes</button>`:''}${hasMore?`<div id="hidden-${idx}" style="display:none">${item.children.slice(showCount).map(c=>`<div class="tree-child" onclick="showProcessDetails(${c.pid})" title="Click to view details"><strong>→ ${c.name}</strong> (PID: ${c.pid})<br><span style="color:#666;font-size:0.85em">Path: ${c.path||'N/A'}</span></div>`).join('')}</div>`:''}</div></div>`}).join('');document.getElementById('processTreeSection').classList.remove('hidden')}})}
function expandChildren(idx,total,event){event.stopPropagation();const hidden=document.getElementById(`hidden-${idx}`);const btn=event.target;if(hidden.style.display==='none'){hidden.style.display='block';btn.textContent='Show less';btn.style.background='#5568d3'}else{hidden.style.display='none';const shown=5;btn.textContent=`+${total-shown} more processes`;btn.style.background='#667eea'}}
function showProcessDetails(pid){console.log('Fetching details for PID:',pid);fetch(`/api/process-details/${pid}`).then(r=>r.json()).then(d=>{console.log('Received data:',d);if(d.error){alert('Error: '+d.error);return}const risk=d.risk_score||0;const riskClass=risk>70?'risk-high':risk>40?'risk-medium':'risk-low';const riskLevel=risk>70?'HIGH RISK':risk>40?'MEDIUM RISK':'LOW RISK';const content=`<div style="text-align:center"><div class="risk-score ${riskClass}">${risk}/100</div><p style="color:#666;font-size:1.1em">${riskLevel}</p></div><div class="process-info"><div><span class="info-label">Process Name:</span><span class="info-value">${d.name||'N/A'}</span></div><div><span class="info-label">PID:</span><span class="info-value">${d.pid||'N/A'}</span></div><div><span class="info-label">Executable Path:</span><span class="info-value" style="word-break:break-all">${d.exe||'N/A'}</span></div><div><span class="info-label">User:</span><span class="info-value">${d.username||'N/A'}</span></div><div><span class="info-label">Status:</span><span class="info-value">${d.status||'N/A'}</span></div><div><span class="info-label">CPU Usage:</span><span class="info-value">${d.cpu_percent||0}%</span></div><div><span class="info-label">Memory:</span><span class="info-value">${d.memory_mb||0} MB</span></div><div><span class="info-label">Threads:</span><span class="info-value">${d.num_threads||0}</span></div><div><span class="info-label">Connections:</span><span class="info-value">${d.num_connections||0}</span></div><div><span class="info-label">Created:</span><span class="info-value">${d.create_time||'N/A'}</span></div><div><span class="info-label">SHA-256:</span><span class="info-value" style="word-break:break-all;font-size:0.75em">${d.file_hash_sha256||'Unable to calculate'}</span></div><div><span class="info-label">Whitelisted:</span><span class="info-value">${d.is_whitelisted?'✅ Yes':'❌ No'}</span></div></div><div style="margin-top:20px;display:flex;gap:10px;justify-content:center;flex-wrap:wrap"><button class="btn btn-danger btn-small" onclick="terminateProcess(${pid})">🛑 Terminate Process</button><button class="btn btn-success btn-small" onclick="whitelistProcess('${d.name}')">✅ Add to Whitelist</button></div>`;document.getElementById('processDetailsContent').innerHTML=content;document.getElementById('processModal').classList.add('show')}).catch(err=>{console.error('Fetch error:',err);alert('Failed to load process details: '+err.message)})}
function terminateProcess(pid){if(confirm('Are you sure you want to terminate this process? This action cannot be undone.')){fetch(`/api/terminate-process/${pid}`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({force:false})}).then(r=>r.json()).then(d=>{alert(d.message);if(d.success){closeModal();updateDashboard()}}).catch(err=>alert('Error: '+err.message))}}
function whitelistProcess(name){fetch('/api/whitelist-process',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({process_name:name})}).then(r=>r.json()).then(d=>{alert(d.message);closeModal()}).catch(err=>alert('Error: '+err.message))}
function closeModal(){document.getElementById('processModal').classList.remove('show')}
function showHelp(){document.getElementById('helpModal').classList.add('show')}
function closeHelpModal(){document.getElementById('helpModal').classList.remove('hidden')}
function loadFullDetails(){fetch('/api/alerts').then(r=>r.json()).then(d=>{document.getElementById('severitySection').classList.remove('hidden');updateSeverityBars(d.summary);document.getElementById('alertCount').textContent=d.alerts.length;const list=document.getElementById('alertsList');if(d.alerts.length===0){list.innerHTML='<div style="background:linear-gradient(135deg,#56ab2f,#a8e063);color:#fff;padding:40px;border-radius:15px;text-align:center;font-size:1.3em;margin:20px 0">✅ No security threats detected! Your system appears clean.</div>'}else{const order={'CRITICAL':0,'HIGH':1,'MEDIUM':2,'LOW':3};d.alerts.sort((a,b)=>order[a.severity]-order[b.severity]);list.innerHTML=d.alerts.map((a,i)=>{let details='';if(a.timestamp)details+=`<div><span class="detail-label">Time:</span><span>${a.timestamp}</span></div>`;if(a.process_name)details+=`<div><span class="detail-label">Process:</span><span>${a.process_name}</span></div>`;if(a.pid)details+=`<div><span class="detail-label">PID:</span><span>${a.pid}</span></div>`;if(a.path)details+=`<div><span class="detail-label">Path:</span><span style="word-break:break-all">${a.path}</span></div>`;if(a.parent_name)details+=`<div><span class="detail-label">Parent:</span><span>${a.parent_name} (PID: ${a.parent_pid||'N/A'})</span></div>`;if(a.child_name)details+=`<div><span class="detail-label">Child:</span><span>${a.child_name} (PID: ${a.child_pid||'N/A'})</span></div>`;if(a.child_path)details+=`<div><span class="detail-label">Child Path:</span><span style="word-break:break-all">${a.child_path}</span></div>`;if(a.service_name)details+=`<div><span class="detail-label">Service:</span><span>${a.service_name}</span></div>`;if(a.display_name)details+=`<div><span class="detail-label">Display:</span><span>${a.display_name}</span></div>`;if(a.state)details+=`<div><span class="detail-label">State:</span><span>${a.state}</span></div>`;if(a.startup_type)details+=`<div><span class="detail-label">Startup:</span><span>${a.startup_type}</span></div>`;return`<div class="alert-item alert-${a.severity.toLowerCase()}"><div class="alert-header"><div class="alert-title">Alert #${i+1}: ${a.type}</div><div class="alert-badge badge-${a.severity.toLowerCase()}">${a.severity}</div></div><div style="color:#555;line-height:1.6;margin-bottom:10px">${a.description}</div>${details?`<div class="alert-details">${details}</div>`:''}</div>`}).join('')}document.getElementById('alertsSection').classList.remove('hidden')})}
function updateSeverityBars(s){const t=s.total_alerts||1;const c=s.by_severity?.CRITICAL||0;const h=s.by_severity?.HIGH||0;const m=s.by_severity?.MEDIUM||0;const cp=(c/t*100).toFixed(1);const hp=(h/t*100).toFixed(1);const mp=(m/t*100).toFixed(1);document.getElementById('barCritical').style.width=cp+'%';document.getElementById('barCritical').textContent=cp+'%';document.getElementById('criticalCountText').textContent=c+' alerts';document.getElementById('barHigh').style.width=hp+'%';document.getElementById('barHigh').textContent=hp+'%';document.getElementById('highCountText').textContent=h+' alerts';document.getElementById('barMedium').style.width=mp+'%';document.getElementById('barMedium').textContent=mp+'%';document.getElementById('mediumCountText').textContent=m+' alerts'}
setInterval(updateDashboard,1000);updateDashboard();
</script>
</body></html>'''
