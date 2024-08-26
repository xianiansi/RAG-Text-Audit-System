from langchain_community.document_loaders import WebBaseLoader  #抓取网页内容
import bs4   # 解析HTML和XML文件
from langchain_text_splitters import RecursiveCharacterTextSplitter  #文本分割器
# from langchain import hub  # 模型/组件集合，可以用于预定义的模型或运行链
from langchain_chroma import Chroma   # 文档存储解决方案,矢量存储
from langchain_core.output_parsers import StrOutputParser  # 把模型输出解析为字符串形式
from langchain_core.runnables import RunnablePassthrough   # 占位符，把原始数据传递给下一环节
from langchain_community.embeddings import DashScopeEmbeddings
# from langchain_openai import OpenAIEmbeddings #文本嵌入模块
import os
from langchain_community.llms import Tongyi
# from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate



DASHSCOPE_API_KEY = 'your-key'
os.environ["DASHSCOPE_API_KEY"] = DASHSCOPE_API_KEY


from langchain.embeddings.huggingface import HuggingFaceEmbeddings
# HuggingFaceEmbeddings(model_name="/root/data/model/sentence-transformer")
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
loader = UnstructuredWordDocumentLoader("报告3.docx")
docs = loader.load()
# print(docs[0].page_content[:100])

# # Load, chunk and index the contents of the blog.
# loader = WebBaseLoader(
#     web_paths=("https://blog.csdn.net/m0_47738450/article/details/141243694",),
#     # bs_kwargs=dict(     # 定制解析行为
#     #     parse_only=bs4.SoupStrainer(    # 筛选网页中感兴趣的部分
#     #         class_=("post-content", "post-title", "post-header")
#     #     )
#     # ),
# )
# docs = loader.load()  # 文档的集合
# print(docs)

# 先分块，再嵌入embedding，再存储向量，再检索
# 把长文本分割成较小的块，每个文本块的最大字符数是1000，每个块之间有200个字符的重叠，保持上下文的连贯性
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200) #文本分块器
splits = text_splitter.split_documents(docs)  # 给文本分块
# 本来向量库直接读取文件，一句一句的映射，但是文件太大只能分块了
embeddings = DashScopeEmbeddings(model="text-embedding-v1")
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

# Retrieve and generate using the relevant snippets of the blog.
retriever = vectorstore.as_retriever()  # 检索器
# prompt = hub.pull("rlm/rag-prompt")     # 拉取一个提示模板


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


template = '''
        【任务描述】
        请根据用户输入的上下文回答问题，并遵守回答要求。

        【背景知识】
        {{context}}

        【回答要求】
        - 你需要严格根据背景知识的内容回答，禁止根据常识和已知信息回答问题。
        - 对于不知道的信息，直接回答“未找到相关答案”
        -----------
        {question}
        '''
prompt = PromptTemplate.from_template(template)  # 先写一个含{}字符串的模板template，然后转化为PromptTemplate类
llm = Tongyi(model_name="qwen-plus", temperature=0.1)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

res = rag_chain.invoke("张政同志自什么时候担任部门总经理的？")
print(res)



