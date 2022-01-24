from bs4 import BeautifulSoup
import requests
import smtplib
import os


url = "https://www.amazon.com.br/%C5%92uvres-Cioran/dp/2070741664/ref=tmm_mmp_swatch_0?_encoding=UTF8&qid=&sr="
max_price = 500

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Accept-Language": "pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7",
}

response = requests.get(url=url, headers=header)
response.raise_for_status()
web_page = response.text

soup = BeautifulSoup(markup=web_page, features="html.parser")
product = [soup.find(name="span", id="productTitle").getText(),
           soup.find(name="span", id="productSubtitle").getText()]
for price in soup.find_all(name="a", class_="a-size-mini a-link-normal"):
    product.append(price.getText().split()[-1])

for price in product[2:]:
    if float(price.replace(",", ".")) <= max_price:
        with smtplib.SMTP(host="smtp.gmail.com") as connection:
            connection.starttls()
            connection.command_encoding = "utf-8"
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=EMAIL,
                                to_addrs=EMAIL,
                                msg=f"Subject:Amazon price alert!\n\n"
                                    f"{' '.join(product[:2])} por apenas R${price}\n{url}".encode())
