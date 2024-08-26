from http import HTTPStatus
import dashscope
from dashscope import Generation

dashscope.api_key = 'sk-your-API-KEY'
responses = Generation.call(model=Generation.Models.qwen_turbo,
                            prompt='今天天气好吗？')

if responses.status_code == HTTPStatus.OK:
    print(responses.output['text'])
else:
    print('Failed request_id: %s, status_code: %s, code: %s, message:%s' %
          (responses.request_id, responses.status_code, responses.code,
           responses.message))




import random
from http import HTTPStatus
# 建议dashscope SDK 的版本 >= 1.14.0
from dashscope import Generation
import dashscope

dashscope.api_key = 'sk-your-API-KEY'
def get_response(messages):
    response = Generation.call(model="qwen-turbo",
                               messages=messages,
                               # 将输出设置为"message"格式
                               result_format='message')
    return response

messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]

# 您可以自定义设置对话轮数，当前为3
for i in range(3):
    user_input = input("请输入：")
    # 将用户问题信息添加到messages列表中
    messages.append({'role': 'user', 'content': user_input})
    assistant_output = get_response(messages).output.choices[0]['message']['content']
    # 将大模型的回复信息添加到messages列表中
    messages.append({'role': 'assistant', 'content': assistant_output})
    print(f'用户输入：{user_input}')
    print(f'模型输出：{assistant_output}')
    print('\n')