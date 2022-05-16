from flask import Flask, render_template, jsonify
from jieba.analyse import extract_tags
import utils

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

#时间显示
@app.route('/time')
def get_time():
    return utils.get_time()

#疫情累计情况
@app.route('/c1')
def get_c1_data():
    data = utils.get_c1_data()
    return jsonify({"confirm":data[0],"confirm_now":data[1],"heal":data[2],"dead":data[3]})

#中国疫情分布情况
@app.route('/c2')
def get_c2_data():
    res = []
    for tup in utils.get_c2_data():
        res.append({"name":tup[0],"value":int(tup[1])})
    return jsonify({"data":res})

#全国累计趋势
@app.route('/l1')
def get_l1_data():
    data = utils.get_l1_data()
    day, confirm_add, heal_add = [], [], []
    for a, b, c in data[7:]:
        day.append(a.strftime("%m-%d"))
        confirm_add.append(b)
        heal_add.append(c)
    return jsonify({"day": day, "confirm_add": confirm_add, "heal_add": heal_add})

#中高风险地区
@app.route('/l2')
def get_l2_data():
    data = utils.get_l2_data()
    details = []
    risk = []
    end_update_time = data[0][0]
    for a, b, c, d, e, f in data:
        risk.append(f)
        details.append(f"{b}\t{c}\t{d}\t{e}")
    return jsonify({"update_time": end_update_time, "details": details, "risk": risk})


#省份确诊top5
@app.route('/r1')
def get_r1_data():
    data = utils.get_r1_data()
    province_name = []
    total_confirm = []
    for k,v in data:
        province_name.append(k)
        total_confirm.append(int(v))
    return jsonify({"province_name": province_name,"total_confirm": total_confirm})

#微博热搜词云显示
@app.route('/r2')
def get_r2_data():
    # [['马某某涉嫌利用网络从事危害国家安全活动', 3512099], ['你习惯用小拇指当支架托住手机吗', 1802972]]
    data = utils.get_r2_data()
    d = []
    for i in data:
        v = i[1]
        ks = extract_tags(i[0])
        for j in ks:
            if not j.isdigit():
                d.append({"name": j, "value": v})
    return jsonify({"kws": d})

if __name__ == '__main__':

    app.run(host="0.0.0.0",port=5000)
