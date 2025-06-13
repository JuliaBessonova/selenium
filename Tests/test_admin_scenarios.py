import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


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

