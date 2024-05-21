import os
import unicodedata
from bs4 import BeautifulSoup
from string import ascii_letters, digits
import requests

def sanitize_filename(filename):
    valid_chars = "-_.() %s%s" % (ascii_letters, digits)
    filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
    return ''.join(c for c in filename if c in valid_chars)

def extract_topic_from_page(url):
    # Function to extract topic from the content of the web page
    # You can customize this function based on your specific requirements
    # This is just a simple example
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract text content from the page
        text = soup.get_text().lower()
        # List of keywords for various topics
        programming_keywords = ["programming", "code", "software", "developer", "algorithm", "python", "java", "c++", "javascript", "coding"]
        technology_keywords = ["technology", "tech", "innovation", "internet", "digital", "electronics", "devices", "computer", "science"]
        for keyword in programming_keywords:
            if keyword in text:
                return "Programming"
        for keyword in technology_keywords:
            if keyword in text:
                return "Technology"
        return "Other"
    except Exception as e:
        print(f"Error extracting topic from page '{url}': {e}")
        return "Other"

def merge_favorites(html_files, output_dir):
    all_links = {}
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            links = soup.find_all('a')
            for link in links:
                href = link.get('href')
                title = link.text
                topic = extract_topic_from_page(href)
                if topic not in all_links:
                    all_links[topic] = []
                all_links[topic].append((href, title))

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for topic, links in all_links.items():
        topic_dir = os.path.join(output_dir, topic)
        if not os.path.exists(topic_dir):
            os.makedirs(topic_dir)

        for link, title in links:
            # Sanitize the title for use as a filename
            filename = sanitize_filename(title)
            # Write links to individual files
            file_path = os.path.join(topic_dir, f'{filename}.url')
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('[InternetShortcut]\n')
                    f.write(f'URL={link}\n')
            except OSError as e:
                print(f"Error writing file '{file_path}': {e}")

def main():
    html_files = ['favorites1.html', 'favorites2.html', 'favorites3.html']
    output_dir = 'organized_favorites'

    merge_favorites(html_files, output_dir)

    print('Organized favorites created successfully.')

if __name__ == "__main__":
    main()
