import streamlit as st
import torch
from PIL import Image
import numpy as np

# Page configuration
st.set_page_config(page_title="Object Detection App", layout="centered")

st.title("🚀 Object Detection Application")
st.write("Upload an image to detect objects using YOLOv5.")

# Model load karne ka function (Cached taaki baar baar download na ho)
@st.cache_resource
def load_model():
    # Hum seedha torch hub se model load kar rahe hain
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    return model

model = load_model()

# File uploader widget
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Image ko open aur process karna
    image = Image.open(uploaded_file)
    img_array = np.array(image)

    # Inference (Detection)
    results = model(img_array)

    # Results ko render karna (Ye image par boxes bana deta hai)
    # results.render() ek list return karta hai, isliye [0] use kar rahe hain
    detected_img_array = results.render()[0] 
    
    # Final image display karna
    st.image(detected_img_array, caption="Detection Results", use_container_width=True)
    
    # Success message
    st.success("Detection Complete!")