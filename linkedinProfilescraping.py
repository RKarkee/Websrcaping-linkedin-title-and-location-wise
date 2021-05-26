from logging import exception
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from bs4.element import Tag
import csv
from parsel import Selector
from time import sleep

#open chrome and login for linked site
driver = webdriver.Chrome()
url = 'https://www.linkedin.com/login'
driver.get(url)
sleep(2)

#import username and password
credential = open('credentials.txt')
line = credential.readlines()
username = line[0]
password = line[1]

#key in username
email_field = driver.find_element_by_id('username')
email_field.send_keys(username)
password_field = driver.find_element_by_id('password')
password_field.send_keys(password)
sleep(2)
login_button = driver.find_element_by_class_name('login__form_action_container')
login_button.click()
sleep(0.5)


# driver.get method() will navigate to a page given by the URL address
driver.get('https://www.google.com')
sleep(3)

# locate search form by_name
search_query = driver.find_element_by_name('q')

# send_keys() to simulate the search text key strokes
search_query.send_keys('site:linkedin.com/in/ AND "Accountant" AND "New York"')

# .send_keys() to simulate the return key 
search_query.send_keys(Keys.RETURN)


def validate_field(field):
    # if field is present pass if field:
    if field:
        pass
    # if field is not present print text else:
    else:
        field = 'No results'
    return field

def find_profiles():
    for r in result_div:
        # Checks if each element is present, else, raise exception
        try:
            link = r.find('a', href=True)
           
            # Check to make sure everything is present before appending
            if link != '' :
                links.append(link['href'])
                
        # Next loop if one element is not present
        except Exception as e:
           # print(e)
            continue
        
# This function iteratively clicks on the "Next" button at the bottom right of the search page. 
def profiles_loop():
    
    find_profiles()
    
    next_button = driver.find_element_by_xpath('//*[@id="pnnext"]') 
    next_button.click()
    
    
def repeat_fun(times, f):
    for i in range(times): f()


soup = BeautifulSoup(driver.page_source,'lxml')
result_div = soup.find_all('div', attrs={'class': 'g'})
    
# initialize empty lists
links = []

# Function call x10 of function profiles_loop; you can change the number to as many pages of search as you like. 
repeat_fun(1, profiles_loop)

#print(links)

with open('computerteacher.csv', 'w', newline = '') as file_output:
    headers = ['Name', 'Job Title', 'Location','Company','URL']
    writer = csv.DictWriter(file_output, delimiter = ',', lineterminator ='\n', fieldnames=headers)
    writer.writeheader()
    for linkedin_URL in links:
        driver.get(linkedin_URL)
        sleep(2)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source,"html.parser")
        try:
            name_div = soup.find('div',{'class':'flex-1 mr5 pv-top-card__list-container'})
            name_loc = name_div.find_all('ul')
            name = name_loc[0].find('li').get_text().strip()

            location = name_loc[1].find('li').get_text().strip()

            profile_title = name_div.find('h2').get_text().strip()
            com_and_uni_ul = soup.find('ul', {'class':'pv-top-card--experience-list'}) 
            com_and_uni_a = com_and_uni_ul.find('a', {'class':'pv-top-card--experience-list-item'})
            company = com_and_uni_a.find('span').get_text().strip()
        except Exception as e:
            continue
        # validating if the fields exist on the profile
        name = validate_field(name)
        profile_title = validate_field(profile_title)
        company = validate_field(company)
        location = validate_field(location)
        linkedin_URL = validate_field(linkedin_URL)
        print('\n')
        print(name)
        print(profile_title)
        print(company)
        print(location)
        print(linkedin_URL)
        
        data ={headers[0]:name, headers[1]:profile_title, headers[2]:location, headers[3]:company,
        headers[4]:linkedin_URL}
        writer.writerow(data)

#driver.quit()