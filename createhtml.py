import pandas as pd
import os
import markdown

def sanitize_filename(text):
    # Replace invalid file name characters with "_"
    return "".join([c if c.isalnum() or c in [' ', '.', '_'] else "_" for c in text])

def process_description(description):
    # Convert description from Markdown to HTML using the markdown package
    if pd.isna(description):
        return ""  # Return an empty string or some default text for missing descriptions
    else:
        return markdown.markdown(str(description))

def create_html_file(title, company, description, job_url, filename, index, total_jobs, output_dir, df):
    processed_description = process_description(description)
    prev_filename = f"{index-1}_{sanitize_filename(df.iloc[index-1]['title'])}_{sanitize_filename(df.iloc[index-1]['company'])}.html" if index > 0 else None
    next_filename = f"{index+1}_{sanitize_filename(df.iloc[index+1]['title'])}_{sanitize_filename(df.iloc[index+1]['company'])}.html" if index < total_jobs-1 else None

    prev_page = prev_filename if prev_filename else "#"
    next_page = next_filename if next_filename else "#"

    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} at {company} - JobHunt Careers</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .subheading {{
            background-color: #007bff;
            color: white;
            padding: 5px;
            margin-bottom: 5px;
        }}
        .navigation {{
            margin-bottom: 20px;
        }}
        .navigation a {{
            margin-right: 10px;
        }}
    </style>
</head>
<body class="bg-light">
    <div class="container mt-5">
        <h1 class="text-center text-primary mb-4">JobHunt Careers</h1>
        <div class="navigation">
            <a href="{prev_page}">Previous</a>
            <a href="{next_page}">Next</a>
        </div>

        <div class="card mb-4">
            <div class="card-body">
                <h1 class="heading">{company}</h1>
                <p class="card-text"></p>
                <h5 class="subheading">Position Summary</h5>
                <p>{title}</p>
                <h5 class="subheading">Description & Requirements</h5>
                {processed_description}
                <a href="{job_url}" class="btn btn-primary" target="_blank">Apply Now</a>
            </div>
        </div>

        <div class="copyright">
            © 2024 JobHunt. All rights reserved.
        </div>
    </div>
</body>
</html>"""

    with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as file:
        file.write(html_content)

def create_html_files(df, output_dir='./html'):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    total_jobs = len(df)
    for index, row in df.iterrows():
        title = sanitize_filename(row['title'])
        company = sanitize_filename(row['company'])
        description = row['description'] if 'description' in row else "No description provided"
        
        # Generate a sanitized filename
        filename = f"{index}_{title}_{company}.html"
        
        # Create HTML file for each job listing
        create_html_file(row['title'], row['company'], description, row['job_url'], filename, index, total_jobs, output_dir, df)
        
        print(f"Generated HTML file: {filename}")

# Assuming 'jobs.csv' is your CSV file path
csv_file_path = './jobs.csv'  # Update this path to your CSV file
df = pd.read_csv(csv_file_path)

# Call the function to generate HTML files
create_html_files(df)
