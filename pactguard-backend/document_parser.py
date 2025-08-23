"""
Document parser utility for extracting text from various file formats
"""

import io
from typing import Optional, Union
from pathlib import Path
import PyPDF2
from docx import Document
from fastapi import UploadFile

class DocumentParser:
    """Parse different document formats and extract text content"""
    
    @staticmethod
    async def extract_text_from_upload(file: UploadFile) -> str:
        """Extract text from uploaded file based on its type"""
        content = await file.read()
        file_extension = Path(file.filename or "").suffix.lower()
        
        if file_extension == '.pdf':
            return DocumentParser.extract_from_pdf(content)
        elif file_extension in ['.doc', '.docx']:
            return DocumentParser.extract_from_docx(content)
        elif file_extension == '.txt':
            return content.decode('utf-8')
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    @staticmethod
    def extract_from_pdf(content: bytes) -> str:
        """Extract text from PDF bytes"""
        try:
            pdf_file = io.BytesIO(content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            raise ValueError(f"Failed to parse PDF: {str(e)}")
    
    @staticmethod
    def extract_from_docx(content: bytes) -> str:
        """Extract text from DOCX bytes"""
        try:
            doc_file = io.BytesIO(content)
            doc = Document(doc_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
        except Exception as e:
            raise ValueError(f"Failed to parse DOCX: {str(e)}")
    
    @staticmethod
    def validate_file(file: UploadFile) -> bool:
        """Validate file type and size"""
        if not file.filename:
            return False
            
        # Check file extension
        allowed_extensions = {'.pdf', '.doc', '.docx', '.txt'}
        file_extension = Path(file.filename).suffix.lower()
        
        if file_extension not in allowed_extensions:
            return False
        
        # Check file size (limit to 10MB)
        if file.size and file.size > 10 * 1024 * 1024:  # 10MB
            return False
            
        return True
