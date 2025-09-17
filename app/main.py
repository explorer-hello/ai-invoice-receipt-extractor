# Add these lines at the VERY TOP of app/main.py
import sys
import os
# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from datetime import datetime
import shutil
from app.ocr import extract_text_from_image
from app.nlp import extract_invoice_data
from app.categorization import categorize_expense
from app.database import save_invoice_data

app = FastAPI(title="Invoice Extractor API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-invoice/")
async def upload_invoice(file: UploadFile = File(...)):
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf')):
            raise HTTPException(400, "Invalid file type. Please upload PNG, JPG, or PDF.")
        
        # Save uploaded file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process the file
        extracted_text = extract_text_from_image(file_path)
        invoice_data = extract_invoice_data(extracted_text)
        invoice_data['category'] = categorize_expense(invoice_data)
        
        # Save to database
        invoice_id = save_invoice_data(invoice_data, filename)
        invoice_data['id'] = invoice_id
        
        return {
            "message": "File processed successfully",
            "data": invoice_data
        }
        
    except Exception as e:
        raise HTTPException(500, f"Error processing file: {str(e)}")

@app.get("/invoices/")
async def get_invoices(limit: int = 50, offset: int = 0):
    from app.database import get_invoices
    return get_invoices(limit, offset)

@app.get("/invoices/{invoice_id}")
async def get_invoice(invoice_id: int):
    from app.database import get_invoice_by_id
    invoice = get_invoice_by_id(invoice_id)
    if not invoice:
        raise HTTPException(404, "Invoice not found")
    return invoice

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)