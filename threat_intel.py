"""
threat_intel.py
Advanced Threat Intelligence & Analysis
Provides MITRE ATT&CK mapping, threat scoring, and security assessments
"""


class ThreatIntelligence:
    """Advanced threat intelligence and MITRE ATT&CK mapping"""
    
    def __init__(self):
        self.mitre_techniques = self.load_mitre_mapping()
        self.known_malware_hashes = set()  # Placeholder for malware hash database
    
    def load_mitre_mapping(self):
        """Map suspicious behaviors to MITRE ATT&CK techniques"""
        return {
            'suspicious_parent_child': {
                'technique_id': 'T1059',
                'technique_name': 'Command and Scripting Interpreter',
                'tactic': 'Execution',
                'description': 'Adversaries may abuse command interpreters to execute commands'
            },
            'suspicious_path': {
                'technique_id': 'T1036',
                'technique_name': 'Masquerading',
                'tactic': 'Defense Evasion',
                'description': 'Adversaries may manipulate file/directory locations'
            },
            'high_risk_process': {
                'technique_id': 'T1003',
                'technique_name': 'Credential Dumping',
                'tactic': 'Credential Access',
                'description': 'Adversaries may steal credentials from memory'
            },
            'service_anomaly': {
                'technique_id': 'T1543',
                'technique_name': 'Create or Modify System Process',
                'tactic': 'Persistence',
                'description': 'Adversaries may create or modify system services for persistence'
            }
        }
    
    def assess_threat(self, process_details):
        """Provide comprehensive threat assessment for a process"""
        assessment = {
            'overall_risk': self._calculate_overall_risk(process_details),
            'threat_indicators': self._identify_threat_indicators(process_details),
            'mitre_techniques': self._map_to_mitre(process_details),
            'recommendations': self._generate_recommendations(process_details)
        }
        return assessment
    
    def _calculate_overall_risk(self, details):
        """Calculate comprehensive risk score"""
        risk_score = details.get('risk_score', 0)
        
        # Additional risk factors
        risk_factors = []
        
        if risk_score > 70:
            risk_factors.append('High baseline risk score')
        
        if details.get('num_connections', 0) > 20:
            risk_factors.append('Excessive network activity')
        
        if not details.get('file_hash_sha256'):
            risk_factors.append('Unable to verify file integrity')
        
        exe_path = str(details.get('exe', '')).lower()
        if any(x in exe_path for x in ['temp', 'appdata', 'public']):
            risk_factors.append('Running from suspicious location')
        
        return {
            'score': risk_score,
            'level': 'CRITICAL' if risk_score > 70 else 'HIGH' if risk_score > 40 else 'MEDIUM' if risk_score > 20 else 'LOW',
            'factors': risk_factors
        }
    
    def _identify_threat_indicators(self, details):
        """Identify specific threat indicators"""
        indicators = []
        
        # Network indicators
        if details.get('num_connections', 0) > 10:
            indicators.append({
                'type': 'Network Activity',
                'severity': 'HIGH' if details.get('num_connections', 0) > 50 else 'MEDIUM',
                'description': f"{details.get('num_connections')} active network connections"
            })
        
        # Resource usage indicators
        if details.get('cpu_percent', 0) > 50:
            indicators.append({
                'type': 'High CPU Usage',
                'severity': 'MEDIUM',
                'description': f"Using {details.get('cpu_percent')}% CPU"
            })
        
        if details.get('memory_mb', 0) > 1000:
            indicators.append({
                'type': 'High Memory Usage',
                'severity': 'MEDIUM',
                'description': f"Using {details.get('memory_mb')} MB RAM"
            })
        
        # Path-based indicators
        exe_path = str(details.get('exe', '')).lower()
        if 'temp' in exe_path:
            indicators.append({
                'type': 'Suspicious Location',
                'severity': 'HIGH',
                'description': 'Running from temporary directory'
            })
        
        return indicators
    
    def _map_to_mitre(self, details):
        """Map detected behaviors to MITRE ATT&CK framework"""
        techniques = []
        
        # Check for command interpreter abuse
        exe_path = str(details.get('exe', '')).lower()
        if any(x in exe_path for x in ['powershell', 'cmd', 'wscript']):
            techniques.append(self.mitre_techniques['suspicious_parent_child'])
        
        # Check for suspicious paths
        if any(x in exe_path for x in ['temp', 'appdata\\local\\temp', 'public']):
            techniques.append(self.mitre_techniques['suspicious_path'])
        
        # Check for credential access tools
        name = str(details.get('name', '')).lower()
        if any(x in name for x in ['mimikatz', 'pwdump', 'procdump']):
            techniques.append(self.mitre_techniques['high_risk_process'])
        
        return techniques
    
    def _generate_recommendations(self, details):
        """Generate actionable security recommendations"""
        recommendations = []
        risk_score = details.get('risk_score', 0)
        
        if risk_score > 70:
            recommendations.append({
                'priority': 'CRITICAL',
                'action': 'Immediate Investigation Required',
                'details': 'This process shows multiple high-risk indicators. Investigate immediately and consider terminating if malicious.'
            })
        
        if details.get('num_connections', 0) > 20:
            recommendations.append({
                'priority': 'HIGH',
                'action': 'Monitor Network Activity',
                'details': 'Review network connections to identify any suspicious external communications.'
            })
        
        if not details.get('is_whitelisted'):
            recommendations.append({
                'priority': 'MEDIUM',
                'action': 'Verify Process Legitimacy',
                'details': 'If this is a trusted application, add it to the whitelist to reduce future alerts.'
            })
        
        exe_path = str(details.get('exe', '')).lower()
        if 'temp' in exe_path or 'appdata' in exe_path:
            recommendations.append({
                'priority': 'HIGH',
                'action': 'Investigate File Origin',
                'details': 'Processes running from temporary directories are often malicious. Verify the file source.'
            })
        
        if not details.get('file_hash_sha256'):
            recommendations.append({
                'priority': 'MEDIUM',
                'action': 'Unable to Verify File',
                'details': 'Could not calculate file hash. This may indicate a protected system process or potential evasion technique.'
            })
        
        return recommendations
    
    def check_known_malware(self, file_hash):
        """Check if file hash matches known malware (placeholder)"""
        # In production, this would query a malware hash database
        # For now, it's a placeholder
        return {
            'is_known_malware': False,
            'malware_family': None,
            'confidence': 0,
            'note': 'Malware database integration pending'
        }
    
    def get_threat_summary(self, all_processes):
        """Generate overall threat summary for all processes"""
        high_risk_count = sum(1 for p in all_processes if p.get('risk_score', 0) > 70)
        medium_risk_count = sum(1 for p in all_processes if 40 < p.get('risk_score', 0) <= 70)
        
        return {
            'total_processes': len(all_processes),
            'high_risk_processes': high_risk_count,
            'medium_risk_processes': medium_risk_count,
            'overall_security_posture': 'POOR' if high_risk_count > 5 else 'FAIR' if high_risk_count > 0 else 'GOOD'
        }


# Test function
if __name__ == "__main__":
    print("Testing Threat Intelligence Module...")
    
    ti = ThreatIntelligence()
    
    # Test with sample process data
    test_process = {
        'name': 'suspicious.exe',
        'pid': 1234,
        'exe': 'C:\\Users\\Public\\suspicious.exe',
        'risk_score': 75,
        'num_connections': 25,
        'cpu_percent': 60,
        'memory_mb': 512,
        'file_hash_sha256': 'abc123...',
        'is_whitelisted': False
    }
    
    assessment = ti.assess_threat(test_process)
    
    print("\n🎯 Threat Assessment:")
    print(f"Overall Risk: {assessment['overall_risk']['level']} ({assessment['overall_risk']['score']}/100)")
    print(f"\n📊 Threat Indicators: {len(assessment['threat_indicators'])}")
    for indicator in assessment['threat_indicators']:
        print(f"  - [{indicator['severity']}] {indicator['type']}: {indicator['description']}")
    
    print(f"\n🎯 MITRE ATT&CK Techniques: {len(assessment['mitre_techniques'])}")
    for tech in assessment['mitre_techniques']:
        print(f"  - {tech['technique_id']}: {tech['technique_name']}")
    
    print(f"\n💡 Recommendations: {len(assessment['recommendations'])}")
    for rec in assessment['recommendations']:
        print(f"  - [{rec['priority']}] {rec['action']}")
    
    print("\n✅ Threat Intelligence Test Complete")
