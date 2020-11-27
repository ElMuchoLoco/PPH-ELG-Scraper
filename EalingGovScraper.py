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
from selenium.webdriver.support.ui import Select

#Sheet Parsing Library
import pandas as pandas
import openpyxl

class DynamicDataEntity:
    internalState = "Empty"
    def __init__(self, DictionaryOfEntity):
        self.internalState = DictionaryOfEntity
        self.age = age

# Utility Function
def check_exists_by_selector(selector,webdriver):
    try:
        webdriver.find_element_by_css_selector(selector)
    except NoSuchElementException:
        return False
    return True

def write_to_csv(listOfEntities, searchTerm):
    print("Launching write_to_csv()")
    csvIndexColumn = []
    csvPageNumberColumn = []
    csvURLColumn = []
    csvSearchThemeColumn = []

    for element in listOfEntities:
        csvIndexColumn.append(element['Index'])
        csvPageNumberColumn.append(element['PageNumber'])
        csvURLColumn.append(element['URL'])
        csvSearchThemeColumn.append(element['SearchQuery'])
    
    print(str(searchTerm) + " -- Preparing To Write To CSV")
    scrapeData = {'SearchQuery':csvSearchThemeColumn,'Index': csvIndexColumn,'PageNumber': csvPageNumberColumn,"URL": csvURLColumn}
    scrapeFrame = pandas.DataFrame(scrapeData,columns = ['SearchQuery','Index','PageNumber','URL'])
    scrapeFrame.to_csv(path_or_buf= (str(searchTerm).strip() + 'data.csv').strip(),index=False)

    print("Ending write_to_csv()")
# For A Given Root Page Of The Search Table, Construct Require URLs For All Search Pages
# EndConditionSelector = r'html.js body div#idox div#pa div.container div.content div#searchResultsContainer.panel p.pager.top a.next'
def allSearchURLs(RootPageString,SelectorFieldToSearchForEntry,EndConditionSelector,SearchString,BrowserInstance):
    print("Launching allSearchURLSs()")
    listOfScrapedElements = []
    # Check Whether There Is A Manual Overwrite To The Current Search Page
    # if RootPageString is None:
    #     pass
    # elif RootPageString is not None:
    #     BrowserInstance.get(RootPageString)
    #     time.sleep(5)

    # Check That The Next Page Button Is Visible
    isOnLastPageFlag = check_exists_by_selector(EndConditionSelector, BrowserInstance)
    pageIterator = 1
    elementCounter = 0

    # find The Page Result Modifier Which Updates Result Numbers On Page
    select = Select(BrowserInstance.find_element_by_css_selector(r'html.js body div#idox div#pa div.container div.content div#searchfilters form#searchResults span.resultsPerPage select#resultsPerPage'))
    time.sleep(5.0)
    select.select_by_value('100')
    time.sleep(5.0)

    # Click The Go Button To Update The Search Page with 100 Results Per Page
    BrowserInstance.find_element_by_css_selector(r'html.js body div#idox div#pa div.container div.content div#searchfilters form#searchResults input.button.primary').click()

    time.sleep(10)
    #After Being Primed For 100 Results Per Page In Cookies, Iterate Round Until Flag Is Raised To Indicate there Is Not A Next Button On The Reuslts e.g Last Page
    while isOnLastPageFlag:
        isOnLastPageFlag = check_exists_by_selector(EndConditionSelector, BrowserInstance)
        print("CHECKING PAGE = [" + RootPageString + str(pageIterator) + "]")
        for element in BrowserInstance.find_elements_by_css_selector(SelectorFieldToSearchForEntry):
            elementCounter += 1
            # print("Found [" + str(elementCounter) + "] at [" + element.get_attribute('href') + "]")
            listOfScrapedElements.append({'SearchQuery':str(SearchString),'Index':str(elementCounter),'PageNumber':str(pageIterator),'URL':element.get_attribute('href')})
            print('SearchQuery' + " --- " + str(SearchString) + " --- " + 'Index ' + "[" + str(elementCounter) + "]" + " --- " + 'PageNumber '  + "[" + str(pageIterator) + "]" + " --- " + 'URL ' + "[" + str(element.get_attribute('href')) + "]")
            #https://pam.ealing.gov.uk/online-applications/pagedSearchResults.do?action=page&searchCriteria.page=1
        pageIterator += 1
        BrowserInstance.get(RootPageString + str(pageIterator))
        time.sleep(4)
    
    return listOfScrapedElements
    # element.get_attribute('href')
    # yearProfileList.append(str(element.text).replace("YEAR\n",""))
        
# Paramaters: {SearchButtonUID: }
def initiateSearch(SearchButtonSelectorString, ValueToInsert, SelectorToInsertInto, SearchURL, BrowserInstance):
    print("Launching initiateSearch()")
    BrowserInstance.get(SearchURL)
    print("Got Search URL Pause For 10")
    time.sleep(5)
    print("Resume")
    print("Inserted [" + ValueToInsert + "] at [" + SelectorToInsertInto + "]")
    BrowserInstance.find_element_by_css_selector(SelectorToInsertInto).send_keys(ValueToInsert)
    print("About To Click For Search")
    time.sleep(1)
    BrowserInstance.find_element_by_css_selector(SearchButtonSelectorString).click()
    print("Clicked For Search")

# ApprovedBoats.com Scrape Driver
# Generic Load Function Takes A Given String Value & A Given HTML/CSS/XPATH Unique Identifier and Inserts The Value Into The Given Search Field
def handleEalingGovDriver(listOfSearchKeywords,browser,Make,Model,PrioritiseMakeOrModel):

    constNextToggle = r'html.no-js body.page-template.page-template-page-cobrokerage.page-template-page-cobrokerage-php.page.page-id-115.page-parent div.body-wrap div.top-tp-10 div.container.co-brokerage-results div#inventory-display.inventory-display.clearfix.row div.col-sm-9.col-xs-12.pagination div.col-md-12.pagination-top-lower div.col-md-7.col-xs-12 div#page-numbers-wrap div#page-numbers.hidden-sm.hidden-xs a div.next.glyphicon.glyphicon-chevron-right'
    constProfileLink = r'div.inventory-model-single > a'
    constYearLink = r'html.no-js body.page-template.page-template-page-cobrokerage.page-template-page-cobrokerage-php.page.page-id-115.page-parent div.body-wrap div.top-tp-10 div.container.co-brokerage-results div#inventory-display.inventory-display.clearfix.row div#boat-list.col-sm-9.col-xs-12.row.list-group div.col-md-12 div.col-xs-12.boat.col-lg-6.col-md-6.col-sm-6.grid-group-item div.inventory-model-single div.boat-details div.bottom-boat div.col-xs-3.boat-year'
    print("Reaching to Collect ApprovedBoats.com")

    #For A Make And Model, Insert All Components Of This Into The Search String
    searchStringHeader = 'https://www.approvedboats.com/co-brokerage-boats-for-sale/all/'
    searchStringCarriage = '?AdvancedKeywordSearch='
    searchString = ""
    print("=====================SCRAPING APPROVED BOATS")

    for keywordElement in listOfSearchKeywords:
        if(listOfSearchKeywords.index(keywordElement) + 1 < len(listOfSearchKeywords)):
            searchStringCarriage = searchStringCarriage + keywordElement + '%20'
        else:
            searchStringCarriage = searchStringCarriage + str(keywordElement).replace(" ",'%20') + "&currency=GBP&option=100"
        print(searchString)

    if(PrioritiseMakeOrModel == "Make"):
        searchString = searchStringHeader + str(Make).replace(" ","+") + "/" + searchStringCarriage
    elif(PrioritiseMakeOrModel == "Model"):
        searchString = searchStringHeader + str(Make).replace(" ","+") + "-" + str(Model).replace(" ","+") + searchStringCarriage
    else:
        print("=========ERROR==========================")
        print("ERROR----ON CODING OF PRIORITY FIELD")
        print("WILL ATTEMPT TO SEARCH WITH FULL PRECISION")
        searchString = searchStringHeader + str(Make).replace(" ","+") + "-" + str(Model).replace(" ","+") + searchStringCarriage

    print("====COMPLETING SCRAPE OF APPROVED BOATS=========")
    print("searchStringHeader = " + searchStringHeader)
    print("searchStringCarriage = " + searchStringCarriage)
    print("searchString = [" + searchString + "]")
    
    urlProfileList = []
    yearProfileList = []

    #State & Constants for Scraping Session
    paginationIndex = 1
    allListings = []
    browser.get(searchStringHeader + str(Make).replace(" ","+") + "-" + str(Model).replace(" ","+") + "/" + str(paginationIndex) + "/" + searchStringCarriage)
    print("=======BEGINNING FIRST PAGE OF SCRAPE")
    print("=======NEXT PAGE CONDITIONAL STATE = [" + str(check_exists_by_selector(constNextToggle,browser)) + "]")

    while check_exists_by_selector(constNextToggle, browser):
        print("======STARTING NEW PAGE======<3 :)")

        #Re-Write to Address Staleness
        allElements =  browser.find_elements_by_css_selector(constProfileLink)
        for element in allElements:
            urlProfileList.append(str(element.get_attribute('href')))
        
        allYears =  browser.find_elements_by_css_selector(constYearLink)
        allListings = allListings + browser.find_elements_by_css_selector(constProfileLink)
        print("Scraping Element - [" +  constProfileLink + "]")
        print("Total Profiles Collected = [" + str(len(allListings)) + "]")
        print("Scraped Page = [Page=" + str(paginationIndex) + "]")
        paginationIndex = paginationIndex + 1
        print("Next to Be Scraped = [" + searchStringHeader + str(paginationIndex) + "/" + searchStringCarriage + "]")
        browser.get(searchStringHeader + str(paginationIndex) + "/" + searchStringCarriage)
        time.sleep(1)
        print("======COMPLETING PAGE========<3 :)")


    print("=======BEGINNING LAST PAGE OF SCRAPE")

    #Re-Write to Adress Staleness
    allElements =  browser.find_elements_by_css_selector(constProfileLink)
    for element in allElements:
        urlProfileList.append(str(element.get_attribute('href')))

    allYearsListings = browser.find_elements_by_css_selector(constYearLink)
    for element in allYearsListings:
        yearProfileList.append(str(element.text).replace("YEAR\n",""))

    print("Scraping Element - [" +  constProfileLink + "]")
    print("Total Profiles Collected = [" + str(len(allListings)) + "]")
    time.sleep(1)
    print("=======END OF SCRAPE LOOP===========")
    print("Total Profiles Collected = [" + str(len(allListings)) + "]")
    print("Number of Pages Scraped = [" + str(paginationIndex) + "]")

    print("=====RAW DEBUG BLOCK PRINT COLLECTED RESULT====")
    # print(allListings)
    print("=====CLEANED URL LIST=========================")
    for element in urlProfileList:
         print("ELEMENT [" + str(urlProfileList.index(element) + 1) + "] = " + element)
    print("=====COMPLETED SCRAPE=========================")

    outputDataStructure = []

    for element in urlProfileList:
        browser.get(element)
        #dataExtract = {"URL": element,"Year": str(browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/div[4]/div/div/div[1]/div/div[1]/div[1]/div[5]').text),"Price": str(browser.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[2]/span[1]/h2').text),"Currency": "GBP"}
        dataExtract = {"URL": element,"Year": yearProfileList[urlProfileList.index(element)],"Price": str(browser.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[2]/span[1]/h2').text),"Currency": "GBP"}
        outputDataStructure.append(dataExtract)
        print("SCRAPED ELEMENT [" + str(urlProfileList.index(element)) + "] - RESULT = [" + str(dataExtract) + "] FOR LISTING = " + "[" + str(element) + "]")

    print("======FINAL OUTPUT OF SCRAPE")
    for element in outputDataStructure:
        print("FINAL OUTPUT - ELEMENT [" + str(outputDataStructure.index(element) + 1) + "]" + " = " + str(element))
    
    buildSheet("Approved Boats",searchStringHeader + str(Make).replace(" ","+") + "-" + str(Model).replace(" ","+") + "/" + str(paginationIndex) + "/" + searchStringCarriage,"TRUE",Make,Model,outputDataStructure)

    return outputDataStructure

# Main Driver
def main():
    # Input Search Paramater to https://pam.ealing.gov.uk/online-applications/search.do?action=advanced
    SearchButtonSelectorStringVar = r'html.js body div#idox div#pa div.container div.content div.tabcontainer form#advancedSearchForm div.buttons input.button.primary'
    DictionaryOfKeysForSearchVar = {"Advertisement Content":r'html.js body div#idox div#pa div.container div.content div.tabcontainer form#advancedSearchForm div#details fieldset div.caseType select#caseType'
                                    ,"Article 4 Application":r'html.js body div#idox div#pa div.container div.content div.tabcontainer form#advancedSearchForm div#details fieldset div.caseType select#caseType'}
    SearchURLVar = 'https://pam.ealing.gov.uk/online-applications/search.do?action=advanced'
    
    #Instantiate Web Browser Window
    BrowserSpawnedVar = webdriver.Chrome()
    time.sleep(5)

    # Constants For File
    RootPageStringValue = r'https://pam.ealing.gov.uk/online-applications/pagedSearchResults.do?action=page&searchCriteria.page='
    SelectorFieldForURL = r'html.js body div#idox div#pa div.container div.content div#searchResultsContainer.panel div.col-a ul#searchresults li.searchresult a'
    EndConditionSelector = r'html.js body div#idox div#pa div.container div.content div#searchResultsContainer.panel p.pager.top a.next'

    # Launch The Parser To Walk Over Search Results
    for element in DictionaryOfKeysForSearchVar:
        
        #LaunchSearchResults
        initiateSearch(SearchButtonSelectorStringVar,element,DictionaryOfKeysForSearchVar[element],SearchURLVar,BrowserSpawnedVar)
        time.sleep(5)

        scrapedEntities = allSearchURLs(RootPageStringValue,SelectorFieldForURL,EndConditionSelector,str(element),BrowserSpawnedVar)

         # Process Search Outputs to CSV
        write_to_csv(scrapedEntities, element)

# Launcher
main()