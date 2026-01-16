import streamlit as st
import torch
from PIL import Image
import numpy as np

# Page configuration
st.set_page_config(page_title="Object Detection App", layout="centered")

st.title("🚀 Object Detection Application")
st.write("Upload an image to detect objects using YOLOv5.")

# Model load karne ka function
@st.cache_resource
def load_model():
    # Torch hub se seedha model load karein
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True, force_reload=True)
    return model

model = load_model()

# Image uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Image process karna
    image = Image.open(uploaded_file)
    img_array = np.array(image)

    # Inference (Detection)
    results = model(img_array)

    # Results render karna (boxes draw karna)
    # results.render() ek list deta hai, pehli image [0] lein
    detected_img_array = results.render()[0] 
    
    # Result display karna
    st.image(detected_img_array, caption="Detection Results", use_container_width=True)
    st.success("Detection Successful!")