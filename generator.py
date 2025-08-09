import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Form URL
form_url = "https://docs.google.com/forms/"

# Random data generators
def biased_random_choice():
    """Return 4 or 5 more frequently."""
    return random.choices([5, 4, 3, 2, 1], weights=[44, 40, 10, 3, 3])[0]

def random_choice(choices):
    return random.choice(choices)

def random_int(min_val, max_val):
    return random.randint(min_val, max_val)

# Function to click the "Next" button
def click_next(browser):
    try:
        next_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and @jsname="OCpkoe"]'))
        )
        next_button.click()
        time.sleep(2)
    except Exception as e:
        print(f"Error clicking next: {e}")

# Functions for filling each field
def fill_age(browser):
    try:
        age_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="text" and @aria-labelledby="i6 i9"]'))
        )
        age_input.send_keys(str(random_int(21, 50)))
        print("Filled Age")
    except Exception as e:
        print(f"Error locating or filling Age field: {e}")

def fill_city_province(browser):
    try:
        city_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="text" and @aria-labelledby="i11 i14"]'))
        )
        city_input.send_keys(random_choice([
            "Manila", "Quezon City", "Rizal", "Laguna", "Batangas", "Pampanga",
            "San Juan City", "Taguig", "Bulacan", "Caloocan", "Valenzuela"
        ]))
        print("Filled City/Province")
    except Exception as e:
        print(f"Error locating or filling City/Province field: {e}")

def select_employees(browser):
    try:
        employees_option = browser.find_element(
            By.XPATH, f'//div[@aria-label="{random_choice(["0", "1", "2", "3 or more"])}"]'
        )
        employees_option.click()
        print("Selected Employees/Helpers")
    except Exception as e:
        print(f"Error selecting Employees/Helpers: {e}")

def select_business_type(browser):
    try:
        business_option = browser.find_element(
            By.XPATH, f'//div[@aria-label="{random_choice(["Retail Business", "Food and Beverage", "Service-Based Business", "Personal Care Services", "Home-Based Businesses", "Agriculture or Food Supply", "Repair and Maintenance", "Specialty Shops"])}"]'
        )
        business_option.click()
        print("Selected Type of Business")
    except Exception as e:
        print(f"Error selecting Type of Business: {e}")

def select_years_in_business(browser):
    try:
        years_option = browser.find_element(
            By.XPATH, f'//div[@aria-label="{random_choice(["Less than 1 year", "1-2 years", "3-4 years", "5+"])}"]'
        )
        years_option.click()
        print("Selected Years in Business")
    except Exception as e:
        print(f"Error selecting Years in Business: {e}")

def select_monthly_income(browser):
    try:
        income_option = browser.find_element(
            By.XPATH, f'//div[@aria-label="{random_choice(["₱10,000 - ₱20,000", "₱20,001 - ₱30,000", "₱30,001 - ₱50,000", "Prefer not to say"])}"]'
        )
        income_option.click()
        print("Selected Monthly Income Range")
    except Exception as e:
        print(f"Error selecting Monthly Income Range: {e}")

# Main function to fill personal information
def fill_personal_information(browser):
    try:
        fill_age(browser)
        fill_city_province(browser)
        select_employees(browser)
        select_business_type(browser)
        select_years_in_business(browser)
        select_monthly_income(browser)
    except Exception as e:
        print(f"Error filling personal information: {e}")

# Main function to handle form submission
def fill_and_submit_form(browser):
    try:
        # Page 1: Click Next
        click_next(browser)

        # Page 2: Check Consent and click Next
        consent_checkbox = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@role="checkbox"]'))
        )
        consent_checkbox.click()
        click_next(browser)

        # Page 3: Fill personal information
        fill_personal_information(browser)

        # Proceed to the next page
        click_next(browser)

        # Page 4: Fill evaluation questions
        try:
            questions = WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@role="radiogroup"]'))
            )
            for question in questions:
                options = question.find_elements(By.XPATH, './/div[@role="radio"]')
                # Biased towards 4 or 5
                preferred_option = options[biased_random_choice() - 1]  # Adjust for zero-based index
                preferred_option.click()
                time.sleep(1)
            print("Filled evaluation questions")
        except Exception as e:
            print(f"Error selecting evaluation options: {e}")

        # Submit the form
        submit_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and @jsname="M2UYVd"]'))
        )
        submit_button.click()
    except Exception as e:
        print(f"Error filling out the form: {e}")

# Handle "Submit another response"
def handle_submit_another_response(browser):
    try:
        another_response = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "usp=form_confirm")]'))
        )
        another_response.click()
        print("Clicked 'Submit another response'")
        time.sleep(2)
    except Exception as e:
        print(f"Could not find 'Submit another response' link: {e}")

# Main function
def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    DRIVER_PATH = r"C:\\Users\\harle\\Downloads\\chromedriver-win64\\chromedriver.exe"
    browser = webdriver.Chrome(service=Service(DRIVER_PATH), options=options)

    browser.get(form_url)

    for i in range(45):
        print(f"Submitting form {i + 1}...")
        fill_and_submit_form(browser)

        handle_submit_another_response(browser)

    browser.quit()

if __name__ == "__main__":
    main()
