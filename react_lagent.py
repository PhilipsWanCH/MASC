# Import necessary modules and classes from the 'lagent' library.
from lagent.actions import ActionExecutor, GoogleSearch, PythonInterpreter
from lagent.agents import ReAct
from lagent.llms import HFTransformer,HFTransformerCasualLM
from lagent.llms.meta_template import INTERNLM2_META as META

# Initialize the HFTransformer-based Language Model (llm) and
# provide the model name.
# llm = HFTransformer(path='../model/Shanghai_AI_Laboratory/internlm2-chat-7b', meta_template=META)
llm = HFTransformerCasualLM(path='../model/Shanghai_AI_Laboratory/internlm2-chat-7b', meta_template=META)

# Initialize the Google Search tool and provide your API key.
search_tool = GoogleSearch(api_key='Your SERPER_API_KEY')

# Initialize the Python Interpreter tool.
python_interpreter = PythonInterpreter()

# Create a chatbot by configuring the ReAct agent.
# Specify the actions the chatbot can perform.
chatbot = ReAct(
    llm=llm,  # Provide the Language Model instance.
    action_executor=ActionExecutor(actions=[python_interpreter]),
)
# Ask the chatbot a mathematical question in LaTeX format.
def input_prompt():
    print('\ndouble enter to end input >>> ', end='')
    sentinel = ''  # ends when this string is seen
    return '\n'.join(iter(input, sentinel))


while True:
    try:
        prompt = input_prompt()
    except UnicodeDecodeError:
        print('UnicodeDecodeError')
        continue
    if prompt == 'exit':
        exit(0)

    agent_return = chatbot.chat(prompt)
    print(agent_return.response)
    print(agent_return.inner_steps)