import time
import os
import traceback
import csv
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

time_out = 5
profile_number = 10000
gmail = ''
mypassword = ''


def scrape_tinder():
    options = config_chrome_option()
    browser = uc.Chrome(options=options)
    browser.maximize_window()

    login_tinder(browser)
    #browser.implicitly_wait(20)

    fields = ['name', 'age', 'height', 'sex', 'location', 'lives in', 'education', 'about me', 'looking for',
              'lifestyle', 'basics', 'passions']
    filename = 'Tinder user data.csv'
    with open(filename, 'a', newline='', encoding="utf-8-sig") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        for i in range(profile_number):
            profile = Profile()
            try:
                #if is_notification_overlayed(browser):
                    #click_not_interest_button(browser)

                click_open_profile_button(browser)

                get_name(browser, profile)
                get_age(browser, profile)
                get_another_information(browser, profile)
                get_about_me(browser, profile)
                get_looking_for(browser, profile)
                get_interest(browser, profile)

                
                print('Name: ' + profile.name)
                print('Age: ' + profile.age)
                print('About me: ' + profile.about_me)
                print('Height: ' + profile.height)
                print('Sex: ' + profile.sex)
                print('Location: ' + profile.location)
                print('Lives in' + profile.lives_in)
                print('School: ' + profile.education)
                print('Looking for: ' + profile.looking_for)
                print('Lifestyle: ' + profile.lifestyle)
                print('Basics: ' + profile.basics)
                print('Passions' + profile.passions)
                print()
                #time.sleep(5)
                mydict = {'name': profile.name, 'age': profile.age, 'height': profile.height, 'sex': profile.sex,
                               'location': profile.location, 'lives in': profile.lives_in,
                               'education': profile.education, 'about me': profile.about_me,
                               'looking for': profile.looking_for,
                               'lifestyle': profile.lifestyle, 'basics': profile.basics,
                               'passions': profile.passions}
                writer.writerow(mydict)

                click_nope_button(browser)
            except Exception:
                print('Profile not show yet...')
        print('DONE LOOP')
    print('DONE WRITE TO FILE')
    time.sleep(30)
    browser.quit()


def config_chrome_option():
    options = uc.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.geolocation": 1,
        "profile.default_content_setting_values.notifications": 1,
        "profile.default_content_setting_values.cookies": 1,
    })
    return options


def login_tinder(browser):
    tinder_homepage = 'https://tinder.com/'
    # google_signin = 'https://accounts.google.com/signin'

    browser.get(tinder_homepage)

    tinder_login_button = WebDriverWait(browser, time_out).until(
        ec.visibility_of_all_elements_located((By.TAG_NAME, 'button')))[1]
    tinder_login_button.click()

    google_login_button = WebDriverWait(browser, time_out).until(
        ec.visibility_of_element_located((By.TAG_NAME, 'iframe')))
    google_login_button.click()

    b = WebDriverWait(browser, time_out).until(
        ec.visibility_of_all_elements_located((By.TAG_NAME, 'button')))
    b[7].click()

    login_google(browser)


def login_google(browser):
    main_window = browser.current_window_handle
    sign_in_window = None

    for window in browser.window_handles:
        if window != main_window:
            sign_in_window = window

    if sign_in_window is not None:
        browser.switch_to.window(sign_in_window)
        fill_google_sign_in_form(browser)
        browser.implicitly_wait(5)
        browser.switch_to.window(main_window)
        # print(browser.current_url + '\n' + browser.page_source)


def fill_google_sign_in_form(browser):
    email = WebDriverWait(browser, time_out).until(ec.visibility_of_element_located((By.ID, 'identifierId')))
    email.send_keys(gmail)
    email.send_keys(Keys.ENTER)
    password = WebDriverWait(browser, time_out).until(ec.visibility_of_element_located((By.NAME, 'Passwd')))
    password.send_keys(mypassword)
    password.send_keys(Keys.ENTER)


def set_fake_location(browser):
    script = """
        function setFakeLocation(latitude, longitude) {
            navigator.geolocation.getCurrentPosition = function(success, error, options) {
                success({
                    'coords': {
                        'latitude': latitude,
                        'longitude': longitude,
                        'accuracy': 100  // Example accuracy in meters
                    }
                });
            }
        }

        // Set fake location (e.g., Berlin, Germany)
        setFakeLocation(52.52, 13.405);
        """
    browser.execute_script(script)


def click_nope_button(browser):
    nope_button = WebDriverWait(browser, time_out).until(
        ec.element_to_be_clickable((By.XPATH, "//button[.//span/span/span[text()='Nope']]")))
    nope_button.click()


def click_open_profile_button(browser):
    open_profile_button = WebDriverWait(browser, time_out).until(
        ec.presence_of_all_elements_located((By.XPATH, "//button[.//span[text()='Open Profile']]")))[1]
    open_profile_button.click()


def get_name(browser, profile):
    try:
        name = WebDriverWait(browser, time_out).until(
            ec.visibility_of_element_located(
                (By.XPATH, "//h1[@class='Typs(display-1-strong) Fxs(1) Fxw(w) Pend(8px) M(0) D(i)']"))).text
        profile.name = name
    except:
        print('Name: NOT FOUND')


def get_age(browser, profile):
    try:
        age = WebDriverWait(browser, time_out).until(
            ec.visibility_of_element_located(
                (By.XPATH, "//span[@class='Whs(nw) Typs(display-2-strong)']"))).text
        profile.age = age
    except:
        print('Age: NOT FOUND')


def get_another_information(browser, profile):
    try:
        another_infor = WebDriverWait(browser, time_out).until(
            ec.visibility_of_all_elements_located(
                (By.XPATH, "//div[@class='Us(t) Va(m) D(ib) NetWidth(100%,20px) C($c-ds-text-secondary)']")))
        for infor in another_infor:
            if 'cm' in infor.text:
                profile.height = infor.text
            elif 'kilometers' in infor.text:
                profile.location = infor.text
            elif 'Trường' in infor.text or 'University' in infor.text or 'College' in infor.text:
                profile.education = infor.text
            elif infor.text == 'Woman' or infor.text == 'Man':
                profile.sex = infor.text
            elif 'Lives in' in infor.text:
                profile.lives_in = infor.text
    except:
        print("Another infor: NOT FOUND")


def get_about_me(browser, profile):
    try:
        about_me = WebDriverWait(browser, time_out).until(
            ec.visibility_of_element_located(
                (By.XPATH,
                 "//div[@class='Px(16px) Py(12px) Us(t) C($c-ds-text-secondary) BreakWord Whs(pl) Typs(body-1-regular)']")))
        profile.about_me = about_me.text
    except:
        print('About me: NOT FOUND')


def get_looking_for(browser, profile):
    try:
        looking_for = WebDriverWait(browser, time_out).until(
            ec.visibility_of_element_located(
                (By.XPATH, "//div[@class='Typs(subheading-1) CenterAlign']"))).text
        profile.looking_for = looking_for
    except:
        print('Looking for: NOT FOUND')


def get_interest(browser, profile):
    try:
        some_interest = WebDriverWait(browser, time_out).until(
            ec.visibility_of_all_elements_located((By.XPATH, "//div[@class='Px(16px) Py(12px)']")))
        for interest in some_interest:
            title = interest.find_element(By.XPATH,
                                          ".//h2[@class='C($c-ds-text-primary) Typs(heading-1) M(0)']").text
            interest_list = interest.find_elements(By.XPATH, ".//div//div")
            temp = ''
            seperator = '|'
            if 'Basics' in title or 'Lifestyle' in title or 'Passions' in title:
                for a in interest_list:
                    temp += a.get_attribute('innerText')
                    temp += seperator
                if 'Passions' in title:
                    temp = temp[temp.find('|') + 1:]
                if '\n' in temp:
                    temp = temp.replace('\n', ':')
                if '||' in temp:
                    temp = temp.replace('||', '|')
                if temp[-1] == '|':
                    temp = temp[:-1]
                if 'Basics' in title:
                    profile.basics = temp
                elif 'Lifestyle' in title:
                    profile.lifestyle = temp
                elif 'Passions' in title:
                    profile.passions = temp
    except:
        print('Interest: NOT FOUND')


def is_notification_overlayed(browser):
    try:
        WebDriverWait(browser, time_out).until(
            ec.visibility_of_element_located((By.XPATH, "//div[@id='t27493331']")))
        return True
    except:
        print('No overlay')
        return False


def click_not_interest_button(browser):
    if is_notification_overlayed(browser):
        try:
            not_interest_button = WebDriverWait(browser, time_out).until(
                ec.element_to_be_clickable((By.XPATH, "//button[@class='c1p6lbu0 D(b) Mx(a)'")))
            not_interest_button.click()
        except:
            print('Not found Not interest button')


class Profile:
    name = ''
    age = ''
    sex = ''
    height = ''
    location = ''
    lives_in = ''
    education = ''
    about_me = ''
    looking_for = ''
    lifestyle = ''
    basics = ''
    passions = ''

    def __init__(self):
        self.name = ''
        self.age = ''
        self.sex = ''
        self.height = ''
        self.location = ''
        self.lives_in = ''
        self.education = ''
        self.about_me = ''
        self.looking_for = ''
        self.lifestyle = ''
        self.basics = ''
        self.passions = ''


if __name__ == '__main__':
    scrape_tinder()
