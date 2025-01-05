'''
Author: LeiChen9 chenlei9691@gmail.com
Date: 2025-01-05 14:26:45
LastEditors: LeiChen9 chenlei9691@gmail.com
LastEditTime: 2025-01-05 14:42:54
FilePath: /Code/Baize/model/fortune_model.py
Description: OpenAI聊天模型封装

Copyright (c) 2025 by ${chenlei9691@gmail.com}, All Rights Reserved. 
'''
from openai import OpenAI
import json
import pdb
from typing import Dict, Any

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

def get_daily_fortune(zodiac: str, mbti: str) -> Dict[str, str]:
    """根据星座和MBTI获取运势分析
    
    Args:
        zodiac: 星座，如 "天蝎座"
        mbti: MBTI性格类型，如 "INTJ"
        
    Returns:
        包含日运、周运、月运的字典
    """
    config = load_config()
    client = init_openai_client(config)
    
    system_prompt = """你是一位专业的占星师和MBTI分析师。
请根据用户的星座和MBTI性格特征，从以下几个维度进行运势分析：
1. 事业发展
2. 人际关系
3. 健康状况
4. 财运
5. 个人成长

分析时请考虑：
- 星座特征与当前星象
- MBTI性格特点对各方面的影响
- 具体可行的建议

请用简洁专业的语言输出，每个时间维度(日运/周运/月运)控制在200字以内。
"""

    user_prompt = f"""请为星座是{zodiac}、MBTI是{mbti}的用户进行运势分析，分别给出：
1. 今日运势
2. 本周运势预测
3. 本月运势预测"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    response = chat_completion(client, messages)
    return {
        "content": response.content,
        "zodiac": zodiac,
        "mbti": mbti
    }

if __name__ == "__main__":
    # 测试用例
    result = get_daily_fortune("天秤座", "INFJ")
    print(result["content"])