
import os
import json
import streamlit as st
import chromadb

from dotenv import load_dotenv
from google import genai
from langchain_groq import ChatGroq


# ==========================================
# 1. STREAMLIT PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Research Paper Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI Research Paper Assistant")


# ==========================================
# 2. LOAD API KEYS
# ==========================================

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

if not gemini_key or not groq_key:
    st.error("API keys are missing from .env file.")
    st.stop()


# ==========================================
# 3. CONNECT TO GEMINI
# ==========================================

embedding_client = genai.Client(
    api_key=gemini_key
)


# ==========================================
# 4. CONNECT TO GROQ
# ==========================================

llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0,
    groq_api_key=groq_key
)


# ==========================================
# 5. CONNECT TO CHROMADB
# ==========================================

chroma_client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = chroma_client.get_collection(
    name="research_paper"
)


# ==========================================
# 6. CHAT HISTORY JSON FUNCTIONS
# ==========================================

HISTORY_FILE = "chat_history.json"


def load_chat_history():

    if os.path.exists(HISTORY_FILE):

        try:
            with open(
                HISTORY_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                return {
                    "chat_history": data.get("chat_history", {}),
                    "current_chat_id": data.get(
                        "current_chat_id", "Chat 1"
                    ),
                    "chat_counter": data.get("chat_counter", 1)
                }

        except (json.JSONDecodeError, OSError):
            st.warning(
                "Could not read chat history. Starting a new history."
            )

    return {
        "chat_history": {},
        "current_chat_id": "Chat 1",
        "chat_counter": 1
    }


def save_chat_history():

    data = {
        "chat_history": st.session_state.chat_history,
        "current_chat_id": st.session_state.current_chat_id,
        "chat_counter": st.session_state.chat_counter
    }

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


# ==========================================
# 7. INITIALIZE CHAT MEMORY
# ==========================================

if "chat_history" not in st.session_state:

    saved_data = load_chat_history()

    st.session_state.chat_history = saved_data["chat_history"]

    st.session_state.current_chat_id = saved_data["current_chat_id"]

    st.session_state.chat_counter = saved_data["chat_counter"]


if "messages" not in st.session_state:

    st.session_state.messages = st.session_state.chat_history.get(
        st.session_state.current_chat_id,
        []
    ).copy()


# ==========================================
# 8. SAVE CURRENT CHAT FUNCTION
# ==========================================

def save_current_chat():

    if st.session_state.messages:

        st.session_state.chat_history[
            st.session_state.current_chat_id
        ] = st.session_state.messages.copy()

    save_chat_history()


# ==========================================
# 9. SIDEBAR - CHAT HISTORY
# ==========================================

st.sidebar.title("📚 Chat History")


# New Chat Button
if st.sidebar.button(
    "➕ New Chat",
    use_container_width=True
):

    save_current_chat()

    st.session_state.chat_counter += 1

    st.session_state.current_chat_id = (
        f"Chat {st.session_state.chat_counter}"
    )

    st.session_state.messages = []

    save_chat_history()

    st.rerun()


st.sidebar.divider()

st.sidebar.subheader("Previous Chats")


# Display Previous Chats
for chat_id, messages in list(
    st.session_state.chat_history.items()
):

    first_question = next(
        (
            message["content"]
            for message in messages
            if message["role"] == "user"
        ),
        chat_id
    )

    chat_title = first_question[:30]

    if len(first_question) > 30:
        chat_title += "..."

    if st.sidebar.button(
        chat_title,
        key=f"history_{chat_id}",
        use_container_width=True
    ):

        save_current_chat()

        st.session_state.current_chat_id = chat_id

        st.session_state.messages = (
            st.session_state.chat_history[chat_id].copy()
        )

        save_chat_history()

        st.rerun()


st.sidebar.divider()


# Clear All History
if st.sidebar.button(
    "🗑️ Clear All History",
    use_container_width=True
):

    st.session_state.chat_history = {}

    st.session_state.messages = []

    st.session_state.chat_counter = 1

    st.session_state.current_chat_id = "Chat 1"

    save_chat_history()

    st.rerun()


# Clear Current Chat
if st.sidebar.button(
    "🧹 Clear Chat",
    use_container_width=True
):

    st.session_state.messages = []

    st.session_state.chat_history.pop(
        st.session_state.current_chat_id,
        None
    )

    save_chat_history()

    st.rerun()


# ==========================================
# 10. DISPLAY CURRENT CONVERSATION
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])

        if message.get("sources"):

            st.caption(
                "Sources: " + ", ".join(message["sources"])
            )

        # Display saved source text
        if message.get("source_details"):

            st.subheader("Sources")

            for i, source in enumerate(
                message["source_details"]
            ):

                with st.expander(
                    f"View Source {i + 1} - Page {source['page']}"
                ):

                    st.write(source["text"])


# ==========================================
# 11. TAKE USER QUESTION
# ==========================================

question = st.chat_input(
    "Ask a question about the research paper..."
)


if question:

    # Display user question
    with st.chat_message("user"):
        st.write(question)

    # Save user question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    try:

        with st.spinner("Finding your answer..."):

            # ==================================
            # 12. GET PREVIOUS CONVERSATION
            # ==================================

            previous_messages = (
                st.session_state.messages[:-1]
            )

            conversation_text = ""

            for message in previous_messages:

                conversation_text += (
                    message["role"]
                    + ": "
                    + message["content"]
                    + "\n"
                )


            # ==================================
            # 13. QUERY REWRITING
            # ==================================

            if conversation_text:

                rewrite_prompt = f"""
                Convert the latest question into a standalone
                search question using the conversation history.

                Keep the original meaning.
                Return only the rewritten question.

                Conversation:
                {conversation_text}

                Latest question:
                {question}
                """

                search_question = llm.invoke(
                    rewrite_prompt
                ).content.strip()

            else:

                search_question = question


            # ==================================
            # 14. GENERATE QUESTION EMBEDDING
            # ==================================

            response = embedding_client.models.embed_content(
                model="gemini-embedding-2",
                contents=search_question
            )

            question_embedding = (
                response.embeddings[0].values
            )


            # ==================================
            # 15. RETRIEVE RELEVANT CHUNKS
            # ==================================

            results = collection.query(
                query_embeddings=[question_embedding],
                n_results=3
            )

            chunks = results["documents"][0] or []

            metadatas = results["metadatas"][0] or []


            # ==================================
            # 16. CHECK RETRIEVED CHUNKS
            # ==================================

            sources = []
            source_details = []

            if not chunks:

                answer_text = (
                    "I could not find relevant information "
                    "in the research paper."
                )

            else:

                # Combine retrieved chunks
                context = "\n\n".join(chunks)


                # ==================================
                # 17. CREATE FINAL PROMPT
                # ==================================

                prompt = f"""
                You are an AI Research Paper Assistant.

                Use the conversation history and the given
                context to understand the user's question.

                Answer using only the provided paper context.

                If the answer is not available in the context,
                clearly say so.

                Explain in simple English.

                Conversation History:
                {conversation_text}

                Context:
                {context}

                Current Question:
                {question}

                Answer:
                """


                # ==================================
                # 18. GENERATE ANSWER USING GROQ
                # ==================================

                answer = llm.invoke(prompt)

                answer_text = answer.content


                # ==================================
                # 19. GET SOURCE PAGE NUMBERS
                # ==================================

                for metadata in metadatas:

                    if isinstance(metadata, dict):

                        page_number = metadata.get("page_label")

                        if not page_number:

                            page_number = str(
                                int(metadata.get("page", 0)) + 1
                            )

                        source = f"Page {page_number}"

                        if source not in sources:
                            sources.append(source)


                # Save source text and page numbers
                for chunk, metadata in zip(chunks, metadatas):

                    if isinstance(metadata, dict):

                        page_number = metadata.get("page_label")

                        if not page_number:

                            page_number = str(
                                int(metadata.get("page", 0)) + 1
                            )

                        source_details.append({
                            "page": str(page_number),
                            "text": chunk
                        })


        # ==================================
        # 20. DISPLAY ASSISTANT ANSWER
        # ==================================

        with st.chat_message("assistant"):

            st.write(answer_text)

            if source_details:

                st.subheader("Sources")

                for i, source in enumerate(source_details):

                    with st.expander(
                        f"View Source {i + 1} - Page {source['page']}"
                    ):

                        st.write(source["text"])


        # ==================================
        # 21. SAVE ASSISTANT ANSWER
        # ==================================

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer_text,
            "sources": sources,
            "source_details": source_details
        })

        save_current_chat()

        st.rerun()


    except Exception as e :
        error_message = str(e).lower()

        if "429" in error_message or "quota" in error_message:
            st.error(
                "api quota exceeded . please try again later."
            )
        elif "401"in error_message or "403"in error_message:
            st.error(
                "api authentication failed please check your api keys "
            )
        elif "connection" in error_message or "timeout" in error_message:
            st.error(
                "connection problem.please check your internet connection"
            )
        elif "404"in error_message:
            st.error(
                "requested model or resource was not found please check the model configuration "
            )
        else:
            st.error(
                "something went wrong while processing your question"
            )
        with st.expander("technical error details"):
            st.code(str(e))


    