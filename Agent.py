from typing import Dict, List, Optional, Tuple, Union
import json5

from LLM import InternLM2Chat, Llama3Chat, QwenChat
from tool import Tools

TOOL_DESC = """{name_for_model}: Call this tool to interact with the {name_for_human} API. What is the {name_for_human} API useful for? {description_for_model} Parameters: {parameters} Format the arguments as a JSON object."""
REACT_PROMPT = """Answer the following questions as best you can. You have access to the following tools:

{tool_descs}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can be repeated zero or more times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!
"""


class Agent:
    def __init__(self, path: str = '', root_path: str = '', model: str = '') -> None:
        self.path = path
        self.tool = Tools(root_path)
        self.system_prompt = self.build_system_input()
        if model == 'internlm':
            self.model = InternLM2Chat(path)
        elif model == 'llama':
            self.model = Llama3Chat(path)
        elif model == 'qwen':
            self.model = QwenChat(path)

    def update_tool(self, root_path: str):
        self.tool = Tools(root_path)
        self.system_prompt = self.build_system_input()

    def build_system_input(self):
        tool_descs, tool_names = [], []
        for tool in self.tool.toolConfig:
            tool_descs.append(TOOL_DESC.format(**tool))
            tool_names.append(tool['name_for_model'])
        tool_descs = '\n\n'.join(tool_descs)
        tool_names = ','.join(tool_names)
        sys_prompt = REACT_PROMPT.format(tool_descs=tool_descs, tool_names=tool_names)
        return sys_prompt

    def parse_latest_plugin_call(self, text):
        plugin_name, plugin_args = '', ''
        i = text.rfind('\nAction:')
        j = text.rfind('\nAction Input:')
        k = text.rfind('\nObservation:')
        if 0 <= i < j:  # If the text has `Action` and `Action input`,
            if k < j:  # but does not contain `Observation`,
                text = text.rstrip() + '\nObservation:'  # Add it back.
            k = text.rfind('\nObservation:')
            plugin_name = text[i + len('\nAction:'): j].strip()
            plugin_args = text[j + len('\nAction Input:'): k].strip()
            text = text[:k]
        return plugin_name, plugin_args, text

    def call_plugin(self, plugin_name, plugin_args):
        try:
            plugin_args = json5.loads(plugin_args)
            # if plugin_name == 'google_search':
            #     return '\nObservation:' + self.tool.google_search(**plugin_args)
            if plugin_name == 'calculate_indicators':

                return '\nObservation:' + self.tool.calculate_indicators(**plugin_args)
            elif plugin_name == 'run_GA':

                return '\nObservation:' + self.tool.run_GA(**plugin_args)
            elif plugin_name == 'run_MIP':

                return '\nObservation:' + self.tool.run_MIP(**plugin_args)
            elif plugin_name == 'run_Rules':

                return '\nObservation:' + self.tool.run_Rules(**plugin_args)
        except TypeError as e:
            return f'\nError: Type error - {e}'
        except ValueError as e:
            return f'\nError: Value error - {e}'
        except Exception as e:
            return f'\nError: An unexpected error occurred - {e}'

    def text_completion(self, text, history=[]):
        text = "\nQuestion:" + text
        response, his = self.model.chat(text, history, self.system_prompt)
        print("===============第一response=====================")
        print(f"{response=}{his=}")
        plugin_name, plugin_args, response = self.parse_latest_plugin_call(response)
        # print(f"{plugin_name=}{plugin_args=}{response=}")
        # 限定重复次数，防止死循环
        count = 0
        while plugin_name:
            count += 1
            if count > 3:
                break
            # response += self.call_plugin(plugin_name, plugin_args) # 使用internlm时用这个
            response = self.call_plugin(plugin_name, plugin_args)  # 使用llama时用这个，因为history是全的
            response, his = self.model.chat(response, his, self.system_prompt)
            print("===============response=====================")
            print(f"{response=}{his=}")
            plugin_name, plugin_args, response = self.parse_latest_plugin_call(response)

        # response, his = self.model.chat(response, history, self.system_prompt)

        return response, his


def parse_latest_plugin_call(text):
    plugin_name, plugin_args = '', ''
    i = text.rfind('\nAction:')
    j = text.rfind('\nAction Input:')
    k = text.rfind('\nObservation:')
    if 0 <= i < j:  # If the text has `Action` and `Action input`,
        if k < j:  # but does not contain `Observation`,
            text = text.rstrip() + '\nObservation:'  # Add it back.
        k = text.rfind('\nObservation:')
        plugin_name = text[i + len('\nAction:'): j].strip()
        plugin_args = text[j + len('\nAction Input:'): k].strip()
        text = text[:k]
    return plugin_name, plugin_args, text


if __name__ == '__main__':
    # agent = Agent('/root/share/model_repos/internlm2-chat-7b')
    # prompt = agent.build_system_input()

    plugin_name, plugin_args, text = parse_latest_plugin_call("""```
Thought: I need to solve a scheduling problem quickly. The rules-based scheduler is a good choice for fast results.

Action: run_Rules

Action Input: {'data_path': 'data_path.csv'}
```

After the tool call:

```
Observation: The scheduling results are ...
```""")
    print(f"{plugin_name=}, {plugin_args=}, {text=}")
