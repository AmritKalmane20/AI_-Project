# AI_-Project

This repository contains two advanced AI/ML projects built for the **Embarko Student Challenge**.

---

## 🛡️ ThreatIntel AI - Cybersecurity Threat Intelligence Platform

**Live Demo:** https://threat-intel-ai.embarko.app (deployed via Embarko)

An advanced cybersecurity threat intelligence platform analyzing IPs, domains, URLs, and file hashes with 11 analysis tabs.

### Features
- **11 Analysis Tabs**: Overview, Reputation, Network, SSL/TLS, Subdomains, Vulnerabilities, Behavior, Threat Intel, Threat Hunt, Report, Raw Data
- **Smart Paste** - Auto-extracts URLs, IPs, hashes from clipboard text
- **SSL/TLS Analysis** - Certificate grading, CT logs, config checks (HSTS, PFS, TLS 1.3)
- **Subdomain Enumeration** - 50+ discovered subdomains with threat scoring
- **Vulnerability Scanning** - 20+ real CVEs with CVSS, exploit availability, severity filter
- **MITRE ATT&CK Mapping** - Technique mapping with confidence scores
- **Threat Hunting** - 6 ready-to-run queries (copyable), IOC collections, campaign attribution
- **Report Generation** - Executive summary, recommendations, export (JSON/CSV/STIX/TAXII/PDF)
- **Zero-trust** - No logging, client-side processing

### Social Media Posts (Embarko Challenge)
- **LinkedIn:** ✅ Posted
- **Reddit:** ✅ Posted (r/cybersecurity)
- **Medium:** ✅ Posted

---

## 📁 Repository Structure

```
AI_-Project/
├── threat-intel-ai/           # Cybersecurity Threat Intel Project
│   ├── deploy_app/            # Single HTML file with all logic
│   │   └── index.html         # Full threat intel platform
│
└── README.md
```

---

## 🚀 Quick Start


### ThreatIntel AI
```bash
cd threat-intel-ai
# Just open deploy_app/index.html in a browser
# Or deploy to Embarko:
tar -czf app.tar.gz -C deploy_app .
curl -X POST 'https://ship.embarko.ai/apps' \
  -H 'X-App-Name: threat-intel-ai' \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -F 'source=@app.tar.gz'
```

---

## 🏆 Embarko Student Challenge

Both projects are deployed on **Embarko** (https://embarko.ai) - a platform for deploying ML/AI apps without Docker, no signup required.

- **ThreatIntel AI:** https://threat-intel-ai.embarko.app

### Social Media Presence
- **LinkedIn:** Posted with #embarko.ai #DeployWithEmbarko
- **Reddit:** Posted on r/cybersecurity with #embarko.ai #DeployWithEmbarko
- **Medium:** Published with #embarko.ai #DeployWithEmbarko


---

## 📄 License

MIT License - see individual project directories for details.

---

Built with ❤️ for the **Embarko Student Challenge**
