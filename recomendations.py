import cx_Oracle

# Connect to the Oracle database
def get_disease_info(dis):
    
    # Disease data dictionary
    disease_data = {
        "Apple___Apple_scab": {
            "description": "A fungal disease causing dark spots on leaves and fruit.",
            "treatment": "Use fungicides like captan or mancozeb.",
            "prevention": "Remove fallen leaves; prune trees for better air circulation."
        },
        "Apple___Black_rot": {
            "description": "A fungal infection causing fruit and leaf lesions.",
            "treatment": "Apply copper-based fungicides.",
            "prevention": "Avoid overhead watering; remove infected branches."
        },
        "Apple___Cedar_apple_rust": {
            "description": "A fungal disease affecting apples and cedar trees, causing leaf spots.",
            "treatment": "Use fungicides containing myclobutanil.",
            "prevention": "Remove nearby cedar trees if possible."
        },
        "Apple___healthy": {
            "description": "No disease detected.",
            "treatment": "No treatment required.",
            "prevention": "Continue proper care and monitoring."
        },
        "Blueberry___healthy": {
            "description": "No disease detected.",
            "treatment": "No treatment required.",
            "prevention": "Ensure regular watering and mulching."
        },
        "Cherry_(including_sour)___Powdery_mildew": {
            "description": "A fungal disease causing white powder on leaves.",
            "treatment": "Use sulfur or potassium bicarbonate sprays.",
            "prevention": "Ensure good air circulation and avoid overhead watering."
        },
        "Cherry_(including_sour)___healthy": {
            "description": "No disease detected.",
            "treatment": "No treatment required.",
            "prevention": "Regular pruning and care recommended."
        },
        "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
            "description": "A fungal infection causing leaf spots.",
            "treatment": "Apply fungicides like strobilurin.",
            "prevention": "Rotate crops and use resistant varieties."
        },
        "Corn_(maize)___Common_rust_": {
            "description": "A fungal disease causing rust-colored pustules on leaves.",
            "treatment": "Use fungicides like chlorothalonil.",
            "prevention": "Plant rust-resistant corn varieties."
        },
        "Corn_(maize)___Northern_Leaf_Blight": {
            "description": "A fungal infection leading to long, gray lesions on leaves.",
            "treatment": "Apply fungicides like azoxystrobin.",
            "prevention": "Plant resistant varieties and rotate crops."
        },
        "Corn_(maize)___healthy": {
            "description": "No disease detected.",
            "treatment": "No treatment required.",
            "prevention": "Regular monitoring and care."
        },
        "Grape___Black_rot": {
            "description": "A fungal disease causing black spots on leaves and fruits.",
            "treatment": "Apply fungicides like myclobutanil.",
            "prevention": "Remove affected vines and maintain good air circulation."
        },
        "Grape___Esca_(Black_Measles)": {
            "description": "A fungal infection causing brown streaks on leaves.",
            "treatment": "Prune and remove infected parts.",
            "prevention": "Avoid excessive irrigation."
        },
        "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
            "description": "A fungal disease causing blight on leaves.",
            "treatment": "Use copper-based fungicides.",
            "prevention": "Regular pruning and avoid overcrowding."
        },
        "Grape___healthy": {
            "description": "No disease detected.",
            "treatment": "No treatment required.",
            "prevention": "Regular care and good vine management."
        },
        "Orange___Haunglongbing_(Citrus_greening)": {
            "description": "A bacterial disease spread by insect vectors, leading to green, misshapen fruit.",
            "treatment": "No cure; remove infected trees.",
            "prevention": "Control the spread of citrus psyllids with insecticides."
        },
        "Peach___Bacterial_spot": {
            "description": "A bacterial infection causing dark spots on fruit and leaves.",
            "treatment": "Apply copper sprays in early season.",
            "prevention": "Use resistant peach varieties if available."
        },
        "Peach___healthy": {
            "description": "No disease detected.",
            "treatment": "No treatment required.",
            "prevention": "Continue proper care and monitoring."
        },
        "Pepper,_bell___Bacterial_spot": {
            "description": "A bacterial disease causing dark lesions on leaves and fruits.",
            "treatment": "Apply copper-based bactericides.",
            "prevention": "Avoid overhead watering and practice crop rotation."
        },
        "Pepper,_bell___healthy": {
            "description": "No disease detected.",
            "treatment": "No treatment required.",
            "prevention": "Regular monitoring and care recommended."
        },
        "Potato___Early_blight": {
            "description": "A fungal disease causing brown spots on leaves.",
            "treatment": "Use fungicides like chlorothalonil.",
            "prevention": "Rotate crops and remove infected plants."
        },
        "Potato___Late_blight": {
            "description": "A fungal disease causing dark spots on leaves and tubers.",
            "treatment": "Use fungicides containing metalaxyl.",
            "prevention": "Avoid overhead watering and ensure proper plant spacing."
        },
        "Potato___healthy": {
            "description": "No disease detected.",
            "treatment": "No treatment required.",
            "prevention": "Regular care and proper spacing."
        },
        "Raspberry___healthy": {
            "description": "No disease detected.",
            "treatment": "No treatment required.",
            "prevention": "Regular monitoring and care recommended."
        },
        "Soybean___healthy": {
            "description": "No disease detected.",
            "treatment": "No treatment required.",
            "prevention": "Regular monitoring and care."
        },
        "Squash___Powdery_mildew": {
            "description": "A fungal disease causing white powder on leaves.",
            "treatment": "Apply potassium bicarbonate sprays.",
            "prevention": "Ensure good air circulation around plants."
        },
        "Strawberry___Leaf_scorch": {
            "description": "A fungal disease causing dark edges on leaves.",
            "treatment": "Use fungicides like captan.",
            "prevention": "Avoid overhead watering and overcrowding."
        },
        "Strawberry___healthy": {
            "description": "No disease detected.",
            "treatment": "No treatment required.",
            "prevention": "Regular monitoring and care."
        },
        "Tomato___Bacterial_spot": {
            "description": "A bacterial disease causing dark spots on leaves and fruit.",
            "treatment": "Use copper-based bactericides.",
            "prevention": "Avoid overhead watering and ensure proper spacing."
        },
        "Tomato___Early_blight": {
            "description": "A fungal disease causing brown lesions on leaves.",
            "treatment": "Use fungicides like chlorothalonil.",
            "prevention": "Rotate crops and avoid overhead watering."
        },
        "Tomato___Late_blight": {
            "description": "A fungal disease leading to dark, water-soaked spots on leaves.",
            "treatment": "Apply fungicides containing mancozeb or chlorothalonil.",
            "prevention": "Plant disease-resistant varieties if possible."
        },
        "Tomato___Leaf_Mold": {
            "description": "A fungal infection leading to yellow spots on leaves.",
            "treatment": "Apply fungicides like copper oxychloride.",
            "prevention": "Ensure good air circulation and avoid overhead watering."
        },
        "Tomato___Septoria_leaf_spot": {
            "description": "A fungal disease causing small dark spots on leaves.",
            "treatment": "Use fungicides like mancozeb.",
            "prevention": "Avoid watering from above and remove infected leaves."
        },
        "Tomato___Spider_mites Two-spotted_spider_mite": {
            "description": "Mites that cause leaves to turn yellow and brown.",
            "treatment": "Use insecticidal soaps or neem oil.",
            "prevention": "Regularly monitor and increase humidity around plants."
        },
        "Tomato___Target_Spot": {
            "description": "A fungal infection leading to dark spots on leaves.",
            "treatment": "Apply fungicides containing azoxystrobin.",
            "prevention": "Ensure good air circulation around plants."
        },
        "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
            "description": "A viral disease causing yellowing and curling of leaves.",
            "treatment": "Remove infected plants and control whiteflies.",
            "prevention": "Plant disease-resistant varieties and use insect barriers."
        },
        "Tomato___Tomato_mosaic_virus": {
            "description": "A viral disease causing mottling and curling of leaves.",
            "treatment": "Remove infected plants.",
            "prevention": "Practice good hygiene and avoid insect vectors."
        },
        "Tomato___healthy": {
            "description": "No disease detected.",
            "treatment": "No treatment required.",
            "prevention": "Regular care and monitoring."
        },
    }
    return disease_data[dis]
  


    