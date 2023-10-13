import autogen

# load config list from json file
config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")

# config for autogen's enhanced inference API which is compatible with OpenAI API
llm_config={
    "request_timeout": 600,
    "seed": 50,                     # for caching and reproducibility
    "config_list": config_list,     # which models to use
    "temperature": 0,               # for sampling
}

# create an AssistantAgent instance named "assistant"
agent_assistant = autogen.AssistantAgent(
    name="agent_assistant",
    llm_config=llm_config,
)

# create a UserProxyAgent that acts on the humans behalf 
agent_proxy = autogen.UserProxyAgent(
    name="agent_proxy",
    human_input_mode="NEVER",           # NEVER, TERMINATE, or ALWAYS 
                                            # TERMINATE - human input needed when assistant sends TERMINATE 
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "agent_output",     # path for file output of program
        "use_docker": False,            # True or image name like "python:3" to use docker image
    },
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
                      Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)


agent_proxy.initiate_chat(
    agent_assistant,
    message="""I'd like for you to create a python script that meets the following requirements:
    - uses the selenium python package
    - uses the presence_of_element_located method from selenium
    - does not use the method find_element_by_css_selector
    - searches iphone 14 at ebay
    - finds all the prices by looking for the class "s-item__price"
    - prints to the screen all the prices it finds 
    - check the length of the text of the price before printing or sending to slack, just skip if the length is less than 1
    - sends all the prices to a slack channel 
    - the slack url to use is '<YOUR_SLACK_WEBHOOK_HERE>' 
    """,
)



