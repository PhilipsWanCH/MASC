import os, json
import requests

"""
工具函数

- 首先要在 tools 中添加工具的描述信息
- 然后在 tools 中添加工具的具体实现

"""



class Tools:
    def __init__(self) -> None:
        self.toolConfig = self._tools()
    
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
            },
            {
                "name_for_human": "设备故障重调度",
                "name_for_model": "update_process_fault",
                "description_for_model": "此函数在动态调度过程判断故障设备，更改现有的工艺流程。",
                "parameters": [
                    {
                        "name": "current_time",
                        "description": "设备故障的时间点",
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
                        "name": "fault_machine",
                        "description": "故障机器号",
                        "required": True,
                        "schema": {"type": "integer"}
                    }
                ]
            }

        ]
        return tools

