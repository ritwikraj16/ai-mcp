import streamlit as st
import ollama
from PIL import Image
import io
import fitz  # PyMuPDF

# Page configuration
st.set_page_config(
    page_title="Llama OCR",
    page_icon="🦙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description in main area
st.title("🦙 Llama OCR")

# Add clear button to top right
col1, col2 = st.columns([6, 1])
with col2:
    if st.button("Clear 🗑️"):
        if 'ocr_result' in st.session_state:
            del st.session_state['ocr_result']
        st.rerun()

st.markdown('<p style="margin-top: -20px;">Extract structured text from images using Llama 3.2 Vision!</p>', unsafe_allow_html=True)
st.markdown("---")

# Function to convert PDF to image using in-memory byte stream
def pdf_to_image(pdf_file):
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")  # Open PDF directly from byte stream
    # Convert the first page to an image
    page = pdf_document[0]  # Get the first page
    pix = page.get_pixmap()
    img_data = pix.tobytes("png")  # Convert to PNG image bytes
    img = Image.open(io.BytesIO(img_data))  # Open the image from bytes
    return img

# Move upload controls to sidebar
with st.sidebar:
    st.header("Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg', 'pdf'])

    if uploaded_file is not None:
        if uploaded_file.type == 'application/pdf':
            # If the uploaded file is a PDF, convert it to an image
            with st.spinner("Converting PDF to image..."):
                try:
                    image = pdf_to_image(uploaded_file)
                    st.image(image, caption="Converted Image from PDF")
                except Exception as e:
                    st.error(f"Error converting PDF: {str(e)}")
        else:
            # If it's an image file, load it directly
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image")

        # Convert the image to bytes (PNG/JPG format) before sending to OCR
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='PNG')  # Convert to PNG format
        image_bytes.seek(0)  # Reset the stream pointer to the beginning

        if st.button("Extract Text 🔍", type="primary"):
            with st.spinner("Processing image..."):
                try:
                    # Send the image as bytes to Ollama OCR model
                    response = ollama.chat(
                        model='llama3.2-vision',
                        messages=[{
                            'role': 'user',
                            'content': """Give me the total amount only.""",
                            'images': [image_bytes.getvalue()]
                        }]
                    )
                    st.session_state['ocr_result'] = response.message.content
                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")

# Main content area for results
if 'ocr_result' in st.session_state:
    st.markdown(st.session_state['ocr_result'])
else:
    st.info("Upload an image and click 'Extract Text' to see the results here.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Llama Vision Model2 | [Report an Issue](https://github.com/patchy631/ai-engineering-hub/issues)")
