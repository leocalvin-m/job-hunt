import os
from bs4 import BeautifulSoup

def correct_html_files(input_dir):
    # List all HTML files in the input directory
    html_files = [f for f in os.listdir(input_dir) if f.endswith('.html')]
    
    for filename in html_files:
        file_path = os.path.join(input_dir, filename)
        
        # Read the HTML content
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
        
        # Convert to string for processing
        html_content = str(soup)
        
        # Correct **text** to <h2>text</h2>
        while '**' in html_content:
            start_index = html_content.find('**')
            end_index = html_content.find('**', start_index + 2)
            if start_index != -1 and end_index != -1:
                text_to_convert = html_content[start_index+2:end_index]
                html_content = html_content[:start_index] + '<h2>' + text_to_convert + '</h2>' + html_content[end_index+2:]
            else:
                break  # Exit loop if no matching ** found
        
        # Correct *text* to <li>text</li>
        # This simplistic approach may convert unintended * instances. A more robust markdown parser might be needed for complex cases.
        html_content = html_content.replace('*', '<li>', 1).replace('*', '</li>', 1)
        
        # Parse the corrected HTML content again
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Write the corrected HTML content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup.prettify()))
        
        print(f"Corrected HTML file: {file_path}")

# Specify the directory containing the HTML files to correct
input_dir = './html'  # Adjust this to your directory
correct_html_files(input_dir)
