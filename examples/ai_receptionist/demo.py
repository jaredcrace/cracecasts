import autogen
from icecream import ic

DATA_FILE = "resume_data.txt"

def start_ai():
    autogen.ChatCompletion.start_logging()

    # read in data
    with open(DATA_FILE, 'r') as file:
        resume_data = file.read()

    # load config list from json file
    config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")

    # config for autogen's enhanced inference API which is compatible with OpenAI API
    llm_config={
        "request_timeout": 600,
        "seed": 34,                     # for caching and reproducibility
        "config_list": config_list,     # which models to use
        "temperature": 0,               # for sampling
    }

    # create an AssistantAgent instance named "assistant"
    agent_assistant = autogen.AssistantAgent(
        name="agent_assistant",
        llm_config=llm_config,
        system_message=f"""
        You are a receptionist for an an expert whose resume is as follows:

            Resume:
            {resume_data}

            Your responsibilities are in the following order:

            1. You are responsible for vetting potential clients and weeding out those clients that would not be a good fit for this expert.  
            You must ask questions to the potential client to determine if they are a good candidate. 

            2. Once you have determined the client is a good fit, your job is to receive their intake information.
                You are to gather the following information from them:
                    - reason for meeting with the expert
                    - name
                    - phone number
                    - address
            If you have any problems, please respond with the problem and how you can be helped to resolve the problem.    
            Whenever you are asked, please send the message TERMINATE
            """
    )

     # create a UserProxyAgent that acts on the humans behalf 
    agent_proxy = autogen.UserProxyAgent(
        name="agent_proxy",
        human_input_mode="ALWAYS",           # NEVER, TERMINATE, or ALWAYS 
                                             # TERMINATE - human input needed when assistant sends TERMINATE 
        max_consecutive_auto_reply=10,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config={
            "work_dir": "agent_output",     # path for file output of program
            "use_docker": False,            # True or image name like "python:3" to use docker image
        },
        llm_config=llm_config,
    )

    agent_proxy.initiate_chat(
        agent_assistant,
        message="""
            I am a new client and that needs to meet with an expert. Please ask me as many questions as you need to determine
            if I'm a good potential client. 
            
            If I am not a good fit for this expert, please tell me and end the chat. 
            If I am a good fit, please gather any needed information. 

            After the information is gathered, please provide a summary of the data in the following format:
            ---SUMMARY_START---
            name: <name>
            phone: <phone>
            address: <address>
            reason: <reason>
            ---SUMMARY_END---
        """,
    )

    logs = autogen.ChatCompletion.logged_history

     # write all data to a file
    with open("log_data.txt", "w") as file:
        line_split = str(logs).split("\\\\n")
        for i in line_split:
            file.write(i + "\n")

    autogen.ChatCompletion.stop_logging()

start_ai()

