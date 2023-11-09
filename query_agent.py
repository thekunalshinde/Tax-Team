import os
import autogen
from query_agent_tool import VectaraQueryTool


config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"],
        # "model": [ "gpt-3.5-turbo-16k"],
        # "model": "gpt-3.5-turbo",
    },
)

# config_list = autogen.config_list_from_json(
#     "OAI_CONFIG_LIST",
#     filter_dict={
#         # "model": ["gpt-4", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"],
#         "model": [ "gpt-3.5-turbo-16k"],
#         # "model": "gpt-3.5-turbo",
#     },

# )


# Define a function to generate llm_config from a LangChain tool
def generate_llm_config(tool):
    # Define the function schema based on the tool's args_schema
    function_schema = {
        "name": tool.name.lower().replace (' ', '_'),
        "description": tool.description,
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    }

    if tool.args is not None:
      function_schema["parameters"]["properties"] = tool.args

    return function_schema


custom_tool = VectaraQueryTool()

# Construct the llm_config
llm_config = {
  #Generate functions config for the Tool
  "functions":[
      generate_llm_config(custom_tool),
    #   generate_llm_config(read_file_tool),
  ],
  "config_list": config_list,  # Assuming you have this defined elsewhere
  "timeout": 120,
}

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "coding"},
)


# Register the tool and start the conversation
user_proxy.register_function(
    function_map={
        custom_tool.name: custom_tool._run,
        # read_file_tool.name: read_file_tool._run,
    }
)

chatbot = autogen.AssistantAgent(
    name="chatbot",
    system_message="For coding tasks, only use the functions you have been provided with. Reply TERMINATE when the task is done.",
    llm_config=llm_config,
    # llm_config={"api_key": os.environ['OPENAI_API_KEY']},
)

# user_proxy.initiate_chat(
#     chatbot,
#     message=f"Read the file with the path {get_file_path_of_example()}, then calculate the circumference of a circle that has a radius of that files contents.", #7.81mm in the file
#     llm_config=llm_config,
# )
assistant = autogen.AssistantAgent(name="assistant", llm_config={"api_key": ...})
user_proxy.initiate_chat(
   chatbot,
   message="You are tasked with using vectara querying to get enough information about the body of data by asking 4 questions",
   lm_config=llm_config,
#    llm_config={"api_key": os.environ['OPENAI_API_KEY']}
)