import urllib.request

URL = "https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/README.md"

try:
    print(f"Fetching from {URL}...")
    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        data = response.read().decode('utf-8')
    
    with open("gh_dump.txt", "w", encoding="utf-8") as f:
        f.write(data[:5000])
    print("Dumped first 5000 chars to gh_dump.txt")

except Exception as e:
    print(f"Error: {e}")
