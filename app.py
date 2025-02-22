import re
import streamlit as st
import json
from langchain_core.prompts import PromptTemplate

# from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import ConversationChain
from langchain_community.llms import Ollama
from api import get_chunks
from RAG import retrieve_relevant_chunks  # Import RAG functionality

# Define prompt templates
coach_template = """[INST] You are a tactical soccer coach assistant for FRMF Morocco. Your task is to analyze match data in JSON format for the current 1-minute interval (e.g., 0-1, 1-2 minutes). The data includes fields like "timestamp," "type" (e.g., "Pass," "Shot"), "possession_team," "player," "position," "location," and event details. Based solely on this data, generate actionable insights and predict the next most effective move to help FRMF Morocco win.

Provide your analysis in this format:
- **Latest Minute Trends**: Summarize key patterns from this 1-minute interval (e.g., possession shifts, defensive pressure).
- **Strengths & Weaknesses**: Highlight FRMF Morocco's performance in this minute.
- **Opponent Analysis**: Identify opponent tendencies or weaknesses in this minute.
- **Offensive Mark**: A percentage (0-100%) indicating attacking effectiveness this minute.
- **Defensive Mark**: A percentage (0-100%) indicating defensive strength this minute.
- **Player Instructions**: Tactical advice for 2-3 specific players, using data (e.g., "Achraf Hakimi: Increase overlaps—3/4 passes successful").
- **Recommended Action**: Suggest one precise move (e.g., "Exploit their left flank").
- **Justification**: Provide a data-driven reason (e.g., "Their left back lost 2/3 duels").
- **Tactical Adjustment**: Recommend a formation or style tweak if necessary (e.g., "Switch to 4-3-3").
- **Substitution Suggestions**: Propose substitutions based on this minute’s data (e.g., "Replace X—1/5 passes completed").

Focus on actionable coaching decisions for FRMF Morocco, not commentary. Use only the provided data, do not invent details, and do not assist the opponent. Do not mention event IDs.
Make sure to analyze the whole prompt.
Don't mention event id's.
Provide insights on how to improve the strategy of FRMF Morocco.
Data: {query} [/INST]
"""

amateur_template = """You are a soccer coach assistant for FRMF Morocco, helping new fans enjoy and understand the game. Your task is to analyze cumulative match data in JSON format, covering all events from the start up to the current 5-minute interval (e.g., 0-5, 0-10 minutes). The data includes "timestamp" (when stuff happens), "type" (e.g., passes, shots), "possession_team" (who has the ball), "player" (player name), "position" (their role), and details (e.g., where it happened). Based only on this, give fun, simple advice and predict the next best move to help FRMF Morocco win.

Use this easy format:
- **Team Trends of the Latest 5 Minutes**: What’s happening now (e.g., “We’re keeping the ball!” or “They’re coming at us!”).
- **In-Depth Analysis**: What’s working or not (e.g., “We’re good at passing but lose it up front”).
- **Offensive Mark**: How well we’re attacking (e.g., “Great at pushing forward!” or “We need more kicks!”).
- **Defensive Mark**: How well we’re stopping them (e.g., “Solid at the back!” or “They’re sneaking through!”).
- **Players’ Advice and Corrections**: Fun tips for 2-3 named players (e.g., “Achraf, run faster to the side!”).
- **Opponent Behavior**: What they’re up to (e.g., “They love long kicks”).
- **Most Effective Action**: One easy idea (e.g., “Pass it quick to the wings!”).
- **Decision Justification**: Simple reason (e.g., “They’re slow over there”).
- **Tactic**: Basic plan (e.g., “Push up and chase!”).
- **Substitution Recommendations**: Swap idea if someone’s struggling (e.g., “Bring Y in—X isn’t keeping up!”).

Keep it super simple, fun, and focused on FRMF Morocco winning. Use only the data, don’t make stuff up, and don’t help the other team.
Make sure to analyze the whole prompt.
Don't mention event id's.

Data: {query}"""

# # Define the prompt template for the conversation
# coach_template = """You are a soccer coach assistant for FMRF Morocco you will receive data in the next prompts collected from a match, generate solutions, ideas and decisions in order to win the game based on only and only the previous actions you have to predict the next most effective move for the coach to make after each 5 minutes for the duration from the start to the end of the match.

# The desired format:
# - Team Trends of the 5 minutes
# - in-depth analysis
# - offensive mark, defensive mark both in percentage
# - players advices and corrections
# - opponent behavior
# - most effectives action
# - decision justification
# - tactic
# - substitution recommendations.

# Notes:
# Make sure to analyze the whole prompt.
# Don't mention event id's.
# Don't help the opposing team.

# Data: {query}"""

# amateur_template = """You are a soccer coach assistant for FMRF Morocco you will receive data in the next prompts collected from a match, generate solutions, ideas and decisions in order to win the game based on only and only the previous actions you have to predict the next most effective move for the coach to make after each 5 minutes for the duration from the start to the end of the match, the data is dedicated for audience with low level understanding of football.

# The desired format:
# - Team Trends of the 5 minutes
# - in-depth analysis
# - offensive mark, defensive mark both in percentage
# - players advices and corrections
# - opponent behavior
# - most effectives action
# - decision justification
# - tactic
# - substitution recommendations.

# Notes:
# The data is dedicated for audience with low level understanding of football.
# Make sure to analyze the whole prompt.
# Don't mention event id's.
# Don't help the opposing team.

# Data: {query}"""


# Create prompt templates
coach_prompt_template = PromptTemplate(
    input_variables=["query", "context"], template=coach_template
)
amateur_prompt_template = PromptTemplate(
    input_variables=["query", "context"], template=amateur_template
)

# Set up the LLM and conversation chain

# Kinda Trash
# llm = Ollama(model="llama3.2:latest")
# llm = Ollama(model="llama3:8b-instruct-q6_K")
# llm = Ollama(model="qwen2.5")
# llm = Ollama(model="deepseek-r1:14b")


# Good
llm = Ollama(model="mistral-nemo")
# llm = Ollama(model="huihui_ai/qwen2.5-1m-abliterated")

# memory = ConversationBufferMemory()
memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=2000)
conversation = ConversationChain(llm=llm, verbose=True, memory=memory)

# Streamlit page configuration
st.set_page_config(layout="wide")
st.title("e-RegragAI")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_chunk" not in st.session_state:
    st.session_state.current_chunk = 0

# Load all chunks at startup
chunks = get_chunks()

# User role selection
user_role = st.selectbox(
    "Are you a coach or an amateur?", ["Select your role", "Coach", "Amateur"], key=1
)
if user_role == "Coach":
    st.session_state.user_role = "coach"
elif user_role == "Amateur":
    st.session_state.user_role = "amateur"
else:
    st.session_state.user_role = None

if st.session_state.user_role:
    st.write(f"You selected: {user_role}")
else:
    st.write("Please select your role to continue.")
    st.stop()


# Function to process a chunk and generate an insight with RAG
def process_chunk(chunk, prompt_template, chunk_index):
    query = json.dumps(chunk)
    # Retrieve relevant coaching course context
    context = retrieve_relevant_chunks(query)
    new_prompt = prompt_template.format(query=query, context=context)
    response = conversation.predict(input=new_prompt)
    # Strip <think> and </think> tags
    cleaned_response = re.sub(
        r"<think>.*?</think>", "", response, flags=re.DOTALL
    ).strip()
    # Add minute indicator
    minute_start = chunk_index
    minute_end = chunk_index + 1
    return f"**Minute {minute_start}-{minute_end} Analysis**\n\n{cleaned_response}"


# Create two columns for layout
left_column, right_column = st.columns([5, 5])

# Left column: Live Match Insights
with left_column:
    st.title("Live Match Insights")
    if st.button("Next 1 Minute"):
        if st.session_state.current_chunk < len(chunks):
            chunk = chunks[st.session_state.current_chunk]
            prompt_template = (
                coach_prompt_template
                if st.session_state.user_role == "coach"
                else amateur_prompt_template
            )
            insight = process_chunk(
                chunk, prompt_template, st.session_state.current_chunk
            )
            st.session_state.messages.append(
                {"role": "assistant", "content": insight, "source": "insight"}
            )
            st.session_state.current_chunk += 1

    # Display messages in reverse order (newest at top)
    for message in reversed(st.session_state.messages):
        if message.get("source") == "insight":
            with st.chat_message("ai"):
                st.markdown(message["content"])

# Right column: Chat Interface
with right_column:
    st.title("Chat with Assistant")
    prompt = st.chat_input("Ask your question here")
    if prompt:
        st.session_state.messages.append(
            {"role": "user", "content": prompt, "source": "chat"}
        )
        # Add RAG context for chat responses too
        context = retrieve_relevant_chunks(prompt)
        rag_prompt = f"Based on the GRASSROOTS FOOTBALL COACHING COURSE PART II context: {context}\n\n{prompt}"
        response = conversation.predict(input=rag_prompt)
        # Use for DeepSeek R1
        cleaned_response = re.sub(
            r"<think>.*?</think>", "", response, flags=re.DOTALL
        ).strip()
        st.session_state.messages.append(
            {"role": "assistant", "content": cleaned_response, "source": "chat"}
        )
    for message in st.session_state.messages:
        if message.get("source") == "chat":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
