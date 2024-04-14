import io

import requests
from PIL import Image

import streamlit as st
from streamlit_paste_button import paste_image_button as pbutton


st.set_page_config(page_title="Image To Latex Converter")


st.title("Image to Latex Converter")

image_data = pbutton("Воткуть из буффера обмена")
uploaded_file = None
# uploaded_file = st.file_uploader(
#     "Upload an image of latex math equation",
#     type=["png", "jpg"],
# )
if st.button("Получить LaTeX"):
    if uploaded_file is not None or image_data.image_data is not None:
        if uploaded_file is not None:
            files = {"file": uploaded_file.getvalue()}
        elif image_data.image_data is not None:
            files = {"file": io.BytesIO(image_data.image_data._repr_png_())}
        with st.spinner("Wait for it..."):
            response = requests.post("http://localhost:8000/predict/", files=files)
        latex_code = response.json()["data"]["pred"]
        st.code(latex_code)
        st.markdown(f"${latex_code}$")
    else:
        st.error("Надо воткнуть фотку!")

if image_data.image_data is not None:
    st.image(image_data.image_data, caption="Загруженная имага", use_column_width=True)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image)
