# import streamlit as st
# import pandas as pd
# import numpy as np
#
# st.title('Uber pickups in NYC')
# DATA_COLUMN = 'data/time'
# DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
#             'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
#
#
# # 增加缓存
# @st.cache_data
# # 下载数据函数
# def load_data(nrows):
#     # 读取csv文件
#     data = pd.read_csv(DATA_URL, nrows=nrows)
#     # 转换小写字母
#     lowercase = lambda x: x.lower()
#     # 将数据重命名
#     data.rename(lowercase, axis='columns', inplace=True)
#     # 将数据以panda的数据列的形式展示出来
#     data[DATA_COLUMN] = pd.to_datetime(data[DATA_COLUMN])
#     # 返回最终数据
#     return data
#
#
# # 直接打印文本信息
# data_load_state = st.text('正在下载')
# # 下载一万条数据中的数据
# data = load_data(10000)
# # 最后输出文本显示
# data_load_state.text("完成！(using st.cache_data)")
#
# # 检查原始数据
# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(data)
#
# # 绘制直方图
# # 添加一个子标题
# st.subheader('Number of pickups by hour')
#
# # 使用numpy生成一个直方图，按小时排列
# hist_values = np.histogram(data[DATA_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
# # 使用Streamlit 的 st.bar_chart（） 方法来绘制直方图
# st.bar_chart(hist_values)
#
# # 使用滑动块筛选结果
# hour_to_filter = st.slider('hour', 0, 23, 17)
# # 实时更新
# filtered_data = data[data[DATA_COLUMN].dt.hour == hour_to_filter]
#
# # 为地图添加一个副标题
# st.subheader('Map of all pickups at %s:00' % hour_to_filter)
# # 使用st.map()函数绘制数据
# st.map(filtered_data)


# from transformers import AutoModel, AutoTokenizer
# import streamlit as st
# from streamlit_chat import message
#
# st.set_page_config(
#     page_title="ChatGLM-6b 演示",
#     page_icon=":robot:"
# )
# # robot是自带的emoji
#
#
# # 这个装饰器可以把读的数据放在缓存里，不用反复加载
# @st.cache_resource
# def get_model():
#     tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
#     model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).half().cuda()
#     model = model.eval()
#     return tokenizer, model
#
#
# MAX_TURNS = 20
# MAX_BOXES = MAX_TURNS * 2
#
#
# def predict(input, max_length, top_p, temperature, history=None):
#     tokenizer, model = get_model()
#     if history is None:
#         history = []
#
#     with container:
#         if len(history) > 0:
#             if len(history) > MAX_BOXES:
#                 history = history[-MAX_TURNS:]
#             for i, (query, response) in enumerate(history):
#                 message(query, avatar_style="big-smile", key=str(i) + "_user") #用来显示气泡，设置avatar_style头像
#                 message(response, avatar_style="bottts", key=str(i))
#
#         message(input, avatar_style="big-smile", key=str(len(history)) + "_user")
#         st.write("AI正在回复:")
#         with st.empty():
#             for response, history in model.stream_chat(tokenizer, input, history, max_length=max_length, top_p=top_p,
#                                                        temperature=temperature):
#                 query, response = history[-1]
#                 st.write(response)
#
#     return history
#
#
# container = st.container()
# # create a prompt text for the text generation
# prompt_text = st.text_area(label="用户命令输入",
#                            height=100,
#                            placeholder="请在这儿输入您的命令")
#
# max_length = st.sidebar.slider(
#     'max_length', 0, 4096, 2048, step=1
# )
# top_p = st.sidebar.slider(
#     'top_p', 0.0, 1.0, 0.6, step=0.01
# )
# temperature = st.sidebar.slider(
#     'temperature', 0.0, 1.0, 0.95, step=0.01
# )
#
# if 'state' not in st.session_state:
#     st.session_state['state'] = []
#
# if st.button("发送", key="predict"):
#     with st.spinner("AI正在思考，请稍等........"):
#         # text generation
#         st.session_state["state"] = predict(prompt_text, max_length, top_p, temperature, st.session_state["state"])

import streamlit as st

# 设置页面标题
st.title('我的Streamlit应用')
# 显示文本
st.write("欢迎来到我的Streamlit应用！")
# 添加一个文本输入框
user_input = st.text_input("请输入一些文本:")

# 根据用户输入显示结果
if user_input:
    st.write(f"你输入的文本是: {user_input}")

# 添加一个按钮
if st.button("点击我"):
    st.write("你点击了按钮！")
