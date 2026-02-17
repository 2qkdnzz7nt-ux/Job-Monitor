import urllib.request
import ssl
import sys

# Log to file
def log(msg):
    with open("download_log.txt", "a") as f:
        f.write(msg + "\n")

log("Starting download script...")

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/README.md"
log(f"Target URL: {url}")

try:
    # Add User-Agent header
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    log("Request created, opening url...")
    with urllib.request.urlopen(req, context=ctx) as response:
        log("Response received, reading data...")
        data = response.read().decode('utf-8')
    
    log(f"Downloaded {len(data)} characters.")
    
    with open("github_jobs_raw.md", "w", encoding="utf-8") as f:
        f.write(data)
    log("Success! Saved to github_jobs_raw.md")
    
except Exception as e:
    log(f"Error: {e}")
