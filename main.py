# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

options = Options()
# options.add_argument('--headless')
options.add_argument('--user-data-dir=D:\\user_data')


# options.add_argument('--window-size=1366,768')

# 查看是否已经登录，没有登录的话在生成login.png进行扫码登录
def login():
    png_name = 'login.png'
    browser.get('https://www.iqiyi.com/u/point')
    if browser.current_url != 'https://www.iqiyi.com/u/point':
        if os.path.exists(png_name):
            os.remove(png_name)
        browser.get_screenshot_as_file(png_name)
        time.sleep(60)
        browser.get('https://www.iqiyi.com/u/point')
        if browser.current_url != 'https://www.iqiyi.com/u/point':
            return 0
    if browser.current_url == 'https://www.iqiyi.com/u/point':
        return 1
    else:
        return 0


def browser_close():
    browser.close()
    browser.quit()


browser = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options, service_log_path='web.log',
                           service_args=['--verbose', '--log-path=web.log'])

if login() == 0:
    print u'登录失败，退出'
    browser_close()
    exit(0)

window_handle = browser.current_window_handle
task_element = browser.find_element_by_xpath('//a[@data-signenabled]')
if task_element.get_attribute('data-signenabled') == 'true':
    task_element.click()
    time.sleep(1)
    if task_element.text == u'已签到':
        print u'签到领成长值完成' + browser.find_element_by_xpath('//em[contains(@class,\'growth-value-add\')]').text
    else:
        print u'签到领成长值失败'
else:
    print u'签到领成长值已经完成'

task_element = browser.find_element_by_class_name('score-task-sign-box')
task_done_count = task_element.find_element_by_xpath('.//span[contains(@class,"score-task-done-num")]').text
if task_done_count == '0':
    print u'进行积分签到……'
    task_element.find_element_by_xpath('.//a[contains(@class,"j-task-sign")]').click()
    time.sleep(1)
    task_done_count = task_element.find_element_by_xpath('.//span[contains(@class,"score-task-done-num")]').text
    if task_done_count == '1':
        print u'积分签到完成'
    else:
        print u'积分签到失败'
else:
    print u'积分签到已经完成'

task_element = browser.find_element_by_class_name('score-task-visitpp-box')
task_done_count = task_element.find_element_by_xpath('.//span[contains(@class,"score-task-done-num")]').text
if task_done_count == '0':
    print u'进行泡泡积分……'
    click_button = task_element.find_element_by_xpath('.//a[contains(@class,"j-task-paopao")]')
    if click_button.text.strip() == u'去逛逛':
        browser.execute_script('argument[0].setAttribute("data-pao-rewardcount","1")', click_button)
    click_button.click()
    browser.switch_to.window(window_handle)
    time.sleep(1)
    task_done_count = task_element.find_element_by_xpath('.//span[contains(@class,"score-task-done-num")]').text
    if task_done_count == '1':
        print u'泡泡积分完成'
    else:
        print u'泡泡积分失败'
else:
    print u'泡泡积分已经完成'

task_element = browser.find_element_by_class_name('score-task-watch-box')
task_done_count = task_element.find_element_by_xpath('.//span[contains(@class,"score-task-done-num")]').text
print u'视频积分完成' + task_done_count + u'次'


browser.get('https://vip.iqiyi.com/pcw_task.html')
task_element = browser.find_element_by_xpath('//li[contains(@class,"j_task_vipClub")]')
task_text = task_element.find_element_by_xpath('.//div[@class="task_status"]/span[not (contains(@class,"dn"))]').text.strip()
if task_text.strip() == u'去完成':
    task_element.find_element_by_xpath("./a").click()
    time.sleep(1)
    browser.switch_to.window(window_handle)
    task_element.find_element_by_xpath("./a").click()
    print u'俱乐部积分完成'
elif task_text == u'领取':
    task_element.find_element_by_xpath("./a").click()
    print u'俱乐部积分完成'
else:
    print u'俱乐部积分已经完成'


browser_close()