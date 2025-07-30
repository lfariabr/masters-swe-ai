#!/usr/bin/env python3
"""
TikTok Comments Converter
Converts raw TikTok comments from markdown format to CSV matching clinicTrendsAiSample.csv structure.

Author: Luis Faria
Date: July 30, 2025
Project: ClinicTrends AI - Assessment 3 Demo Data Preparation
"""

import pandas as pd
import re
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import csv
import random

class TikTokCommentsConverter:
    """Converts TikTok raw comments to structured CSV format."""
    
    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file
        self.comments_data = []
        
    def parse_raw_comments(self) -> List[Dict]:
        """Parse raw markdown comments into structured data."""
        print("📖 Reading raw comments file...")
        
        with open(self.input_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Split content into lines for processing
        lines = content.split('\n')
        
        comments = []
        current_comment = {}
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip empty lines and metadata
            if not line or line.isdigit() or 'K' in line and line.replace('K', '').replace('.', '').isdigit():
                i += 1
                continue
                
            # Check for username patterns (not containing common words)
            if self._is_username(line) and i + 1 < len(lines):
                # Look ahead for comment text
                comment_text = ""
                j = i + 1
                
                # Skip metadata lines and find actual comment
                while j < len(lines) and j < i + 10:  # Look within next 10 lines
                    next_line = lines[j].strip()
                    
                    # Skip common metadata patterns
                    if (not next_line or 
                        next_line in ['Reply', 'Follow', 'Post', 'Add comment...', '·', 'Friend'] or
                        'ago' in next_line or
                        next_line.startswith('View ') or
                        next_line == 'avatar' or
                        next_line.isdigit() or
                        'See translation' in next_line):
                        j += 1
                        continue
                    
                    # Found potential comment text
                    if len(next_line) > 10 and not self._is_username(next_line):
                        comment_text = next_line
                        break
                    
                    j += 1
                
                # If we found a valid comment, add it
                if comment_text and len(comment_text) > 5:
                    # Generate synthetic data to match sample format
                    date = self._generate_date()
                    score = self._generate_score_from_sentiment(comment_text)
                    store = self._generate_store()
                    year = 2024  # Current year for TikTok data
                    
                    comment_entry = {
                        'Date': date,
                        'Score': score,
                        'Store': store,
                        'Year': year,
                        'Comment': comment_text
                    }
                    
                    comments.append(comment_entry)
                    print(f"✅ Extracted: {line[:20]}... -> {comment_text[:50]}...")
                
                i = j + 1
            else:
                i += 1
        
        print(f"📊 Total comments extracted: {len(comments)}")
        return comments
    
    def _is_username(self, text: str) -> bool:
        """Determine if a line is likely a username."""
        # Skip common non-username patterns
        skip_patterns = [
            'Reply', 'Follow', 'Post', 'Add comment', 'See translation',
            'Comedy Scenes', 'View', 'ago', 'Friend', 'avatar'
        ]
        
        for pattern in skip_patterns:
            if pattern.lower() in text.lower():
                return False
        
        # Username characteristics
        return (len(text) < 50 and 
                not text.endswith('.') and 
                not text.endswith('?') and
                not text.endswith('!') and
                not any(char in text for char in ['(', ')', '[', ']']) and
                len(text.split()) <= 3)
    
    def _generate_date(self) -> str:
        """Generate a realistic date for the comment."""
        # Generate dates from last 30 days (TikTok viral video timeframe)
        base_date = datetime(2024, 7, 27)  # Approximate viral video date
        days_ago = random.randint(0, 30)
        comment_date = base_date - timedelta(days=days_ago)
        
        # Add random time
        hour = random.randint(8, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        
        comment_datetime = comment_date.replace(hour=hour, minute=minute, second=second)
        return comment_datetime.strftime("%m/%d/%Y %H:%M:%S")
    
    def _generate_score_from_sentiment(self, comment: str) -> int:
        """Generate NPS score based on comment sentiment analysis."""
        comment_lower = comment.lower()
        
        # Positive sentiment indicators
        positive_words = [
            'amo', 'adoro', 'perfeito', 'maravilhoso', 'incrível', 'ótimo', 'bom',
            'feliz', 'alegre', 'divertido', 'engraçado', 'legal', 'top', 'show',
            'love', 'amazing', 'perfect', 'great', 'good', 'happy', 'funny', 'lol'
        ]
        
        # Negative sentiment indicators  
        negative_words = [
            'odeio', 'nojo', 'credo', 'horrível', 'péssimo', 'ruim', 'deselegante',
            'sem graça', 'porcaria', 'hate', 'disgusting', 'terrible', 'bad', 'awful'
        ]
        
        # Neutral/mixed indicators
        neutral_words = [
            'normal', 'ok', 'tanto faz', 'cada um', 'opinião', 'acho que'
        ]
        
        positive_count = sum(1 for word in positive_words if word in comment_lower)
        negative_count = sum(1 for word in negative_words if word in comment_lower)
        neutral_count = sum(1 for word in neutral_words if word in comment_lower)
        
        # Score logic based on sentiment
        if positive_count > negative_count:
            return random.choice([9, 10])  # Promoters
        elif negative_count > positive_count:
            return random.choice([1, 2, 3, 4, 5, 6])  # Detractors
        else:
            return random.choice([7, 8])  # Passives
    
    def _generate_store(self) -> str:
        """Generate a realistic store location."""
        # Brazilian cities/locations to match sample data theme
        locations = [
            'TikTok_SP', 'TikTok_RJ', 'TikTok_BH', 'TikTok_Brasília', 'TikTok_Salvador',
            'TikTok_Fortaleza', 'TikTok_Recife', 'TikTok_Porto_Alegre', 'TikTok_Curitiba',
            'Social_Media_Hub', 'Digital_Platform', 'Online_Community'
        ]
        return random.choice(locations)
    
    def convert_to_csv(self):
        """Main conversion method."""
        print("🚀 Starting TikTok Comments Conversion...")
        print(f"📁 Input: {self.input_file}")
        print(f"📁 Output: {self.output_file}")
        
        # Parse comments
        comments = self.parse_raw_comments()
        
        if not comments:
            print("❌ No comments found to convert!")
            return
        
        # Create DataFrame
        df = pd.DataFrame(comments)
        
        # Sort by date for better organization
        df['Date_parsed'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date_parsed').drop('Date_parsed', axis=1)
        
        # Save to CSV
        df.to_csv(self.output_file, index=False, encoding='utf-8', quoting=csv.QUOTE_ALL)
        
        print(f"✅ Conversion completed!")
        print(f"📊 Total records: {len(df)}")
        print(f"📈 Score distribution:")
        print(df['Score'].value_counts().sort_index())
        print(f"🏪 Store distribution:")
        print(df['Store'].value_counts().head())
        
        # Display sample
        print(f"\n📋 Sample records:")
        print(df.head().to_string(index=False))

def main():
    """Main execution function."""
    input_file = "/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/T1-Software-Engineering-Principles/projects/clinictrends_ai/docs/tiktok1m/rawComments.md"
    output_file = "/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/T1-Software-Engineering-Principles/projects/clinictrends_ai/docs/tiktok1m/tiktok_comments_processed.csv"
    
    converter = TikTokCommentsConverter(input_file, output_file)
    converter.convert_to_csv()

if __name__ == "__main__":
    main()
