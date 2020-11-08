import os
import time
import traceback

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of, presence_of_element_located
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from dingding import DingDing


class MeowDriver:
    def __init__(self, headless=True):
        options = Options()
        options.headless = headless
        self.driver = webdriver.Firefox(executable_path=os.getenv("driver_path"), options=options)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)
        self.switch_to = self.driver.switch_to

    def find_element_by_xpath(self, xpath):
        self.wait.until(presence_of_element_located((By.XPATH, xpath)))
        element = self.driver.find_element_by_xpath(xpath)
        self.wait.until(visibility_of(element))
        return element

    def find_elements_by_xpath(self, xpath):
        self.wait.until(presence_of_element_located((By.XPATH, xpath)))
        elements = self.driver.find_elements_by_xpath(xpath)
        for element in elements:
            self.wait.until(visibility_of(element))
        return elements

    def close(self):
        self.driver.close()

    def get(self, url):
        self.driver.get(url)


def login_buaa_sso(driver):
    driver.get("https://sso.buaa.edu.cn/login")

    iframe = driver.find_element_by_xpath('//*[@id="loginIframe"]')
    driver.switch_to.frame(iframe)

    username_input = driver.find_element_by_xpath('//*[@id="unPassword"]')
    password_input = driver.find_element_by_xpath('//*[@id="pwPassword"]')
    login_button = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div[2]/div[1]/div[7]/input')

    username_input.send_keys(os.getenv("username"))
    password_input.send_keys(os.getenv("password"))
    login_button.click()

    driver.switch_to.default_content()


def goto_bykc_list(driver):
    driver.get("http://bykc.buaa.edu.cn")
    jump_button = driver.find_element_by_xpath('/html/body/main/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/button')
    jump_button.click()

    class_menu_button = driver.find_element_by_xpath('/html/body/main/div[1]/aside/div/ul/li[3]/div/div')
    class_menu_button.click()

    class_select_button = driver.find_element_by_xpath('/html/body/main/div[1]/aside/div/ul/li[3]/div/ul/li[2]')
    class_select_button.click()


def loop_bykc_list(driver, ding):
    count = 0
    ding.send("开始查询")

    goto_bykc_list(driver)
    while True:
        print("count: {}".format(count))
        elements = driver.find_elements_by_xpath(
            '/html/body/main/div[1]/div/div/div[2]/div[1]/div/div/div/div/div[2]/table/tbody/tr[*]/td[8]')

        for element in elements:
            text = element.text
            print(text)
            current_num, max_num = text.split("/")
            current_num, max_num = int(current_num), int(max_num)

            if current_num < max_num:
                ding.send("发现可选课程！！！", at=[os.getenv("phone_number")])

        refresh_button = driver.find_element_by_xpath(
            '/html/body/main/div[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[2]/a')
        try:
            refresh_button.click()
        except:
            print("click failed")
            goto_bykc_list(driver)
            continue

        if count % (60 * 24) == 0:
            ding.send("累计轮询次数：{}".format(count))
        count += 1
        time.sleep(60)


if __name__ == "__main__":
    from dotenv import find_dotenv, load_dotenv

    load_dotenv(find_dotenv(), override=True)

    ding = DingDing(os.getenv("dingding_url"), os.getenv("dingding_secret"), prefix="【博雅课程】")

    try:
        driver = MeowDriver(headless=True)

        login_buaa_sso(driver)
        loop_bykc_list(driver, ding)
    except:
        traceback.print_exc()
    finally:
        ding.send("监视器意外退出", at=[os.getenv("phone_number")])
        driver.close()
