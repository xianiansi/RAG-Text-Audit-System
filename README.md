# RAG-Text-Audit-System
``` streamlit run RAG_2.py ```
+ Transformers<br>
Transformers provide some basic models
Provide the entire paragraph to the pipeline and receive an answer;
Give the entire paragraph to the tokenizer AutoTokenizer first
Send it to AutoModelForSequenceClassification again and get the answer
+ 
## Result
+ **If there is relevant information in the original text：**
<br><img src=https://github.com/user-attachments/assets/10af91de-cac8-487d-aea5-36f587f8f0b1 width=600 height=250 /><br>
+ **Ask a vague question：**
<br><img src=https://github.com/user-attachments/assets/76376933-d152-46d1-82f0-49d84a0e248d width=600 height=200 /><br>
+ **Ask a completely unrelated question：**
<br><img src=https://github.com/user-attachments/assets/05866d70-81dc-4bc3-bfd4-c8da4bee61fa width=600 height=300 /><br>

