"""
Document OCR: AI-powered document reading and data extraction
Implements OCR capabilities for automated data capture from documents
"""

import cv2
import numpy as np
import pytesseract
from PIL import Image
import io
import json
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import re
import tempfile
import os
from pathlib import Path

from sqlalchemy.orm import Session
from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.sql import func
import uuid

from app.core.database import Base
from app.models.invoice import ComprobanteFiscal


@dataclass
class OCRResult:
    """Result of OCR processing"""
    text: str
    confidence: float
    extracted_data: Dict[str, Any]
    processing_time: float
    document_type: str


@dataclass
class ExtractedField:
    """Represents an extracted field from a document"""
    name: str
    value: str
    confidence: float
    bbox: Tuple[int, int, int, int]  # x, y, width, height


class DocumentOCR(Base):
    """Stored OCR results"""
    __tablename__ = "ai_document_ocr"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Document info
    nombre_archivo = Column(String(255), nullable=False)
    tipo_documento = Column(String(100))  # factura, recibo, cotizacion, etc.
    ruta_archivo = Column(String(500))  # Path to the uploaded file
    
    # Processing results
    texto_extraido = Column(Text)
    datos_extraidos = Column(Text)  # JSON with structured data
    confianza_promedio = Column(String(10))  # Average confidence percentage
    
    # Related entities
    comprobante_relacionado_id = Column(PostgresUUID(as_uuid=True), ForeignKey("inv_comprobante_fiscal.id"))
    
    # Metadata
    fecha_procesamiento = Column(DateTime(timezone=True), server_default=func.now())
    usuario_id = Column(PostgresUUID(as_uuid=True))  # User who initiated the processing
    
    # Relationships
    comprobante_relacionado = relationship("ComprobanteFiscal")


class DocumentOCRProcessor:
    """
    Processor for OCR and document data extraction
    """
    
    def __init__(self):
        # Set tesseract path if needed (for Windows)
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pass
    
    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """
        Preprocess image for better OCR results
        :param image: Input PIL Image
        :return: Preprocessed OpenCV image
        """
        # Convert PIL to OpenCV format
        opencv_image = np.array(image)
        
        # Convert RGB to BGR (OpenCV uses BGR)
        if len(opencv_image.shape) == 3:
            opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2BGR)
        
        # Convert to grayscale
        gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold to get image with only black and white
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Apply morphological operations to remove noise
        kernel = np.ones((1, 1), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        
        # Apply median blur to smooth image
        blur = cv2.medianBlur(opening, 3)
        
        return blur
    
    def extract_text_with_confidence(self, image: Image.Image) -> Tuple[str, float]:
        """
        Extract text from image with confidence scoring
        :param image: Input PIL Image
        :return: Tuple of (extracted_text, average_confidence)
        """
        preprocessed = self.preprocess_image(image)
        
        # Get detailed output including boxes and confidence
        data = pytesseract.image_to_data(preprocessed, output_type=pytesseract.Output.DICT)
        
        # Calculate average confidence excluding zero values
        confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        # Extract text
        text = pytesseract.image_to_string(preprocessed)
        
        return text.strip(), avg_confidence / 100  # Normalize confidence to 0-1 scale
    
    def detect_document_type(self, text: str) -> str:
        """
        Detect the type of document based on its content
        :param text: Extracted text from document
        :return: Document type
        """
        text_lower = text.lower()
        
        # Define keywords for different document types
        document_keywords = {
            'factura': ['factura', 'rfc', 'regimen fiscal', 'subtotal', 'iva', 'total'],
            'recibo': ['recibo', 'cobro', 'importe', 'recibí', 'cantidad'],
            'cotizacion': ['cotización', 'presupuesto', 'precio', 'producto', 'cantidad'],
            'pedido': ['pedido', 'orden de compra', 'solicito', 'requiero'],
            'remision': ['remisión', 'albarán', 'entrega', 'despacho'],
            'contrato': ['contrato', 'cláusula', 'partes contratantes', 'objeto del contrato'],
            'recibo_nomina': ['nómina', 'percepciones', 'deducciones', 'sueldo', 'agux', 'vacaciones']
        }
        
        scores = {}
        for doc_type, keywords in document_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[doc_type] = score
        
        # Return the document type with highest score, or 'otro' if no matches
        return max(scores, key=scores.get) if max(scores.values()) > 0 else 'otro'
    
    def extract_structured_data(self, text: str, document_type: str) -> Dict[str, Any]:
        """
        Extract structured data from document text based on type
        :param text: Extracted text from document
        :param document_type: Type of document
        :return: Dictionary with structured data
        """
        # Define regex patterns for common fields
        patterns = {
            'rfc': r'[A-Z&Ñ]{3,4}\d{6}[A-Z0-9]{3}',
            'total': r'(?:TOTAL|total)[^\d]*([\d,]+\.?\d*)',
            'subtotal': r'(?:SUBTOTAL|subtotal)[^\d]*([\d,]+\.?\d*)',
            'iva|iva_tasa': r'(?:IVA|iva)[^\d]*([\d,]+\.?\d*)%',
            'fecha': r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b',
            'folio': r'(?:FOLIO|folio|no\.?)[^\w\d]*([A-Z0-9]+[-]?[A-Z0-9]*)',
            'serie': r'(?:SERIE|serie)[^\w\d]*([A-Z0-9]+)',
            'monto': r'\$?[\d,]+\.?\d*',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'telefono': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'direccion': r'\bCalle|Av\.?|Avenida\b[^,]*,\s*\w+',
        }
        
        extracted_data = {}
        
        # Apply patterns based on document type
        for field, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Take the most relevant match (usually the first or most complete)
                if field in ['total', 'subtotal', 'iva', 'monto']:
                    # Extract only numeric values
                    numeric_values = []
                    for match in matches:
                        # Clean the value and convert to float
                        cleaned = re.sub(r'[^\d.]', '', str(match))
                        if cleaned:
                            try:
                                numeric_values.append(float(cleaned))
                            except ValueError:
                                continue
                    if numeric_values:
                        extracted_data[field] = max(numeric_values)  # Take the largest value
                elif field == 'fecha':
                    # Parse the date
                    for match in matches:
                        try:
                            # Try different date formats
                            for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%m/%d/%Y", "%Y/%m/%d"):
                                try:
                                    parsed_date = datetime.strptime(match, fmt)
                                    extracted_data[field] = parsed_date.strftime('%Y-%m-%d')
                                    break
                                except ValueError:
                                    continue
                        except:
                            continue
                else:
                    extracted_data[field] = matches[0] if len(matches) == 1 else matches
        
        # Additional processing based on document type
        if document_type == 'factura':
            # Process invoice-specific fields
            self._process_invoice_fields(text, extracted_data)
        elif document_type == 'recibo_nomina':
            # Process payroll-specific fields
            self._process_payroll_fields(text, extracted_data)
        
        return extracted_data
    
    def _process_invoice_fields(self, text: str, data: Dict[str, Any]):
        """Process invoice-specific fields"""
        # Extract concepts/line items
        concept_pattern = r'(\d+)\s+(.+?)\s+(\$\d+\.?\d*)'
        concepts = re.findall(concept_pattern, text)
        if concepts:
            data['conceptos'] = []
            for qty, desc, price in concepts:
                data['conceptos'].append({
                    'cantidad': int(qty),
                    'descripcion': desc.strip(),
                    'precio_unitario': float(price.replace('$', ''))
                })
    
    def _process_payroll_fields(self, text: str, data: Dict[str, Any]):
        """Process payroll-specific fields"""
        # Extract payroll details
        percepciones_match = re.search(r'PERCEPCIONES[^\n\r]*\$?([\d,]+\.?\d*)', text, re.IGNORECASE)
        if percepciones_match:
            data['percepciones_total'] = float(re.sub(r'[^\d.]', '', percepciones_match.group(1)))
        
        deducciones_match = re.search(r'DEDUCCIONES[^\n\r]*\$?([\d,]+\.?\d*)', text, re.IGNORECASE)
        if deducciones_match:
            data['deducciones_total'] = float(re.sub(r'[^\d.]', '', deducciones_match.group(1)))
    
    def process_document(self, image: Image.Image) -> OCRResult:
        """
        Process a document image and extract data
        :param image: Input PIL Image
        :return: OCRResult object with extracted data
        """
        import time
        
        start_time = time.time()
        
        # Extract text and confidence
        text, confidence = self.extract_text_with_confidence(image)
        
        # Detect document type
        doc_type = self.detect_document_type(text)
        
        # Extract structured data
        structured_data = self.extract_structured_data(text, doc_type)
        
        processing_time = time.time() - start_time
        
        return OCRResult(
            text=text,
            confidence=confidence,
            extracted_data=structured_data,
            processing_time=processing_time,
            document_type=doc_type
        )
    
    def save_ocr_result(self, db: Session, result: OCRResult, filename: str, user_id: Optional[str] = None) -> DocumentOCR:
        """
        Save OCR result to database
        :param db: Database session
        :param result: OCRResult object
        :param filename: Original filename
        :param user_id: ID of user who initiated processing
        :return: Saved DocumentOCR object
        """
        import json
        
        ocr_record = DocumentOCR(
            nombre_archivo=filename,
            tipo_documento=result.document_type,
            texto_extraido=result.text,
            datos_extraidos=json.dumps(result.extracted_data, default=str),
            confianza_promedio=f"{result.confidence:.2f}",
            usuario_id=user_id
        )
        
        db.add(ocr_record)
        db.commit()
        db.refresh(ocr_record)
        
        return ocr_record
    
    def process_document_from_file(self, file_path: str) -> OCRResult:
        """
        Process a document from file path
        :param file_path: Path to the document file
        :return: OCRResult object with extracted data
        """
        # Open and process the image
        with Image.open(file_path) as img:
            return self.process_document(img)
    
    def process_document_from_bytes(self, file_bytes: bytes) -> OCRResult:
        """
        Process a document from bytes data
        :param file_bytes: Bytes of the document
        :return: OCRResult object with extracted data
        """
        # Create PIL image from bytes
        image = Image.open(io.BytesIO(file_bytes))
        return self.process_document(image)


# Global instance
ocr_processor = DocumentOCRProcessor()