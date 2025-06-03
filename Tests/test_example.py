import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    # print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def login_as_admin(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin")
    driver.find_element(By.NAME, "login").click()


def find_title(driver):
    driver.find_element(By.TAG_NAME, "h1")


def test_check_admin_navigation_menu(driver):
    login_as_admin(driver)

    driver.find_element(By.LINK_TEXT, "Appearence").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-template").click() 
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-logotype").click()
    find_title(driver)

    driver.find_element(By.LINK_TEXT, "Catalog").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-catalog").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-product_groups").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-option_groups").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-manufacturers").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-suppliers").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-delivery_statuses").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-sold_out_statuses").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-quantity_units").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-csv").click()
    find_title(driver)

    driver.find_element(By.LINK_TEXT, "Countries").click()
    find_title(driver)

    driver.find_element(By.LINK_TEXT, "Currencies").click()
    find_title(driver)

    driver.find_element(By.LINK_TEXT, "Customers").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-customers").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-csv").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-newsletter").click()
    find_title(driver)

    driver.find_element(By.LINK_TEXT, "Geo Zones").click()
    find_title(driver)

    driver.find_element(By.LINK_TEXT, "Languages").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-languages").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-storage_encoding").click()
    find_title(driver)

    driver.find_element(By.LINK_TEXT, "Modules").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-jobs").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-customer").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-shipping").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-payment").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-order_total").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-order_success").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-order_action").click()
    find_title(driver)

    driver.find_element(By.LINK_TEXT, "Orders").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-orders").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-order_statuses").click()
    find_title(driver)

    driver.find_element(By.LINK_TEXT, "Pages").click()
    find_title(driver)

    driver.find_element(By.LINK_TEXT, "Reports").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-monthly_sales").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-most_sold_products").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-most_shopping_customers").click()
    find_title(driver)

    driver.find_element(By.LINK_TEXT, "Settings").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-store_info").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-defaults").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-general").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-listings").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-images").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-checkout").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-advanced").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-security").click()
    find_title(driver)

    driver.find_element(By.LINK_TEXT, "Slides").click()
    find_title(driver)

    driver.find_element(By.LINK_TEXT, "Tax").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-tax_classes").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-tax_rates").click()
    find_title(driver)

    driver.find_element(By.LINK_TEXT, "Translations").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-search").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-scan").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-csv").click()
    find_title(driver)

    driver.find_element(By.LINK_TEXT, "Users").click()
    find_title(driver)

    driver.find_element(By.LINK_TEXT, "vQmods").click()
    find_title(driver)
    driver.find_element(By.CSS_SELECTOR, "li#doc-vqmods").click()
    find_title(driver)
