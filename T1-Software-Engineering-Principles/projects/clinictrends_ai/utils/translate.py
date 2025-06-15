import pandas as pd
from deep_translator import GoogleTranslator
import time
from typing import List, Optional

def translate_text(text: str, source_lang: str = 'pt', target_lang: str = 'en', max_retries: int = 3) -> str:
    """
    Translate text from source language to target language with retry logic.
    
    Args:
        text: The text to translate
        source_lang: Source language code (default: 'pt' for Portuguese)
        target_lang: Target language code (default: 'en' for English)
        max_retries: Maximum number of retry attempts
        
    Returns:
        Translated text
    """
    for attempt in range(max_retries):
        try:
            return GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        except Exception as e:
            if attempt == max_retries - 1:  # Last attempt
                print(f"Failed to translate after {max_retries} attempts")
                return text  # Return original text if all retries fail
            time.sleep(2 ** attempt)  # Exponential backoff

def translate_dataframe(df: pd.DataFrame, 
                      text_column: str = 'Comment', 
                      source_lang: str = 'pt',
                      target_lang: str = 'en') -> pd.DataFrame:
    """
    Translate text column in a pandas DataFrame.
    
    Args:
        df: Input DataFrame
        text_column: Name of the column containing text to translate
        source_lang: Source language code
        target_lang: Target language code
        
    Returns:
        DataFrame with an additional column containing translated text
    """
    if df.empty or text_column not in df.columns:
        return df
        
    # Clean the text column
    df = df[df[text_column].notnull() & (df[text_column].astype(str).str.strip() != '')]
    
    # Create a copy to avoid SettingWithCopyWarning
    df = df.copy()
    
    # Add translated column
    output_column = f"{text_column}_{target_lang}"
    df[output_column] = df[text_column].apply(
        lambda x: translate_text(str(x), source_lang, target_lang)
    )
    
    return df

def main():
    """Command-line interface for the translation utility."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Translate text in a CSV file.')
    parser.add_argument('input_file', help='Input CSV file path')
    parser.add_argument('--output', '-o', default='output_translated.csv',
                       help='Output CSV file path (default: output_translated.csv)')
    parser.add_argument('--source', '-s', default='pt',
                       help='Source language code (default: pt)')
    parser.add_argument('--target', '-t', default='en',
                       help='Target language code (default: en)')
    parser.add_argument('--column', '-c', default='Comment',
                       help='Column name containing text to translate (default: Comment)')
    
    args = parser.parse_args()
    
    try:
        df = pd.read_csv(args.input_file)
        translated_df = translate_dataframe(
            df, 
            text_column=args.column,
            source_lang=args.source,
            target_lang=args.target
        )
        translated_df.to_csv(args.output, index=False)
        print(f"Translation complete. Results saved to {args.output}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()