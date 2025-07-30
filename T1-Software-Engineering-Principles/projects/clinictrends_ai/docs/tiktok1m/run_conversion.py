#!/usr/bin/env python3
"""
Test runner for TikTok Comments Conversion
Executes the conversion script and provides feedback.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from convert_tiktok_comments import TikTokCommentsConverter
    
    print("🚀 Starting TikTok Comments Conversion Test...")
    
    # File paths
    input_file = "/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/T1-Software-Engineering-Principles/projects/clinictrends_ai/docs/tiktok1m/rawComments.md"
    output_file = "/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/T1-Software-Engineering-Principles/projects/clinictrends_ai/docs/tiktok1m/tiktok_comments_processed.csv"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Input file not found: {input_file}")
        sys.exit(1)
    
    print(f"✅ Input file found: {input_file}")
    print(f"📁 Output will be saved to: {output_file}")
    
    # Create converter and run
    converter = TikTokCommentsConverter(input_file, output_file)
    converter.convert_to_csv()
    
    # Verify output
    if os.path.exists(output_file):
        file_size = os.path.getsize(output_file)
        print(f"✅ Conversion successful!")
        print(f"📊 Output file size: {file_size:,} bytes")
        
        # Read first few lines to verify format
        with open(output_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:6]  # Header + 5 sample rows
            
        print(f"\n📋 Sample output (first 5 rows):")
        for line in lines:
            print(line.strip())
            
    else:
        print("❌ Output file was not created!")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error during conversion: {e}")
    import traceback
    traceback.print_exc()
