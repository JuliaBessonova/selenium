import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import random
import string


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


def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))


def test_check_product_stickers(driver):
    driver.get("http://localhost/litecart/")

    most_popular_products = driver.find_elements(By.CSS_SELECTOR, "div#box-most-popular li.product")
    check_stickers(most_popular_products)

    campaigns = driver.find_elements(By.CSS_SELECTOR, "div#box-campaigns li.product")
    check_stickers(campaigns)

    latest_products = driver.find_elements(By.CSS_SELECTOR, "div#box-latest-products li.product")
    check_stickers(latest_products)


def test_check_product_information(driver):
    driver.get("http://localhost/litecart/")

    campaigns_product = driver.find_element(By.CSS_SELECTOR, "div#box-campaigns li:nth-child(1)")
    campaigns_product_name = campaigns_product.find_element(By.CSS_SELECTOR, "div.name").text
    campaigns_regular_price = campaigns_product.find_element(By.CSS_SELECTOR, "s.regular-price").text
    campaigns_campaign_price = campaigns_product.find_element(By.CSS_SELECTOR, "strong.campaign-price").text

    assert "119, 119, 119" in campaigns_product.find_element(By.CSS_SELECTOR, "s.regular-price").value_of_css_property("color"), "Regular price color in campaigns block contains (119, 119, 119)"
    assert "line-through" in campaigns_product.find_element(By.CSS_SELECTOR, "s.regular-price").value_of_css_property("text-decoration"), "Regular price text-decoration in campaigns block does not contain line-through"
    assert "204, 0, 0" in campaigns_product.find_element(By.CSS_SELECTOR, "strong.campaign-price").value_of_css_property("color"), "Campaign price color in campaigns block contains (204, 0, 0)"
    assert int(campaigns_product.find_element(By.CSS_SELECTOR, "strong.campaign-price").value_of_css_property("font-weight")) >= 700, "Campaign price font-weight in campaigns block is not equal to 900"

    regular_price_size = campaigns_product.find_element(By.CSS_SELECTOR, "s.regular-price").size
    campaign_price_size = campaigns_product.find_element(By.CSS_SELECTOR, "strong.campaign-price").size

    assert campaign_price_size['height'] > regular_price_size['height'], f"Campaign price height {campaign_price_size['height']} is not larger than regular price height {regular_price_size['height']}"
    assert campaign_price_size['width'] > regular_price_size['width'], f"Campaign price width {campaign_price_size['width']} is not larger than regular price width {regular_price_size['width']}"

    campaigns_product.click()

    product_page_name = driver.find_element(By.CSS_SELECTOR, "h1.title").text
    product_regular_price = driver.find_element(By.CSS_SELECTOR, "s.regular-price").text
    product_campaign_price = driver.find_element(By.CSS_SELECTOR, "strong.campaign-price").text

    assert campaigns_product_name == product_page_name, f"Names in campaigns block {campaigns_product_name} and on product page {product_page_name} are not equal"
    assert campaigns_regular_price == product_regular_price, f"Regular prices in campaigns block {campaigns_regular_price} and on product page {product_regular_price} are not equal"
    assert campaigns_campaign_price == product_campaign_price, f"Campaign prices in campaigns block {campaigns_campaign_price} and on product page {product_campaign_price} are not equal"

    assert "102, 102, 102" in driver.find_element(By.CSS_SELECTOR, "s.regular-price").value_of_css_property("color"), "Regular price color on product page coontains (102, 102, 102)"
    assert "line-through" in driver.find_element(By.CSS_SELECTOR, "s.regular-price").value_of_css_property("text-decoration"), "Regular price text-decoration on product page does not contain line-through"
    assert "204, 0, 0" in driver.find_element(By.CSS_SELECTOR, "strong.campaign-price").value_of_css_property("color"), "Campaign price color on product page contains (204, 0, 0)"
    assert int(driver.find_element(By.CSS_SELECTOR, "strong.campaign-price").value_of_css_property("font-weight")) >= 700, "Campaign price font-weight on product page is not equal to 700"

    product_page_regular_price_size = driver.find_element(By.CSS_SELECTOR, "s.regular-price").size
    product_page_campaign_price_size = driver.find_element(By.CSS_SELECTOR, "strong.campaign-price").size

    assert product_page_campaign_price_size['height'] > product_page_regular_price_size['height'], f"Campaign price height {product_page_campaign_price_size['height']} is not larger than regular price height {product_page_regular_price_size['height']}"
    assert product_page_campaign_price_size['width'] > product_page_regular_price_size['width'], f"Campaign price width {product_page_campaign_price_size['width']} is not larger than regular price width {product_page_regular_price_size['width']}"


def test_create_new_user_account(driver):
    randstring = generate_random_string(10)
    email = "testuser" + randstring + "@test.com"
    password = "Tester01"

    driver.get("http://localhost/litecart/")
    driver.find_element(By.CSS_SELECTOR, "table tr:nth-child(5)").click()

    driver.find_element(By.CSS_SELECTOR, "input[name=firstname]").send_keys("Ivan")
    driver.find_element(By.CSS_SELECTOR, "input[name=lastname]").send_keys("Ivanov")
    driver.find_element(By.CSS_SELECTOR, "input[name=address1]").send_keys("address")
    driver.find_element(By.CSS_SELECTOR, "input[name=postcode]").send_keys("12345")
    driver.find_element(By.CSS_SELECTOR, "input[name=city]").send_keys("New York")
    select = Select(driver.find_element(By.CSS_SELECTOR, "select[name=country_code]"))
    select.select_by_visible_text("United States")
    driver.find_element(By.CSS_SELECTOR, "input[name=email]").send_keys(email)
    driver.find_element(By.CSS_SELECTOR, "input[name=phone]").send_keys("11111111111")
    driver.find_element(By.CSS_SELECTOR, "input[name=password]").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "input[name=confirmed_password]").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[name=create_account]").click()
    driver.find_element(By.CSS_SELECTOR, "div#box-account li:nth-child(4)").click()

    driver.find_element(By.CSS_SELECTOR, "input[name=email]").send_keys(email)
    driver.find_element(By.CSS_SELECTOR, "input[name=password]").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[name=login]").click()
    driver.find_element(By.CSS_SELECTOR, "div#box-account li:nth-child(4)").click()
