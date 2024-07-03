from service.pdf_processing_service import process_pdf

def main_workflow():
    
    pdf_path = "C:/Users/heung/Downloads/Chabot_innocean data ex - news.pdf"
    process_pdf(pdf_path)
    
if __name__ == "__main__":
    main_workflow()