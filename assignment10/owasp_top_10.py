from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

# TASK 6: Scraping Structured Data - OWASP Top 10

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url = "https://owasp.org/Top10/2025/"
driver.get(url)
print(f"Loaded page: {url}")

results = []

try:
    wait = WebDriverWait(driver, 10)
    vulnerability_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//ol//li//a[contains(@href, '/Top10/')]")))
    print(f"\nFound {len(vulnerability_elements)} vulnerabilities")
    
    for i, link_element in enumerate(vulnerability_elements[:10]):
        try:
            title = link_element.text
            href = link_element.get_attribute("href")
            
            if title and href:
                print(f"{i+1}. {title}")
                print(f"   Link: {href}")
                
                vuln_dict = {
                    "Title": title,
                    "Link": href
                }
                results.append(vuln_dict)
            
        except Exception as e:
            print(f"Error processing element {i+1}: {e}")
            continue

except Exception as e:
    print(f"Error finding vulnerability elements: {e}")

print(f"\n{'='*60}")
print(f"Total vulnerabilities collected: {len(results)}")
print(f"{'='*60}\n")

print("Results:")
for vuln in results:
    print(f"  {vuln['Title']}")
    print(f"  {vuln['Link']}\n")

if results:
    df = pd.DataFrame(results)
    print("\nDataFrame:")
    print(df)
    
    df.to_csv("owasp_top_10.csv", index=False)
    print("\nResults saved to owasp_top_10.csv")
else:
    print("No results were collected. Check your XPath selectors.")

driver.quit()
print("\nDriver closed.")
