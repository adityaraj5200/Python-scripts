import requests
from bs4 import BeautifulSoup
import pandas as pd

# List of target company career URLs
COMPANIES = {
    "Visa": "https://careers.smartrecruiters.com/Visa",
    "Atlassian": "https://www.atlassian.com/company/careers/all-jobs",
    "Nvidia": "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite",
}

# Keywords to search for
KEYWORDS = ["Software Engineer", "Backend", "Java", "Developer"]

results = []

for company, url in COMPANIES.items():
    try:
        print(f"Checking {company}...")
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            print(f"Failed to fetch {url}")
            continue

        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.get_text(" ", strip=True)

        for kw in KEYWORDS:
            if kw.lower() in text.lower():
                results.append({"Company": company, "Keyword": kw, "URL": url})
                break
    except Exception as e:
        print(f"Error scraping {company}: {e}")

# Save results
df = pd.DataFrame(results)
df.to_csv("jobs.csv", index=False)
print("✅ Scraping complete. Results saved in jobs.csv")
