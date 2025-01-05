'''
Author: LeiChen9 chenlei9691@gmail.com
Date: 2025-01-05 14:26:45
LastEditors: LeiChen9 chenlei9691@gmail.com
LastEditTime: 2025-01-05 15:14:39
FilePath: /Code/Baize/model/fortune_model.py
Description: OpenAI聊天模型封装

Copyright (c) 2025 by ${chenlei9691@gmail.com}, All Rights Reserved. 
'''
from openai import OpenAI
import json
from typing import Dict, Any, Tuple
from datetime import datetime
import locale
from kerykeion import AstrologicalSubject
import calendar
import pdb
# 设置中文环境
locale.setlocale(locale.LC_TIME, 'zh_CN.UTF-8')

def load_config(config_path: str = 'config.json') -> Dict[str, Any]:
    """加载配置文件
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        配置字典
    """
    with open(config_path, 'r') as f:
        return json.load(f)

def init_openai_client(config: Dict[str, str]) -> OpenAI:
    """初始化OpenAI客户端
    
    Args:
        config: 包含OpenAI配置的字典
        
    Returns:
        OpenAI客户端实例
    """
    return OpenAI(
        base_url=config['openai_endpoint'],
        api_key=config['openai_api_key']
    )

def chat_completion(client: OpenAI, 
                   messages: list,
                   model: str = "gpt-3.5-turbo") -> str:
    """执行聊天完成
    
    Args:
        client: OpenAI客户端实例
        messages: 对话消息列表
        model: 使用的模型名称
        
    Returns:
        助手的回复内容
    """
    completion = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return completion.choices[0].message

def get_time_info() -> Dict[str, Any]:
    """获取当前详细时间信息，并判断是否为工作日
    
    Returns:
        包含日期、星期、周数和日期类型信息的字典
    """
    now = datetime.now()
    
    # 获取当月第几周
    cal = calendar.monthcalendar(now.year, now.month)
    week_of_month = 0
    for i, week in enumerate(cal):
        if now.day in week:
            week_of_month = i + 1
            break
    
    # 判断是否为周末
    weekday = now.strftime("%A")
    is_weekend = now.weekday() >= 5
    
    # TODO: 这里可以添加节假日判断逻辑
    # 可以通过调用节假日API或维护节假日列表来实现
    is_holiday = False  # 暂时只判断周末
    
    return {
        "date": now.strftime("%Y年%m月%d日"),
        "weekday": weekday,
        "week_of_month": f"第{week_of_month}周",
        "month": now.strftime("%B"),
        "is_weekend": is_weekend,
        "is_holiday": is_holiday
    }

def calculate_zodiac(birth_date: datetime, birth_place: str = None) -> Dict[str, str]:
    """根据生日和出生地点计算星座信息
    
    Args:
        birth_date: 出生日期时间
        birth_place: 出生地点，格式如："北京市" 或 "30.5N,114.3E"
        
    Returns:
        包含太阳星座、上升星座、月亮星座的字典
    """
    # 星座日期范围（修正后的精确日期）
    zodiac_dates = [
        ((1, 20), "摩羯座"), ((2, 19), "水瓶座"), ((3, 21), "双鱼座"),
        ((4, 20), "白羊座"), ((5, 21), "金牛座"), ((6, 21), "双子座"),
        ((7, 23), "巨蟹座"), ((8, 23), "狮子座"), ((9, 23), "处女座"),
        ((10, 23), "天秤座"), ((11, 22), "天蝎座"), ((12, 22), "射手座"),
        ((12, 31), "摩羯座")
    ]
    
    # 获取月份和日期
    month = birth_date.month
    day = birth_date.day
    
    # 确定星座
    sun_sign = "摩羯座"  # 默认值
    for (end_month, end_day), sign in zodiac_dates:
        if month < end_month or (month == end_month and day <= end_day):
            sun_sign = sign
            break
    
    # 上升星座计算（简化版）
    rising_sign = "计算中"
    if birth_place:
        # TODO: 实现基于出生时间和地点的上升星座精确计算
        # 这需要考虑：
        # 1. 出生地点的经纬度
        # 2. 出生时间的地方时
        # 3. 黄道十二宫的计算
        rising_sign = f"需要精确计算 ({birth_place})"
    else:
        rising_sign = "需要出生地点信息"
    
    # 月亮星座计算（简化版）
    # TODO: 实现月亮星座计算
    # 这需要考虑：
    # 1. 月亮在黄道上的位置
    # 2. 出生时刻的月相
    moon_sign = "需要专业历书数据"
    
    return {
        "sun_sign": sun_sign,
        "rising_sign": rising_sign,
        "moon_sign": moon_sign,
        "birth_info": {
            "date": birth_date.strftime("%Y年%m月%d日 %H:%M"),
            "place": birth_place if birth_place else "未提供"
        }
    }

def get_daily_fortune(birth_date: datetime, gender: str, birth_place: str = None) -> Dict[str, Any]:
    """根据生日、性别和出生地点获取运势分析
    
    Args:
        birth_date: 出生日期时间
        gender: 性别 ("男"/"女")
        birth_place: 出生地点
        
    Returns:
        包含运势分析和时间信息的字典
    """
    config = load_config()
    client = init_openai_client(config)
    time_info = get_time_info()
    zodiac_info = calculate_zodiac(birth_date, birth_place)
    
    system_prompt = f"""你是一位专业的占星师。请根据用户的详细星座信息和个人特征，进行全面的运势分析。

分析对象信息：
- 性别：{gender}
- 出生信息：{zodiac_info['birth_info']['date']} {zodiac_info['birth_info']['place']}
- 太阳星座：{zodiac_info['sun_sign']}
- 上升星座：{zodiac_info['rising_sign']}
- 月亮星座：{zodiac_info['moon_sign']}

请首先给出一段总体运势概述（200字以内），然后从以下维度详细分析：

1. 爱情运势
   - {'桃花运和恋爱机遇' if gender == '男' else '异性缘和恋爱际遇'}
   - 当前感情状态的发展方向
   - 潜在的感情问题和建议
   - 适合的社交场合和活动

2. 财富运势
   - 财运走向和机遇
   - 理财投资建议
   - 支出管理策略
   - 事业带来的收益机会

3. 事业发展
   {'工作日分析：' if not (time_info['is_weekend'] or time_info['is_holiday']) else '休息日分析：'}
   - 职业发展方向
   - 工作中的机遇与挑战
   - 人际关系处理建议
   - 能力提升建议

4. 学习成长
   - 适合学习的领域和方向
   - 知识技能提升重点
   - 个人成长的机会
   - 心灵修养的建议

分析维度：
1. 今日运势：重点关注24小时内的关键时段和事项
2. 本周运势：{time_info['month']}{time_info['week_of_month']}整体走向
3. 本月运势：{time_info['month']}长期发展预测

注意事项：
- 结合性别特征给出针对性建议
- 考虑当前时间节点的特殊性
- 分析星座特征与当前星象的互动关系
- 给出具体可行的建议和预警
- 保持专业、积极、建设性的分析态度

请用简洁专业的语言输出，每个时间维度控制在300字以内。
"""

    user_prompt = f"""今天是{time_info['date']}，{time_info['weekday']}，{time_info['month']}{time_info['week_of_month']}。
请为这位{gender}性用户进行运势分析，请先给出总体运势概述，然后分别详细分析今日、本周、本月运势。"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    response = chat_completion(client, messages)
    return {
        "content": response.content,
        "zodiac_info": zodiac_info,
        "time_info": time_info,
        "gender": gender
    }

if __name__ == "__main__":
    # 测试用例
    birth_date = datetime(1996, 9, 24, 23, 40)  # 示例生日
    kanye = AstrologicalSubject("Kanye", 1996, 9, 24, 23, 40, "Beijing", "CN")
    print(kanye)
    pdb.set_trace()
    gender = "男"
    birth_place = "武汉市"
    
    result = get_daily_fortune(birth_date, gender, birth_place)
    print(f"时间：{result['time_info']['date']} {result['time_info']['weekday']}")
    print(f"出生信息：")
    print(f"- 出生时间：{result['zodiac_info']['birth_info']['date']}")
    print(f"- 出生地点：{result['zodiac_info']['birth_info']['place']}")
    print(f"\n星座信息：")
    print(f"- 太阳星座：{result['zodiac_info']['sun_sign']}")
    print(f"- 上升星座：{result['zodiac_info']['rising_sign']}")
    print(f"- 月亮星座：{result['zodiac_info']['moon_sign']}")
    print(f"\n运势分析：\n{result['content']}")