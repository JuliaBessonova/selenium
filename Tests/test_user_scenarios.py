import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    #letters = string.ascii_letters + string.digits
    return ''.join(random.choice(string.digits) for i in range(length))


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

    campaigns_regular_price_color = campaigns_product.find_element(By.CSS_SELECTOR, "s.regular-price").value_of_css_property("color").strip("rgba()").split(",")

    assert int(campaigns_regular_price_color[0].strip()) == int(campaigns_regular_price_color[1].strip()) == int(campaigns_regular_price_color[2].strip()), "Regular price is not grey"
    assert "line-through" in campaigns_product.find_element(By.CSS_SELECTOR, "s.regular-price").value_of_css_property("text-decoration"), "Regular price text-decoration in campaigns block does not contain line-through"

    campaigns_campaign_price_color = campaigns_product.find_element(By.CSS_SELECTOR, "strong.campaign-price").value_of_css_property("color").strip("rgba()").split(",")
    
    assert int(campaigns_campaign_price_color[0].strip()) != 0 and int(campaigns_campaign_price_color[1].strip()) == 0 and int(campaigns_campaign_price_color[2].strip()) == 0, "Campaign price color is not red"
    assert int(campaigns_product.find_element(By.CSS_SELECTOR, "strong.campaign-price").value_of_css_property("font-weight")) >= 700, "Campaign price font-weight in campaigns block is not equal to 900"

    campaign_price_size = float(campaigns_product.find_element(By.CSS_SELECTOR, "strong.campaign-price").value_of_css_property("font-size")[:-2])
    regular_price_size = float(campaigns_product.find_element(By.CSS_SELECTOR, "s.regular-price").value_of_css_property("font-size")[:-2])

    assert campaign_price_size > regular_price_size, f"Campaign price height {campaign_price_size} is not larger than regular price height {regular_price_size}"

    campaigns_product.click()

    product_page_name = driver.find_element(By.CSS_SELECTOR, "h1.title").text
    product_regular_price = driver.find_element(By.CSS_SELECTOR, "s.regular-price").text
    product_campaign_price = driver.find_element(By.CSS_SELECTOR, "strong.campaign-price").text

    assert campaigns_product_name == product_page_name, f"Names in campaigns block {campaigns_product_name} and on product page {product_page_name} are not equal"
    assert campaigns_regular_price == product_regular_price, f"Regular prices in campaigns block {campaigns_regular_price} and on product page {product_regular_price} are not equal"
    assert campaigns_campaign_price == product_campaign_price, f"Campaign prices in campaigns block {campaigns_campaign_price} and on product page {product_campaign_price} are not equal"

    product_page_regular_price_color = driver.find_element(By.CSS_SELECTOR, "s.regular-price").value_of_css_property("color").strip("rgba()").split(",")

    assert int(product_page_regular_price_color[0].strip()) == int(product_page_regular_price_color[1].strip()) == int(product_page_regular_price_color[2].strip()), "Regular price is not grey"
    assert "line-through" in driver.find_element(By.CSS_SELECTOR, "s.regular-price").value_of_css_property("text-decoration"), "Regular price text-decoration on product page does not contain line-through"

    product_page_price_color = driver.find_element(By.CSS_SELECTOR, "strong.campaign-price").value_of_css_property("color").strip("rgba()").split(",")

    assert int(product_page_price_color[0].strip()) != 0 and int(product_page_price_color[1].strip()) == 0 and int(product_page_price_color[2].strip()) == 0, "Campaign price color is not red"
    assert int(driver.find_element(By.CSS_SELECTOR, "strong.campaign-price").value_of_css_property("font-weight")) >= 700, "Campaign price font-weight on product page is not equal to 700"

    product_page_regular_price_size = float(driver.find_element(By.CSS_SELECTOR, "s.regular-price").value_of_css_property("font-size")[:-2])
    product_page_campaign_price_size = float(driver.find_element(By.CSS_SELECTOR, "strong.campaign-price").value_of_css_property("font-size")[:-2])

    assert product_page_campaign_price_size > product_page_regular_price_size, f"Campaign price height {product_page_campaign_price_size} is not larger than regular price height {product_page_regular_price_size}"



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
    driver.find_element(By.CSS_SELECTOR, "span.select2-selection__rendered").click()
    driver.find_element(By.CSS_SELECTOR, "input.select2-search__field").send_keys("United States")
    driver.find_element(By.CSS_SELECTOR, "li.select2-results__option--highlighted").click()
    driver.find_element(By.CSS_SELECTOR, "input[name=email]").send_keys(email)
    driver.find_element(By.CSS_SELECTOR, "input[name=phone]").send_keys("11111111111")
    driver.find_element(By.CSS_SELECTOR, "input[name=password]").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "input[name=confirmed_password]").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[name=create_account]").click()
    driver.find_element(By.LINK_TEXT, "Logout").click()

    driver.find_element(By.CSS_SELECTOR, "input[name=email]").send_keys(email)
    driver.find_element(By.CSS_SELECTOR, "input[name=password]").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[name=login]").click()
    driver.find_element(By.LINK_TEXT, "Logout").click()


def test_add_and_delete_items_from_cart(driver):
    driver.get("http://localhost/litecart/")

    wait = WebDriverWait(driver, 2)
    cart_quantity = int(driver.find_element(By.CSS_SELECTOR, "div#cart-wrapper span.quantity").text)

    while cart_quantity < 3:
        driver.find_element(By.CSS_SELECTOR, "div#box-most-popular li:nth-child(1)").click()
        driver.find_element(By.CSS_SELECTOR, "button[name=add_cart_product]").click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "div#cart-wrapper span.quantity"), str(cart_quantity + 1)))
        cart_quantity += 1
        driver.find_element(By.CSS_SELECTOR, "div.content nav#breadcrumbs li:nth-child(1)").click()

    driver.find_element(By.CSS_SELECTOR, "div#cart a.link").click()

    data_table = driver.find_element(By.CSS_SELECTOR, "table.dataTable")
    lines_in_table = len(driver.find_elements(By.CSS_SELECTOR, "table.dataTable td.item"))

    while lines_in_table > 1:
        driver.find_element(By.CSS_SELECTOR, "button[name=remove_cart_item]").click()
        wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "table.dataTable td.item")) == lines_in_table - 1)
        lines_in_table -=1

    driver.find_element(By.CSS_SELECTOR, "button[name=remove_cart_item]").click()
    wait.until(EC.staleness_of(data_table))