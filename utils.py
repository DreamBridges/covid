import time
from mysql import sqlExecute

# 获取实时时间
def get_time():
    time_str = time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format("年","月","日")

#获取疫情数据情况
def get_c1_data():
    date_time = time.strftime("%Y-%m-%d, %H:%M:%S")
    sqlDb = sqlExecute.MysqlDb()
    sql = "select confirm,confirm_now,heal,dead from history ORDER BY ds desc LIMIT 1"
    result = sqlDb.selectOne(sql)
    return result

#获取各省疫情数据情况
def get_c2_data():
    sqlDb = sqlExecute.MysqlDb()
    # 因为会更新多次数据，取时间戳最新的那组数据
    sql = "select province,sum(confirm) from details " \
          "where update_time=(select update_time from details " \
          "order by update_time desc limit 1) " \
          "group by province"
    result = sqlDb.selectMany(sql, 34)
    data_list = []
    for i in result:
        data_list.append(list(i))
    for i in data_list:
        i[1] = int(i[1])
    return data_list

# 日期、新增确诊、新增治愈
def get_l1_data():
    sqlDb = sqlExecute.MysqlDb()
    sql = "select ds,confirm_add,heal_add from history"
    sql1 = "select count(1) from history"
    count = sqlDb.selectOne(sql1)
    result = sqlDb.selectMany(sql, count[0])
    data_list = []
    for i in result:
        data_list.append(list(i))
    return data_list

# 中高风险地区
def get_l2_data():
    sqlDb = sqlExecute.MysqlDb()
    sql = "select end_update_time,province,city,county,address,type" \
          " from risk_area " \
          "where end_update_time=(select end_update_time " \
          "from risk_area " \
          "order by end_update_time desc limit 1) "
    sql_query = "select count(1) from risk_area " \
                "where end_update_time=(select end_update_time " \
                "from risk_area " \
                "order by end_update_time desc limit 1) "
    result = sqlDb.selectOne(sql_query)
    datalist = sqlDb.selectMany(sql, result[0])
    return datalist

def get_r1_data():
    sqlDb = sqlExecute.MysqlDb()
    sql = 'SELECT province,confirm FROM ' \
          '(select province ,sum(confirm) as confirm from details  ' \
          'where update_time=(select update_time from details ' \
          'order by update_time desc limit 1) ' \
          'group by province) as a ' \
          'ORDER BY confirm DESC LIMIT 5'
    result = sqlDb.selectMany(sql, 5)
    data_list = []
    for i in result:
        data_list.append(list(i))
    for i in data_list:
        i[1] = int(i[1])
    return data_list

def get_r2_data():
    sqlDb = sqlExecute.MysqlDb()
    sql = "select web_text,web_hot from hotsearch order by id desc limit 50"
    result = sqlDb.selectMany(sql, 50)
    return result

#数据清洗

# {'2022-03-13':
#       {'confirm': 397659,
#       'suspect': 5,
#       'heal': 145499,
#       'dead': 9482,
#       'confirm_now': 242678,
#       'confirm_add': 5944,
#       'suspect_add': 1,
#       'heal_add': 876,
#       'dead_add': 264}
def data_clear():
    pass
