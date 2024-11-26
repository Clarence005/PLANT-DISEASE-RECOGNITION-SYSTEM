import streamlit as st
import tensorflow as tf
import numpy as np
# from recomendations import get_disease_info
import base64
from AgriBot.chat import get_response
import streamlit as st
from segmentation import calculate_disease_area_percentage
from PIL import Image
import cx_Oracle
from recomendations import get_disease_info

# Connect to the Oracle database
try:
    oracle_connection_string = 'system/clarence@localhost:1521/XE'
    connection = cx_Oracle.connect(oracle_connection_string)
    cursor = connection.cursor()
except cx_Oracle.DatabaseError as e:
    error, = e.args
    print("Oracle-Error-Code:", error.code)
    print("Oracle-Error-Message:", error.message)
    
def model_prediction(test_image):
    model = tf.keras.models.load_model("trained_model.keras")
    image = tf.keras.preprocessing.image.load_img(test_image,target_size=(128,128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr]) 
    predictions = model.predict(input_arr)
    return np.argmax(predictions) 

st.sidebar.title("Dashboard")
app_mode = st.sidebar.selectbox("Select Page",["Home","About","Disease Recognition","AgriBot"])

#Main Page
if(app_mode=="Home"):
    st.header("PLANT DISEASE RECOGNITION SYSTEM")
    image_path = "home_page.jpeg"
    st.image(image_path,use_column_width=True)
    st.markdown("""
    Welcome to the Plant Disease Recognition System! 🌿🔍
    
    Our mission is to help in identifying plant diseases efficiently. Upload an image of a plant, and our system will analyze it to detect any signs of diseases. Together, let's protect our crops and ensure a healthier harvest!

    ### How It Works
    1. **Upload Image:** Go to the **Disease Recognition** page and upload an image of a plant with suspected diseases.
    2. **Analysis:** Our system will process the image using advanced algorithms to identify potential diseases.
    3. **Results:** View the results and recommendations for further action.

    ### Why Choose Us?
    - **Accuracy:** Our system utilizes state-of-the-art machine learning techniques for accurate disease detection.
    - **User-Friendly:** Simple and intuitive interface for seamless user experience.
    - **Fast and Efficient:** Receive results in seconds, allowing for quick decision-making.

    ### Get Started
    Click on the **Disease Recognition** page in the sidebar to upload an image and experience the power of our Plant Disease Recognition System!

    ### About Us
    Learn more about the project, our team, and our goals on the **About** page.
    """)

elif(app_mode=="About"):
    st.header("About")
    st.markdown("""
                #### About Dataset
                This dataset is recreated using offline augmentation from the original dataset.The original dataset can be found on this github repo.
                This dataset consists of about 87K rgb images of healthy and diseased crop leaves which is categorized into 38 different classes.The total dataset is divided into 80/20 ratio of training and validation set preserving the directory structure.
                A new directory containing 33 test images is created later for prediction purpose.
                #### Content
                1. train (70295 images)
                2. test (33 images)
                3. validation (17572 images)

                """)

elif(app_mode=="Disease Recognition"):
    st.header("Disease Recognition")
    test_image = st.file_uploader("Choose an Image:")
    if(st.button("Show Image")):
        st.image(test_image,width=4,use_column_width=True)
    #Predict button
    if(st.button("Predict")):
        st.snow()
        st.write("Our Prediction")
        result_index = model_prediction(test_image)
        class_name = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
                    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 
                    'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 
                    'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 
                    'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 
                    'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
                    'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 
                    'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 
                    'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 
                    'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 
                    'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 
                    'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 
                    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
                      'Tomato___healthy']
        img = Image.open(test_image)
        diseased_percentage, mask, result_img = calculate_disease_area_percentage(img)    
        if("healthy" in class_name[result_index]):
            st.image(test_image, caption=f"Resilt Image", use_column_width=True)
        else:
            st.image(result_img, caption="Result Image", use_column_width=True)
        
        dis =class_name[result_index].replace("_","  ")
        st.success(" it's a {}".format(dis))
        table1 = "plant_dis"
        dis = get_disease_info(class_name[result_index])
        # query = f"select * from  {table1} where disease = '{class_name[result_index]}' "
        # cursor.execute(query)
        # result = cursor.fetchall() 
        # val = result
        # print(val)
        st.markdown(
        """
        <div style='background-color: #f0f0f0; padding: 15px; border-radius: 5px;'>
            <h5>Description:</h5>
            <p>{}</p>
            <h5>Treatment:</h5>
            <p>{}</p>
            <h5>Prevention:</h5>
            <p>{}</p>
        </div>
        """.format(dis["description"], dis["treatment"], dis["prevention"]),
        unsafe_allow_html=True
    )
elif(app_mode == "AgriBot"):


    # Function to convert local image to base64 string
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
        