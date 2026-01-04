import os
import sys
from openai import OpenAI

def translate_text(text, target_lang, api_key):
    client = OpenAI(api_key=api_key)
    
    # 여기에 사용자님의 노하우(프롬프트 엔지니어링)가 들어갑니다.
    prompt = f"""
    You are a professional technical translator for developers.
    Translate the following Markdown content into {target_lang}.
    
    RULES:
    1. Do NOT translate variable names, function names, or code blocks.
    2. Maintain the original Markdown structure strictly.
    3. Use professional developer terminology (e.g., 'Commit' -> '커밋', not '약속').
    
    Content:
    {text}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini", # 가성비 모델
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def main():
    # action.yml에서 넘겨준 값 받기
    api_key = sys.argv[1]
    target_langs = sys.argv[2].split(',')
    source_file = sys.argv[3]

    # 1. 원본 파일 읽기
    if not os.path.exists(source_file):
        print(f"Error: {source_file} not found.")
        sys.exit(1)

    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 2. 언어별로 번역해서 저장
    for lang in target_langs:
        lang = lang.strip()
        print(f"Translating to {lang}...")
        
        translated_content = translate_text(content, lang, api_key)
        
        # 파일명 생성 (예: README.ko.md)
        filename, ext = os.path.splitext(source_file)
        new_filename = f"{filename}.{lang}{ext}"
        
        with open(new_filename, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        
        print(f"Saved: {new_filename}")

if __name__ == "__main__":
    main()
