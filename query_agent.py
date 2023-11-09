import os
import autogen
from query_agent_tool import VectaraQueryTool
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json


# config_list = autogen.config_list_from_json(
#     "OAI_CONFIG_LIST",
#     filter_dict={
#         # "model": ["gpt-4", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"],
#         # "model": [ "gpt-3.5-turbo-16k"],
#         "model": "gpt-3.5-turbo",
#         "max_retries": 1,
#     },
# )

config_list = autogen.config_list_from_json(
    env_or_file="OAI_CONFIG_LIST",  # or OAI_CONFIG_LIST.json if file extension is added
    filter_dict={
        "model": {
            # "gpt-4",
            # "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k"
        }
    }
)

# config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

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
#    message="You are tasked with using vectara querying to get enough information about the body of data by asking 2 questions",
   message="""vectara provides a way to query a corpus of data.
   It will return several answers to your query.
   You must use vectara to query the corpus and try to determine what the corpus is about
     and you must return the results that seems to make the most sense. """,
   llm_config=llm_config,
#    llm_config={"api_key": os.environ['OPENAI_API_KEY']}
)

def user_generated_query(user_query):
    # query = input("Enter a query: ")
    # return query
    user_proxy.initiate_chat(
   chatbot,
#    message="You are tasked with using vectara querying to get enough information about the body of data by asking 2 questions",
#    message="""vectara provides a way to query a corpus of data.
#    It will return several answers to your query.
#    You must use vectara to query the corpus and try to determine what the corpus is about
#      and you must return the results that seems to make the most sense. """,
    message= f"""a user will query vectara with the following query: {user_query}
you must use this query to use vectara and please provide feeback to the user as to how they can produce a better response. 
If the query is high quality then compliment them on it""" + user_query, 
   llm_config=llm_config,
#    llm_config={"api_key": os.environ['OPENAI_API_KEY']}
)