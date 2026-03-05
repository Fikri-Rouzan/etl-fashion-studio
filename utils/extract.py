import requests
import logging
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

logger = logging.getLogger(__name__)


def extract_data(base_url, total_pages=50):
    try:
        all_products = []
        execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        logger.info(f"Starting the extraction process from {total_pages} pages...")

        for page in range(1, total_pages + 1):
            try:
                if page == 1:
                    url = base_url
                else:
                    url = f"{base_url}/page{page}"

                response = requests.get(url, headers=headers, timeout=10)

                if response.status_code != 200:
                    url_alt = f"{base_url}/page/{page}"
                    response = requests.get(url_alt, headers=headers, timeout=10)

                if response.status_code != 200:
                    logger.error(
                        f"Failed to fetch page {page} (Status: {response.status_code})"
                    )
                    continue

                soup = BeautifulSoup(response.content, "html.parser")
                products = soup.find_all("div", class_="collection-card")

                if not products:
                    logger.warning(f"No products found on page {page}")
                    continue

                for product in products:
                    try:
                        title_tag = product.find("h3", class_="product-title")
                        title = (
                            title_tag.text.strip() if title_tag else "Unknown Product"
                        )
                        price_tag = product.find("span", class_="price")
                        price = price_tag.text.strip() if price_tag else None
                        details_container = product.find(
                            "div", class_="product-details"
                        )
                        rating = None
                        colors = None
                        size = None
                        gender = None

                        if details_container:
                            paragraphs = details_container.find_all("p")
                            for p in paragraphs:
                                text = p.text.strip()
                                if "Rating" in text or "/ 5" in text:
                                    rating = text
                                elif "Colors" in text:
                                    colors = text
                                elif "Size" in text:
                                    size = text
                                elif "Gender" in text:
                                    gender = text

                        all_products.append(
                            {
                                "Title": title,
                                "Price": price,
                                "Rating": rating,
                                "Colors": colors,
                                "Size": size,
                                "Gender": gender,
                                "timestamp": execution_time,
                            }
                        )

                    except Exception as e:
                        logger.error(
                            f"An error occurred while parsing the product on the page {page}: {e}"
                        )
                        continue

                if page % 10 == 0:
                    logger.info(
                        f"Page {page} completed. Total data collected so far: {len(all_products)}"
                    )

            except Exception as e:
                logger.error(f"Fatal error on page {page}: {e}")
                continue

        logger.info(
            f"Extraction complete. Total raw data obtained: {len(all_products)}"
        )
        return pd.DataFrame(all_products)
    except Exception as e:
        logger.error(f"The extraction process failed completely: {e}")
        return pd.DataFrame()
