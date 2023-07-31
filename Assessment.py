import requests
from bs4 import BeautifulSoup
import re


def is_valid_wiki_link(link):
    return bool(re.match(r'^https://en.wikipedia.org/wiki/.+$', link))


def get_unique_links(url, visited_links):
    unique_links = set()
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        for anchor in soup.find_all('a', href=True):
            href = anchor['href']
            if is_valid_wiki_link(href):
                full_link = f"https://en.wikipedia.org{href}"
                if full_link not in visited_links:
                    unique_links.add(full_link)
                    if len(unique_links) >= 10:
                        break
    except requests.exceptions.RequestException:
        print(f"Error: Unable to access {url}")
    return unique_links


def main():
    wikipedia_link = input("Enter a valid Wikipedia link: ")
    if not is_valid_wiki_link(wikipedia_link):
        raise ValueError("Error: Invalid Wikipedia link!")

    n = int(input("Enter a valid integer between 1 and 3: "))
    if not 1 <= n <= 3:
        raise ValueError("Error: Invalid value for n!")

    visited_links = set()
    new_links = [wikipedia_link]

    for cycle in range(n):
        unique_links = set()
        for link in new_links:
            unique_links.update(get_unique_links(link, visited_links))
        visited_links.update(unique_links)
        new_links = list(unique_links)

    print(f"Total Wikipedia Links Found: {len(visited_links)}")
    print(f"Unique Wikipedia Links Found: {len(new_links)}")
    print("All Wikipedia Links:")
    for link in visited_links:
        print(link)


if __name__ == "__main__":
    main()
