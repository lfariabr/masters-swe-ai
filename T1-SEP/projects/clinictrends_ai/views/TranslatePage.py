import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Add parent directory to path to import utils
sys.path.append(str(Path(__file__).parent.parent))
from utils.translate import translate_dataframe, translate_text
from utils.alerts import send_discord_message

def show_translate():
    st.title(" Text & File Translation")
    st.markdown("""
    Translate customer feedback between different languages. 
    You can either translate individual pieces of text or process entire CSV files.
    """)

    # Create tabs for different translation methods
    tab1, tab2 = st.tabs([" Text Translation", " File Translation"])

    with tab1:
        st.header("Text Translation")
        st.markdown("Quickly translate individual pieces of text.")
        
        # Input text area
        text_to_translate = st.text_area("Enter text to translate:", height=150)
        
        # Language selection
        col1, col2 = st.columns(2)
        with col1:
            source_lang = st.selectbox(
                "From:",
                ["pt", "es", "fr", "de", "it", "ru", "zh", "ja", "ko", "ar"],
                index=0,
                help="Source language code",
                key="text_source_lang"
            )
        
        with col2:
            target_lang = st.selectbox(
                "To:",
                ["en", "es", "fr", "de", "it", "pt", "ru", "zh", "ja", "ko", "ar"],
                index=0,
                help="Target language code",
                key="text_target_lang"
            )
        
        # Translate button
        if st.button("Translate", type="primary", key="translate_btn"):
            if text_to_translate.strip():
                send_discord_message(f"A translation request has been made with '{text_to_translate[:50]}' from '{source_lang}' to '{target_lang}'")
                with st.spinner("Translating..."):
                    try:
                        translated_text = translate_text(
                            text_to_translate, 
                            source_lang=source_lang,
                            target_lang=target_lang
                        )
                        st.text_area("Translated text:", value=translated_text, height=150, key="translated_text")
                    except Exception as e:
                        st.error(f"Translation failed: {str(e)}")
            else:
                st.warning("Please enter some text to translate.")

    with tab2:
        st.header("File Translation")
        st.markdown("Upload a CSV file to translate text in a specific column.")
        
        # File uploader
        uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"], key="file_uploader")
        
        if uploaded_file is not None:
            try:
                # Read the uploaded file
                df = pd.read_csv(uploaded_file)
                
                # Show file info
                st.success(f"Successfully loaded {len(df)} rows")
                
                # Column selection
                text_column = st.selectbox(
                    "Select the column to translate:",
                    df.columns,
                    index=0 if 'Comment' in df.columns else 0,
                    key="column_selector"
                )
                
                # Language selection
                col1, col2 = st.columns(2)
                with col1:
                    source_lang = st.selectbox(
                        "Source language:",
                        ["pt", "es", "fr", "de", "it", "ru", "zh", "ja", "ko", "ar", "en"],
                        index=0,
                        key="file_source_lang"
                    )
                
                with col2:
                    target_lang = st.selectbox(
                        "Target language:",
                        ["en", "es", "fr", "de", "it", "pt", "ru", "zh", "ja", "ko", "ar"],
                        index=0,
                        key="file_target_lang"
                    )
                
                # Preview
                if st.checkbox("Show data preview"):
                    st.dataframe(df.head())
                
                # Translate button
                if st.button("Translate File", type="primary", key="translate_file_btn"):
                    with st.spinner("Translating file (this may take a while for large files)..."):
                        try:
                            # Process the file
                            translated_df = translate_dataframe(
                                df,
                                text_column=text_column,
                                source_lang=source_lang,
                                target_lang=target_lang
                            )
                            
                            # Show success message
                            st.success("Translation complete!")
                            
                            # Show sample of translated data
                            st.subheader("Translation Sample")
                            st.dataframe(translated_df[[text_column, f"{text_column}_{target_lang}"]].head())
                            
                            # Download button
                            csv = translated_df.to_csv(index=False).encode('utf-8')
                            st.download_button(
                                label="Download Translated CSV",
                                data=csv,
                                file_name=f"translated_{uploaded_file.name}",
                                mime="text/csv"
                            )
                            
                        except Exception as e:
                            st.error(f"An error occurred during translation: {str(e)}")
            
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")

    # Add some documentation
    with st.expander(" How to use"):
        st.markdown("""
        ### Text Translation
        1. Enter or paste your text in the text area
        2. Select the source and target languages
        3. Click the 'Translate' button
        
        ### File Translation
        1. Upload a CSV file containing the text you want to translate
        2. Select the column that contains the text to translate
        3. Choose the source and target languages
        4. Click 'Translate File' and wait for the process to complete
        5. Download the translated file
        
        ### Notes:
        - For large files, the translation may take some time
        - The translated text will be added as a new column in the CSV
        - The original text will be preserved
        """)

if __name__ == "__main__":
    show_translate()
