# OpenRouterプロジェクトへようこそ
このテストは、OpenRouterを介してAIモデルが正しく動作することを検証するために行われます。

## 能
-高速翻訳
-開発者向け
-元のコード構造を維持します。

---
## コード保護テスト 
このセクションでは、コードブロックが正しく保存されるかどうかをテストします。

### 1. Pythonコード
以下のPythonコードは、合計を計算します。**変数名は翻訳されません。**

```python
def calculate_total(price, tax_rate):
    # これはコード内のコメントです
    total = price * (1 + tax_rate)
    print(f"合計金額は: {total}")
    return total
```

### 2. JSONデータ
JSONのキーは、構文エラーを避けるために英語のままにする必要があります。

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