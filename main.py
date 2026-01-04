import os
import sys
import re
from openai import OpenAI

def translate_text(text, target_lang, api_key, model_name):
    # OpenRouter 연결 설정
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    # --- [핵심 로직] 코드 블록 보호 시작 ---
    code_blocks = {}
    counter = 0

    # 1. 코드 블록(```...```)을 찾아서 __CODE_BLOCK_N__으로 바꿔치기하는 함수
    def replace_code(match):
        nonlocal counter
        placeholder = f"__CODE_BLOCK_{counter}__"
        code_blocks[placeholder] = match.group(0) # 원래 코드는 딕셔너리에 따로 저장
        counter += 1
        return placeholder

    # 정규식: ```로 감싸진 모든 것(Code Block)을 찾습니다.
    # [\s\S]*? 는 줄바꿈을 포함한 모든 문자를 의미합니다.
    protected_text = re.sub(r'```[\s\S]*?```', replace_code, text)
    
    # --------------------------------------

    # 프롬프트: AI에게 "번역하되, __CODE_BLOCK_N__ 은 절대 건드리지 마라"고 지시
    prompt = f"""
    You are a technical translator. Translate the Markdown content to {target_lang}.
    
    RULES:
    1. Keep the placeholders like __CODE_BLOCK_0__ exactly as they are. Do NOT translate or change them.
    2. Maintain markdown structure (headers, bullets).
    3. Use polite and professional tone.
    
    Content:
    {protected_text}
    """
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        translated_text = response.choices[0].message.content
    except Exception as e:
        print(f"API Error: {e}")
        return text # 에러나면 원본 반환

    # --- [핵심 로직] 코드 블록 복원 ---
    # 번역된 텍스트 안에 있는 __CODE_BLOCK_N__을 다시 원래 코드로 교체
    if translated_text:
        for placeholder, original_code in code_blocks.items():
            translated_text = translated_text.replace(placeholder, original_code)
    
    return translated_text

def main():
    # 깃허브 액션에서 넘겨준 값들 받기
    api_key = sys.argv[1]
    target_langs = sys.argv[2].split(',')
    source_file = sys.argv[3]
    model_name = sys.argv[4]

    if not os.path.exists(source_file):
        print(f"Error: {source_file} not found.")
        sys.exit(1)

    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()

    for lang in target_langs:
        lang = lang.strip()
        print(f"Translating to {lang} using {model_name}...")
        
        # 번역 실행
        result = translate_text(content, lang, api_key, model_name)
        
        # 파일 저장 (예: README.ko.md)
        filename, ext = os.path.splitext(source_file)
        new_filename = f"{filename}.{lang}{ext}"
        
        with open(new_filename, 'w', encoding='utf-8') as f:
            f.write(result)
        
        print(f"Saved: {new_filename}")

if __name__ == "__main__":
    main()
