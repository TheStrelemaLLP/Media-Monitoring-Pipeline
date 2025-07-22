import os
import sys
import logging

# Add parent directory to path for local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from docx import Document
from docx.enum.style import WD_STYLE_TYPE

from utils import setup_logger

logger = setup_logger("FacebookDocs")

class FacebookDocsError(Exception):
    """Base exception for FacebookDocs errors."""
    pass

class Facebook_doc:
    def create_facebook_doc(self, excel_file_path: str, output_dir: str, leader: str) -> str:
        """Convert Excel file with Facebook posts to a formatted Word document."""
        logger.info(f"Processing Facebook posts from {excel_file_path}")
        
        # Validate input file
        if not os.path.exists(excel_file_path):
            logger.error(f"Input file '{excel_file_path}' does not exist.")
            raise FacebookDocsError(f"Input file '{excel_file_path}' does not exist.")
        
        try:
            # Read the Excel file
            df = pd.read_excel(excel_file_path)
            logger.debug(f"Loaded Excel file with {len(df)} rows.")
            
            # Check for required columns
            required_columns = ['text']
            if not all(col in df.columns for col in required_columns):
                missing_cols = [col for col in required_columns if col not in df.columns]
                logger.error(f"Missing required columns: {', '.join(missing_cols)}")
                raise FacebookDocsError(f"Missing required columns: {', '.join(missing_cols)}")
            
            # Remove rows with null values in 'text' column
            initial_rows = len(df)
            df = df.dropna(subset=['text']).reset_index(drop=True)
            logger.debug(f"Removed {initial_rows - len(df)} rows with null 'text' values.")
            
            # Initialize Word document
            doc = Document()
            
            # Ensure Heading 3 style exists
            try:
                doc.styles['Heading 3']
            except KeyError:
                logger.error("Style 'Heading 3' not found in document.")
                raise FacebookDocsError("Style 'Heading 3' not found in document.")
            
            # Format each row and add to the Word document
            for index, row in df.iterrows():
                article_number = index + 1
                # Add heading
                heading_text = f"Facebook Post {article_number}"
                doc.add_heading(heading_text, level=3)
                
                # Add URL
                # doc.add_paragraph(row['url'])
                
                # Add content
                content_text = f"Content:\n{leader} posted:\n\"{row['text']}\""
                doc.add_paragraph(content_text)
                
                # Add blank paragraph for spacing
                doc.add_paragraph()
            
            # Generate output filename
            output_filename = f"{leader}_fb_output.docx"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, output_filename)
            
            # Save the document
            doc.save(output_path)
            logger.info(f"Formatted Word document saved as {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Failed to process Facebook posts: {str(e)}")
            raise FacebookDocsError(f"Failed to process Facebook posts: {str(e)}")