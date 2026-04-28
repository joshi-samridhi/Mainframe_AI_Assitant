"""
OCR processor for extracting text from mainframe log images
"""
import os
from typing import Optional, Tuple
from PIL import Image
import pytesseract


class OCRProcessor:
    """Process images to extract text using Tesseract OCR"""
    
    def __init__(self, tesseract_path: Optional[str] = None):
        """
        Initialize OCR processor
        
        Args:
            tesseract_path: Path to tesseract executable
        """
        if tesseract_path and os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        self.supported_formats = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif'}
    
    def is_supported_format(self, filename: str) -> bool:
        """
        Check if file format is supported
        
        Args:
            filename: Name of the file
            
        Returns:
            True if format is supported
        """
        ext = os.path.splitext(filename)[1].lower()
        return ext in self.supported_formats
    
    def extract_text(self, image_path: str) -> Tuple[str, bool]:
        """
        Extract text from image using OCR
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Tuple of (extracted_text, success)
        """
        try:
            # Validate file exists
            if not os.path.exists(image_path):
                return f"Error: Image file not found: {image_path}", False
            
            # Validate format
            if not self.is_supported_format(image_path):
                return f"Error: Unsupported image format", False
            
            # Open and preprocess image
            image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Perform OCR with custom config for terminal text
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(image, config=custom_config)
            
            # Clean up extracted text
            text = self._clean_text(text)
            
            if not text or len(text.strip()) < 10:
                return "Error: Could not extract meaningful text from image", False
            
            return text, True
            
        except pytesseract.TesseractNotFoundError:
            return "Error: Tesseract OCR is not installed or not found in PATH", False
        except Exception as e:
            return f"Error during OCR processing: {str(e)}", False
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize extracted text
        
        Args:
            text: Raw OCR text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        lines = [line.strip() for line in text.split('\n')]
        
        # Remove empty lines
        lines = [line for line in lines if line]
        
        # Join with newlines
        cleaned = '\n'.join(lines)
        
        return cleaned
    
    def preprocess_image(self, image_path: str, output_path: str) -> bool:
        """
        Preprocess image to improve OCR accuracy
        
        Args:
            image_path: Path to input image
            output_path: Path to save preprocessed image
            
        Returns:
            True if successful
        """
        try:
            image = Image.open(image_path)
            
            # Convert to grayscale
            image = image.convert('L')
            
            # Increase contrast (simple threshold)
            # This works well for terminal screenshots with green text on black
            threshold = 100
            image = image.point(lambda x: 255 if x > threshold else 0)
            
            # Save preprocessed image
            image.save(output_path)
            
            return True
            
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return False
    
    def extract_with_preprocessing(self, image_path: str) -> Tuple[str, bool]:
        """
        Extract text with automatic preprocessing
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Tuple of (extracted_text, success)
        """
        # Try normal extraction first
        text, success = self.extract_text(image_path)
        
        if success and len(text.strip()) > 50:
            return text, True
        
        # If failed or poor results, try with preprocessing
        try:
            preprocessed_path = image_path.replace('.', '_preprocessed.')
            if self.preprocess_image(image_path, preprocessed_path):
                text, success = self.extract_text(preprocessed_path)
                
                # Clean up preprocessed file
                if os.path.exists(preprocessed_path):
                    os.remove(preprocessed_path)
                
                return text, success
        except Exception as e:
            print(f"Preprocessing failed: {e}")
        
        return text, success
    
    def validate_ocr_output(self, text: str) -> bool:
        """
        Validate OCR output quality
        
        Args:
            text: Extracted text
            
        Returns:
            True if output seems valid
        """
        if not text or len(text.strip()) < 10:
            return False
        
        # Check for common mainframe keywords
        keywords = ['JOB', 'STEP', 'ERROR', 'ABEND', 'RETURN', 'CODE', 'STATUS']
        found_keywords = sum(1 for keyword in keywords if keyword in text.upper())
        
        return found_keywords >= 2


# Example usage and testing
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        
        processor = OCRProcessor()
        print(f"Processing image: {image_path}")
        print("=" * 50)
        
        text, success = processor.extract_with_preprocessing(image_path)
        
        if success:
            print("Extracted Text:")
            print("-" * 50)
            print(text)
            print("-" * 50)
            print(f"Valid: {processor.validate_ocr_output(text)}")
        else:
            print(f"Failed: {text}")
    else:
        print("Usage: python ocr_processor.py <image_path>")

# Made with Bob
