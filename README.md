# AI Invoice & Receipt Extractor

=======
A Python-based application that extracts structured data from invoices and receipts using OCR and NLP.

## Features

- Upload PDF/JPEG/PNG invoices and receipts
- Extract text using Tesseract OCR
- Parse structured data (vendor, date, amount, etc.) using spaCy NLP
- Categorize expenses automatically
- Store data in MySQL database
- Dashboard for viewing and analytics

## Setup Instructions

1. **Install dependencies**:
pip install -r requirements.txt
python -m spacy download en_core_web_sm


2. **Setup MySQL database**:
- Install MySQL on your system
- Create a database named `invoice_extractor`
- Update the database credentials in `.env` file

3. **Configure environment variables**:
Create a `.env` file in the root directory:
