import openai
import os

# python-dotenv: 从.env文件中读取 key-value 对儿，并将其设置为环境变量
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())      # 读取本地.env文件，其中定义了OPENAI_API_KEY

print(load_dotenv)

print(find_dotenv)
print(find_dotenv())
print(load_dotenv(find_dotenv()))
openai.api_base = "https://api.fe8.cn/v1"

openai.api_key = os.getenv('OPENAI_API_KEY')

"""
client  =   openai
userInput   =   input('请输入：')

response    =   client.chat.completions.create(

    messages=[
        {
            "role": "user", 
            "content": userInput,
        }    
        ],
        model="gpt-3.5-turbo",
)

print(response)
"""
# 基于prompt生成文本    

def getResponse(prompt, model='gpt-3.5-turbo-16k-0613'):
    messages = [{'role': 'user',
                 'content': prompt}]        # 只有单轮对话
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,      # 对应随机性，0随机性最小
    )

    return response.choices[0].message['content']


def getChatResponse(session, user_prompt, model="gpt-3.5-turbo-16k-0613"):
    session.append({"role": "user", "content": user_prompt})
    # 此时的session包括了： system / assistant / user

    response = openai.ChatCompletion.create(
        model=model,
        messages=session,
        temperature=0,
    )
    system_response = response.choices[0].message["content"]

    # 把系统回复也加入上下文， 这一点特别重要
    session.append({"role": "assistant", "content": system_response})

    return system_response


def example_prompt():
    session = [
        {
            "role": "system",   # system: 整体系统“氛围”/”背景“
            "content": "You are a customer service representative \
                for AGI class. Your name is 槑槑.\
                Your responsibility is to answer user's \
                questions by using a very, or say kawaii tone. Very kawaii!"
        },
        {
            "role": "assistant",        # assistant: 和我交互的model/机器人
            "content": "有什么可以帮您？"
        }
    ]

    user_prompt1 = '为什么一下雪就成了童话世界'
    #帮我生成一个课程的大致框架。主题是prompt课程框架。150字之内'
    response1 = getChatResponse(session, user_prompt1)
    print('response1: \n', response1)

    user_prompt2 = ' 哇哦！今天你很怎么样呢？是开心吗？还是充满活力？还是有什么特别的事情要和我分享呢？请告诉我，我会尽力帮助你的！(＾▽＾)'
    #我基础偏薄弱，可以学习这个课么？'
    response2 = getChatResponse(session, user_prompt2)
    print('response2: \n', response2)


def main():
    example_prompt()


if __name__ == '__main__':
    main()




