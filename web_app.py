import streamlit as st
import torch
from PIL import Image
import numpy as np

st.set_page_config(page_title="Live Object Detection", layout="centered")

st.title("🚀 Real-time Object Detection")
st.write("Upload an image OR use your Camera for live detection.")

@st.cache_resource
def load_model():
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    return model

model = load_model()

# User ko do options dena: Camera ya File Upload
option = st.radio("Select Input Method:", ("Camera", "Upload Image"))

source_img = None

if option == "Camera":
    source_img = st.camera_input("Take a picture")
else:
    source_img = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])

if source_img:
    # Image process karna
    image = Image.open(source_img)
    img_array = np.array(image)

    # Detection
    results = model(img_array)
    detected_img = results.render()[0]

    # Result dikhana
    st.image(detected_img, caption="Detection Result", use_container_width=True)
    st.success("Detected successfully!")