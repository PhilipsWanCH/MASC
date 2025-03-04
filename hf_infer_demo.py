# 显存占用：16181MiB
# 速度：较快
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


tokenizer = AutoTokenizer.from_pretrained("../model/Shanghai_AI_Laboratory/internlm2-chat-7b", trust_remote_code=True)
# 设置`torch_dtype=torch.float16`来将模型精度指定为torch.float16，否则可能会因为您的硬件原因造成显存不足的问题。
model = AutoModelForCausalLM.from_pretrained("../model/Shanghai_AI_Laboratory/internlm2-chat-7b", trust_remote_code=True, torch_dtype=torch.float16).cuda()
model = model.eval()


system_prompt = """You are an AI assistant whose name is InternLM (书生·浦语).
- InternLM (书生·浦语) is a conversational language model that is developed by Shanghai AI Laboratory (上海人工智能实验室). It is designed to be helpful, honest, and harmless.
- InternLM (书生·浦语) can understand and communicate fluently in the language chosen by the user such as English and 中文.
"""

messages = [(system_prompt, '')]

print("=============Welcome to InternLM chatbot, type 'exit' to exit.=============")

while True:
    input_text = input("User  >>> ")
    input_text = input_text.replace(' ', '')
    if input_text == "exit":
        break
    response, history = model.chat(tokenizer, input_text, history=messages)
    messages.append((input_text, response))
    print(f"robot >>> {response}")