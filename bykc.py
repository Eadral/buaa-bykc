import os
import traceback
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import argparse
import getpass

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of, presence_of_element_located
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

parser = argparse.ArgumentParser(description="北航博雅小助手")
parser.add_argument("username", help="统一认证用户名")

parser.add_argument("--driver_path", "-d", help="webdriver地址 默认: http://10.128.63.245:4444/wd/hub", default="http://10.128.63.245:4444/wd/hub")
parser.add_argument("--interval", "-i", type=int, help="轮询间隔时间(s) 默认：1", default="1")
parser.add_argument("--number", "-n", type=int, help="抢课数量，达到后程序终止 默认：1", default="1")
parser.add_argument("--target", "-t", nargs="+", help="目标课程")
parser.add_argument("--type", help="目标课程类型 默认：讲座", default="讲座")

parser.add_argument("--dingding_url", help="dingding机器人url")
parser.add_argument("--dingding_secret", help="dingding机器人secret")
parser.add_argument("--dingding_phone_number", help="dingding机器人at手机号")

class DingDing:
    def __init__(self, url, secret, prefix=""):
        self.secret = secret
        self.url = url
        self.prefix=prefix

    def send(self, mes, at=None):
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

        res = requests.post(self.url + "&timestamp={}&sign={}".format(timestamp, sign), json={
            "msgtype": "text",
            "text": {
                "content": self.prefix + mes
            },
            "at": {
                "atMobiles": at if at is not None else [],
            }
        })

        return res

class MeowDriver:
    def __init__(self, driver_path, headless=True):
        options = Options()
        options.headless = headless
        self.driver = webdriver.Remote(
            command_executor=driver_path,
            options=options)
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

    def quit(self):
        self.driver.quit()

    def get(self, url):
        self.driver.get(url)


def login_buaa_sso(driver, args):
    driver.get("https://sso.buaa.edu.cn/login")

    iframe = driver.find_element_by_xpath('//*[@id="loginIframe"]')
    driver.switch_to.frame(iframe)

    username_input = driver.find_element_by_xpath('//*[@id="unPassword"]')
    password_input = driver.find_element_by_xpath('//*[@id="pwPassword"]')
    login_button = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div[2]/div[1]/div[7]/input')

    username_input.send_keys(args.username)
    password_input.send_keys(args.password)
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

targets = []

def loop_bykc_list(driver, args, ding, acc_number):
    count = 0
    if ding:
        ding.send("开始查询")

    goto_bykc_list(driver)
    while True:
        print("count: {}".format(count))
        elements = driver.find_elements_by_xpath(
            '/html/body/main/div[1]/div/div/div[2]/div[1]/div/div/div/div/div[2]/table/tbody/tr[*]/td[8]')
        names = driver.find_elements_by_xpath('/html/body/main/div[1]/div/div/div[2]/div[1]/div/div/div/div/div[2]/table/tbody/tr[*]/td[1]')
        types = driver.find_elements_by_xpath('/html/body/main/div[1]/div/div/div[2]/div[1]/div/div/div/div/div[2]/table/tbody/tr[*]/td[2]')

        for i, element in enumerate(elements):
            number_text = element.text
            name = names[i].text
            type_text = types[i].text
            is_target = True
            if args.target or args.type:
                is_target = False
                if not is_target and args.target:
                    is_target = name in args.target
                if not is_target and args.type:
                    is_target = args.type in type_text

            print(name, number_text, type_text, is_target)
            current_num, max_num = number_text.split("/")
            current_num, max_num = int(current_num), int(max_num)

            if current_num < max_num and is_target:
                if ding:
                    ding.send("发现目标可选课程 {}".format(name), at=[args.dingding_phone_number])
                try:
                    registers = driver.find_elements_by_xpath(
                        '/html/body/main/div[1]/div/div/div[2]/div[1]/div/div/div/div/div[2]/table/tbody/tr[*]/td[9]/a[2]')

                    registers[i].click()
                    yes_button = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/button[2]')
                    yes_button.click()
                    if ding:
                        ding.send("选课成功 {}".format(name), at=[args.dingding_phone_number])
                    acc_number += 1
                    if acc_number >= args.number:
                        exit(0)
                except:
                    if ding:
                        ding.send("选课失败 {}".format(name), at=[args.dingding_phone_number])


        refresh_button = driver.find_element_by_xpath(
            '/html/body/main/div[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[2]/a')
        try:
            refresh_button.click()
        except:
            print("click failed")
            goto_bykc_list(driver)
            continue

        if count % (60 * 24) == 0:
            if ding:
                ding.send("累计轮询次数：{}".format(count))
        count += 1
        time.sleep(args.interval)


if __name__ == "__main__":
    args = parser.parse_args()
    args.password = getpass.getpass()

    acc_number = 0

    while True:
        if args.dingding_url is not None:
            ding = DingDing(args.dingding_url, args.dingding_secret, prefix="【博雅课程】")
        else:
            ding = None

        driver = None
        try:
            driver = MeowDriver(args.driver_path, headless=True)

            login_buaa_sso(driver, args)
            loop_bykc_list(driver, args, ding, acc_number)
        except:
            traceback.print_exc()
        finally:
            ding.send("监视器意外退出", at=[args.dingding_phone_number])
            if driver:
                driver.quit()
