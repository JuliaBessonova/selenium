import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    # print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def check_stickers(products):
    for product in products:
        stickers = product.find_elements(By.CSS_SELECTOR, "div.sticker")
        assert len(stickers) == 1, f"The number of stickers is {len(stickers)}"


def test_check_product_stickers(driver):
    driver.get("http://localhost/litecart/")

    most_popular_products = driver.find_elements(By.CSS_SELECTOR, "div#box-most-popular li.product")
    check_stickers(most_popular_products)

    campaigns = driver.find_elements(By.CSS_SELECTOR, "div#box-campaigns li.product")
    check_stickers(campaigns)

    latest_products = driver.find_elements(By.CSS_SELECTOR, "div#box-latest-products li.product")
    check_stickers(latest_products)