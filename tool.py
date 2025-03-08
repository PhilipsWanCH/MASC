import os, json

import pandas as pd
import requests
from SchedAlgoLib.heuristic_algorithms.genetic_algorithm.FJSPGAMain import run_GA
from SchedAlgoLib.exact_algorithms.FJSPMain import run_MIP
from SchedAlgoLib.rule_based_scheduling.RuleBasedMain import run_Rules
from SchedAlgoLib.utils.data_loader import update_process_with_robots, calculate_indicators

from SchedAlgoLib.utils.read_json import load_machine_time_windows, decode_robot_transfers
from SchedAlgoLib.utils.Gantt import Gantt, Gantt_tp

import os


def find_file(filename, root_dir):
    # 遍历根目录和所有子目录
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 检查文件名是否在当前目录的文件列表中
        if filename in filenames:
            # 生成文件的完整路径
            full_path = os.path.join(dirpath, filename)
            # 返回相对于当前工作目录的路径
            return os.path.relpath(full_path, start=os.getcwd())
    return None  # 如果文件没有找到，返回None


def get_excel_name(path, time):
    file_path_ = path.split('\\')
    print(file_path_)
    if len(file_path_) >= 8:
        excel_path = os.path.join('results', f'{file_path_[4]}_{file_path_[-2]}_{time}.xlsx')
    else:
        excel_path = os.path.join('results', f'{file_path_[4]}_{time}.xlsx')

    return excel_path


def write_to_excel(excel_path, filename, method, result, run_time):
    results = []
    results.append({
        'Filename': filename,
        'Method': method,
        'result': result,
        'run_time': run_time
    })
    df = pd.DataFrame(results)
    # 检查文件是否存在
    # 检查文件是否存在
    if os.path.exists(excel_path):
        # 文件存在，追加数据不包括列头
        try:
            old_df = pd.read_excel(excel_path, sheet_name='Sheet1')
            startrow = len(old_df) + 1
        except Exception as e:
            print(f"Error reading existing file: {e}")
            startrow = 0  # 如果读取出错，默认从第一行开始
        header = False
        mode = 'a'
        # 使用 ExcelWriter 追加数据或创建新文件
        if startrow == 1:
            header = True
            startrow -= 1
        with pd.ExcelWriter(excel_path, mode=mode, engine='openpyxl', if_sheet_exists='overlay') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False, header=header, startrow=startrow)
    else:
        # 文件不存在，添加列头，并创建文件
        startrow = 0
        header = True
        mode = 'w'
        # 使用 ExcelWriter 追加数据或创建新文件
        with pd.ExcelWriter(excel_path, mode=mode, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False, header=header, startrow=startrow)



class Tools:
    def __init__(self,root_path) -> None:
        self.toolConfig = self._tools()
        # self.root_path = '../../SchedAlgoLib/data'
        self.root_path = root_path

    def _tools(self):
        tools = [

            {
                "name_for_human": "计算指标",
                "name_for_model": "calculate_indicators",
                "description_for_model": "此函数用于计算调度案例的各种性能指标。",
                "parameters": [
                    {
                        "name": "data_path",
                        "description": "调度案例文件的位置",
                        "required": True,
                        "schema": {"type": "string"}
                    }
                ]
            },
            {
                "name_for_human": "运行遗传算法",
                "name_for_model": "run_GA",
                "description_for_model": "此函数运行遗传算法来优化调度案例。遗传算法是一种基于自然选择和遗传学原理的搜索启发式算法。",
                "parameters": [
                    {
                        "name": "TimeLimit",
                        "description": "算法运行的时间限制",
                        "required": True,
                        "schema": {"type": "integer"}
                    },
                    {
                        "name": "data_path",
                        "description": "调度案例文件的位置",
                        "required": True,
                        "schema": {"type": "string"}
                    }
                ]
            },
            {
                "name_for_human": "运行混合整数规划",
                "name_for_model": "run_MIP",
                "description_for_model": "此函数运行混合整数规划算法来处理调度问题，大规模问题上耗时很长。",
                "parameters": [
                    {
                        "name": "TimeLimit",
                        "description": "算法运行的时间限制",
                        "required": True,
                        "schema": {"type": "integer"}
                    },
                    {
                        "name": "data_path",
                        "description": "调度案例文件的位置",
                        "required": True,
                        "schema": {"type": "string"}
                    }
                ]
            },
            {
                "name_for_human": "规则式调度",
                "name_for_model": "run_Rules",
                "description_for_model": "此函数根据选择的规则执行规则式调度。它直接应用简单规则来分配任务，适合快速实施，但可能不如优化算法在性能上优异。",
                "parameters": [
                    {
                        "name": "rule",
                        "description": "调度规则，可选规则包括 FIFO_SPT, FIFO_EET, MOPNR_SPT, MOPNR_EET, LWKR_SPT, LWKR_EET, MWKR_SPT, MWKR_EET",
                        "required": True,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "data_path",
                        "description": "调度案例文件的位置",
                        "required": True,
                        "schema": {"type": "string"}
                    }
                ]
            },
            {
                "name_for_human": "加入自动化设备",
                "name_for_model": "update_process_with_robots",
                "description_for_model": "此函数在工艺流程中加入自动化设备，在使用自动化设备时可以先用该函数转换。",
                "parameters": [
                    {
                        "name": "num_robots",
                        "description": "自动化设备的数量",
                        "required": True,
                        "schema": {"type": "integer"}
                    },
                    {
                        "name": "tp_time",
                        "description": "转运的时间",
                        "required": True,
                        "schema": {"type": "integer"}
                    },
                    {
                        "name": "path",
                        "description": "待重新建立工艺流程的文件路径",
                        "required": True,
                        "schema": {"type": "string"}
                    }
                ]
            },
            {
                "name_for_human": "紧急订单重调度",
                "name_for_model": "update_process_order",
                "description_for_model": "此函数在动态调度过程中加入紧急订单，更改现有的工艺流程。",
                "parameters": [
                    {
                        "name": "current_time",
                        "description": "加入订单的时间点",
                        "required": True,
                        "schema": {"type": "integer"}
                    },
                    {
                        "name": "schedule_path",
                        "description": "生成的调度方案的路径",
                        "required": True,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "process_path",
                        "description": "原有的工艺流程路径",
                        "required": True,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "new_process_path",
                        "description": "新加订单的工艺流程路径",
                        "required": True,
                        "schema": {"type": "string"}
                    }
                ]
            }

        ]
        return tools



    def calculate_indicators(self, data_path: str):
        # print(data_path)
        found_path = find_file(data_path, self.root_path)
        print(found_path)
        num_jobs, num_machines, total_operations, std_dev_job_time, max_min_diff_avg, average_processing_time, job_machine_ratio, avg_machines_per_operation, density = calculate_indicators(
            found_path)
        # print(num_jobs, num_machines, total_operations, std_dev_job_time, max_min_diff_avg, average_processing_time, job_machine_ratio, avg_machines_per_operation, density)
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
        return '{' + ', '.join(observation_items) + '}'

    def run_GA(self, TimeLimit, data_path):
        found_path = find_file(data_path, self.root_path)
        print(found_path)
        result, run_time = run_GA(TimeLimit=TimeLimit, data_path=found_path)
        observation_items = [
            f"result: {result}",
            f"run_time: {run_time}",
        ]
        execl_path = get_excel_name(found_path, TimeLimit)
        write_to_excel(execl_path, data_path, 'GA', result, run_time)
        return '{' + ', '.join(observation_items) + '}'

    def run_MIP(self, TimeLimit, data_path):
        found_path = find_file(data_path, self.root_path)
        print(found_path)
        result, run_time = run_MIP(TimeLimit=TimeLimit, data_path=found_path)
        observation_items = [
            f"result: {result}",
            f"run_time: {run_time}",
        ]
        execl_path = get_excel_name(found_path, TimeLimit)
        write_to_excel(execl_path, data_path, 'MIP', result, run_time)
        return '{' + ', '.join(observation_items) + '}'

    def run_Rules(self, rule, data_path):
        found_path = find_file(data_path, self.root_path)
        print(found_path)
        result, run_time = run_Rules(rule=rule, data_path=found_path)
        observation_items = [
            f"result: {result}",
            f"run_time: {run_time}",
        ]
        # =================得修改=======================
        execl_path = get_excel_name(found_path, 10)
        write_to_excel(execl_path, data_path, rule, result, run_time)
        return '{' + ', '.join(observation_items) + '}'
