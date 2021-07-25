import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def get_url(search_term):
    template = "https://www.amazon.in/s?k={}&ref=nb_sb_noss_2"
    search_term = search_term.replace(" ", "+")

    url = template.format(search_term)
    url += "&page{}"
    return url


def extract_record(item):
    atag = item.h2.a
    description = atag.text.strip()
    product_url = "https://www.amazon.in" + atag.get("href")
    try:
        price_parent = item.find("span", "a-price")
        price = price_parent.find("span", "a-offscreen").text
    except AttributeError:
        return
    try:
        rating = item.i.text
    except AttributeError:
        rating = ""

    result = (description, price, rating, product_url)
    return result


def main(search_term):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    record = []
    url = get_url(search_term)
    try:
        for page in range(1, 21):
            driver.get(url.format(page))
            soup = BeautifulSoup(driver.page_source, "html.parser")
            results = soup.find_all("div", {"data-component-type": "s-search-result"})

            for item in results:
                record = extract_record(item)
                if record:
                    records.append(record)
    except AttributeError:
        return
    driver.close()

    with open(
        "OutputCSV/ultrawide-monitor.csv", "w", newline="", encoding="utf-8"
    ) as f:
        writer = csv.writer(f)
        writer.writerow(["Description", "Price", "Rating", "Product URL"])
        writer.writerows(records)


main("ultrawide monitor")
