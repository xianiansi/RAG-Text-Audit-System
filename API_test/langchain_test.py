# 通义 langchain 拼接
# langchain_community中自带的langchain拼接，用它的Template和Tongyi连接在一起变成一个pipeline，这和RAG有什么关系，嘶
import os
from langchain_community.llms import Tongyi
DASHSCOPE_API_KEY = 'sk-your-API-KEY'
os.environ["DASHSCOPE_API_KEY"] = DASHSCOPE_API_KEY


# # 方法1，先尝试一下invoke直接输出的效果，Tongyi()这个函数就已经是llm集成化的函数了，可能有默认设置的模型
# text = "What NFL team won the Super Bowl in the year Justin Bieber was born?"
# res = Tongyi().invoke(text)
# print(res)


# 方法2：指定特定模型
from langchain_core.prompts import PromptTemplate


llm = Tongyi(model_name="qwen-plus", temperature=0.1)
template = """Question: {question}
            Answer: Let's think step by step."""
prompt = PromptTemplate.from_template(template)  # 先写一个含{}字符串的模板template，然后转化为PromptTemplate类
chain = prompt | llm    # PromptTemplate模板|Tongyi模型 = 新的模型，注意！prompt在前面，llm在后面！

question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"
# result = chain.invoke(question)  # 新模型invoke出result，传入的参数是question
result = chain.invoke({"question": question}) # 我现在有模板了，我要告诉它，我现在传入的参数是{}里的question


print(result)
# 'Justin Bieber was born on March 1, 1994. The Super Bowl that took place in the same calendar year was Super Bowl XXVIII, which was played on January 30, 1994. The winner of Super Bowl XXVIII was the Dallas Cowboys, who defeated the Buffalo Bills with a score of 30-13.'
#
#
