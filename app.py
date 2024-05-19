import streamlit as st
import asyncio
from langchain import PromptTemplate
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationChain
from langchain_community.llms import Ollama
from api import send_chunked_json  # Assuming you have this implemented elsewhere

# Define the prompt template for the conversation
coach_template = """You are a soccer coach assistant for FMRF Morocco you will receive data in the next prompts collected from a match, generate solutions, ideas and decisions in order to win the game based on only and only the previous actions you have to predict the next most effective move for the coach to make after each 5 minutes for the duration from the start to the end of the match.

The desired format:
- Team Trends of the 5 minutes
- in-depth analysis
- offensive mark, defensive mark both in percentage
- players advices and corrections
- opponent behavior
- most effectives action
- decision justification
- tactic
- substitution recommendations.

Notes:
Make sure to analyze the whole prompt.
Don't mention event id's.
Don't help the opposing team.

Data: {query}"""

amateur_template = """You are a soccer coach assistant for FMRF Morocco you will receive data in the next prompts collected from a match, generate solutions, ideas and decisions in order to win the game based on only and only the previous actions you have to predict the next most effective move for the coach to make after each 5 minutes for the duration from the start to the end of the match, the data is dedicated for audience with low level understanding of football.

The desired format:
- Team Trends of the 5 minutes
- in-depth analysis
- offensive mark, defensive mark both in percentage
- players advices and corrections
- opponent behavior
- most effectives action
- decision justification
- tactic
- substitution recommendations.

Notes:
The data is dedicated for audience with low level understanding of football.
Make sure to analyze the whole prompt.
Don't mention event id's.
Don't help the opposing team.

Data: {query}"""

# Create prompt templates for both roles
coach_prompt_template = PromptTemplate(
    input_variables=["query"], template=coach_template
)
amateur_prompt_template = PromptTemplate(
    input_variables=["query"], template=amateur_template
)

# Set up the LLM (Large Language Model) and conversation chain
llm = Ollama(model="llama3:8b-instruct-q6_K")
memory = ConversationSummaryMemory(llm=llm)
conversation = ConversationChain(llm=llm, verbose=False, memory=memory)

# Streamlit page configuration
st.set_page_config(layout="wide")
st.title("e-RegragAI")

# Initialize session state for storing messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages in the session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Prompt the user to select their role
user_role = st.selectbox(
    "Are you a coach or an amateur?",
    ["Select your role", "Coach", "Amateur"],
    key=1,
)

# Update session state based on user selection
if user_role == "Coach":
    st.session_state.user_role = "coach"
elif user_role == "Amateur":
    st.session_state.user_role = "amateur"
else:
    st.session_state.user_role = None

# Display the user's selected role
if st.session_state.user_role:
    st.write(f"You selected: {user_role}")
else:
    st.write("Please select your role to continue.")


# Function to process the chunked JSON data and generate prompts
async def process_chunked_json(send_chunked_json, prompt_template):
    result = await send_chunked_json()
    for chunk in result:
        new_prompt = prompt_template.format(query=chunk)
        user_input = st.text_input(new_prompt)
        if user_input:
            response = conversation.predict(input=user_input)
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append({"role": "assistant", "content": response})

            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("ai"):
                st.markdown(response)


# Display different interfaces based on the user's role
if st.session_state.user_role == "coach":
    left_column, right_column = st.columns([5, 5])

    # Right column for chat input and responses
    with right_column:
        with st.container():
            prompt = st.chat_input("Pass your prompt here")
            if prompt:
                st.session_state.messages.append({"role": "user", "content": prompt})
                response = conversation.predict(input=prompt)

                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("ai"):
                    st.markdown(response)

                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )

    # Left column for live match insights
    with left_column:
        st.title("Live Match Insights")
        # Start processing chunked JSON data asynchronously
        asyncio.run(process_chunked_json(send_chunked_json, coach_prompt_template))

elif st.session_state.user_role == "amateur":
    # Process chunked JSON data for amateurs
    asyncio.run(process_chunked_json(send_chunked_json, amateur_prompt_template))
