import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import random
import string
import os


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    # print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def login_as_admin(driver, link):
    driver.get(link)
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin")
    driver.find_element(By.NAME, "login").click()


def find_title(driver):
    driver.find_element(By.TAG_NAME, "h1")


def generate_random_string(length):
    return ''.join(random.choice(string.digits) for i in range(length))


def test_check_admin_navigation_menu(driver):
    login_as_admin(driver, "http://localhost/litecart/admin/")

    sections = driver.find_elements(By.CSS_SELECTOR, "ul#box-apps-menu li span.name")
    names = []

    for section in sections:
        names.append(section.text)

    for name in names:
        driver.find_element(By.LINK_TEXT, name).click()
        find_title(driver)

        subs = driver.find_elements(By.CSS_SELECTOR, "ul.docs li span.name")
        subs_names = []
        if subs != []:
            for sub in subs:
                subs_names.append(sub.text)

        if subs_names != []:
            for name in subs_names:
                driver.find_element(By.LINK_TEXT, name).click()
                find_title(driver)

    
def test_check_countries_and_zones_lists(driver):
    login_as_admin(driver, "http://localhost/litecart/admin/?app=countries&doc=countries")
    rows = driver.find_elements(By.CSS_SELECTOR, "tr.row")

    countries = []
    rows_with_zones = []

    for row in rows:
        countries.append(row.find_element(By.CSS_SELECTOR, "td:nth-child(5) a").text)

        if row.find_element(By.CSS_SELECTOR, "td:nth-child(6)").text != '0':
            rows_with_zones.append(row.find_element(By.CSS_SELECTOR, "td:nth-child(5) a").get_attribute("href"))

    assert countries == sorted(countries), f"The list of countries {countries} is not alphabetically sorted"

    for link in rows_with_zones:
        driver.get(link)
        country_zones = []
        zones = driver.find_elements(By.CSS_SELECTOR, "table.dataTable tr td:nth-child(3)")
        for zone in zones:
            if zone.text != '':
                country_zones.append(zone.text)

        assert country_zones == sorted(country_zones), f"The list of zones {country_zones} is not alphabetically sorted"



def test_check_country_zones_sorting(driver):
    login_as_admin(driver, "http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones")

    country_links = []
    rows = driver.find_elements(By.CSS_SELECTOR, "tr.row td:nth-child(3) a")

    for row in rows:
        country_links.append(row.get_attribute("href"))

    for link in country_links:
        driver.get(link)
        zone_list = []
        zones = driver.find_elements(By.CSS_SELECTOR, "table.dataTable tr td:nth-child(3) option[selected=selected]")
        for zone in zones:
            zone_list.append(zone.text)

        assert zone_list == sorted(zone_list), f"The list of zones {zone_list} is not alphabetically sorted"


def test_add_product_to_a_catalog(driver):
    login_as_admin(driver, "http://localhost/litecart/admin/")

    path_to_file = os.path.abspath('./flower.jpeg')
    product_name = "Product name" + generate_random_string(5)

    driver.find_element(By.CSS_SELECTOR, "ul#box-apps-menu li:nth-child(2) a").click()
    driver.find_element(By.CSS_SELECTOR, "td#content div a:nth-child(2)").click()

    # заполняем вкладку General
    driver.find_element(By.CSS_SELECTOR, "input[name=status][value='1']").click()
    driver.find_element(By.CSS_SELECTOR, "input[name='name[en]']").send_keys(product_name)
    driver.find_element(By.CSS_SELECTOR, "input[name=code]").send_keys("123")
    driver.find_element(By.CSS_SELECTOR, "input[data-name='Rubber Ducks']").click()
    driver.find_element(By.CSS_SELECTOR, "input[name='product_groups[]'][value='1-3']").click()
    driver.find_element(By.CSS_SELECTOR, "input[name=quantity]").clear()
    driver.find_element(By.CSS_SELECTOR, "input[name=quantity]").send_keys("10")
    driver.find_element(By.CSS_SELECTOR, "input[name='new_images[]']").send_keys(path_to_file)

    # календарик
    date_from_element = driver.find_element(By.CSS_SELECTOR, "input[name=date_valid_from]")
    date_from_element.clear()
    date_from_element.send_keys("2025-07-14")
    date_from_element.click()

    date_to_element = driver.find_element(By.CSS_SELECTOR, "input[name=date_valid_to]")
    date_to_element.clear()
    date_to_element.send_keys("2025-07-24")
    date_to_element.click()

    # переключаемся на вкладку Information
    driver.find_element(By.LINK_TEXT, "Information").click()
    wait = WebDriverWait(driver, 3)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#tab-information")))

    # заполняем вкладку Information
    manufacturer_select =  Select(driver.find_element(By.NAME, "manufacturer_id"))
    manufacturer_select.select_by_visible_text("ACME Corp.")
    driver.find_element(By.CSS_SELECTOR, "input[name=keywords]").send_keys("test product")
    driver.find_element(By.CSS_SELECTOR, "input[name='short_description[en]']").send_keys("short description")
    driver.find_element(By.CSS_SELECTOR, "div.trumbowyg-editor").send_keys("full description")
    driver.find_element(By.CSS_SELECTOR, "input[name='head_title[en]']").send_keys("product title")
    driver.find_element(By.CSS_SELECTOR, "input[name='meta_description[en]']").send_keys("meta description")

    # переключаемся на вкладку Prices
    driver.find_element(By.LINK_TEXT, "Prices").click()
    wait = WebDriverWait(driver, 3)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#tab-prices")))

    # заполняем вкладку Prices
    purchase_price = driver.find_element(By.CSS_SELECTOR, "input[name=purchase_price]")
    purchase_price.clear()
    purchase_price.send_keys("10")
    currency_select = Select(driver.find_element(By.NAME, "purchase_price_currency_code"))
    currency_select.select_by_visible_text("US Dollars")
    driver.find_element(By.CSS_SELECTOR, "input[name='prices[USD]']").send_keys("10")
    driver.find_element(By.CSS_SELECTOR, "input[name='gross_prices[USD]']").clear()
    driver.find_element(By.CSS_SELECTOR, "input[name='gross_prices[USD]']").send_keys("12")
    driver.find_element(By.CSS_SELECTOR, "input[name='prices[EUR]']").send_keys("7")
    driver.find_element(By.CSS_SELECTOR, "input[name='gross_prices[EUR]']").clear()
    driver.find_element(By.CSS_SELECTOR, "input[name='gross_prices[EUR]']").send_keys("9")

    # сохраняем созданный продукт
    driver.find_element(By.CSS_SELECTOR, "button[name=save]").click()
    wait = WebDriverWait(driver, 3)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "form[name=catalog_form]")))

    # проверяем, что созданный продукт появился в каталоге

    products_names = []
    products = driver.find_elements(By.CSS_SELECTOR, "tr.row td:nth-child(3) a")

    for product in products:
        products_names.append(product.text)

    assert product_name in products_names, f"Created product {product_name} is not in the catalog"


def test_check_links_open_in_new_window(driver):
    login_as_admin(driver, "http://localhost/litecart/admin/?app=countries&doc=countries")
    driver.find_element(By.CSS_SELECTOR, "#content a.button").click()

    external_links = driver.find_elements(By.CSS_SELECTOR, "a i.fa-external-link")

    main_window = driver.current_window_handle
    old_windows = driver.window_handles
    wait = WebDriverWait(driver, 2)

    for link in external_links:
        link.click()
        wait.until(lambda driver: len(driver.window_handles) > len(old_windows))

        handles = driver.window_handles
        for handle in handles:
            if handle != main_window:
                driver.switch_to.window(handle)
                driver.close()
                driver.switch_to.window(main_window)


def test_check_browser_log(driver):
    login_as_admin(driver, "http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1")

    links = []
    rows = driver.find_elements(By.CSS_SELECTOR, "table.dataTable td a[title=Edit]")

    for row in rows:
        links.append(row.get_attribute("href"))

    for link in links:
        driver.get(link)
        browser_log = driver.get_log("browser")

        assert len(browser_log) == 0, f"Page {link} contains messages in browser log: {browser_log}"
