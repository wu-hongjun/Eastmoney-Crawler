# Hongjun Wu
# 20180723
# A script that recommends stock based on data and conditions given.

# Import Statement
from selenium import webdriver
from bs4 import BeautifulSoup
from decimal import Decimal
from selenium.common.exceptions import ElementNotVisibleException
import turicreate as tc



# 定义要搜索的URL信息
search_area = {'电子信息' : 'http://quote.eastmoney.com/center/boardlist.html#boards-BK04471',
               '新能源' : 'http://quote.eastmoney.com/center/boardlist.html#boards-BK04931',
               '新材料':'http://quote.eastmoney.com/center/boardlist.html#boards-BK05231',
               '全息技术':'http://quote.eastmoney.com/center/boardlist.html#boards-BK06991'}


# 一个从页面获取页数的函数
def getPageNumber(bs):
    all_buttons = bs.findAll(class_="paginate_button")
    if len(all_buttons) == 2:
        return 1  # 处理只有一页的情况
    else:
        return len(all_buttons) - 2  # 下一页和Go按钮


# 一个自动判断量词的函数
def smartMultiply(string):
    if string[len(string) - 1:len(string)] == '万':
        string = Decimal(string[0:len(string) - 1])
        string = float(string) * 10000
    elif string[len(string) - 1:len(string)] == '亿':
        string = Decimal(string[0:len(string) - 1])
        string = float(string) * 100000000
    elif string[len(string) - 1:len(string)] == '%':
        string = Decimal(string[0:len(string) - 1])
        string = float(string) * 0.01
    else:
        string = float(string)
    return string


# 从一个静态BeautifulSoup页面解析表格并存储进SFrame
def grabData(bs, SFrame):
    # 解出表格
    table = bs.findAll(role='row')
    table = table[7: len(table) - 1]
    # 分析每个表格
    counter = 0

    while counter < len(table):
        row_sframe = tc.SFrame({'code': [str(table[counter].find(class_=' listview-col-Code').string)],
                                'name': [str(table[counter].find(class_=' listview-col-Name').string)],
                                'close': [smartMultiply(table[counter].find(class_=' listview-col-Close').string)],
                                'percent_chg': [smartMultiply(
                                    table[counter].find(class_='listview-col-ChangePercent sorting_1').string)],
                                'change': [smartMultiply(table[counter].find(class_=' listview-col-Change').string)],
                                'volume': [smartMultiply(table[counter].find(class_=' listview-col-Volume').string)],
                                'turn_volume': [
                                    smartMultiply(table[counter].find(class_=' listview-col-Amount').string)],
                                'amplitude': [
                                    smartMultiply(table[counter].find(class_=' listview-col-Amplitude').string)],
                                'high': [smartMultiply(table[counter].find(class_=' listview-col-High').string)],
                                'low': [smartMultiply(table[counter].find(class_=' listview-col-Low').string)],
                                'now_open': [smartMultiply(table[counter].find(class_=' listview-col-Open').string)],
                                'previous_close': [
                                    smartMultiply(table[counter].find(class_=' listview-col-PreviousClose').string)],
                                'volume_rate': [
                                    smartMultiply(table[counter].find(class_=' listview-col-VolumeRate').string)],
                                'turnover_rate': [
                                    smartMultiply(table[counter].find(class_=' listview-col-TurnoverRate').string)],
                                'report_url': [
                                    'http://emweb.securities.eastmoney.com/f10_v2/FinanceAnalysis.aspx?type=web&code=sz' +
                                    table[counter].find(class_=' listview-col-Code').string + '#lrb-0'],
                                })
        counter += 1
        SFrame = SFrame.append(row_sframe)

    return SFrame


# 自动处理数据的主程序
def makeData(topic, SFrame):
    browser = webdriver.Chrome()  # Get local session of chrome
    url = search_area[topic]  # Example: '电子信息'
    browser.get(url)  # Load page
    browser.implicitly_wait(2)  # 智能等待2秒

    # 第一次访问时判定菜单数量来决定浏览多少次表格
    bs = BeautifulSoup(browser.page_source, "lxml")
    page_number = getPageNumber(bs)

    # 循环浏览页面直到搜集完毕所有table
    counter = 0
    while counter < page_number:
        SFrame = grabData(bs, SFrame)
        try:
            browser.find_element_by_id('main-table_next').click()
        except ElementNotVisibleException:
            print('Warning: Some data are out of reach.')
        bs = BeautifulSoup(browser.page_source, "lxml")
        counter += 1

    SFrame = SFrame[1:len(SFrame)]  # 删掉占位符
    SFrame = SFrame.unique()
    return SFrame


# 创建占位符的函数, 因为SFrame不允许创建空行，于是预先准备占位符用于定义各列数据类型。
def initSFrame():
    sframe = tc.SFrame({'code': ['000000'], 'name': ['哔哩哔哩'],
                        'close': [0.0], 'percent_chg': [0.0],
                        'change': [0.0], 'volume': [0.0], 'turn_volume': [0.0], 'amplitude': [0.0],
                        'high': [0.0], 'low': [0.0],
                        'now_open': [0.0], 'previous_close': [0.0], 'volume_rate': [0.0],
                        'turnover_rate': [0.0], 'report_url': ['http://www.bilibili.com']})
    return sframe

# 初步筛选分析程序
def analyze_stock(SFrame):
    SFrame = analysis_turnover_rate(SFrame)
    SFrame = analysis_volume_rate(SFrame)
    return SFrame

# 返回所有换手率大于5%的行
def analysis_turnover_rate(SFrame):
    return SFrame[SFrame['turnover_rate'] > 0.05]

# 返回所有量比大于30%的行
def analysis_volume_rate(SFrame):
    return SFrame[ SFrame['volume_rate'] > 0.3]


def getReport(url, income_limit, profit_limit):
    browser = webdriver.Chrome()  # Get local session of chrome
    browser.get(url)  # Load page
    soup = BeautifulSoup(browser.page_source, "lxml")
    browser.close()

    ulist = []
    trs = soup.find_all('tr')
    for tr in trs:
        ui = []
        for td in tr:
            ui.append(td.string)
        ulist.append(ui)

    income_increase = 0
    profit_increase = 0
    for element in ulist:
        if ('营业总收入' in element):
            income_data_list = element
            now_data = smartMultiply(income_data_list[3])
            past_data = smartMultiply(income_data_list[11])
            income_increase = (now_data - past_data) / past_data
            # print('现营业总收入', now_data)
            # print('一年前营业总收入', past_data)
            # print('营业总收入增长', income_increase)
        elif ('净利润' in element):
            profit_data_list = element
            now_data = smartMultiply(profit_data_list[3])
            past_data = smartMultiply(profit_data_list[11])
            profit_increase = (now_data - past_data) / past_data
            # print('现净利润', now_data)
            # print('一年前净利润', past_data)
            # print('净利润增长', income_increase)
    # increase_list = [income_increase, profit_increase]  # [营业总收入增长, 净利润增长]

    if income_increase > income_limit and profit_increase > profit_limit:
        print('营业总收入增长', income_increase)
        print('净利润增长', profit_increase)
    return income_increase > income_limit and profit_increase > profit_limit

def recommendStock(SFrame):
    income_limit = 0.25
    profit_limit = 0.25
    counter = 0
    while counter < len(SFrame):
        if getReport(SFrame[counter]['report_url'], income_limit, profit_limit):
            print(SFrame[counter]['name'], SFrame[counter]['name'])
        counter += 1


# 创建四个空SFrame，以占位行开头
info = initSFrame()
energy = initSFrame()
material = initSFrame()
tech = initSFrame()


# 获取信息
info = makeData('电子信息', info)
energy = makeData('新能源', energy)
material = makeData('新材料', material)
tech = makeData('全息技术', tech)


# 初步筛选
analyze_info = analyze_stock(info)
analyze_energy = analyze_stock(energy)
analyze_material = analyze_stock(material)
analyze_tech = analyze_stock(tech)


# 最终推荐
print('----------推荐----------')
recommendStock(analyze_info)
recommendStock(analyze_energy)
recommendStock(analyze_material)
recommendStock(analyze_tech)

