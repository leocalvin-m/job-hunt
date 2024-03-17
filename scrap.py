import requests
from bs4 import BeautifulSoup

def scrape_indeed_jobs(search_term, location=""):
    base_url = "https://www.indeed.com/jobs"
    query_params = f"?q={search_term}&l={location}"
    response = requests.get(base_url + query_params)
    
    if response.status_code != 200:
        print("Failed to retrieve data")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    job_listings = soup.find_all('div', class_="jobsearch-SerpJobCard")
    
    jobs = []
    for listing in job_listings:
        title = listing.find('a', class_="jobtitle").text.strip()
        company = listing.find('span', class_="company").text.strip()
        summary = listing.find('div', class_="summary").text.strip()
        jobs.append({"title": title, "company": company, "summary": summary})
    
    return jobs

# Example usage
jobs = scrape_indeed_jobs("software engineer", "New York")
for job in jobs:
    print(job)
