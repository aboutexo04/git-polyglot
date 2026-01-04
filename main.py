import os
import sys
from openai import OpenAI

def translate_text(text, target_lang, api_key, model_name):
    # OpenRouter 설정
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1", # 여기가 핵심!
        api_key=api_key,
    )
    
    prompt = f"""
    You are a professional technical translator for developers.
    Translate the following Markdown content into {target_lang}.
    
    RULES:
    1. Do NOT translate variable names, function names, or code blocks.
    2. Maintain the original Markdown structure strictly.
    3. Use professional developer terminology.
    
    Content:
    {text}
    """
    
    response = client.chat.completions.create(
        model=model_name, # 사용자가 선택한 모델 사용
        messages=[{"role": "user", "content": prompt}],
        # OpenRouter 랭킹을 위한 헤더 (선택사항)
        extra_headers={
            "HTTP-Referer": "https://github.com", 
            "X-Title": "GitPolyglot"
        }
    )
    return response.choices[0].message.content

def main():
    # 인자 순서가 바뀌었으니 주의하세요!
    api_key = sys.argv[1]
    target_langs = sys.argv[2].split(',')
    source_file = sys.argv[3]
    model_name = sys.argv[4] # 모델 이름 받기

    if not os.path.exists(source_file):
        print(f"Error: {source_file} not found.")
        sys.exit(1)

    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()

    for lang in target_langs:
        lang = lang.strip()
        print(f"Translating to {lang} using {model_name}...")
        
        try:
            translated_content = translate_text(content, lang, api_key, model_name)
            
            filename, ext = os.path.splitext(source_file)
            new_filename = f"{filename}.{lang}{ext}"
            
            with open(new_filename, 'w', encoding='utf-8') as f:
                f.write(translated_content)
            
            print(f"Saved: {new_filename}")
            
        except Exception as e:
            print(f"Error translating to {lang}: {e}")

if __name__ == "__main__":
    main()
