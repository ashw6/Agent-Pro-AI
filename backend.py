from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3:8b")

def decide_tool(query):
    q = query.lower()
    if "pdf" in q or "document" in q:
        return "pdf"
    return "chat"

def create_plan(query):
    plan_prompt = f"""
Break this task into steps:

Task: {query}
Steps:
"""
    return llm.invoke(plan_prompt).content

def stream_answer(query, db, chat_history):
    tool = decide_tool(query)
    plan = create_plan(query)

    if tool == "pdf" and db:
        docs = db.similarity_search(query, k=3)
        context = "\n".join([d.page_content for d in docs])

        prompt = f"""
You are an AI agent.

Plan:
{plan}

Context:
{context}

Chat History:
{chat_history}

Answer:
{query}
"""
    else:
        prompt = f"""
You are an AI agent.

Plan:
{plan}

Chat History:
{chat_history}

User: {query}
Assistant:
"""

    for chunk in llm.stream(prompt):
        yield chunk.content