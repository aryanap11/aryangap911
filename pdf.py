import fitz  # PyMuPDF
from PIL import Image, ImageOps
import streamlit as st
import io
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="PDF Background Cleaner",
    page_icon="🖨️",
    layout="wide",
)


def show_feedback():
    st.write("🔗 Connect with me on:")
    st.markdown(
        "[LinkedIn](https://www.linkedin.com/in/aryanpatel11) | [GitHub](https://github.com/aryanap11)")

    st.title("Thank Me Here 😁")
    st.write("🎉 Hey there, I'm Aryan! I made this app just for you all! If you enjoyed it, feel free to thank me or share your thoughts below! 😊💬")

    # Embed Google Form using Markdown
    st.markdown(
        """<style>
    /* Container */
    .form-container {
        max-width: 400px;
        margin: 0;
    }

    /* Labels */
    label {
        display: block;
        margin-bottom: 5px;
        font-weight: bold;
    }

    /* Input fields and textarea */
    input[type="text"],
    input[type="email"],
    textarea {
        width: 100%;
        padding: 8px;
        margin-bottom: 15px;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-sizing: border-box;
    }

    /* Button */
    button[type="submit"] {
        background-color: #4caf50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }

    button[type="submit"]:hover {
        background-color: #45a049;
    }
</style>

<div class="form-container">
<form action="https://submit-form.com/6Gh4t63hK">
        <label for="name">Your Name</label>
        <input type="text" id="name" name="name" placeholder="Name" required="" />
        <label for="message">Your Message</label>
        <textarea
            id="message"
            name="message"
            placeholder="Message"
            required=""
        ></textarea>
        <button type="submit">Send</button>
    </form>
</div>

        """, unsafe_allow_html=True)


def process_pdf(uploaded_file):
    try:
        # Open the PDF file
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        processed_images = []

        # Process each page in the PDF
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            zoom = 3.50  # 2.0 will double the resolution (increase DPI)
            mat = fitz.Matrix(zoom, zoom)  # Create transformation matrix

            # Render page to a high-resolution image
            pix = page.get_pixmap(matrix=mat)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # Convert to grayscale
            grayscale_img = img.convert("L")

            # Apply threshold
            thresholded_img = grayscale_img.point(
                lambda p: 255 if p > 100 else 0)

            # Invert colors
            inverted_img = ImageOps.invert(thresholded_img)

            processed_images.append(inverted_img)

        # Save processed images to a new PDF
        output_pdf = io.BytesIO()
        processed_images[0].save(
            output_pdf, format="PDF", save_all=True, append_images=processed_images[1:])
        output_pdf.seek(0)

        return output_pdf

    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None


def main_app():
    st.title("PDF Background Cleaner")
    st.write(
        "Easily transform PDFs with dark backgrounds into print-friendly, high-contrast documents.")
    uploaded_file = st.file_uploader(
        "Upload your PDF file to begin", type=["pdf"])

    if uploaded_file:
        st.write("Processing your PDF...")
        processed_pdf = process_pdf(uploaded_file)
        original_filename = uploaded_file.name

        if processed_pdf:
            st.success("PDF processed successfully!")
            st.download_button(
                label="Download Processed PDF",
                data=processed_pdf,
                file_name=original_filename.replace('.pdf', '_neg.pdf'),
                mime="application/pdf"
            )


def display_other_apps():
    st.header("Other Apps Links:")

    # Description of Syllabus Tracker App
    st.subheader("Syllabus Tracker App 📘")
    st.write(
        "Keep track of your GATE preparation with the Syllabus Tracker App! "
        "Mark topics as completed, view your overall progress, and stay organized with a comprehensive checklist."
    )

    # Link to Syllabus Tracker App
    st.write(
        "[Open Syllabus Tracker App](https://syllabus-tracker-gate-da.streamlit.app/)")


def main():
    with st.sidebar:
        selected_page = option_menu("Navigation", ["PDF Background Cleaner", "Connect with me", "Other Apps"],
                                    icons=['file-earmark-binary',
                                           'person-fill', 'app-indicator'],
                                    menu_icon="cast", default_index=0, orientation="vertical")
        selected_page


# Navigation logic
    if selected_page == "PDF Background Cleaner":
        main_app()
    elif selected_page == "Connect with me":
        show_feedback()
    elif selected_page == "Other Apps":
        display_other_apps()


if __name__ == "__main__":
    main()
