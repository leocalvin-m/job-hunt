from bs4 import BeautifulSoup
import os

def extract_job_info(job_html_path):
    with open(job_html_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'lxml')
    
    title = soup.find('h1', class_='heading').get_text(strip=True)
    summary = soup.find('h5', class_='subheading').find_next_sibling('p').get_text(strip=True)[:150] + "..."
    
    return title, summary

def create_job_card(title, summary, link):
    return f'''
    <div class="card mb-4 job-card">
        <div class="card-body">
            <h5 class="card-title">{title}</h5>
            <p class="card-text">{summary}</p>
            <a href="{link}" class="btn btn-primary" target="_blank">Read More</a>
        </div>
    </div>
    '''

def insert_cards_into_index(cards_html, index_html_path):
    with open(index_html_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'lxml')
    
    cards_column = soup.find('div', class_='col-lg-6')
    for card_html in cards_html:
        card_soup = BeautifulSoup(card_html, 'html.parser')
        cards_column.append(card_soup)
    
    with open(index_html_path, 'w', encoding='utf-8') as file:
        file.write(str(soup.prettify()))

# Configuration
index_html_path = './index.html'
job_html_dir = './html/'

cards_html = []
for filename in os.listdir(job_html_dir):
    if filename.endswith('.html'):
        title, summary = extract_job_info(os.path.join(job_html_dir, filename))
        card_html = create_job_card(title, summary, f'html/{filename}')
        cards_html.append(card_html)

insert_cards_into_index(cards_html, index_html_path)

print("Job cards successfully inserted into index.html.")
