import streamlit as st
import cv2
import torch
from PIL import Image
import numpy as np

st.set_page_config(page_title="Object Detection App", layout="centered")

st.title("🚀 Object Detection Application")
st.write("Upload an image to detect objects using YOLO.")

@st.cache_resource
def load_model():
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    return model

model = load_model()

uploaded_file = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    img = np.array(image)

    results = model(img)
    detected_img = np.squeeze(results.render())

    st.image(detected_img, caption="Detected Image", use_container_width=True)
