# GitPolyglot - AI README Translator

Automatically translate your README and GitHub Issues/PRs into multiple languages using AI (via OpenRouter).

## Features

- Translate README files to Korean, Japanese, and Simplified Chinese
- Auto-translate Issues and Pull Requests with comments
- Preserves code blocks and markdown formatting
- Supports multiple AI models (Llama, Gemini, Claude, etc.)

## Quick Start

### 1. Get OpenRouter API Key

Sign up at [OpenRouter](https://openrouter.ai/) and get your API key.

### 2. Add Secret to Repository

Go to your repo **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

- Name: `OPENROUTER_API_KEY`
- Value: Your OpenRouter API key

### 3. Create Workflow

#### README Translation (Manual Trigger)

Create `.github/workflows/translate-readme.yml`:

```yaml
name: Translate README

on:
  workflow_dispatch:

jobs:
  translate:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Run GitPolyglot
        env:
          OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
          MODEL_NAME: 'meta-llama/llama-3.3-70b-instruct:free'
        run: |
          pip install openai PyGithub
          curl -o main.py https://raw.githubusercontent.com/aboutexo04/git-polyglot/main/main.py
          python main.py README.md

      - name: Commit translations
        run: |
          git config --global user.name "GitHub Actions"
          git config --global user.email "actions@github.com"
          git add README.*.md
          git commit -m "Auto-translated README" || echo "No changes"
          git push
```

#### Issue/PR Auto Translation

Create `.github/workflows/issue-translator.yml`:

```yaml
name: Auto Issue Translator

on:
  issues:
    types: [opened]
  pull_request:
    types: [opened]

jobs:
  translate:
    runs-on: ubuntu-latest
    permissions:
      issues: write
      pull-requests: write

    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Run Translator
        env:
          OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          MODEL_NAME: 'meta-llama/llama-3.3-70b-instruct:free'
        run: |
          pip install openai PyGithub
          curl -o main.py https://raw.githubusercontent.com/aboutexo04/git-polyglot/main/main.py
          if [[ "${{ github.event_name }}" == "pull_request" ]]; then
            NUMBER="${{ github.event.pull_request.number }}"
          else
            NUMBER="${{ github.event.issue.number }}"
          fi
          python main.py "$NUMBER"
```

## Supported Languages

| Code | Language |
|------|----------|
| ko | Korean |
| ja | Japanese |
| zh-CN | Simplified Chinese |

## Supported Models

Any model available on [OpenRouter](https://openrouter.ai/models) can be used. Free options include:

- `meta-llama/llama-3.3-70b-instruct:free`
- `google/gemini-2.0-flash-exp:free`
- `deepseek/deepseek-r1:free`

## License

MIT License
