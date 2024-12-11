
from flask import Flask, request, jsonify, render_template
import random
from collections import Counter

app = Flask(__name__)

# 干员列表
character_names = [
    "推进之王", "风笛", "嵯峨", "琴柳", "焰尾", "伺夜", "伊内丝", "缪尔赛思", "忍冬",
    "陈", "赫拉格", "煌", "斯卡蒂", "银灰", "棘刺", "史尔特尔", "山", "帕拉斯",
    "耀骑士临光", "艾丽妮", "百炼嘉维尔", "玛恩纳", "重岳", "仇白", "圣约送葬人", "赫德雷",
    "薇薇安娜", "止颂", "锏", "左乐", "乌尔比安", "佩佩", "维娜·维多利亚", "荒芜拉普兰德",
    "黑", "能天使", "W", "早露", "迷迭香", "空弦", "灰烬", "假日威龙陈", "远牙",
    "菲亚梅塔", "鸿雪", "提丰", "莱伊", "维什戴尔", "娜仁图亚",
    "年", "塞雷娅", "星熊", "森蚺", "瑕光", "泥岩", "号角", "斥罪", "涤火杰西卡", "黍",
    "闪灵", "夜莺", "凯尔希", "流明",
    "焰影苇草", "纯烬艾雅法拉", "安洁莉娜", "麦哲伦", "铃兰", "浊心斯卡蒂", "灵知", "令", "白铁",
    "淬羽赫默", "塑心", "魔王",
    "艾雅法拉", "莫斯提马", "伊芙利特", "刻俄柏", "夕", "异客", "卡涅利安", "澄闪",
    "黑键", "林", "霍尔海雅", "逻各斯", "妮芙", "玛露希尔",
    "阿", "傀影", "温蒂", "歌蕾蒂娅", "水月", "老鲤", "归溟幽灵鲨", "多萝西", "缄默德克萨斯",
    "麒麟R夜刀", "琳琅诗怀雅", "艾拉", "阿斯卡纶", "弑君者", "引星棘刺"
]

# 初始化投票结果
votes = Counter({name: 0 for name in character_names})

@app.route("/")
def index():
    """主页：随机显示两名角色供投票"""
    char1, char2 = random.sample(character_names, 2)
    return render_template("index.html", char1=char1, char2=char2)

@app.route("/vote", methods=["POST"])
def vote():
    """处理投票请求"""
    data = request.json
    winner = data.get("winner")
    loser = data.get("loser")
    if winner in votes and loser in votes:
        votes[winner] += 1
        votes[loser] -= 1
        return jsonify({"message": "投票成功", "votes": dict(votes)})
    else:
        return jsonify({"error": "无效的角色"}), 400

@app.route("/results")
def results():
    """显示投票结果"""
    # 按分数从高到低排序
    sorted_votes = sorted(votes.items(), key=lambda x: x[1], reverse=True)
    # 构造带有排名的结果
    ranked_results = [{"rank": i + 1, "name": name, "score": score} for i, (name, score) in enumerate(sorted_votes)]
    # 渲染模板并传递结果
    return render_template("results.html", results=ranked_results)

if __name__ == "__main__":
    app.run(debug=True)