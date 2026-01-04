import os
import sys
import re
from openai import OpenAI
from github import Github

# --- 설정 ---
# 번역하고 싶은 언어 목록 (한국어, 일본어, 중국어)
TARGET_LANGS = {
    'ko': 'Korean',
    'ja': 'Japanese',
    'zh': 'Simplified Chinese'
}

def get_ai_client(api_key):
    return OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

def translate_content(client, text, target_lang, model_name):
    """
    AI에게 텍스트를 던져서 번역을 받아오는 핵심 함수
    """
    if not text or len(text.strip()) == 0:
        return ""

    # [스마트 감지 프롬프트]
    # 소스 언어를 자동 감지하고, 타겟 언어와 같으면 번역하지 말라고 지시합니다.
    system_prompt = f"""
    You are a professional technical translator.
    Task: Translate the input text into **{target_lang}**.
    
    RULES:
    1. Detect the source language automatically.
    2. If the source text is ALREADY in {target_lang}, return only the word "SKIP".
    3. Keep code blocks (```...```) and technical terms (English) intact.
    4. Do not add explanations. Just output the translation.
    """

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.3
        )
        result = response.choices[0].message.content.strip()
        
        # 이미 같은 언어라면 번역 스킵
        if result == "SKIP":
            return None
            
        return result
    except Exception as e:
        print(f"Translation Error ({target_lang}): {e}")
        return None

def handle_file_translation(client, filename, model_name):
    """ README.md 같은 파일 번역 모드 """
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"translating file: {filename}...")

    # 한/중/일 루프 돌면서 번역
    for lang_code, lang_name in TARGET_LANGS.items():
        print(f"  -> {lang_name} ({lang_code})...")
        translated = translate_content(client, content, lang_name, model_name)
        
        if translated:
            new_filename = f"{os.path.splitext(filename)[0]}.{lang_code}.md"
            with open(new_filename, 'w', encoding='utf-8') as f:
                f.write(translated)
            print(f"     Saved: {new_filename}")
        else:
            print("     Skipped (Same language or empty).")

def handle_issue_translation(client, token, repo_name, issue_number, model_name):
    """ 이슈/PR 댓글 번역 모드 """
    g = Github(token)
    repo = g.get_repo(repo_name)
    issue = repo.get_issue(number=issue_number)
    
    title = issue.title
    body = issue.body or ""
    
    print(f"Processing Issue #{issue_number}: {title}")
    
    comment_body = "## 🤖 Global Translation Bot\n"
    has_translation = False

    # 한/중/일 루프
    for lang_code, lang_name in TARGET_LANGS.items():
        print(f"  -> Translating to {lang_name}...")
        
        # 제목과 본문 각각 번역
        t_title = translate_content(client, title, lang_name, model_name)
        t_body = translate_content(client, body, lang_name, model_name)
        
        if t_title or t_body:
            has_translation = True
            comment_body += f"\n<details><summary><b>🌏 {lang_name} Translation</b></summary>\n\n"
            if t_title:
                comment_body += f"**Title:** {t_title}\n\n"
            if t_body:
                comment_body += f"{t_body}\n"
            comment_body += "\n</details>\n"

    # 번역된 게 하나라도 있으면 댓글 달기
    if has_translation:
        issue.create_comment(comment_body)
        print("✅ Comment posted!")
    else:
        print("No translation needed.")

def main():
    api_key = os.environ.get('OPENROUTER_API_KEY')
    model_name = os.environ.get('MODEL_NAME', 'qwen/qwen-2-7b-instruct:free')
    
    # GitHub Action이 주는 환경변수로 '지금 무슨 상황인지' 파악
    event_name = os.environ.get('GITHUB_EVENT_NAME')
    
    client = get_ai_client(api_key)

    if event_name in ['issues', 'pull_request']:
        # --- [모드 1] 이슈/PR 번역 ---
        token = os.environ.get('GITHUB_TOKEN')
        repo_name = os.environ.get('GITHUB_REPOSITORY')
        
        # 이벤트 페이로드에서 이슈 번호 찾기 (조금 복잡하지만 이게 정석)
        # 간단하게 환경변수 GITHUB_REF 등을 쓸 수도 있지만, event.json을 읽는 게 정확함.
        # 여기서는 간단히 workflow arguments로 받는 구조로 가정하거나
        # main.py 실행 시 인자로 받도록 처리
        try:
            issue_number = int(sys.argv[1]) # 워크플로우에서 넘겨줄 예정
            handle_issue_translation(client, token, repo_name, issue_number, model_name)
        except IndexError:
            print("Error: Issue number required for issue mode.")
            
    else:
        # --- [모드 2] 파일(README) 번역 ---
        try:
            filename = sys.argv[1] # 예: README.md
            handle_file_translation(client, filename, model_name)
        except IndexError:
            print("Usage: python main.py <file>")

if __name__ == "__main__":
    main()
