import hashlib
import datetime
from selenium import webdriver
import time
import sys
import requests
from mysql import sqlExecute

sqlDb = sqlExecute.MysqlDb()
"""
    获取历史数据和详细数据
"""
def get_data():
    header = {'User-Agent':
                  r'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36'}
    url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,diseaseh5Shelf,provinceCompare,diseaseh5Shelf'
    res = requests.get(url, headers=header).json()

    data = res['data']

    history = {}
    for i in data['chinaDayList']:
        ds = i['y'] + '.' + i['date']
        tup = time.strptime(ds, '%Y.%m.%d')
        ds = time.strftime('%Y-%m-%d', tup)
        history[ds] = {'confirm': i['confirm'],
                       'suspect': i['suspect'],
                       'heal': i['heal'],
                       'dead': i['dead'],
                       'confirm_now':i['nowConfirm']}

    for i in data['chinaDayAddList']:
        ds = i['y'] + '.' + i['date']
        tup = time.strptime(ds, '%Y.%m.%d')
        ds = time.strftime('%Y-%m-%d', tup)
        if ds not in history.keys():
            continue
        history[ds].update({'confirm_add': i['confirm'],
                            'suspect_add': i['suspect'],
                            'heal_add': i['heal'], 'dead_add': i['dead']})
    details = []
    update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    data_province = data['diseaseh5Shelf']['areaTree'][0]['children']
    for pro_infos in data_province:
        province = pro_infos['name']
        for city_infos in pro_infos['children']:
            city = city_infos['name']
            confirm = city_infos['total']['confirm']
            confirm_now = city_infos['total']['nowConfirm']
            confirm_add = city_infos['today']['confirm']
            heal = city_infos['total']['heal']
            dead = city_infos['total']['dead']
            details.append([update_time, province, city, confirm, confirm_add,confirm_now, heal, dead])
    return history,details

"""
    获取微博热搜数据
"""
def get_top_data():
    opt = webdriver.ChromeOptions()  # 创建浏览
    path = "/usr/local/bin/chromedriver"
    opt.add_argument("--headless")  # 隐藏浏览器
    opt.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=path,options=opt)  # 创建浏览器对象
    driver.get('https://www.weibotop.cn/2.0/')  # 打开网页
    time.sleep(2)  # 加载等待
    xpath = "//html/body/div/div[2]/div[2]/div[3]/ul/div/li/h5"
    top_text = driver.find_elements_by_xpath(xpath)
    path = "//html/body/div/div[2]/div[2]/div[3]/ul/div/li/p"
    web_hot = driver.find_elements_by_xpath(path)

    date_all = []
    for index in range(0, len(web_hot)):
        i = index + 1
        data_list = []
        #日期
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_list.append(date)
        #微博热搜内容
        web_text = top_text[i].text
        data_list.append(web_text)
        #微博热搜指数
        hot_index = web_hot[index].text
        data_list.append(hot_index)
        date_all.append(data_list)
    return date_all

"""
    获取中高风险地区的数据信息
"""
def get_risk_area():
    url_ = "http://103.66.32.242:8005/zwfwMovePortal/interface/interfaceJson"
    timestamp_ = str(time.time())[:10]
    no256sign = str(timestamp_) + "23y0ufFl5YxIyGrI8hWRUZmKkvtSjLQA" + "123456789abcdefg" + str(timestamp_)
    signature = hashlib.sha256(no256sign.encode('utf-8')).hexdigest().upper()

    data_ = {"appId": "NcApplication",
             "key": "3C502C97ABDA40D0A60FBEE50FAAD1DA",
             "nonceHeader": "123456789abcdefg",
             "paasHeader": "zdww",
             "signatureHeader": signature,
             "timestampHeader": str(timestamp_)}

    no256smt_sig = str(timestamp_) + "fTN2pfuisxTavbTuYVSsNJHetwq5bJvCQkjjtiLM2dCratiA" + str(timestamp_)
    smt_sig = hashlib.sha256(no256smt_sig.encode('utf-8')).hexdigest().upper()

    headers_ = {'x-wif-nonce': 'QkjjtiLM2dCratiA',
                'x-wif-paasid': 'smt-application',
                'x-wif-signature': smt_sig,
                'x-wif-timestamp': str(timestamp_),
                'Content-Type': "application/json; charset=UTF-8",
                }
    res = requests.post(url_, json=data_, headers=headers_).json()
    # print(str(getedthings))
    utime = res['data']['end_update_time']  # 更新时间
    hcount = res['data'].get('hcount', 0)  # 高风险地区个数
    mcount = res['data'].get('mcount', 0)  # 低风险地区个数
    # 具体数据
    hlist = res['data']['highlist']
    mlist = res['data']['middlelist']

    risk_h = []
    risk_m = []
    for hd in hlist:
        type = "高风险"
        province = hd['province']
        city = hd['city']
        county = hd['county']
        area_name = hd['area_name']
        communitys = hd['communitys']
        for x in communitys:
            risk_h.append([utime, province, city, county, x, type])

    for md in mlist:
        type = "中风险"
        province = md['province']
        city = md['city']
        county = md['county']
        area_name = md['area_name']
        communitys = md['communitys']
        for x in communitys:
            risk_m.append([utime, province, city, county, x, type])

    return risk_h, risk_m

"""
    将微博热搜插入数据库
"""
def update_hotsearch():
    datalist = get_top_data()
    print(f"{time.asctime()}开始更新热搜数据")
    sql = "insert into hotsearch(date,web_text,web_hot) " \
          "values(%s,%s,%s)"

    sqlDb.execute_sql(sql, datalist)
    print(f"{time.asctime()}结束更新热搜数据")

"""
   疫情详细数据 
"""
def update_details():
    details_datalist = get_data()[1]
    print(f"{time.asctime()}开始更新详细数据")
    sql = "insert into details(update_time,province,city,confirm,confirm_add,confirm_now,heal,dead) " \
          "values(%s,%s,%s,%s,%s,%s,%s,%s)"
    result = sqlDb.execute_sql(sql, details_datalist)
    print(f"{time.asctime()}结束更新详细数据")
    return result

"""
   疫情历史数据 
"""
def update_history():
    history_datalist = get_data()[0]
    print(f"{time.asctime()}开始更新历史数据")
    sql = "insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    sql_query = "select confirm from history where ds=%s"
    datalist = []
    for k, v in history_datalist.items():
        if v.get('confirm') is None: v.update({'confirm':0})
        if v.get('suspect_add') is None: v.update({'suspect_add': 0})
        if v.get('confirm_add') is None: v.update({'confirm_add':0})
        if v.get('confirm_now') is None: v.update({'confirm_now': 0})
        if v.get('suspect') is None: v.update({'suspect':0})
        if v.get('heal') is None: v.update({'heal':0})
        if v.get('heal_add') is None: v.update({'heal_add': 0})
        if v.get('dead') is None: v.update({'dead':0})
        if v.get('dead_add') is None: v.update({'dead_add': 0})
        # item 格式 {'2020-01-13': {'confirm': 41, 'suspect': 0, 'heal': 0, 'dead': 1}
        if not sqlDb.cursor.execute(sql_query, k):  # 如果当天数据不存在，才写入
            # print(k,type(v.get("confirm")),type(v.get("confirm_add")),v.get("confirm_now"),v.get("suspect"),v.get("suspect_add"),v.get("heal"),v.get("heal_add"),v.get("dead"),v.get('dead_add'))
            data = [k, v.get("confirm"), v.get("confirm_add"), v.get("confirm_now"),
                                 v.get("suspect"), v.get("suspect_add"), v.get("heal"),
                                 v.get("heal_add"), v.get("dead"), v.get("dead_add")]
            datalist.append(data)
    sqlDb.execute_sql(sql, datalist)
    print(f"{time.asctime()}历史数据更新完毕")

"""
   risk_h,risk_m 中高风险地区详细数据
"""
def update_risk_area():
    risk_h, risk_m = get_risk_area()
    sql = "insert into risk_area(end_update_time,province,city,county,address,type) values(%s,%s,%s,%s,%s,%s)"
    sql_query = 'select %s=(select end_update_time from risk_area order by id desc limit 1)'  # 对比当前最大时间戳
    res = sqlDb.cursor.execute(sql_query,risk_h[0][0])
    if not sqlDb.cursor.fetchone()[0]:
        print(f"{time.asctime()}开始更新最新数据")
        sqlDb.execute_sql(sql, risk_h)
        sqlDb.execute_sql(sql, risk_m)
        print(f"{time.asctime()}更新最新数据完毕")
    else:
        print(f"{time.asctime()}已是最新数据！")

if __name__ == "__main__":
    #update_hotsearch()
    #update_details()
    #update_history()
    #update_risk_area()
    s = """请输入参数:
            update_history  更新历史记录表
            update_details  更新详细表
            update_hotsearch  更新微博热搜
            update_risk_area  更新风险表
        """
    l = len(sys.argv)
    if l == 1:
        print(s)
    else:
        order = sys.argv[1]
        if order == "update_history":
            update_history()
        elif order == "update_details":
            update_details()
        elif order == "update_hotsearch":
            update_hotsearch()
        elif order == "update_risk_area":
            update_risk_area()
        else:
            print("错误的参数")


