import streamlit as st
import uuid
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory

system_prompt = """
You are a Data Science Tutor.
If a user ask any question other than datascience than ask him to ask questions only related to data science
"""
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.7, google_api_key="AIzaSyD93jv-nUCK30PGZNJgShG0xI0kYocz_AU")

def get_session_history(session_id: str):
    return ChatMessageHistory()

if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

conversation = RunnableWithMessageHistory(llm, get_session_history=get_session_history)

st.title("Data Science Tutor")
st.markdown("Ask **data science-related** questions! (ML, AI, Stats, Python, etc.)")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if st.button("Remove Chat"):
    st.session_state["messages"] = []
    st.rerun()

for chat in st.session_state["messages"]:
    role = "**You:**" if chat["is_user"] else "**Tutor:**"
    st.markdown(f"{role} {chat['content']}")

user_input = st.text_input("Your question:")

if user_input:
    response = conversation.invoke(
        {"input": f"{system_prompt}\nUser: {user_input}"},
        config={"configurable": {"session_id": st.session_state["session_id"]}}
    )

    ai_response = response.content  # Fix: Access content directly instead of using response["output"]

    st.session_state["messages"].append({"content": user_input, "is_user": True})
    st.session_state["messages"].append({"content": ai_response, "is_user": False})

    st.markdown(f"**You:** {user_input}")
    st.markdown(f"**Tutor:** {ai_response}")

with st.expander("Full Chat History"):
    for chat in st.session_state["messages"]:
        role = "**You:**" if chat["is_user"] else "**Tutor:**"
        st.write(f"{role} {chat['content']}")
