import os
import autogen
from query_agent_tool import VectaraQueryTool
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

# Define the config_list

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
    }
)

chatbot = autogen.AssistantAgent(
    name="chatbot",
    system_message="For coding tasks, only use the functions you have been provided with. Reply TERMINATE when the task is done.",
    llm_config=llm_config,

)


def user_generated_query(user_query):

    user_proxy.initiate_chat(
    chatbot,
    message= f"""a user will query vectara with the following query: {user_query}
you must use this query to use vectara and please provide feeback to the user as to how they can produce a better response. 
If the query is high quality then compliment them on it. Also give the user a sample query that could protentally provide them with a good output""" + user_query, 
   llm_config=llm_config,

)

if __name__ == "__main__":
#    user_generated_query("What is the overall sentiment in the data?")
    user_generated_query("What does the document contain pertaining to pets?")