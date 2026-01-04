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
    
    # --- [핵심 로직 1] 코드 블록 보호 ---
    # 번역기가 코드를 건드리지 못하게 __CODE_BLOCK_N__으로 숨김
    code_blocks = {}
    counter = 0

    def replace_code(match):
        nonlocal counter
        placeholder = f"__CODE_BLOCK_{counter}__"
        code_blocks[placeholder] = match.group(0)
        counter += 1
        return placeholder

    protected_text = re.sub(r'```[\s\S]*?```', replace_code, text)
    # --------------------------------------

    # --- [핵심 로직 2] 프롬프트 강화 ---
    # 1. 언어 코드 매핑 (AI가 'ko'보다 'Korean'을 더 잘 알아듣습니다)
    lang_map = {
        'ko': 'Korean',
        'ja': 'Japanese',
        'zh': 'Simplified Chinese',
        'en': 'English'
    }
    full_lang_name = lang_map.get(target_lang, target_lang)

    # 2. 시스템 프롬프트 (강력한 지시사항: 딴소리 금지, 번역만 해!)
    system_instruction = f"""
    You are a professional technical translator.
    Your task is to translate the Markdown content into **{full_lang_name}**.
    
    CRITICAL RULES:
    1. Translate ONLY the text parts. Do NOT echo the English text.
    2. Keep the placeholders like `__CODE_BLOCK_0__` exactly as they are.
    3. Do NOT add any conversational fillers like "Here is the translation".
    4. Maintain the markdown structure (headers, lists) exactly.
    """

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_instruction}, # 시스템 역할 분리
                {"role": "user", "content": f"Translate this:\n\n{protected_text}"}
            ]
        )
        translated_text = response.choices[0].message.content
    except Exception as e:
        print(f"API Error: {e}")
        return text 

    # --- [핵심 로직 3] 코드 블록 복원 ---
    # 숨겨뒀던 코드를 다시 원래 자리에 끼워넣기
    if translated_text:
        for placeholder, original_code in code_blocks.items():
            translated_text = translated_text.replace(placeholder, original_code)
    
    return translated_text

def main():
    try:
        api_key = sys.argv[1]
        target_langs = sys.argv[2].split(',')
        source_file = sys.argv[3]
        model_name = sys.argv[4]
    except IndexError:
        print("Usage: python main.py <key> <langs> <file> <model>")
        sys.exit(1)

    if not os.path.exists(source_file):
        print(f"Error: {source_file} not found.")
        sys.exit(1)

    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()

    for lang in target_langs:
        lang = lang.strip()
        print(f"Translating to {lang} using {model_name}...")
        
        result = translate_text(content, lang, api_key, model_name)
        
        filename, ext = os.path.splitext(source_file)
        new_filename = f"{filename}.{lang}{ext}"
        
        with open(new_filename, 'w', encoding='utf-8') as f:
            f.write(result)
        
        print(f"Saved: {new_filename}")

if __name__ == "__main__":
    main()
