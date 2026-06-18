# How to Detect This Keylogger (Blue Team Guide)

## Overview
This document explains how a SOC analyst or security team would detect and respond to this keylogger if it was running on a system.

## Detection Methods

### 1. Process and DLL Analysis
**What to look for:**
- Process running with `pynput` library imported — check Python process imports using tools like:
  - `Autoruns` (Sysinternals) — look for suspicious Python scripts in startup
  - `Process Explorer` — examine loaded DLLs, look for `pynput` or keyboard hooking patterns
  - `Get-Process | Select-Object Name, Path` — PowerShell to list all running processes

**Why it works:** `pynput` uses Windows API hooks to monitor keyboard input — this leaves traces in the process memory and DLL loading.

### 2. Network Analysis (Email Exfiltration Detection)
**What to look for:**
- Outbound SMTP connections on port 587 from unusual processes (Python.exe)
- Use `netstat -ano` or Wireshark to monitor:
  - Connections to `smtp.gmail.com`
  - Any non-system process initiating SMTP traffic
- Monitor email logs for:
  - Emails sent from corporate accounts at unusual times
  - Emails with no legitimate business purpose

**Why it works:** Malware must "phone home" with stolen data. Email exfiltration creates detectable network traffic.

### 3. File System Monitoring
**What to look for:**
- Presence of `keylog.txt` or similar log files in suspicious locations
- Use tools like:
  - `Autoruns` — check for Python scripts in startup folders
  - `YARA` rules — scan for keylogger signatures
  - File Integrity Monitoring (FIM) — detect unauthorized files

### 4. Event Log Analysis (Windows Event Viewer)
**What to look for:**
- Event ID 4688 (Process Creation) — look for Python.exe launching with suspicious arguments
- Event ID 592 (Process Exit) — abnormal process termination patterns
- Event ID 800 (WMI) — check for WMI-based process execution

### 5. Behavioral Analysis (EDR/SIEM)
**What to look for:**
- Unusual Python process behavior:
  - Python.exe accessing `keyboard` input APIs
  - Python spawning `smtplib` connections
  - Reading/writing to log files at regular intervals
- Timeline correlation:
  - If `password` appears in a log, check if user actually typed that legitimately
  - If emails are sent at regular 60-second intervals, that's a behavioral anomaly

## Indicators of Compromise (IOCs)

| Indicator | Type | Value |
|-----------|------|-------|
| Process Name | Process | `python.exe` or `pythonw.exe` |
| Command Line | Process | Contains `keylogger.py` or `pynput` |
| Network Destination | Network | `smtp.gmail.com:587` |
| File Created | File | `keylog.txt` |
| Loaded Library | DLL | `pynput` library artifacts |

## Mitigation Strategies

1. **Endpoint Detection & Response (EDR):** Deploy tools like CrowdStrike, Sentinel One, or Microsoft Defender to monitor process behavior
2. **Disable Python Execution:** Block Python.exe in Group Policy if not needed for legitimate development
3. **Network Segmentation:** Restrict outbound SMTP to approved mail servers only
4. **File Integrity Monitoring:** Alert on creation of log files in unexpected directories
5. **User Education:** Train employees to recognize when unusual keyboard activity is happening

## What Makes This Keylogger Hard to Detect

- ✓ Runs in-process (no separate executable)
- ✓ Uses standard Python libraries (not custom malware)
- ✓ Exfiltrates via legitimate email (harder to flag as malicious)
- ✓ No obvious binary indicators

## What Makes It Easy to Detect

- ✗ Python process accessing keyboard hooks (unusual behavior)
- ✗ Regular SMTP connections from a user process
- ✗ Plaintext log file on disk
- ✗ Predictable email timing (every 60 seconds)
- ✗ No process masking or obfuscation

## Real-World Context
Professional malware tries to avoid these detection methods by:
- Code obfuscation and encryption
- Process hollowing and injection
- Rootkit techniques to hide from tools
- Using legitimate system processes as cover
- Randomizing exfiltration timing
- Using encrypted channels instead of plaintext

This educational keylogger skips those complexities, making it useful for learning but obviously detectable in a real environment.