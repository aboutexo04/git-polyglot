# OpenRouter 프로젝트에 오신 것을 환영합니다
AI 모델이 OpenRouter를 통해 올바르게 작동하는지 확인하는 테스트입니다.

## 기능
- 빠른 번역
- 개발자 친화적
- 원본 코드 구조 유지.

---
## 코드 보호 테스트
이 션에서는 코드 블록이 올바르게 보존되는지 테스트합니다.

### 1. Python 코드
다음 Python 코드는 합계를 계산합니다. **변수 이름은 번역되어서는 안 됩니다.**

```python
def calculate_total(price, tax_rate):
    # This is a comment inside code
    total = price * (1 + tax_rate)
    print(f"Total price is: {total}")
    return total
```

### 2. JSON 데이터
JSON 키는 구문 오류를 방지하기 위해 영어로 유지해야 합니다.

```json
{
  "user_id": "user_1234",
  "is_admin": false,
  "settings": {
    "theme": "dark_mode",
    "notifications": true
  }
}
```