# 显存占用16159MiB
# 响应速度：较快
from lmdeploy import pipeline
pipe = pipeline("../model/Shanghai_AI_Laboratory/internlm2-chat-7b")

print("=============Welcome to chatbot, type 'exit' to exit.=============")
# while True:
#     response = pipe(["Hi, pls intro yourself", "Shanghai is"])

system_prompt = "Hi, pls intro yourself"
messages = system_prompt
while True:
    input_text = input("User  >>> ")
    input_text = input_text.replace(' ', '')
    if input_text == "exit":
        break
    response = pipe([messages, input_text])
    print(f"robot >>> {response}")
    # messages.append((input_text, response))
    # print(f"robot >>> {response}")

# from lmdeploy import turbomind as tm
#
# # load model
# model_path = "../model/Shanghai_AI_Laboratory/internlm2-chat-7b"
# tm_model = tm.TurboMind.from_pretrained(model_path, model_name='internlm2-chat-7b')
# generator = tm_model.create_instance()
#
# # process query
# query = "你好啊兄嘚"
# prompt = tm_model.model.get_prompt(query)
# input_ids = tm_model.tokenizer.encode(prompt)
#
# # inference
# for outputs in generator.stream_infer(
#         session_id=0,
#         input_ids=[input_ids]):
#     res, tokens = outputs[0]
#
# response = tm_model.tokenizer.decode(res.tolist())
# print(response)