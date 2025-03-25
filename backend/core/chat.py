import openai
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

class ChatRequest(BaseModel):
    question: str

def generate_answer_from_llm(query: str, diagnosis_context: str) -> str:
    prompt = f""" 
Bạn cần trả lời câu hỏi dựa trên kết quả chẩn đoán từ ảnh đã cho.
    
**Kết quả chẩn đoán:** {diagnosis_context}

**Câu hỏi:** {query}

**Yêu cầu:**
- Trả lời bằng tiếng Việt, rõ ràng và súc tích.
- Nếu có nhiều ý, hãy liệt kê bằng dấu "-" ở đầu dòng.

**Câu trả lời:**
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Bạn là một trợ lý AI chuyên tư vấn về sức khỏe dựa trên kết quả chẩn đoán từ ảnh."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    return response["choices"][0]["message"]["content"].strip() if response["choices"] else "No valid answer generated."

async def rag_flow(question: str, diagnosis: str) -> str:
    try:
        answer = generate_answer_from_llm(question, diagnosis)
        return answer if answer else "No valid answer generated."
    except Exception as e:
        return f"Error during answer generation: {str(e)}"
