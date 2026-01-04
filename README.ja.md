# OpenRouterプロジェクトへようこそ
AIモデルがOpenRouterを介して正しく機能することを確認するためのテストです。

## 能
-高速翻訳
-開発者に優しい
-元のコード構造を維持します。

---
## コード保護テスト
コードブロックが正しく保存されるかどうかをテストするセクションです。

### 1. Pythonコード
次のPythonコードは合計を計算します。**変数名は翻訳されません。**

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