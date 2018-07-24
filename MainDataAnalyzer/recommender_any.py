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
"""
a - 电子信息 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04471
b - 新能源 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04931
c - 新材料 - http://quote.eastmoney.com/center/boardlist.html#boards-BK05231
d - 全息技术 - http://quote.eastmoney.com/center/boardlist.html#boards-BK06991

e - 医疗行业 - http://quote.eastmoney.com/center/boardlist.html#boards-BK07271
f - 保险 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04741
g - 化工行业 - http://quote.eastmoney.com/center/boardlist.html#boards-BK05381
h - 化肥行业 - http://quote.eastmoney.com/center/boardlist.html#boards-BK07311

i - 有色金属 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04781
j - 钢铁行业 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04791
k - 家电行业 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04561
l - 包装材料 - http://quote.eastmoney.com/center/boardlist.html#boards-BK07331

m - 水泥建材 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04241
n - 贵金属 - http://quote.eastmoney.com/center/boardlist.html#boards-BK07321
o - 电信运营 - http://quote.eastmoney.com/center/boardlist.html#boards-BK07361
p - 航天航空 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04801

q - 木业家具 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04761
r - 多元金融 - http://quote.eastmoney.com/center/boardlist.html#boards-BK07381
s - 食品饮料 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04381
t - 化工行业 - http://quote.eastmoney.com/center/boardlist.html#boards-BK05381

u - 水泥建材 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04241
v - 电信运营 - http://quote.eastmoney.com/center/boardlist.html#boards-BK07361
w - 家电行业 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04561
x - 专用设备 - http://quote.eastmoney.com/center/boardlist.html#boards-BK09101

y - 文教休闲 - http://quote.eastmoney.com/center/boardlist.html#boards-BK07401
z - 交运物流 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04221
aa - 塑胶制品 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04541
bb - 金属制品 - http://quote.eastmoney.com/center/boardlist.html#boards-BK07391

cc - 输配电气 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04571
dd - 石油行业 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04641
ee - 机械行业 - http://quote.eastmoney.com/center/boardlist.html#boards-BK05451
ff - 环保工程 - http://quote.eastmoney.com/center/boardlist.html#boards-BK07281

gg - 旅游酒店 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04851
hh - 船舶制造 - http://quote.eastmoney.com/center/boardlist.html#boards-BK07291
ii - 安防设备 - http://quote.eastmoney.com/center/boardlist.html#boards-BK07351
jj - 房地产 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04511

kk - 银行 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04751
ll - 汽车行业 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04811
mm - 装修装饰 - http://quote.eastmoney.com/center/boardlist.html#boards-BK07251
nn - 金属制品 - http://quote.eastmoney.com/center/boardlist.html#boards-BK07391

oo - 园林工程 - http://quote.eastmoney.com/center/boardlist.html#boards-BK07261
pp - 券商信托 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04731
qq - 港口水运 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04501
rr - 电力行业 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04281

ss - 造纸印刷 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04701
tt - 输配电气 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04571
uu - 化肥行业 - http://quote.eastmoney.com/center/boardlist.html#boards-BK07311
vv - 交运设备 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04291

ww - 农药兽药 - http://quote.eastmoney.com/center/boardlist.html#boards-BK07301
xx - 综合行业 - http://quote.eastmoney.com/center/boardlist.html#boards-BK05391
yy - 材料行业 - http://quote.eastmoney.com/center/boardlist.html#boards-BK05371
zz - 文化传媒 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04861

aaa - 国际贸易 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04841
bbb - 软件服务 - http://quote.eastmoney.com/center/boardlist.html#boards-BK07371
ccc - 电子信息 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04471
ddd - 电子元件 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04591

eee - 医药制造 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04651
fff - 包装材料 - http://quote.eastmoney.com/center/boardlist.html#boards-BK07331
ggg - 农牧饲渔 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04331
hhh - 酿酒行业 - http://quote.eastmoney.com/center/boardlist.html#boards-BK04771

"""
code_dict = {'a' : 'http://quote.eastmoney.com/center/boardlist.html#boards-BK04471',
             'b' : 'http://quote.eastmoney.com/center/boardlist.html#boards-BK04931',
             'c':'http://quote.eastmoney.com/center/boardlist.html#boards-BK05231',
             'd':'http://quote.eastmoney.com/center/boardlist.html#boards-BK06991',
             'e':'http://quote.eastmoney.com/center/boardlist.html#boards-BK07271',
             'f':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04741',
             'g':'http://quote.eastmoney.com/center/boardlist.html#boards-BK05381',
             'h':'http://quote.eastmoney.com/center/boardlist.html#boards-BK07311',
             'i':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04781',
             'j':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04791',
             'k':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04561',
             'l':'http://quote.eastmoney.com/center/boardlist.html#boards-BK07331',
             'm':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04241',
             'n':'http://quote.eastmoney.com/center/boardlist.html#boards-BK07321',
             'o':'http://quote.eastmoney.com/center/boardlist.html#boards-BK07361',
             'p':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04801',
             'q':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04761',
             'r':'http://quote.eastmoney.com/center/boardlist.html#boards-BK07381',
             's':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04381',
             't':'http://quote.eastmoney.com/center/boardlist.html#boards-BK05381',
             'u':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04241',
             'v':'http://quote.eastmoney.com/center/boardlist.html#boards-BK07361',
             'w':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04561',
             'x':'http://quote.eastmoney.com/center/boardlist.html#boards-BK09101',
             'y':'http://quote.eastmoney.com/center/boardlist.html#boards-BK07401',
             'z':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04221',
             'aa':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04541',
             'bb':'http://quote.eastmoney.com/center/boardlist.html#boards-BK07391',
             'cc':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04571',
             'dd':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04641',
             'ee':'http://quote.eastmoney.com/center/boardlist.html#boards-BK05451',
             'ff':'http://quote.eastmoney.com/center/boardlist.html#boards-BK07281',
             'gg':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04851',
             'hh':'http://quote.eastmoney.com/center/boardlist.html#boards-BK07291',
             'ii':'http://quote.eastmoney.com/center/boardlist.html#boards-BK07351',
             'jj':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04511',
             'kk':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04751',
             'll':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04811',
             'mm':'http://quote.eastmoney.com/center/boardlist.html#boards-BK07251',
             'nn':'http://quote.eastmoney.com/center/boardlist.html#boards-BK07391',
             'oo':'http://quote.eastmoney.com/center/boardlist.html#boards-BK07261',
             'pp':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04731',
             'qq':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04501',
             'rr':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04281',
             'ss':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04701',
             'tt':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04571',
             'uu':'http://quote.eastmoney.com/center/boardlist.html#boards-BK07311',
             'vv':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04291',
             'ww':'http://quote.eastmoney.com/center/boardlist.html#boards-BK07301',
             'xx':'http://quote.eastmoney.com/center/boardlist.html#boards-BK05391',
             'yy':'http://quote.eastmoney.com/center/boardlist.html#boards-BK05371',
             'zz':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04861',
             'aaa':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04841',
             'bbb':'http://quote.eastmoney.com/center/boardlist.html#boards-BK07371',
             'ccc':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04471',
             'ddd':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04591',
             'eee':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04651',
             'fff':'http://quote.eastmoney.com/center/boardlist.html#boards-BK07331',
             'ggg':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04331',
             'hhh':'http://quote.eastmoney.com/center/boardlist.html#boards-BK04771'}

name_dict = {'电子信息': 'a',
             '新能源':'b',
             '新材料':'c',
             '全息技术':'d',
             '医疗行业':'e',
             '保险':'f',
             '化工行业':'g',
             '化肥行业':'h',
             '有色金属':'i',
             '钢铁行业':'j',
             '家电行业':'k',
             '包装材料':'l',
             '水泥建材':'m',
             '贵金属':'n',
             '电信运营':'o',
             '航天航空':'p',
             '木业家具':'q',
             '多元金融':'r',
             '食品饮料':'s',
             '化工行业':'t',
             '水泥建材':'u',
             '电信运营':'v',
             '家电行业':'w',
             '专用设备':'x',
             '文教休闲':'y',
             '交运物流':'z',
             '塑胶制品':'aa',
             '金属制品':'bb',
             '输配电气':'cc',
             '石油行业':'dd',
             '机械行业':'ee',
             '环保工程':'ff',
             '旅游酒店':'gg',
             '船舶制造':'hh',
             '安防设备':'ii',
             '房地产':'jj',
             '银行':'kk',
             '汽车行业':'ll',
             '装修装饰':'mm',
             '金属制品':'nn',
             '园林工程':'oo',
             '券商信托':'pp',
             '港口水运':'qq',
             '电力行业':'rr',
             '造纸印刷':'ss',
             '输配电气':'tt',
             '化肥行业':'uu',
             '交运设备':'vv',
             '农药兽药':'ww',
             '综合行业':'xx',
             '材料行业':'yy',
             '文化传媒':'zz',
             '国际贸易':'aaa',
             '软件服务':'bbb',
             '电子信息':'ccc',
             '电子元件':'ddd',
             '医药制造':'eee',
             '包装材料':'fff',
             '农牧饲渔':'ggg',
             '酿酒行业':'hhh'}

codename_dict = {'a':'电子信息',
             'b':'新能源',
             'c':'新材料',
             'd':'全息技术',
             'e':'医疗行业',
             'f':'保险',
             'g':'化工行业',
             'h':'化肥行业',
             'i':'有色金属',
             'j':'钢铁行业',
             'k':'家电行业',
             'l':'包装材料',
             'm':'水泥建材',
             'n':'贵金属',
             'o':'电信运营',
             'p':'航天航空',
             'q':'木业家具',
             'r':'多元金融',
             's':'食品饮料',
             't':'化工行业',
             'u':'水泥建材',
             'v':'电信运营',
             'w':'家电行业',
             'x':'专用设备',
             'y':'文教休闲',
             'z':'交运物流',
             'aa':'塑胶制品',
             'bb':'金属制品',
             'cc':'输配电气',
             'dd':'石油行业',
             'ee':'机械行业',
             'ff':'环保工程',
             'gg':'旅游酒店',
             'hh':'船舶制造',
             'ii':'安防设备',
             'jj':'房地产',
             'kk':'银行',
             'll':'汽车行业',
             'mm':'装修装饰',
             'nn':'金属制品',
             'oo':'园林工程',
             'pp':'券商信托',
             'qq':'港口水运',
             'rr':'电力行业',
             'ss':'造纸印刷',
             'tt':'输配电气',
             'uu':'化肥行业',
             'vv':'交运设备',
             'ww':'农药兽药',
             'xx':'综合行业',
             'yy':'材料行业',
             'zz':'文化传媒',
             'aaa':'国际贸易',
             'bbb':'软件服务',
             'ccc':'电子信息',
             'ddd':'电子元件',
             'eee':'医药制造',
             'fff':'包装材料',
             'ggg':'农牧饲渔',
             'hhh':'酿酒行业'}

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

# 把数据中的 - 改为 0
def noSlash(str):
    if str == '-':
        return '0'
    else:
        return str


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
                                'close': [smartMultiply(noSlash(table[counter].find(class_=' listview-col-Close').string))],
                                'percent_chg': [smartMultiply(noSlash(table[counter].find(class_='listview-col-ChangePercent sorting_1').string))],
                                'change': [smartMultiply(noSlash(table[counter].find(class_=' listview-col-Change').string))],
                                'volume': [smartMultiply(noSlash(table[counter].find(class_=' listview-col-Volume').string))],
                                'turn_volume': [
                                    smartMultiply(noSlash(table[counter].find(class_=' listview-col-Amount').string))],
                                'amplitude': [
                                    smartMultiply(noSlash(table[counter].find(class_=' listview-col-Amplitude').string))],
                                'high': [smartMultiply(noSlash(table[counter].find(class_=' listview-col-High').string))],
                                'low': [smartMultiply(noSlash(table[counter].find(class_=' listview-col-Low').string))],
                                'now_open': [smartMultiply(noSlash(table[counter].find(class_=' listview-col-Open').string))],
                                'previous_close': [
                                    smartMultiply(noSlash(table[counter].find(class_=' listview-col-PreviousClose').string))],
                                'volume_rate': [
                                    smartMultiply(noSlash(table[counter].find(class_=' listview-col-VolumeRate').string))],
                                'turnover_rate': [
                                    smartMultiply(noSlash(table[counter].find(class_=' listview-col-TurnoverRate').string))],
                                'report_url': [
                                    'http://emweb.securities.eastmoney.com/f10_v2/FinanceAnalysis.aspx?type=web&code=sz' +
                                    table[counter].find(class_=' listview-col-Code').string + '#lrb-0'],
                                })
        counter += 1
        SFrame = SFrame.append(row_sframe)

    return SFrame


# 自动处理数据的主程序
def makeData(url, SFrame):
    browser = webdriver.Chrome()  # Get local session of chrome
    # url = search_area[topic]  # Example: '电子信息'
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
            print('Warning: 无法获得某些破损的数据.')
        bs = BeautifulSoup(browser.page_source, "lxml")
        counter += 1

    SFrame = SFrame[1:len(SFrame)]  # 删掉占位符
    SFrame = SFrame.unique()
    return SFrame


# 初步筛选分析程序
def analyze_stock(SFrame):
    SFrame = analysis_turnover_rate(SFrame, var_list[0])
    SFrame = analysis_volume_rate(SFrame, var_list[1])
    return SFrame

# 返回所有换手率大于5%的行
def analysis_turnover_rate(SFrame, turnover_rate):
    return SFrame[SFrame['turnover_rate'] > turnover_rate]

# 返回所有量比大于30%的行
def analysis_volume_rate(SFrame, volume_rate):
    return SFrame[ SFrame['volume_rate'] > volume_rate]

# 查找报表
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
    income_limit = var_list[2]
    profit_limit = var_list[3]
    counter = 0
    while counter < len(SFrame):
        if getReport(SFrame[counter]['report_url'], income_limit, profit_limit):
            print('股票名称：' + SFrame[counter]['name'])
            print('股票代码：' + SFrame[counter]['code'])
            print('成交量：' + str(SFrame[counter]['volume']))
            print('成交额：' + str(SFrame[counter]['turn_volume']))
            print('成交量比增幅：' + str(SFrame[counter]['amplitude']))
            print('换手率：' + str(SFrame[counter]['turnover_rate']))
            print('-------------------------------------------------')
        counter += 1

def user_interface():
    choice = greetings()
    if choice == 'a':
        var_list = inputCode()
    elif choice == 's':
        searchCode()
    elif choice == 'l':
        for element in [(k, codename_dict[k]) for k in sorted(codename_dict.keys())]:
            print(element)
        user_interface()
    else:
        user_interface()

def greetings():
    print('+-------------------欢迎界面-------------------+')
    print('| 请选择您要执行的操作:                          |')
    print('| 1. 输入a来分析指定板块                         |')
    print('| 2. 输入s来搜寻板块代码                         |')
    print('| 3. 输入l来显示所有代码                         |')
    print('+---------------------------------------------+')
    choice = str(input('命令:'))
    return choice

def searchCode():
    isDone = False
    print('+--------------输入想要查找的板块名--------------+')
    while isDone == False:
        user_input = str(input('搜索板块名:'))
        if user_input == 'quit':
            print('用户已取消操作！')
            break
        try:
            print(user_input + '代码是：' + name_dict[user_input])
            isDone = True
        except KeyError:
            print('板块不存在!')
    user_interface()

# 分析板块
def inputCode():
    print('+-------------------分析板块--------------------+')
    print('|输入变量：                                     |')
    print('-----------------------------------------------')
    turnover_rate = input('换手率大于（小数，如0.05对应5%）：')
    volume_rate= input('量比大于（小数，如0.3对应30%）：')
    income_rate = input('营业收入大于（小数，如0.3对应30%）：')
    benefit_rate = input('净利润大于（小数，如0.3对应30%）')
    print('+----------------------------------------------+')
    print('|输入板块代号（输入quit退出至主页面, all分析所有板块）|')
    print('-----------------------------------------------')
    code_name = str(input('代号:'))
    if code_name == 'all':
        for each_bk in code_dict:
            bk_name = codename_dict[each_bk]
            makeRecommend(code_dict[each_bk], bk_name)
    elif code_name == 'quit':
        user_interface()
    else:
        makeRecommend(code_dict[code_name], codename_dict[code_name])
    return [turnover_rate, volume_rate, income_rate, benefit_rate]

# 推荐股票
def makeRecommend(url, bk_name):
    # 创建四个空SFrame，以占位行开头
    all_data = tc.SFrame({'code': ['000000'], 'name': ['哔哩哔哩'],
                          'close': [0.0], 'percent_chg': [0.0],
                          'change': [0.0], 'volume': [0.0], 'turn_volume': [0.0], 'amplitude': [0.0],
                          'high': [0.0], 'low': [0.0],
                          'now_open': [0.0], 'previous_close': [0.0], 'volume_rate': [0.0],
                          'turnover_rate': [0.0], 'report_url': ['http://www.bilibili.com']})

    # 获取信息
    all_data = makeData(url, all_data)

    # 初步筛选
    analyze_data = analyze_stock(all_data)

    # 最终推荐
    print('---------------------' + bk_name + '---------------------')
    recommendStock(analyze_data)


# 执行UI
var_list= []
user_interface()

















