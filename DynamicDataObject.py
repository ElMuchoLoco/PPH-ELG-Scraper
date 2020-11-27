#https://www.peopleperhour.com/freelance-jobs/technology-programming/databases/data-mine-scrape-pull-information-from-website-into-csv-3060429

#Applied Dependencies
from selenium import webdriver
import time 
from selenium.common.exceptions import NoSuchElementException

#Unsused Additional Dependencies
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

#Sheet Parsing Library
import pandas as pandas
import openpyxl

# Utility Function

def main():
    # Input Search Paramater to https://pam.ealing.gov.uk/online-applications/search.do?action=advanced
    # Process Search Input Into All Fields On The Search Field

# Launcher
main()