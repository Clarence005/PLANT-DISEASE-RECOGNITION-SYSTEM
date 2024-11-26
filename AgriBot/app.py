import base64
from chat import get_response
def get_base64_image(image_path):
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
        return encoded


    # Set background image with the uploaded image
image_path = "D:\\Academic\\SDP\\data\\cropdisease\\AgriBot\\img\\bg.png"  # Path to the uploaded image file
background_image = get_base64_image(image_path)

# Background styling and container style
st.markdown(
f"""
<style>
/* Set full-page background */
.stApp {{
    background-image: url("data:image/png;base64,{background_image}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: top center;
}}
.chat-bubble-user {{
    background-color: #DCF8C6;
    padding: 10px;
    border-radius: 8px;
    max-width: 70%;
    text-align: right;
    margin: 5px;
    float: right;
    clear: both;
}}
.chat-bubble-bot {{
    background-color: #F1F0F0;
    padding: 10px;
    border-radius: 8px;
    max-width: 70%;
    text-align: left;
    margin: 5px;
    float: left;
    clear: both;
}}
</style>
""",
unsafe_allow_html=True
)

container_bg = """
<style> 
[data-testid="stHeader"]{
background-color:rgba(0,0,0,0);
}
[data-testid="stVerticalBlockBorderWrapper"]{
background-color: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    max-width: 800px;
    margin: 5vh auto;
}
[data-testid="element-container"]{
text-align:center;
}
[data-testid="stImageContainer"]{
display: flex;
    justify-content: center;
    align-items: center;
        /* Adjust size */
}
</style>
"""
# Start the white content box container
st.markdown(container_bg, unsafe_allow_html=True)

if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Function to add a message to the conversation
def add_message(sender, message):
    st.session_state.conversation.append({"sender": sender, "message": message})

st.title("AGRIBOT.CHAT")
st.subheader("Revolutionizing Agriculture with Insight and Innovation 🌱")

# Description text
st.write("Disclaimer: Agribot is currently optimized for Apple, Corn, Potato, Tomato, Pepper, Grape, and Strawberry crops only.")

# Display example questions in a grid
cols = st.columns(2)

# Define buttons to store the value in session state
button_values = {
"How to boost tomato plant growth?": "How to boost tomato plant growth?",
"Grape pest control tips?": "Grape pest control tips?",
"Indian government scheme for indian farmer": "indian government scheme for indian farmer",
"Tips for better harvest?": "Tips for better harvest?"
}

# Display buttons and store the button text in session_state when clicked
with cols[0]:
    if st.button(button_values["How to boost tomato plant growth?"]):
        st.session_state.user_input = button_values["How to boost tomato plant growth?"]
    if st.button(button_values["Grape pest control tips?"]):
        st.session_state.user_input = button_values["Grape pest control tips?"]

with cols[1]:
    if st.button(button_values["Indian government scheme for indian farmer"]):
        st.session_state.user_input = button_values["Indian government scheme for indian farmer"]
    if st.button(button_values["Tips for better harvest?"]):
        st.session_state.user_input = button_values["Tips for better harvest?"]

# Message box for user input
user_message = st.text_input("Message AGRI.CHAT", placeholder="Type your question here...", key="user_input_field")

# Store the text input in session_state if the user has typed something
if user_message:
    st.session_state.user_input = user_message 

if 'user_input' in st.session_state:
    add_message("user", st.session_state.user_input)
    # Example bot response (you can replace this with real bot logic)
    bot_response = get_response(st.session_state.user_input)
    add_message("bot", bot_response)
    st.session_state.user_input = ""

for msg in st.session_state.conversation:
    if msg["sender"] == "user":
        st.markdown(f'<div class="chat-bubble-user">{msg["message"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble-bot">{msg["message"]}</div>', unsafe_allow_html=True)

# Close the white box div
st.markdown('</div>', unsafe_allow_html=True)