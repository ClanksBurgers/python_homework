from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pandas as pd
import json
import time


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"
driver.get(url)
print(f"Loaded page: {url}")

search_result_li_class = "cp-search-result-item"
title_class = "title-content"
author_class = "author-link"
format_year_container_class = "cp-format-indicator"
format_year_class = "cp-biblio-description"

results = []

li_elements = driver.find_elements(By.CSS_SELECTOR, f"li.{search_result_li_class}")
print(f"\nFound {len(li_elements)} search result items")

for i, li in enumerate(li_elements):
    try:
        title_element = li.find_element(By.CSS_SELECTOR, f".{title_class}")
        title = title_element.text
        print(f"Title: {title}")
        
        author_elements = li.find_elements(By.CSS_SELECTOR, f"a.{author_class}")
        
        authors = [author.text for author in author_elements if author.text.strip()]
        author_text = "; ".join(authors)
        print(f"Authors: {author_text}")
        
        format_year = ""
        try:
            format_year_container = li.find_element(By.CSS_SELECTOR, f".{format_year_container_class}")
            format_year_element = format_year_container.find_element(By.CSS_SELECTOR, f".{format_year_class}")
            format_year = format_year_element.text
        except:
            try:
                format_year_container = li.find_element(By.CSS_SELECTOR, f".{format_year_container_class}")
                format_year = format_year_container.text
            except:
                format_year = "N/A"
        
        print(f"Format-Year: {format_year}")
        
        book_dict = {
            "Title": title,
            "Author": author_text,
            "Format-Year": format_year
        }
        
        results.append(book_dict)
        print(f"✓ Successfully added to results")
        
    except Exception as e:
        print(f"✗ Error processing result {i+1}: {e}")
        continue

print(f"\n{'='*50}")
print(f"Total results collected: {len(results)}")
print(f"{'='*50}\n")

if results:
    df = pd.DataFrame(results)
    print(df)
    
    df.to_csv("get_books.csv", index=False)
    print("\nResults saved to get_books.csv")
    
    with open("get_books.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("Results saved to get_books.json")
else:
    print("No results were collected. Check your CSS selectors from Task 2.")

driver.quit()
print("\nDriver closed.")
