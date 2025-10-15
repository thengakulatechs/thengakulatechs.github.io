---
title: The Ultimate Guide to Bug Bounty Automation
date: 2025-10-15 14:39:48 +0530
categories: [Cybersecurity, Bug Bounty]
tags: ['bug-bounty', 'automation', 'ethical-hacking', 'security-testing', 'reconnaissance', 'vulnerability-assessment']
---

# The Ultimate Guide to Bug Bounty Automation: Tools, Techniques, and Pro Tips

## Why Automation is Non-Negotiable in Modern Bug Bounties

Bug bounty hunting has evolved from a manual testing process to a high-speed, data-intensive discipline where automation isn't just helpful—it's essential. Top hunters process thousands of endpoints and subdomains daily, something impossible to achieve manually.

**The Automation Advantage:**
- **Scale:** Process hundreds of targets simultaneously
- **Speed:** Identify low-hanging fruit while you sleep
- **Consistency:** Eliminate human error in repetitive tasks
- **Depth:** Combine multiple tools for comprehensive coverage
- **Focus:** Free up mental energy for complex vulnerability chaining

> **Critical Disclaimer:** This guide is for educational purposes only. Always test on systems you own or have explicit, written permission to test. Unauthorized testing is illegal. Responsible disclosure is mandatory.

## The Complete Automation Pipeline: 20 Steps to Success

### 1. Subdomain Enumeration: Casting the Widest Net

**Why It Matters:** Subdomains are the forgotten backdoors of organizations. Development, staging, and legacy subdomains often have weaker security controls.

**Tools & Deep Dive:**

**Subfinder** - Fast and focused
```bash
# Basic enumeration
subfinder -d target.com -o subdomains.txt

# Comprehensive scan with all sources
subfinder -d target.com -all -o subdomains_full.txt

# Silent mode for clean output
subfinder -d target.com -silent
```

**Amass** - The Industrial-Grade Option
```bash
# Passive enumeration (stealthy)
amass enum -passive -d target.com -o amass_passive.txt

# Active enumeration (more comprehensive but noisier)
amass enum -active -d target.com -brute -w wordlist.txt -o amass_active.txt

# Continuous monitoring (Note: amass track deprecated in newer versions)
amass enum -d target.com -monitor -o continuous_monitoring.txt
```

**⚠️ Update Note:** The `amass track` command has been deprecated in newer versions. Use `amass enum -monitor` for continuous monitoring.

**Pro Tip:** Combine multiple tools and de-duplicate results:
```bash
cat subfinder.txt amass.txt assetfinder.txt | sort -u > all_subdomains.txt
```

**Modern Alternative - Using Chaos:**
```bash
# ProjectDiscovery's Chaos for subdomain enumeration
chaos -d target.com -o chaos_subs.txt

# Combine with traditional tools
cat subfinder.txt amass.txt chaos_subs.txt | anew all_subdomains.txt
```

### 2. Port Scanning: Mapping the Attack Surface

**Why It Matters:** Open ports reveal the technology stack and potential attack vectors. Different services mean different vulnerability classes.

**Masscan for Speed:**
```bash
# Scan top 1000 ports extremely fast
masscan -p1-65535 10.0.0.0/8 --rate=10000 -oG masscan_output.txt

# Scan specific port ranges
masscan -p80,443,8000-9000,22,21 target.com -oG web_ports.txt

# Export in different formats for different tools
masscan -p1-65535 target.com -oX masscan.xml
```

**Nmap for Depth:**
```bash
# Comprehensive scan with service detection
nmap -sS -sV -sC -O -p- -T4 -oA full_scan target.com

# Quick web service scan
nmap -sS -sV -p80,443,8000-9000 --script http-title -oA web_scan target.com

# Vulnerability script scanning
nmap -sS -sV --script vuln -p80,443 -oA vuln_scan target.com
```

### 3. Visual Reconnaissance: Seeing What Others Miss

**Why It Matters:** Screenshots help identify custom applications, login portals, and outdated software at a glance.

**⚠️ Aquatone Status Update:**
> **Note:** Aquatone is no longer actively maintained. Consider modern alternatives like Gowitness or httpx with screenshot capabilities.

**Gowitness (Modern Alternative):**
```bash
# Basic screenshot capture
gowitness file -f subdomains.txt --threads 20

# With specific ports and timeout settings
gowitness file -f subdomains.txt --ports 80,443,8080,8443 --timeout 10

# Generate comprehensive report with screenshots
gowitness file -f subdomains.txt --write-db --write-csv
```

**httpx with Screenshots:**
```bash
# Take screenshots with httpx
cat subdomains.txt | httpx -screenshot -store-response-dir screenshots/
```

**Eyewitness Alternative:**
```bash
# File input
eyewitness --file urls.txt --web --no-prompt

# Pre-scan to filter active hosts
eyewitness --prepend-https --threads 10 --timeout 10 -f urls.txt
```

### 4. Directory Bruteforcing: Finding Hidden Treasure

**Why It Matters:** Hidden directories often contain backup files, admin panels, configuration files, and development artifacts.

**FFuf - The Modern Workhorse:**
```bash
# Basic directory discovery
ffuf -u https://target.com/FUZZ -w /usr/share/wordlists/dirb/common.txt

# Recursive scanning
ffuf -u https://target.com/FUZZ -w wordlist.txt -recursion -recursion-depth 2

# Filter by response size (remove clutter)
ffuf -u https://target.com/FUZZ -w wordlist.txt -fs 4242

# Multiple extensions
ffuf -u https://target.com/FUZZ -w wordlist.txt -e .php,.txt,.bak,.json

# Rate limiting to avoid detection
ffuf -u https://target.com/FUZZ -w wordlist.txt -p "0.1-1.0" -t 10
```

**Gobuster for Reliability:**
```bash
# Directory scanning
gobuster dir -u https://target.com -w wordlist.txt -x php,html,txt -t 50

# DNS subdomain bruteforcing
gobuster dns -d target.com -w subdomains.txt -t 50 -o gobuster_dns.txt

# Virtual host discovery
gobuster vhost -u https://target.com -w subdomains.txt -t 20
```

### 5. JavaScript Analysis: The Goldmine of Modern Apps

**Why It Matters:** Modern web applications heavily use JavaScript, often exposing API endpoints, keys, and sensitive logic.

**LinkFinder Deep Dive:**
```bash
# Analyze single JS file
python3 LinkFinder.py -i https://target.com/static/app.js -o cli

# Analyze entire domain's JS files
python3 LinkFinder.py -i https://target.com -d -o cli

# Output to HTML for better visualization
python3 LinkFinder.py -i https://target.com -o results.html
```

**Modern Alternative - JSluice:**
```bash
# Modern JavaScript analysis with JSluice
echo "https://target.com/app.js" | jsluice urls
echo "https://target.com/app.js" | jsluice secrets
echo "https://target.com/app.js" | jsluice endpoints
```

**GF Patterns for Targeted Hunting:**
```bash
# First, extract all JavaScript files
cat all_urls.txt | grep "\.js$" > js_files.txt

# Then search for specific patterns
cat js_files.txt | while read url; do
    curl -s $url | gf api-keys
    curl -s $url | gf interesting-params
    curl -s $url | gf ssrf
done

# Or use meg to batch process
meg -d 1000 /path/urls_js js_files.txt
```

**SecretFinder for API Keys:**
```bash
python3 SecretFinder.py -i https://target.com -e -o cli
```

### 6. Parameter Discovery: Finding Hidden Inputs

**Why It Matters:** Unexposed parameters are common sources of SQLi, XSS, and business logic vulnerabilities.

**ParamSpider - Automated Parameter Extraction:**
```bash
# Basic parameter extraction
python3 paramspider.py -d target.com

# Include all subdomains
python3 paramspider.py -d target.com --subs

# Exclude certain file extensions
python3 paramspider.py -d target.com -e php,html,css
```

**Arjun - Intelligent Parameter Discovery:**
```bash
# Single URL scan
arjun -u https://target.com/endpoint

# Batch scanning from file
arjun -i targets.txt -t 50

# JSON output for automation
arjun -u https://target.com/endpoint -oJ params.json
```

### 7. XSS Automation: Beyond Basic Scanning

**Why It Matters:** XSS remains prevalent but often requires creative payloads and context-aware testing.

**Dalfox Advanced Usage:**
```bash
# Basic XSS scanning
dalfox url "https://target.com/page?q=test"

# Pipe from other tools
cat params.txt | dalfox pipe

# Use custom payloads and user-agent
dalfox url "https://target.com/page?q=test" -p ~/custom_payloads.txt -H "User-Agent: Mozilla/5.0"

# Blind XSS testing
dalfox url "https://target.com/search" -b https://your-xss-hunter.xss.ht
```

**XSStrike for Context-Aware Testing:**
```bash
# Basic scan
python3 xsstrike.py -u "https://target.com/search?q=test"

# Crawl and test
python3 xsstrike.py -u "https://target.com" --crawl

# Skip DOM scanning for speed
python3 xsstrike.py -u "https://target.com/search?q=test" --skip-dom
```

**Modern Alternative - Katana + Dalfox Pipeline:**
```bash
# Modern XSS testing pipeline
echo "https://target.com" | katana -silent | grep "=" | dalfox pipe
```

### 8. SQL Injection Automation

**Why It Matters:** SQLi can lead to complete database compromise, yet many automated scanners miss complex cases.

**SQLmap Pro Techniques:**
```bash
# Basic detection
sqlmap -u "https://target.com/product?id=1" --batch

# Crawl and test
sqlmap -u "https://target.com" --crawl=2 --batch

# Specific technique testing
sqlmap -u "https://target.com/product?id=1" --technique=U --batch

# Full database extraction
sqlmap -u "https://target.com/product?id=1" --dbs --tables --columns --dump

# Use tamper scripts for WAF bypass
sqlmap -u "https://target.com/product?id=1" --tamper=between,randomcase --batch
```

### 9. SSRF Automation: The Internal Network Bridge

**Why It Matters:** SSRF can provide access to internal services, cloud metadata, and blind spots.

**Advanced SSRF Testing:**
```bash
# Using Gopherus for protocol attacks
gopherus --exploit mysql

# Generate SSRF payloads for different services
gopherus --exploit redis
gopherus --exploit postgresql

# Interactsh for blind detection
interactsh-client -v -o interactions.txt

# Combine with other tools
cat urls.txt | while read url; do
    curl -s "$url" -G --data-urlencode "url=https://your-interactsh-subdomain.interact.sh" 
done
```

### 10. File Inclusion Automation

**Why It Matters:** LFI/RFI can lead to sensitive file disclosure and remote code execution.

**Advanced LFI Testing:**
```bash
# LFI Suite with multiple techniques
python3 lfi_suite.py -u "https://target.com/include?file=index.html" -d 5

# Custom wordlists for specific frameworks
python3 lfi_suite.py -u "https://target.com/include?file=index.html" -w custom_wordlist.txt
```

**Automated Filter Bypass:**
```bash
# Test various encoding bypasses
curl "https://target.com/include?file=....//....//....//etc/passwd"
curl "https://target.com/include?file=....\/....\/....\/etc/passwd"
curl "https://target.com/include?file=%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd"
```

## Building Your Automation Workflow

### The Reconnaissance Pipeline

A professional setup chains tools together:

```bash
#!/bin/bash
DOMAIN=$1

echo "[+] Starting reconnaissance pipeline for $DOMAIN"

# Subdomain discovery
echo "[+] Enumerating subdomains..."
subfinder -d $DOMAIN -silent | tee subfinder.txt
amass enum -passive -d $DOMAIN -silent | tee amass.txt
assetfinder --subs-only $DOMAIN | tee assetfinder.txt

# Combine and deduplicate
cat subfinder.txt amass.txt assetfinder.txt | sort -u > all_subs.txt
echo "[+] Found $(wc -l < all_subs.txt) unique subdomains"

# Check which are alive
echo "[+] Checking live hosts..."
cat all_subs.txt | httpx -silent -threads 100 > live_subs.txt
echo "[+] Found $(wc -l < live_subs.txt) live hosts"

# Take screenshots
echo "[+] Capturing screenshots..."
cat live_subs.txt | aquatone -ports 80,443,8080,8443 -scan-timeout 2000 -screenshot-timeout 30000

echo "[+] Reconnaissance complete!"
```

### Continuous Monitoring Setup

```bash
#!/bin/bash
# continuous_monitor.sh - Updated 2024 version
DOMAINS="target1.com target2.com target3.com"

while true; do
    for domain in $DOMAINS; do
        echo "[$(date)] Scanning $domain"
        
        # Modern subdomain enumeration
        subfinder -d $domain -silent | anew ${domain}_subs.txt
        chaos -d $domain -silent | anew ${domain}_subs.txt
        
        # Check for new subdomains
        if [ -s ${domain}_subs.txt.new ]; then
            echo "New subdomains found for $domain!"
            
            # Immediate verification of new subdomains
            cat ${domain}_subs.txt.new | httpx -silent | anew ${domain}_live.txt
            
            # Screenshot new live hosts
            cat ${domain}_live.txt | gowitness file -f - --threads 10
            
            # Notify about findings
            cat ${domain}_subs.txt.new | notify -id discord -bulk
        fi
    done
    sleep 3600 # Wait 1 hour
done
```

**Modern Alternative - Using GitHub Actions:**
```yaml
# .github/workflows/continuous-recon.yml
name: Continuous Reconnaissance
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
jobs:
  recon:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Subfinder
        run: |
          subfinder -d ${{ secrets.TARGET_DOMAIN }} -silent | anew subs.txt
          git add subs.txt && git commit -m "Update subdomains" && git push
```

## Advanced Automation Strategies

### 1. Parallel Processing with GNU Parallel

```bash
# Process multiple targets simultaneously
cat targets.txt | parallel -j 10 "subfinder -d {} -silent | tee {}.subs.txt"

# Run different tools in parallel
parallel --line-buffer ::: \
    "subfinder -d target.com -o subfinder.txt" \
    "amass enum -passive -d target.com -o amass.txt" \
    "assetfinder target.com > assetfinder.txt"
```

### 2. Notification Integration

Integrate with notification platforms for real-time alerts:

```bash
# Using notify for multiple platforms
subfinder -d target.com -silent | anew subs.txt | notify -id discord -bulk
# or
subfinder -d target.com -silent | anew subs.txt | notify -id slack -bulk
# or  
subfinder -d target.com -silent | anew subs.txt | notify -id telegram -bulk
```

### 3. Cloud-Scale Automation

For massive programs, use cloud resources:

```bash
# Distributed scanning with Kubernetes
kubectl create job --image=subfinder subfinder-scan -- -d target.com -o /output/subs.txt

# AWS Batch for large-scale processing
aws batch submit-job --job-name bugbounty-scan --job-queue scanning-queue --job-definition recon-container
```

## Common Pitfalls and How to Avoid Them (2024 Update)

1. **Getting Blocked:** Use rate limiting, random delays, and rotate user agents
2. **False Positives:** Implement validation steps and manual verification workflows
3. **Tool Overload:** Focus on mastering a core toolset rather than using every new tool
4. **Analysis Paralysis:** Build pipelines that prioritize and categorize findings automatically
5. **Outdated Tools:** Regularly update tools and replace deprecated ones (Aquatone → Gowitness)
6. **API Rate Limits:** Many tools now use APIs with rate limits - configure API keys properly
7. **WAF Evolution:** Modern WAFs are smarter - use more sophisticated evasion techniques

## 2024 Best Practices

**Tool Maintenance:**
```bash
# Keep tools updated
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest

# Update nuclei templates regularly
nuclei -update-templates
```

**Modern Workflow Integration:**
- Use **anew** for deduplication instead of basic sort/uniq
- Implement **notify** for real-time alerts
- Use **chaos** for additional subdomain sources
- Leverage **katana** for modern crawling

## The Professional's Toolkit (2024 Updated)

**Essential Tools Summary:**
- **Recon:** Subfinder, Amass, Assetfinder, Chaos
- **HTTP Analysis:** httpx, nuclei, katana
- **Content Discovery:** ffuf, feroxbuster, dirsearch
- **Screenshots:** Gowitness, httpx (with screenshot flag)
- **JavaScript Analysis:** JSluice, LinkFinder, SecretFinder
- **Vulnerability Scanning:** nuclei, gau, waybackurls
- **Automation Framework:** ProjectDiscovery tools, custom bash/python scripts

**⚠️ Deprecated/Less Maintained:**
- **Aquatone** → Use Gowitness or httpx screenshots
- **amass track** → Use amass enum -monitor
- **napalm** → Use nuclei with custom templates

## Conclusion: From Automation to Augmentation

True mastery in bug bounties isn't about replacing human intelligence with automation—it's about augmenting your capabilities. The best hunters use automation to handle the scale while they focus on the unique, complex vulnerabilities that machines can't find.

**Remember:** Automation gets you to the starting line faster, but your skill and creativity win the race.

*Tools change, but the principles of thorough reconnaissance and systematic testing remain constant. Stay curious, keep learning, and happy hunting!*
