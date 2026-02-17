import urllib.request
import re
import socket

# Set timeout for network requests
socket.setdefaulttimeout(15)

# List of URLs to try (including mirrors for better accessibility)
URLS = [
    "https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/README.md",
    "https://mirror.ghproxy.com/https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/README.md",
    "https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/main/README.md",
]

def fetch_github_jobs():
    print(f"\n[+] Connecting to GitHub Community Tracker...")
    
    # Prefer local file if it exists (cached or manually downloaded)
    if os.path.exists("github_jobs_raw.md"):
        print("   [+] Found local cache 'github_jobs_raw.md'. Using it.")
        try:
            with open("github_jobs_raw.md", "r", encoding="utf-8") as f:
                data = f.read()
            parsed = parse_jobs(data)
            print(f"   [+] Parsed {len(parsed)} jobs from local file.")
            if len(parsed) > 0:
                return parsed
        except Exception as e:
            print(f"   [-] Failed to read local file: {e}")

    for url in URLS:
        print(f"   Trying: {url} ...")
        try:
            # Use a custom user agent to avoid basic blocks
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = response.read().decode('utf-8')
            
            print(f"   [+] Success! Downloaded {len(data)} characters.")
            
            # SAVE RAW FILE FOR USER INSPECTION
            try:
                with open("github_jobs_raw.md", "w", encoding="utf-8") as f:
                    f.write(data)
                print(f"   [+] Saved raw data to 'github_jobs_raw.md'")
            except Exception as e:
                print(f"   [-] Failed to save raw file: {e}")

            # CHECK IF THIS IS JUST THE INDEX PAGE
            if "Software Engineering Internship Roles" in data:
                print("   [i] Detected Index Page. Fetching Software Engineering Sub-page...")
                # The data structure shows that categories are just ANCHORS in the same file or links to other files.
                # BUT wait, the simplifyjobs repo structure recently changed to use multiple files?
                # Or maybe the raw content I got IS just the README which links to other files?
                # Let's try to find the specific link for Software Engineering and fetch THAT.
                
                # Look for: [Software Engineering Internship Roles](LINK)
                # The link in your debug output was: https://github.com/SimplifyJobs/Summer2026-Internships/blob/dev/README.md#-software-engineering-internship-roles
                # This is a link to the SAME file (README.md) but with an anchor.
                # This means the content SHOULD be in this file.
                
                # HOWEVER, GitHub RAW view often truncates or behaves differently for huge files?
                # OR, maybe the "dev" branch README is just a table of contents now?
                
                # Let's try to fetch the dedicated "Software-Engineering.md" if it exists (common pattern)
                # Or try the "main" branch if "dev" is acting up.
                
                # Let's try a different URL that is KNOWN to contain the table directly if the first one failed to parse anything.
                # Actually, let's try to fetch the list from the JSON data if available? No, stick to markdown.
                
                # Hypothesis: The file is too big and we are only getting the top part? 
                # No, you downloaded 900k chars. That's plenty.
                
                # Hypothesis: The format of the table lines doesn't match my strict filter.
                # Let's relax the filter in parse_jobs.
                pass

            parsed = parse_jobs(data)
            print(f"   [+] Parsed {len(parsed)} jobs.")
            return parsed
        except Exception as e:
            print(f"   [-] Failed: {e}")
            continue
    
    print("\n[!] Could not fetch jobs from any source.")
    print("   Please check your network connection or VPN settings.")
    print("   (Note: GitHub raw content is often blocked in some regions without a VPN)")
    return []

def parse_jobs(md_content):
    jobs = []
    print(f"   [DEBUG] Parsing content length: {len(md_content)}")
    
    # The content seems to be HTML table rows, not Markdown pipes.
    # We will use regex to find <tr>...</tr> blocks.
    
    # Remove newlines to make regex easier across multiple lines
    content_single_line = md_content.replace('\n', ' ')
    
    # Regex for table rows
    # <tr><td>...</td><td>...</td>...</tr>
    row_pattern = re.compile(r'<tr>(.*?)</tr>', re.IGNORECASE)
    matches = row_pattern.findall(content_single_line)
    
    print(f"   [DEBUG] Found {len(matches)} table rows (HTML).")
    
    for i, row_html in enumerate(matches):
        # Extract cells <td>...</td>
        cell_pattern = re.compile(r'<td>(.*?)</td>', re.IGNORECASE)
        cells = cell_pattern.findall(row_html)
        
        if len(cells) < 3:
            continue
            
        # 0: Company (often <strong><a href="...">Name</a></strong>)
        # 1: Role
        # 2: Location
        # 3: Application (links)
        
        try:
            raw_company = cells[0]
            raw_role = cells[1]
            raw_location = cells[2]
            
            # Skip header row if it got matched (usually th, but just in case)
            if "Company" in raw_company and "Role" in raw_role:
                continue
                
            company = extract_text_from_html(raw_company)
            role = extract_text_from_html(raw_role)
            location = extract_text_from_html(raw_location)
            
            link = "N/A"
            if len(cells) > 3:
                # Extract first href from the application cell
                link_match = re.search(r'href="([^"]+)"', cells[3])
                if link_match:
                    link = link_match.group(1)
            
            # Fallback: check role or company for link
            if link == "N/A":
                link_match = re.search(r'href="([^"]+)"', raw_role)
                if link_match:
                    link = link_match.group(1)
            if link == "N/A":
                link_match = re.search(r'href="([^"]+)"', raw_company)
                if link_match:
                    link = link_match.group(1)

            job = {
                "id": f"gh_{len(jobs)}",
                "title": role,
                "company": company,
                "location": location,
                "description": "Source: GitHub (HTML Table)",
                "url": link,
                "source": "github"
            }
            jobs.append(job)
            
        except Exception as e:
            # print(f"   [DEBUG] Error parsing row {i}: {e}")
            continue

    # If no HTML rows found, try Markdown pipe fallback (for older files or other sections)
    if len(jobs) == 0:
        print("   [DEBUG] No HTML rows found. Trying Markdown pipe fallback...")
        lines = md_content.split('\n')
        for line in lines:
            if "|" in line and "---" not in line:
                parts = line.split("|")
                if len(parts) > 3:
                    # Basic markdown parsing logic...
                    pass
                    
    return jobs

def extract_text_from_html(html_fragment):
    # Remove tags
    text = re.sub(r'<[^>]+>', '', html_fragment)
    # Decode entities if needed (basic ones)
    text = text.replace('&amp;', '&').replace('&nbsp;', ' ')
    return text.strip()

def extract_text(cell):
    # Remove markdown links [text](url) -> text
    cell = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', cell)
    # Remove HTML tags (including <br>, <br/>, <br />)
    cell = re.sub(r'<[^>]+>', ' ', cell)
    # Remove bold/italic
    cell = cell.replace('**', '').replace('*', '').replace('↳', '').strip()
    return cell.strip()

if __name__ == "__main__":
    jobs = fetch_github_jobs()
