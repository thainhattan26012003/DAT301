import os
import google.generativeai as genai
from pydantic import BaseModel
from service_config import QDRANT_COLLECTION, vectordb_provider
from vector_db import embed
from dotenv import load_dotenv
load_dotenv()

class ChatRequest(BaseModel):
    question: str

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def generate_answer_from_gemini(query: str, context: str) -> str:
    prompt = f"""
    Bạn là một bác sĩ giỏi với kiến thức chuyên môn sau
    Dựa vào bệnh đã được phân loại ở {context}, hãy trả lời cho bệnh nhân biết về tình trạng của mình.

    Quy tắc khi trả lời:
    1. Chỉ sử dụng thông tin trong phần "Ngữ cảnh".
    2. Trả lời không vượt quá 500 từ.
    3. Nếu thông tin không có trong ngữ cảnh, trả lời: "Tôi không rõ thông tin này."
    4. Luôn trình bày câu trả lời bằng tiếng Việt rõ ràng, dễ hiểu.
    5. Nếu câu trả lời có từ 2 ý trở lên, BẮT BUỘC phải xuống dòng và dùng dấu gạch đầu dòng (-) ở đầu mỗi ý để liệt kê giống như mẫu ở ví dụ phía dưới.

    Câu trả lời của bạn (tuân thủ đúng cấu trúc gạch đầu dòng nếu có nhiều ý):
    """
    
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content(prompt)

    return response.text.strip() if response.text else "Không tạo được câu trả lời hợp lệ."

def rag_flow(question: str, diagnosis: str) -> str:

    try:
        answer = generate_answer_from_gemini(question, diagnosis)
        return answer
    except Exception as e:
        return f"Error during answer generation: {str(e)}"
