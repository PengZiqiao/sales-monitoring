from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import datetime
import calendar
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get('http://192.168.108.16/realty/admin/main.php')


def login():
    print(">>> 正在登陆")
    driver.find_element_by_name('username').send_keys('彭子乔')
    driver.find_element_by_name('password').send_keys('password02!')
    driver.find_element_by_name('submit').click()
    driver.implicitly_wait(1)


def week():
    sunday = datetime.datetime.today()
    while sunday.weekday() != calendar.SUNDAY:
        sunday -= datetime.timedelta(days=1)
    monday = sunday - datetime.timedelta(days=6)
    return monday.strftime('%Y%m%d'), sunday.strftime('%Y%m%d')


def random_statistics():
    print(">>> 随机统计")
    driver.switch_to.frame(driver.find_element_by_name('leftFrame'))
    driver.find_element_by_link_text(u"随机统计脱水版").click()
    driver.implicitly_wait(3)
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_name('mainFrame'))


def chengjiao(proj, date):
    print(">>> 开始查询")
    driver.find_element_by_name("ByProject").clear()
    driver.find_element_by_name("ByProject").send_keys(proj)
    Select(driver.find_element_by_name("d_position1")).select_by_visible_text("*全市*")
    driver.find_element_by_name("ByDate1").clear()
    driver.find_element_by_name("ByDate1").send_keys(date[0])
    driver.find_element_by_name("ByDate2").clear()
    driver.find_element_by_name("ByDate2").send_keys(date[1])
    Select(driver.find_element_by_name("ByModel")).select_by_visible_text("按项目名称")
    ActionChains(driver).key_down(Keys.CONTROL).perform()
    for usage in ['双拼别墅', '独立别墅', '叠加别墅', '联排别墅', '住宅', ]:
        Select(driver.find_element_by_name("usage[]")).select_by_value(usage)
    for item in ['套数', '均价', ]:
        Select(driver.find_element_by_name("item[]")).select_by_visible_text(item)
    ActionChains(driver).key_up(Keys.CONTROL).perform()
    driver.find_element_by_name("Submit").click()
    input('>>> 出现结果后，按回车键继续...')
    return driver.page_source


def rengou(proj):
    input(">>> 按回车键继续查询竞品认购情况")
    driver.find_element_by_name("ByProject").clear()
    driver.find_element_by_name("ByProject").send_keys(proj)
    Select(driver.find_element_by_name("d_position1")).select_by_visible_text("*全市*")
    Select(driver.find_element_by_name("ByType")).select_by_visible_text('认购量')
    driver.find_element_by_name("Submit").click()


def table_chengjiao(html):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table')
    if table.caption:
        tr = table.find_all('tr')
        print()
        for each in tr[3:]:
            td = each.find_all('td')
            name = td[0].string
            tao = td[6].string
            price = td[7].string
            print("{}签约{}套，成交均价{}元/㎡，\n".format(name, tao, price))
    else:
        print('本周无成交。')


if __name__ == '__main__':
    try:
        login()
    except:
        print('something wrong')
    random_statistics()
    table_chengjiao(chengjiao(
        "润锦城,润江城,西江月花苑,荣里,建熙花苑,浦润花园,润尧花园,青秀城,燕江府,洺悦府,依云和府,海赋尚城",
        week()))
    rengou("润锦城,润江城,西江月花苑,荣里,建熙花苑,浦润花园")
