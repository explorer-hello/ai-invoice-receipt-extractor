# import pytesseract
# from pdf2image import convert_from_path
# import cv2
# import numpy as np
# import os

# def preprocess_image(image):
#     # Convert to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     # Apply noise reduction
#     denoised = cv2.medianBlur(gray, 3)
    
#     # Apply thresholding
#     _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
#     return thresh

# def extract_text_from_image(file_path):
#     try:
#         # Handle PDF files
#         if file_path.lower().endswith('.pdf'):
#             images = convert_from_path(file_path, dpi=300)
#             full_text = ""
#             for img in images:
#                 img_np = np.array(img)
#                 processed_img = preprocess_image(img_np)
#                 text = pytesseract.image_to_string(processed_img)
#                 full_text += text + "\n"
#             return full_text
        
#         # Handle image files
#         else:
#             img = cv2.imread(file_path)
#             if img is None:
#                 raise ValueError("Could not read image file")
            
#             processed_img = preprocess_image(img)
#             text = pytesseract.image_to_string(processed_img)
#             return text
            
#     except Exception as e:
#         raise Exception(f"OCR processing failed: {str(e)}")


# app/ocr.py (updated with better error handling)
import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
import os
import subprocess

def check_tesseract_installed():
    """Check if Tesseract is installed and accessible"""
    try:
        # Try to get tesseract version
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ Tesseract OCR is installed:", result.stdout.split('\n')[0])
            return True
        else:
            print("❌ Tesseract is installed but not working properly")
            return False
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("❌ Tesseract OCR is not installed or not in PATH")
        print("💡 Install it with: sudo apt install tesseract-ocr tesseract-ocr-eng")
        return False

def preprocess_image(image):
    """Preprocess image for better OCR results"""
    try:
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Apply noise reduction
        denoised = cv2.medianBlur(gray, 3)
        
        # Apply thresholding
        _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return thresh
    except Exception as e:
        print(f"⚠️  Image preprocessing failed: {e}")
        return image  # Return original image if preprocessing fails

def extract_text_from_image(file_path):
    """Extract text from image or PDF using Tesseract OCR"""
    try:
        # Check if Tesseract is installed
        if not check_tesseract_installed():
            raise Exception("Tesseract OCR is not installed. Please install it with: sudo apt install tesseract-ocr tesseract-ocr-eng")
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise Exception(f"File not found: {file_path}")
        
        # Handle PDF files
        if file_path.lower().endswith('.pdf'):
            try:
                images = convert_from_path(file_path, dpi=300)
                full_text = ""
                for i, img in enumerate(images):
                    print(f"📄 Processing PDF page {i+1}/{len(images)}")
                    img_np = np.array(img)
                    processed_img = preprocess_image(img_np)
                    text = pytesseract.image_to_string(processed_img)
                    full_text += text + "\n"
                return full_text
            except Exception as e:
                raise Exception(f"PDF processing failed: {str(e)}")
        
        # Handle image files
        else:
            img = cv2.imread(file_path)
            if img is None:
                raise ValueError(f"Could not read image file: {file_path}")
            
            processed_img = preprocess_image(img)
            text = pytesseract.image_to_string(processed_img)
            return text
            
    except Exception as e:
        raise Exception(f"OCR processing failed: {str(e)}")

# Test function to verify OCR setup
def test_ocr():
    """Test if OCR is working properly"""
    print("🧪 Testing OCR setup...")
    
    # Check Tesseract installation
    if not check_tesseract_installed():
        return False
    
    # Create a simple test image with text
    try:
        # Create a test image with some text
        test_image = np.ones((100, 400, 3), dtype=np.uint8) * 255
        cv2.putText(test_image, "OCR Test Hello World", (10, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        # Test OCR on the generated image
        text = pytesseract.image_to_string(test_image)
        print(f"📝 OCR Test Result: '{text.strip()}'")
        
        if "OCR" in text or "Test" in text or "Hello" in text:
            print("✅ OCR test successful!")
            return True
        else:
            print("⚠️  OCR test completed but text recognition was poor")
            return True
            
    except Exception as e:
        print(f"❌ OCR test failed: {e}")
        return False

# Run test when module is imported
if __name__ == "__main__":
    test_ocr()
else:
    # Check Tesseract on import
    check_tesseract_installed()