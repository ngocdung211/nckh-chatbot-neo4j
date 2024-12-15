from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict
import re
import json

class ChunkingDocument:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        # Định nghĩa các separators theo thứ tự ưu tiên
        self.separators = [
            # Headers
            "\n# ",
            "\n## ",
            "\n### ",
            "\n#### ",
            "\n##### ",
            "\n###### ",
            # Các dấu hiệu kết thúc đoạn
            "\n\n",
            "\n",
            ". ",  # Kết thúc câu
            "! ",
            "? ",
            # Dấu phân cách trong câu
            ": ",
            "; ",
            ", ",
            " ",  # Cuối cùng là khoảng trắng
            ""    # Fallback nếu không có separator nào khác
        ]

        # Khởi tạo text splitter với các tham số tối ưu
        self.text_splitter = RecursiveCharacterTextSplitter(
            separators=self.separators,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            keep_separator=True,
            strip_whitespace=True,
            add_start_index=True,
        )

    def _extract_metadata(self, text: str, start_idx: int) -> Dict:
        """Trích xuất metadata từ chunk text."""
        # Tìm heading gần nhất phía trước
        headers = re.finditer(r'^(#{1,6})\s+(.+)$', text, re.MULTILINE)
        current_headers = []

        for match in headers:
            level = len(match.group(1))
            title = match.group(2).strip()
            # Cập nhật headers tại level hiện tại
            while len(current_headers) >= level:
                current_headers.pop()
            current_headers.append(title)

        # Kiểm tra các thành phần đặc biệt
        metadata = {
            "start_index": start_idx,
            "headers": current_headers,
            "has_code": bool(re.search(r'```[\s\S]*?```', text)),
            "has_list": bool(re.search(r'^\s*[-*+]\s', text, re.MULTILINE)),
            "has_table": bool(re.search(r'\|.*\|', text)),
            "has_blockquote": bool(re.search(r'^\s*>', text, re.MULTILINE)),
        }

        return metadata

    def _clean_chunk(self, text: str) -> str:
        """Làm sạch và chuẩn hóa chunk text."""
        text = re.sub(r'\s+', ' ', text).strip()

        code_blocks = re.finditer(r'```[\s\S]*?```', text)
        for block in code_blocks:
            if block.group().count('```') % 2 != 0:
                text = text[:block.start()]

        if text.count('`') % 2 != 0:
            last_backtick = text.rfind('`')
            if last_backtick != -1:
                text = text[:last_backtick]

        return text.strip()

    def chunk_markdown(self, text: str) -> List[Dict]:
        """Chia văn bản markdown thành các chunks với metadata."""
        chunks = self.text_splitter.create_documents([text])

        processed_chunks = []
        for i, chunk in enumerate(chunks):
            content = self._clean_chunk(chunk.page_content)
            if not content:
                continue

            start_idx = chunk.metadata.get('start_index', 0)

            metadata = self._extract_metadata(content, start_idx)

            processed_chunk = {
                "id": f"chunk_{i+1}",
                "content": content,
                "metadata": {
                    **metadata,
                    "char_count": len(content),
                    "word_count": len(content.split()),
                    "prev_chunk": f"chunk_{i}" if i > 0 else None,
                    "next_chunk": f"chunk_{i+2}" if i < len(chunks)-1 else None
                }
            }
            processed_chunks.append(processed_chunk)

        return processed_chunks

    def process_file(self, file_path: str) -> List[Dict]:
        """Xử lý file markdown."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.chunk_markdown(content)
        except Exception as e:
            print(f"Lỗi khi xử lý file {file_path}: {str(e)}")
            return []

    def save_chunks(self, chunks: List[Dict], output_file: str):
        """Lưu chunks vào file JSON."""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(chunks, f, ensure_ascii=False, indent=2)
            print(f"Đã lưu {len(chunks)} chunks vào {output_file}")
        except Exception as e:
            print(f"Lỗi khi lưu file: {str(e)}")

def process_markdown_document(
    file_path: str,
    output_path: str = None,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> List[Dict]:
    chunker = ChunkingDocument(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunks = chunker.process_file(file_path)

    if output_path:
        chunker.save_chunks(chunks, output_path)

    return chunks