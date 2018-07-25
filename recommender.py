# Hongjun Wu
# 20180723
# A script that recommends stock based on data and conditions given.

# Import Statement
from selenium import webdriver
from bs4 import BeautifulSoup
from decimal import Decimal
from selenium.common.exceptions import ElementNotVisibleException
import turicreate as tc
import datetime


fileRoot = './SelectedData'
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
    browser.implicitly_wait(20)  # 智能等待20秒

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
def getReport(SFrame, bankuai, row, income_limit, profit_limit):
    url = row['report_url']
    browser = webdriver.Chrome()  # Get local session of chrome
    browser.get(url)  # Load page
    soup = BeautifulSoup(browser.page_source, "lxml")
    browser.close()

    # 寻找股票名称
    stock_name = soup.findAll(id="stock_full_name123")

    # 粗加工数据
    ulist = []
    trs = soup.find_all('tr')
    for tr in trs:
        ui = []
        for td in tr:
            ui.append(td.string)
        ulist.append(ui)

    # 提取营业额和净利润
    income_increase = 0
    profit_increase = 0
    for element in ulist:
        if ('营业总收入' in element):
            income_data_list = element
            now_data = smartMultiply(income_data_list[3])
            past_data = smartMultiply(income_data_list[11])
            income_increase = (now_data - past_data) / past_data
        elif ('净利润' in element):
            profit_data_list = element
            now_data = smartMultiply(profit_data_list[3])
            past_data = smartMultiply(profit_data_list[11])
            profit_increase = (now_data - past_data) / past_data

    if income_increase > income_limit and profit_increase > profit_limit:
        print('营业总收入增长', income_increase)
        print('净利润增长', profit_increase)
        new_row = tc.SFrame({'code': [row['code']], 'name': [row['name']], 'bankuai': [bankuai],
                                   'close': [row['close']], 'percent_chg': [row['percent_chg']], 'change': [row['change']],
                                   'volume': [row['volume']], 'turn_volume': [row['turn_volume']],
                                   'amplitude': [row['amplitude']], 'volume_rate': [row['volume_rate']], 'turnover_rate': [row['turnover_rate']],
                                   'news_url': [''], 'income_increase': [income_increase],
                                   'profit_increase': [profit_increase]})
        selected_data.append(new_row)

    return [income_increase > income_limit and profit_increase > profit_limit, income_increase, profit_increase]

"""
# 用于在精选数据库中添加精选信息
def appendSFrame(SFrame, stock_name, bankuai, income_increase, profit_increase):
    origional_data = SFrame['name' == stock_name]
    row = tc.SFrame({'code': [origional_data['code']], 'name': [origional_data['name']],
                     'bankuai': [bankuai],
                     'close': [origional_data['close']], 'percent_chg': [origional_data['percent_chg']],
                     'change': [origional_data['change']], 'volume': [origional_data['volume']],
                     'turn_volume': [origional_data['turn_volume']], 'amplitude': [origional_data['amplitude']],
                     'volume_rate': [origional_data['volume_rate']], 'turnover_rate': [origional_data['turnover_rate']],
                     'news_url': [''],
                     'income_increase': [income_increase], 'profit_increase': [profit_increase]})
    selected_data.append(row)
"""

def recommendStock(SFrame, bankuai):
    income_limit = var_list[2]
    profit_limit = var_list[3]
    counter = 0
    while counter < len(SFrame):
        result_list = getReport(SFrame[counter], bankuai, SFrame[counter], income_limit, profit_limit)
        if result_list[0]:
            print('股票名称：' + SFrame[counter]['name'])
            print('股票代码：' + SFrame[counter]['code'])
            print('成交量：' + str(SFrame[counter]['volume']))
            print('成交额：' + str(SFrame[counter]['turn_volume']))
            print('成交量比增幅：' + str(SFrame[counter]['amplitude']))
            print('换手率：' + str(SFrame[counter]['turnover_rate']))
            print('-------------------------------------------------')
            # appendSFrame(selected_data, SFrame[counter]['name'], bankuai, result_list[1], result_list[2])

            row = tc.SFrame({'code': [SFrame[counter]['code']], 'name': [SFrame[counter]['name']],
                             'bankuai': [bankuai],
                             'close': [SFrame[counter]['close']], 'percent_chg': [SFrame[counter]['percent_chg']],
                             'change': [SFrame[counter]['change']], 'volume': [SFrame[counter]['volume']],
                             'turn_volume': [SFrame[counter]['turn_volume']], 'amplitude': [SFrame[counter]['amplitude']],
                             'volume_rate': [SFrame[counter]['volume_rate']],
                             'turnover_rate': [SFrame[counter]['turnover_rate']],
                             'news_url': [''],
                             'income_increase': [result_list[1]], 'profit_increase': [result_list[2]]})
            selected_data.append(row)

        counter += 1

def user_interface():
    choice = greetings()
    if choice == 'a':
        inputCode()
    elif choice == 's':
        searchCode()
    elif choice == 'l':
        print('----------------以下是所有板块代码----------------')
        element_list = [(k, codename_dict[k]) for k in sorted(codename_dict.keys())]
        counter = 0
        while counter < len(element_list):
            print(element_list[counter][0] + ' - ' + element_list[counter][1])
            counter += 1
        print('-----------------------------------------------')
        user_interface()
    elif choice == 'x':
        print(selected_data)
        if selected_data[0]['name'] != '数据不存在':
            selected_data.show()
        else:
            print('没有分析完成的数据！')
        user_interface()
    elif choice == 'j':
        fileName = input('输入文件名：')
        parseSFrame(fileName)
        user_interface()
    else:
        user_interface()

def greetings():
    print('+-------------------欢迎界面-------------------+')
    print('| 请选择您要执行的操作:                          |')
    print('| 1. 输入a来分析指定板块                         |')
    print('| 2. 输入s来搜寻板块代码                         |')
    print('| 3. 输入l来显示所有代码                         |')
    print('| 4. 输入x来显示所有选股                         |')
    print('| 5. 输入j来加载以前分析完成股票数据               |')
    print('| 6. 输入n来加载以前分析完成新闻数据               |')
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
    turnover_rate = input('换手率大于（默认0.05对应5%）：')
    if turnover_rate == '':
        print('换手率设为默认0.05！')
        turnover_rate = 0.05
    var_list.append(float(turnover_rate))

    volume_rate= input('量比大于（默认0.3对应30%）：')
    if volume_rate == '':
        print('量比设为默认0.3！')
        volume_rate = 0.3
    var_list.append(float(volume_rate))

    income_rate = input('营业收入大于（默认0.3对应30%）：')
    if income_rate == '':
        print('营业收入设为默认0.3！')
        income_rate = 0.3
    var_list.append(float(income_rate))

    benefit_rate = input('净利润大于（默认0.3对应30%）:')
    if benefit_rate == '':
        print('净利润设为默认0.3！')
        benefit_rate = 0.3
    var_list.append(float(benefit_rate))

    print('+----------------------------------------------+')
    print('|输入板块代号（输入quit退出至主页面, all分析所有板块）|')
    print('-----------------------------------------------')
    code_name = str(input('代号:'))
    if code_name == 'all':
        for each_bk in code_dict:
            bk_name = codename_dict[each_bk]
            makeRecommend(selected_data, code_dict[each_bk], bk_name)
    elif code_name == 'quit':
        user_interface()
    else:
        makeRecommend(selected_data, code_dict[code_name], codename_dict[code_name])

    saveSFrame(selected_data, fileRoot)
    showSFrame(selected_data)
    return [turnover_rate, volume_rate, income_rate, benefit_rate]


# 目前很简陋
def showSFrame(selected_data):
    print(selected_data)


# 用于加载SFrame
def parseSFrame(fileName):
    filePath = './SelectedData/' + fileName + '/'
    selected_data = tc.SFrame(data=filePath)


# 用于保存SFrame
def saveSFrame(SFrame, fileRoot):
    # 保存数据
    date = '20' + str(datetime.datetime.now().strftime("%y%m%d-%H%M"))
    filepath = fileRoot + '/' + str(date) + '/'
    SFrame.save(filepath)
    print('成功保存数据文件！数据路径：' + filepath)

    # 打印时间戳
    print('程序运行时间戳：20'
          + str(datetime.datetime.now().strftime("%y")) + '年'
          + str(datetime.datetime.now().strftime("%m")) + '月'
          + str(datetime.datetime.now().strftime("%d")) + '日'
          + str(datetime.datetime.now().strftime("%H")) + '时'
          + str(datetime.datetime.now().strftime("%M")) + '分'
          + str(datetime.datetime.now().strftime("%S")) + '秒')

# 用于移除第一个占位符
def removeFront(SFrame):
    return SFrame[1:len(SFrame)]

# 推荐股票
def makeRecommend(selected_data, url, bk_name):
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
    recommendStock(analyze_data, bk_name)

    # selected_data = removeFront(selected_data)

    # user_interface()

    # return selected_data


# ===================================主执行部分===================================
# 执行UI
var_list= []

# 新建精选数据库
selected_data = tc.SFrame({'code': ['000000'], 'name': ['数据不存在'],'bankuai': ['二次元'],
                      'close': [0.0], 'percent_chg': [0.0],'change': [0.0],
                      'volume': [0.0], 'turn_volume': [0.0],
                      'amplitude': [0.0],'volume_rate': [0.0],'turnover_rate': [0.0],
                      'news_url': ['http://www.bilibili.com'], 'income_increase': [0.0], 'profit_increase': [0.0]})

# UI
user_interface()

















