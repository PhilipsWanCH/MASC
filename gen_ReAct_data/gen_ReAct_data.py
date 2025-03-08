import random

import pandas as pd
from LLM import get_response
import json
import os
import copy

template = {
    "conversation": [
        {
            "system": "xxx",
            "input": "xxx",
            "output": "xxx"
        }
    ]
}
add_template = {
    "input": "xxx",
    "output": "xxx"
}

import re


def extract_key_lines(text):
    # 正则表达式匹配含有'Action'或'Action Input'的行
    pattern = r"^(.*(?:Action|Action Input).*)$"

    # 使用正则表达式找到所有匹配的行
    matches = re.findall(pattern, text, re.MULTILINE)

    # 将匹配的行连接成一个新的字符串，每行之间用换行符分隔
    return "\n".join(matches)


def load_txt(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    return data


def save_answer(answer, save_path):
    with open(save_path, 'a', encoding='utf-8') as f:  # Change to 'a' mode for appending
        json_item = json.dumps(answer, ensure_ascii=False)
        f.write(json_item + "\n")


def read_excel_data(file_path):
    try:
        data = pd.read_excel(file_path)
        return data
    except Exception as e:
        print(f"读取Excel文件时出错: {e}")
        return None


def find_top_three_algorithms(data_frame):
    """
    为每个案例找到前三个结果最小的算法，如果结果相同则按耗时排序。

    参数:
    data_frame (pd.DataFrame): 包含完整数据的DataFrame。

    返回:
    pd.DataFrame: 包含案例特点和前三个算法结果及其运行时间的DataFrame。
    """
    # 算法结果列
    result_columns = ['GA Result', 'MIP Result', 'FIFO_SPT', 'FIFO_EET',
                      'MOPNR_SPT', 'MOPNR_EET', 'LWKR_SPT', 'LWKR_EET',
                      'MWKR_SPT', 'MWKR_EET']
    # 算法运行时间列
    runtime_columns = ['GA Runtime', 'MIP Runtime', 'FIFO_SPTt', 'FIFO_EETt',
                       'MOPNR_SPTt', 'MOPNR_EETt', 'LWKR_SPTt', 'LWKR_EETt',
                       'MWKR_SPTt', 'MWKR_EETt']

    # 存储所有结果的列表
    results = []

    for index, row in data_frame.iterrows():
        # 提取算法结果和运行时间
        algorithms = [(result_col, row[result_col], row[runtime_col])
                      for result_col, runtime_col in zip(result_columns, runtime_columns)]

        # 根据结果排序，如果结果相同则按运行时间排序
        algorithms_sorted = sorted(algorithms, key=lambda x: (x[1], x[2]))

        # 选择前三个结果
        top_three_algorithms = algorithms_sorted[:3]

        # 提取案例特点
        case_features = row[['Filename', 'num_jobs', 'num_machines', 'total_operations', 'std_dev_job_time',
                             'max_min_diff_avg', 'average_processing_time', 'job_machine_ratio',
                             'avg_machines_per_operation', 'density']].to_dict()

        # 合并案例特点和前三个算法的结果
        for i, (alg_name, alg_result, alg_runtime) in enumerate(top_three_algorithms, start=1):
            if alg_name == 'MIP Result':
                alg_name = 'MIP'
            elif alg_name == 'GA Result':
                alg_name = 'GA'
            case_features[f'Top {i} Algorithm'] = alg_name
            case_features[f'Top {i} Result'] = alg_result
            case_features[f'Top {i} Runtime'] = alg_runtime

        # 添加合并的数据到列表
        results.append(case_features)

    # 从列表创建DataFrame
    top_results = pd.DataFrame(results)
    return top_results


# 主逻辑
file_path = '../run_all/Barnes_results_time10.xlsx'
data_frame = read_excel_data(file_path)


system_prompt = """你是一个可以调用外部工具的助手，可以使用的工具包括：\n {'calculate_indicators': '计算调度案例指标','run_GA':'运行遗传算法',
'run_MIP':'运行混合整数规划','run_Rules':'运行规则式调度','update_process_with_robots':'在工艺流程中加入自动化设备',
'update_process_order':'紧急订单更改现有工艺流程','update_process_fault':'设备故障更改现有工艺流程'} \n
如果使用工具请遵循以下格式回复：\n 
\n Thought:思考你当前步骤需要解决什么问题，是否需要使用工具\n 
Action:工具名称，你的工具必须从 [['calculate_indicators','run_GA','run_MIP','run_Rules','update_process_with_robots','update_process_order','update_process_fault']] 选择\n 
Action Input:工具输入参数\n 
\n 工具返回按照以下格式回复：\n 
\n Observation:调用工具后的结果\n 
(Thought/Action/Action Input/Observation 可能会重复多次或者0次)
\n如果你已经知道了答案，或者你不需要工具，请遵循以下格式回复\n 
\nThought:给出最终答案的思考过程\n 
Final Answer:最终答案\n
\n开始!\n """


print(get_response("glm-4", "这是一个调度文件的路径：Mk01.fjs。你有10秒的时间来读取并找出最优的调度方案。", system_prompt))
root_folder = '../run_all'
for subdir, dirs, files in os.walk(root_folder):
    print(f"{subdir=}，{dirs=},{files=}")
    # process_folder(subdir, time_limit)
for filename in os.listdir(root_folder):
    print(filename)




def generate_ReAct(model_use, save_path, sys_prompt, result_path):
    dir_path = os.path.dirname(save_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    sch_file_name = ['random_instance/5rx5_1.fjs', 'SchedAlgoLib/data/Brandimarte_Data/Text/Mk01.fjs',
                     'workpiece_processing_times.csv', 'data_path.json']
    time_quick = 10
    question_quick = ["请在10秒内根据提供的文件路径{data_path}解析并解决调度问题。",
                      "这是一个调度文件的路径：{data_path}。你有10秒的时间来读取并找出最优的调度方案。",
                      "考虑到时间紧迫，你能在10秒内处理这个调度文件吗？文件路径是{data_path}。",
                      "时间只有10秒，请快速从这个路径{data_path}提取数据并求解调度问题。",
                      "利用提供的文件路径{data_path}，你能否迅速执行调度算法并在10秒内给出答案？",
                      ]
    question_slow = ["请在30秒内根据提供的文件路径{data_path}解决调度问题。",
                     "你有30秒时间来分析和解答调度问题，文件路径为{data_path}。请尽快找出解决方案。",
                     "利用这个文件路径{data_path}，你能在30秒内完成调度问题的求解吗？请迅速行动。"
                     ]
    # 随机选择
    data_frame = read_excel_data(result_path)
    best_results_df = find_top_three_algorithms(data_frame)
    indicator_columns = ['Filename', 'num_jobs', 'num_machines', 'total_operations', 'std_dev_job_time',
                         'max_min_diff_avg', 'average_processing_time', 'job_machine_ratio',
                         'avg_machines_per_operation', 'density']
    for index, row in best_results_df.iterrows():
        React_thought = ""
        # 提取算法结果和运行时间
        Filename, num_jobs, num_machines, total_operations, std_dev_job_time, max_min_diff_avg, average_processing_time, job_machine_ratio, avg_machines_per_operation, density = \
            row[indicator_columns]
        # ind_prompt = indicator_prompt.format(num_jobs, num_machines, total_operations, std_dev_job_time, max_min_diff_avg, average_processing_time, job_machine_ratio, avg_machines_per_operation, density)
        ind_prompt = f"""该调度案例的指标为：工件数量为{num_jobs},
         机器数量为{num_machines}, 
         加工工序总数为{total_operations}, 
         工序加工时间的离散度（标准差）为{std_dev_job_time}, 
         机器最大最小加工时间差为{max_min_diff_avg}, 
         平均加工时间为{average_processing_time}, 
         工件-机器比值为{job_machine_ratio}, 
         工序平均可选机器数为{avg_machines_per_operation}, 
         工件-机器矩阵密度（非零元素比例）为{density} """
        # print(f"{ind_prompt=}")
        # 从列表里随机选一个
        # question = random.choice(question_quick)
        question = random.choice(question_quick)
        print(question.format(data_path=Filename))
        answer = copy.deepcopy(template)
        answer['conversation'][0]['system'] = sys_prompt
        answer['conversation'][0]['input'] = question.format(data_path=Filename)
        React_thought += f"Thought:我现在需要求解一个车间调度问题，路径为{Filename}，时间为10s，但不知道该问题的具体情况，不能直接选择算法。需要解析案例进一步分析，使用工具calculate_indicators获得案例指标\n"
        React_thought += "Action: calculate_indicators\n"
        React_thought += "Action Input: {'data_path': '" + f"{Filename}" + "'}\n"
        observation_items = [
            f"num_jobs: {num_jobs}",
            f"num_machines: {num_machines}",
            f"total_operations: {total_operations}",
            f"std_dev_job_time: {std_dev_job_time}",
            f"max_min_diff_avg: {max_min_diff_avg}",
            f"average_processing_time: {average_processing_time}",
            f"job_machine_ratio: {job_machine_ratio}",
            f"avg_machines_per_operation: {avg_machines_per_operation}",
            f"density: {density}"
        ]
        observation_str = ', '.join(observation_items)
        React_thought += "Observation: {" + observation_str + "}\n"
        # print(React_thought)
        result_3 = []
        for i in range(1, 4):
            # result_3.append(
            #     f"算法{i}" + str(row[f'Top {i} Algorithm']) + f"求解结果：" + str(row[f'Top {i} Result']) + "求解用时：" + str(
            #         row[f'Top {i} Runtime']))
            result_3.append(
                f"算法{i}" + str(row[f'Top {i} Algorithm']) + f"求解结果：" + str(row[f'Top {i} Result']))
        algo_knowledge = load_txt("algo_knowledge.txt")
        ind_knowledge = load_txt("ind_knowledge.txt")
        prompt_input = "现在我需要在10s内求解一个车间调度问题，该调度问题的相关指标如下：" + ind_prompt \
                       + "算法库中的算法有：" + algo_knowledge \
                       + "每个指标的含义如下：" + ind_knowledge + f"请结合指标分析为什么{row[f'Top 1 Algorithm']}算法在当前时间限制下得出了最好的解，解释由于xx指标等，确实该选择该算法。尽可能精简，突出重点,直接给出分析和结论"
        # print(prompt_input)
        system_prompt = ""
        oneturn_response = get_response("glm-4", prompt_input, system_prompt)
        system_prompt = f"""你可以选择工具求解调度问题，时间约束为10s,路径为{Filename}，可以使用的工具包括：""" + """ 
        ('run_GA':'运行遗传算法',
         'run_MIP':'运行混合整数规划','run_Rules':'运行规则式调度')\n
         选择，其中参数分别有：run_GA(TimeLimit,data_path),run_MIP(TimeLimit,data_path),run_Rules(rule,data_path),rule可选规则包括 FIFO_SPT, FIFO_EET, MOPNR_SPT, MOPNR_EET, LWKR_SPT, LWKR_EET, MWKR_SPT, MWKR_EET\n 
        必须遵循以下格式回复，不要加其他分析、解释和字符，只输出Action和Action Input的部分！！：
        
        Action:从 'run_GA','run_MIP','run_Rules'中选择
        Action Input:工具输入参数，如{'data_path': filename}
        
        """
        React_thought += "Thought: " + oneturn_response + "\n"
        final_ = get_response("glm-4", oneturn_response, system_prompt)
        # print(final_)

        React_thought += extract_key_lines(final_) + "\n"
        final_str = [
            f"result: {row[f'Top 1 Result']}",
            f"run_time: {row[f'Top 1 Runtime']}"]
        React_thought += "Observation: {" + ','.join(final_str) + "}\n"
        React_thought += f"Final Answer: 通过解析案例指标，结合问题需求，选择了{row[f'Top 1 Algorithm']}算法，得到了调度问题的结果，结果为{row[f'Top 1 Result']},花费时间为{row[f'Top 1 Runtime']}"
        answer['conversation'][0]['output'] = React_thought
        print(React_thought)
        save_answer(answer, save_path)




