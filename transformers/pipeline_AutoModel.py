from transformers import pipeline
# 创建问答pipeline
question_answerer = pipeline('question-answering')
# 提供问题和上下文
result = question_answerer({
    'question': 'What is the name of the repository?',
    'context': 'Pipeline has been included in the hugging face/transformers repository'
})
# 打印结果
print(result)



from transformers import AutoTokenizer,AutoModelForSequenceClassification
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
model = AutoModelForSequenceClassification.from_pretrained('bert-base-uncased')

inputs = tokenizer("Hello world !", return_tensors='pt')
outputs = model(**inputs)
model.save_pretrained("path_to_save_model")



# from datasets import load_dataset, load_metric
# dataset = load_dataset('glue', 'sst2')
# metric = load_metric('glue', 'sst2')
#
# import numpy as np
# from transformers import AutoTokenizer
# tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
#
# def preprocess_function(examples):
#     return tokenizer(examples['sentence'], truncation=True, max_length=512)
#
# encoded_dataset = dataset.map(preprocess_function, batched=True)
#
# from transformers import AutoModelForSequenceClassification
# model = AutoModelForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
#
# from transformers import TrainingArguments
#
# batch_size=16
# args = TrainingArguments(
#     "bert-base-uncased-finetuned-sst2",
#     evaluation_strategy="epoch",
#     save_strategy="epoch",
#     learning_rate=2e-5,
#     per_device_train_batch_size=batch_size,
#     per_device_eval_batch_size=batch_size,
#     num_train_epochs=5,
#     weight_decay=0.01,
#     load_best_model_at_end=True,
#     metric_for_best_model="accuracy"
# )
#
# def compute_metrics(eval_pred):
#     logits, labels = eval_pred                 # predictions: [batch_size,num_labels], labels:[batch_size,]
#     predictions = np.argmax(logits, axis=1)    # 将概率最大的类别作为预测结果
#     return metric.compute(predictions=predictions, references=labels)
#
# from transformers import Trainer
# trainer = Trainer(
#     model,
#     args,
#     train_dataset=encoded_dataset["train"],
#     eval_dataset=encoded_dataset["validation"],
#     tokenizer=tokenizer,
#     compute_metrics=compute_metrics
# )
#
# trainer.train()

# from transformers import GPT2LMHeadModel,GPT2Tokenizer
# import torch
# model = GPT2LMHeadModel .from_pretrained("gpt2")
# text = "Once upon a time ,"
# tokenizer = GPT2Tokenizer.from_pretrained( "gpt2")
# input_ids = tokenizer.encode(text,return_tensors="pt")
# with torch.no_grad():
#     outputs = model.generate(input_ids,max_length=50,num_return_sequences=1)
#     generated_texts = tokenizer.batch_decode(outputs,skip_special_tokens=True)
# for i, generated_text in enumerate(generated_texts ):
#     print(f"Generated text {i + 1}: {generated_text}")


# from transformers import pipeline
# classifier = pipeline('zero-shot-classification', model='roberta-large-mnli')
# sequence_to_classify = "one day I will see the world"
# candidate_labels = ['travel', 'cooking', 'dancing']
# result = classifier(sequence_to_classify, candidate_labels)
# print(result)
# sequence_to_classify = "The CEO had a strong handshake."
# candidate_labels = ['male', 'female']
# hypothesis_template = "This text speaks about a {} profession."
# classifier(sequence_to_classify, candidate_labels, hypothesis_template=hypothesis_template)

# from modelscope.pipelines import pipeline
# from modelscope.utils.constant import Tasks
#
# ner_pipeline = pipeline(Tasks.named_entity_recognition, 'damo/nlp_raner_named-entity-recognition_chinese-large-generic')
# result = ner_pipeline('他继续与貝塞斯達遊戲工作室在接下来辐射4游戏。')
#
# print(result)
# # {'output': [{'type': 'CORP', 'start': 4, 'end': 13, 'span': '貝塞斯達遊戲工作室'}, {'type': 'CW', 'start': 17, 'end': 20, 'span': '辐射4'}]}



key='sk-your-API-KEY'
from openai import OpenAI

client = OpenAI(
    base_url="https://xiaoai.plus/v1",
    api_key=key
)
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "你好"},
    ]
)
print(response)
