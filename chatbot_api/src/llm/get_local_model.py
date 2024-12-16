from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
import os
from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline

# from transformers import BitsAndBytesConfig


if load_dotenv(".env"):
    print("✅✅Environment file in llm loaded successfully")
else:
    print("❌❌Environment file in llm failed to load")
import getpass
from huggingface_hub import InferenceClient
os.environ["HUGGINGFACEHUB_API_TOKEN"] = getpass.getpass(
    "Enter your Hugging Face API key: "
)

from langchain_huggingface import HuggingFacePipeline

llm = HuggingFacePipeline.from_model_id(
    model_id="vinai/PhoGPT-4B-Chat",
    task="text-generation",
    use_auth_token=os.getenv("HUGGINGFACE_HUB_TOKEN"),
    pipeline_kwargs=dict(
        max_new_tokens=512,
        do_sample=False,
        repetition_penalty=1.03,
    ),
)
chat_model = ChatHuggingFace(llm=llm)



from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)

messages = [
    SystemMessage(content="You're a helpful assistant"),
    HumanMessage(
        content="What happens when an unstoppable force meets an immovable object?"
    ),
]

# ai_msg = chat_model.invoke(messages)
# print(ai_msg.content)