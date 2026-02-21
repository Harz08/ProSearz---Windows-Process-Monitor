# 🔒 Windows Security Monitoring Agent 

**Professional-grade security monitoring tool for Windows systems**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 📋 Overview

A comprehensive security monitoring agent designed to detect malicious processes, suspicious service configurations, and potential security threats on Windows systems. Built with real-time scanning, advanced threat detection, and an intuitive web-based dashboard. This tool is currently under development for new features & may fell a bit buggy sometimes so please feedback for any issues

## ✨ Key Features

### 🔍 **Advanced Process Monitoring**
- Real-time process enumeration and analysis
- Parent-child relationship mapping
- Suspicious process chain detection
- CPU, memory, and network usage tracking
- Process termination and suspension controls

### ⚙️ **Service Auditing**
- Windows service configuration analysis
- Startup service enumeration
- Unusual file path detection
- Service permission auditing

### 🎯 **Threat Detection**
- Rule-based detection engine
- MITRE ATT&CK technique mapping
- Risk scoring system (0-100 scale)
- Malicious parent-child relationship detection
- Suspicious path analysis

### 🌐 **Web Dashboard**
- Live scanning progress
- Interactive threat visualization
- Process tree explorer
- Real-time alerts with severity levels
- Warning banner for critical threats

### 📊 **Reporting & Export**
- HTML reports with visual analytics
- JSON data export for automation
- Detailed alert logging
- Severity breakdown charts

### 🛡️ **Process Management**
- Kill/terminate suspicious processes
- Process whitelisting
- SHA-256 hash verification
- Network connection monitoring
- VirusTotal integration ready

## 🚀 Quick Start

### Prerequisites
- Windows 10/11 or Windows Server
- Python 3.8 or higher
- Administrator privileges (recommended)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Harz08/windows-security-monitor.git
cd windows-security-monitor
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python main.py
```

The web dashboard will automatically open in your browser at `http://localhost:5000`

## 📦 Project Structure

```
windows-security-monitor/
│
├── main.py                 # Application entry point
├── core_mon.py             # Process monitoring engine
├── service_mon.py          # Service auditing module
├── detect_rules.py         # Threat detection rules
├── alert_sys.py            # Alert management system
├── report_gen.py           # Report generation
├── web_interface.py        # Web dashboard
├── process_manager.py      # Advanced process control
│
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── LICENSE                # MIT License
```

## 🎯 Detection Capabilities

### Suspicious Process Patterns
- Office applications spawning shells (e.g., `winword.exe → powershell.exe`)
- Browsers launching command-line tools
- Processes running from temporary directories
- Unknown processes in system folders

### Service Anomalies
- Services with unusual executable paths
- Newly registered services
- Services in non-standard locations
- Auto-start service misconfigurations

### Risk Indicators
- High CPU/memory usage
- Excessive network connections
- Many child processes
- Missing file signatures

## 📸 Screenshots

### Dashboard Overview
![Dashboard](docs/screenshots/dashboard.png)

### Process Tree View
![Process Tree](docs/screenshots/process_tree.png)

### Alert Details
![Alerts](docs/screenshots/alerts.png)

### Security Report
![Report](docs/screenshots/report.png)

## 🔧 Configuration

### Custom Detection Rules

Edit `detect_rules.py` to add custom detection patterns:

```python
SUSPICIOUS_PARENT_CHILD = {
    'your_app.exe': ['suspicious_child.exe'],
}
```

### Whitelist Management

Add trusted processes to the whitelist:
```python
python -c "from process_manager import ProcessManager; pm = ProcessManager(); pm.add_to_whitelist('your_app.exe')"
```

## 📊 Usage Examples

### Basic Scan
```bash
python main.py
```

### Command-Line Mode (Coming Soon)
```bash
python main.py --scan --output report.html
```

### Automated Scanning
```bash
# Schedule with Windows Task Scheduler
schtasks /create /tn "SecurityScan" /tr "python C:\path\to\main.py" /sc daily /st 09:00
```

## 🛠️ Advanced Features

### Process Control
- **Terminate Process**: Stop malicious processes instantly
- **Suspend/Resume**: Temporarily pause suspicious activity
- **Network Monitoring**: Track process connections

### Threat Intelligence
- **Hash Verification**: Check file integrity with SHA-256
- **VirusTotal Integration**: Scan hashes against known malware
- **Risk Scoring**: Automated threat assessment (0-100)

### Export Options
- HTML reports for presentations
- JSON data for SIEM integration
- CSV exports for Excel analysis

## 🔐 Security Considerations

- **Administrator Rights**: Some features require elevated privileges
- **Antivirus Compatibility**: May trigger false positives in security software
- **Process Termination**: Use with caution; can affect system stability
- **Network Monitoring**: Requires firewall exceptions

## 🐛 Troubleshooting

### Common Issues

**"Access Denied" errors**
- Run as Administrator
- Check Windows User Account Control (UAC) settings

**Few services detected**
- Requires administrator privileges
- Some services are protected by Windows

**Browser doesn't open**
- Manually navigate to `http://localhost:5000`
- Check firewall settings

**Process termination fails**
- System processes cannot be terminated
- Run with administrator rights

## 📚 Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [User Manual](docs/USER_MANUAL.md)
- [API Documentation](docs/API.md)
- [Contributing Guidelines](CONTRIBUTING.md)

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) first.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **psutil** - Process and system utilities
- **Flask** - Web framework
- **Windows API** - System integration

## 📧 Contact

**Your Name** - [@yourhandle](https://twitter.com/yourhandle)

Project Link: [https://github.com/yourusername/windows-security-monitor](https://github.com/yourusername/windows-security-monitor)

## 🎓 Educational Purpose

This tool is designed for:
- Security research and education
- SOC analyst training
- Threat detection learning
- System administration

## ⚠️ Disclaimer

This tool is for **educational and authorized security testing only**. Users are responsible for compliance with applicable laws and regulations. The authors assume no liability for misuse or damage caused by this tool.

## 🗺️ Roadmap / Future Scope

- [ ] Real-time monitoring mode
- [ ] Machine learning threat detection
- [ ] Multi-system monitoring
- [ ] Email/SMS alerting
- [ ] Integration with SIEM platforms
- [ ] Portable version (no installation)
- [ ] Linux/macOS support

## 📈 Statistics

![GitHub stars](https://img.shields.io/github/stars/yourusername/windows-security-monitor?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/windows-security-monitor?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/windows-security-monitor)

---

**Made with ❤️ for the cybersecurity community**

⭐ **Star this repo if you find it useful!**
