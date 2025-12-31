from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from config import LLM_MODEL, BASE_URL, DUMMY_API_KEY

def get_answer(context, question):
    llm = init_chat_model(
        model=LLM_MODEL,
        model_provider="openai",
        base_url=BASE_URL,
        api_key=DUMMY_API_KEY
    )

    agent = create_agent(
        tools=[],
        model=llm,
        system_prompt=f"""
You are a Sunbeam website assistant.

Rules:
- Answer ONLY from context
- Point-wise answers
- No hallucination
- If any batches related question give answer in table format
- If any heading or title bold or highlight it
- Add bullets when possible
- If any question releated to internship course give available internship courses technology

CONTEXT:
{context}

QUESTION:
{question}
"""
    )

    result = agent.invoke({
        "messages": [{"role": "user", "content": question}]
    })

    return result["messages"][-1].content
