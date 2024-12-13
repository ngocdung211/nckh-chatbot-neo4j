import os
from docx import Document
import pypandoc
import pdfplumber
import re

class DocumentConverter:
    def __init__(self):
        os.makedirs('output', exist_ok=True)
    
    def docx_to_markdown(self, input_path):
        """Chuyển đổi file DOCX sang Markdown."""
        try:
            output_path = os.path.join('output', os.path.splitext(os.path.basename(input_path))[0] + '.md')
            pypandoc.convert_file(
                input_path,
                'markdown',
                outputfile=output_path,
                format='docx'
            )
            print(f"Đã chuyển đổi thành công: {output_path}")
            return output_path
        except Exception as e:
            print(f"Lỗi khi chuyển đổi file DOCX: {str(e)}")
            return None

    def pdf_to_markdown(self, input_path):
        """Chuyển đổi file PDF sang Markdown."""
        try:
            output_path = os.path.join('output', os.path.splitext(os.path.basename(input_path))[0] + '.md')
            markdown_content = []
            
            with pdfplumber.open(input_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        paragraphs = text.split('\n\n')
                        for para in paragraphs:
                            if re.match(r'^[A-Z\d\s]{10,}$', para.strip()):
                                markdown_content.append(f"# {para.strip()}\n")
                            else:
                                markdown_content.append(f"{para.strip()}\n\n")
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(''.join(markdown_content))
            
            print(f"Đã chuyển đổi thành công: {output_path}")
            return output_path
        except Exception as e:
            print(f"Lỗi khi chuyển đổi file PDF: {str(e)}")
            return None

    def convert_document(self, input_path):
        """Chuyển đổi tài liệu dựa vào phần mở rộng của file."""
        if not os.path.exists(input_path):
            print(f"Không tìm thấy file: {input_path}")
            return None
        
        file_extension = os.path.splitext(input_path)[1].lower()
        
        if file_extension == '.docx':
            return self.docx_to_markdown(input_path)
        elif file_extension == '.pdf':
            return self.pdf_to_markdown(input_path)
        else:
            print(f"Định dạng file không được hỗ trợ: {file_extension}")
            return None