# OpenRouter 项目你好
这是一个测试，以验证 AI 型通过 OpenRouter 正确工作。

## 能
- 快速翻译
- 对开发者友好
- 保持原始代码结构。

---
## 代码保护测试 
本节测试代码块是否被正确保留。

### 1. Python 代码
以下 Python 代码计算总和。**变量名不应被翻译。**

```python
def calculate_total(price, tax_rate):
    # 这是代码内的注释
    total = price * (1 + tax_rate)
    print(f"总价是：{total}")
    return total
```

### 2. JSON 数据
JSON 中的键必须保持为英文，以避免语法错误。

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