import autogen

config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")

llm_config={
    "request_timeout": 600,
    "seed": 44,                     # for caching and reproducibility
    "config_list": config_list,     # which models to use
    "temperature": 0,               # for sampling
}

agent_assistant = autogen.AssistantAgent(
    name="agent_assistant",
    llm_config=llm_config,
)

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
    message="""I need you to write a python script that will do the following:
    1. go to airbnb
    2. search for an Austin Texas stay from Oct 10, 2023 - Oct 11, 2023
    3. gather the results, no more than 10. The class html div to search for is "c4mnd7m dir dir-ltr".
    4. print that result to the screen
    """,
)

