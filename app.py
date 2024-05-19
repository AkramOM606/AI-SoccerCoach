import streamlit as st
from openai import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain import memory
import time
from openai import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import Ollama
from langchain import PromptTemplate
from api import send_chunked_json

template = """You are a soccer coach assistant for FMRF Morocco you will receive data in the next prompts collected from a match, generate solutions, ideas and decisions in order to win the game based on only and only the previous actions you have to predict the next most effective move for the coach to make after each 5 minutes for the duration from the start to the end of the match.

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

prompt_template = PromptTemplate(input_variables=["query"], template=template)

st.set_page_config(layout="wide")

llm = Ollama(model="llama3:8b-instruct-q6_K")
memory = ConversationSummaryMemory(llm=llm)

conversation = ConversationChain(llm=llm, verbose=False, memory=memory)


async def process_chunked_json(send_chunked_json, prompt_template):
    # Await the coroutine and get the result
    result = await send_chunked_json()
    # Now you can iterate over the result
    for chunk in result:
        # Process the chunk (optional)
        # You can perform any necessary processing on the chunk here,
        # such as appending it to a list or accumulating results.

        new_prompt = prompt_template.format(query=chunk)
        user_input = st.text_input(new_prompt)

        # Process user input (optional)
        # You can use the user input to filter, refine, or interact with the data.


def data_card(title, content):
    """
    Creates a data card with rounded corners using CSS.

    Args:
        title (str): Title of the card.
        content (str): Content of the card.
    """
    st.markdown(
        f"""
    <style>
        .data-card {{
        background-color: #fbfbfb;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        .data-card-title {{
        font-weight: bold;
        margin-bottom: 5px;
        }}
    </style>
    <div class="data-card">
        <h3 class="data-card-title">{title}</h3>
        <p>{content}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


st.title("e-RegragAI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Step 2: Check if the API key has been entered
# Step 3: Prompt for user role
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

# Display the user's choice
if st.session_state.user_role:
    st.write(f"You selected: {user_role}")
else:
    st.write("Please select your role to continue.")

# Use the session state variable in the rest of your app
if st.session_state.user_role == "coach":
    left_column, right_column = st.columns([5, 5])

    with right_column:
        with st.container():
            prompt = st.chat_input("Pass your prompt here")
            if prompt:
                st.session_state.messages.append({"role": "user", "content": prompt})
                response = conversation.predict(input=prompt)

                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("ai"):
                    completed_message = ""
                    # message = st.empty()
                    message = st.markdown(response)

                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )

    # Chat interface in left column
    with left_column:
        st.title("Live Match Insights")
        time.sleep(30)
        with st.empty():
            st.write(
                "00:00:00 -> 00:00:10\n* From the provided data, I can see that we're dealing with a kick-off event. Our opponent is EFA Egypt, and the\r\ngame has just started. Let's focus on the key events:\r\n\r\n1. **Pass**: Akram Tawfik from EFA Egypt passes the ball to Marwan Ateya (Right Defensive Midfield) at 0:00:04.\r\nThe pass is a ground pass with a length of 25.02 meters and an angle of 1.61 degrees.\r\n2. **Carry**: Marwan Ateya receives the pass and carries the ball for 2 seconds, covering a distance of\r\napproximately 6 meters to [41.0, 51.0].\r\n3. **Pass**: Marwan Ateya passes the ball to Mohamed Abdelmonem (Right Defensive Midfield) at 0:00:07. The pass is\r\nanother ground pass with a length of 11.4 meters and an angle of 2.48 degrees.\r\n4. **Pressure**: Amine Adli from FRMF Morocco applies pressure on EFA Egypt's player, Mohamed Abdelmonem, at\r\n0:00:09.\r\n\r\nThe key observations I can make are:\r\n\r\n* EFA Egypt has the possession of the ball for most of these initial events.\r\n* Our team, FMRF Morocco, is struggling to gain control of the ball in these early moments.\r\n* The pressure applied by Amine Adli on Mohamed Abdelmonem could be an opportunity to win the ball back.\r\n\r\nAs the assistant coach, my recommendations would be:\r\n\r\n1. **Improve ball distribution**: We need to work on our passing accuracy and decision-making to create better\r\nscoring opportunities.\r\n2. **Defend more effectively**: Our players should focus on winning the ball back quickly after losing possession,\r\nrather than allowing EFA Egypt to maintain control for extended periods.\r\n3. **Utilize set pieces**: We should look to exploit any free kicks or corners that come our way, as these can be\r\neffective ways to create scoring opportunities.\r\n\r\nLet's use this data to adjust our strategy and work on improving our performance in the match!"
            )
            time.sleep(30)
            st.write(
                "00:00:10 -> 00:00:20\n* EFA Egypt has maintained possession for most of the game, but with some difficulty in progressing up the field.\r\n* FRMF Morocco has been applying pressure on the Egyptian defense, making it challenging for them to build\r\nattacks.\r\n\r\n**In-Depth Analysis:**\r\n\r\n* The game has started with a high-intensity tempo, with both teams looking to assert their dominance. EFA Egypt's\r\nRight Center Back, Mohamed Abdelmonem, has received the ball multiple times and has attempted to carry the ball up\r\nthe field, but has been under pressure from FRMF Morocco.\r\n* FRMF Morocco's Left Wing, Amine Adli, has made a key block to disrupt an Egyptian attack, showcasing their\r\nability to anticipate and intercept opposition moves.\r\n\r\n**Offensive Mark:**\r\n        + EFA Egypt: 40% (They have had some promising moments, but have struggled to create clear-cut chances)\r\n        + FRMF Morocco: 60% (Their high-pressing game has caused problems for the Egyptian defense)\r\n\r\n**Defensive Mark:**\r\n        + EFA Egypt: 30% (The Moroccan pressure has been effective in limiting their attacking opportunities)\r\n        + FRMF Morocco: 70% (They have managed to win the ball back quickly and apply pressure on the Egyptian defense)\r\n\r\n**Players' Advice and Corrections:**\r\n\r\n* Mohamed Abdelmonem (Right Center Back, EFA Egypt): Continue to carry the ball up the field, but look for more\r\naccurate passing options. Be aware of Amine Adli's runs from midfield.\r\n* Amine Adli (Left Wing, FRMF Morocco): Keep applying pressure on the Egyptian defense and anticipate opposition\r\nmoves.\r\n\r\n**Opponent Behavior:**\r\n\r\n* FRMF Morocco is likely to continue their high-pressing game, trying to win the ball back quickly and disrupt EFA\r\nEgypt's build-up play.\r\n* EFA Egypt may look to switch the point of attack more frequently to find space behind the Moroccan press.\r\n\r\n**Most Effective Action:**\r\n        + Recommended action for EFA Egypt: Switch the point of attack to the left flank, using Mohamed Hany's pace on t\r\nthe right wing back to create a numerical advantage.\r\n        + Recommended action for FRMF Morocco: Continue to apply pressure on the Egyptian defense, focusing on winning t\r\nthe ball back quickly and launching counter-attacks.\r\n\r\n**Decision Justification:**\r\nThe recommended actions are based on the current trends in the game. EFA Egypt needs to adapt to the Moroccan\r\npress by creating more space behind the defense, while FRMF Morocco should continue to exploit the Egyptian\r\ndefense's vulnerability under pressure.\r\n\r\n**Tactic:**\r\n\r\n* EFA Egypt should employ a more direct approach, using Mohamed Abdelmonem's carrying ability and Mohamed Hany's\r\npace on the right wing back to bypass the Moroccan press.\r\n* FRMF Morocco can maintain their high-pressing game, but be prepared to adjust their positioning to account for\r\nEFA Egypt's potential changes in shape.\r\n\r\n**Substitution Recommendations:**\r\n\r\n* None at this stage. Both teams have maintained a strong bench presence so far, and no obvious substitution\r\nopportunities arise from the current situation."
            )

elif st.session_state.user_role == "amateur":
    # Add amateur-specific content here
    st.write("Welcome, Amateur! Here are some resources for you.")
