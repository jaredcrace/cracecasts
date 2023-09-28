import dotenv
from langchain.text_splitter import Language
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains.question_answering import load_qa_chain
from langchain import PromptTemplate, LLMChain

dotenv.load_dotenv()

repo_path = "./langchain-master/"

# Generic Loader
loader = GenericLoader.from_filesystem(
    repo_path+"/libs/langchain/langchain",
    glob="**/*",
    suffixes=[".py"],
    parser=LanguageParser(language=Language.PYTHON, parser_threshold=500)
)
documents = loader.load()
print("documents len: %s" % len(documents))

# Splitting
from langchain.text_splitter import RecursiveCharacterTextSplitter
python_splitter = RecursiveCharacterTextSplitter.from_language(language=Language.PYTHON, 
                                                               chunk_size=2000, 
                                                               chunk_overlap=200)
texts = python_splitter.split_documents(documents)
print("texts len: %s" % len(texts))

# Store the documents
db = Chroma.from_documents(texts, OpenAIEmbeddings(disallowed_special=()))
retriever = db.as_retriever(
    search_type="mmr",          # max marginal relevance 
    search_kwargs={"k": 8},     # chunks to receive
)

# Callback
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
llm = LlamaCpp(
    model_path="./codellama-13b-instruct.Q4_K_M.gguf",
    n_ctx=5000,                         # maximum context size
#    n_gpu_layers=0,                     # number of gpu layers
    n_batch=512,                        # max number of prompt tokens to batch when calling llama_eval
    f16_kv=True,                        # use half-precision for key/value cache (must be true) 
    callback_manager=callback_manager,  # enables streaming the output
    verbose=True,
)

# Prompt, INST and SYS are special tokens
template = """
[INST]

<<SYS>>
You are an expert in software engineering. You will use the provided context to answer the user's
questions. Read the given context before answering the question and think step by step. If you are
unable to answer the question based on the provided context, please inform the user of what context
is missing. Do not use any other information for answering the user. 
<</SYS>>

Context: {context}
User: {question}

[/INST]
"""

QA_CHAIN_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=template,
)

# Docs
question = "How can I initialize a ReAct agent?"
docs = retriever.get_relevant_documents(question)
print(docs)

# Chain
chain = load_qa_chain(llm, chain_type="stuff", prompt=QA_CHAIN_PROMPT)

chain({"input_documents": docs, "question": question}, return_only_outputs=True)

