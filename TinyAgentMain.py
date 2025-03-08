import gc
import os
import time

from Agent import Agent
import pandas as pd


# model:internlm\llama\qwen

def get_excel_name(path, time):
    file_path_ = path.split('/')
    if len(file_path_) >= 7:
        excel_path = os.path.join('results', f'{file_path_[4]}_{file_path_[-1]}_{time}.xlsx')
    else:
        excel_path = os.path.join('results', f'{file_path_[4]}_{time}.xlsx')

    return excel_path


model_path = "models\SchedAgent1"

all_folders = ['data/Brandimarte_Data/Text', 'data/Barnes/Text',
               'data/Dauzere_Data/Text', 'data/Hurink_Data/Text/edata',
               'data/Hurink_Data/Text/rdata', 'data/Hurink_Data/Text/sdata',
               'data/Hurink_Data/Text/vdata']


root_path = '../../SchedAlgoLib/'
agent = Agent(model_path, root_path + all_folders[0], 'llama')

response, _ = agent.text_completion(text='你好，你是谁', history=[])
print("response: ", response)
print("history: ", _)
for folder in all_folders[:]:
    break
    agent.update_tool(root_path + folder)
    print(agent.system_prompt)
    time_ = 30
    execl_path = get_excel_name(root_path + folder, time_)
    # 使用 pandas 的 ExcelWriter，选择 'openpyxl' 作为引擎
    with pd.ExcelWriter(execl_path, engine='openpyxl') as writer:
        # 创建一个空的 DataFrame
        df = pd.DataFrame()
        # 将空的 DataFrame 写入 Excel 文件中，即使它没有数据
        df.to_excel(writer, index=False)
    for filename in os.listdir(root_path + folder):
        print(f"start================={filename}==================================")
        if filename.endswith('xlsx') or filename.endswith('dat'):
            print("xlsx/dat跳过")
            continue
        prompt_use = f"现在有一个调度问题待求解，其文件路径为{filename}，请选择算法在{time_}s内求解该问题"
        response, _ = agent.text_completion(text=prompt_use, history=[])
        print("response: ", response)
        print("history: ", _)


