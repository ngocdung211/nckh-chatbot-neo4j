from langchain_ollama import ChatOllama


# llama3-chatqa
def get_ollama_llama3_model():
    llm = ChatOllama(
    model="llama3.1",
    temperature=0,
    # other params...
    )
    print("OLLLLAAAAMMMAAAAAA")
    return llm
# from langchain_core.messages import AIMessage

# messages = [
#     (
#         "system",
#         "You are a helpful assistant that translates English to French. Translate the user sentence.",
#     ),
#     ("human", "I love programming."),
# ]
# ai_msg = llm.invoke(messages)
# print(ai_msg.content)

