# 🤖 AI & GenOps Guardian

**AI & GenOps Guardian** is a multi-language **DevSecOps automation framework** that runs inside **GitHub Actions** to perform **static analysis, security scanning, and AI-assisted code review** across application code, containers, and infrastructure-as-code.

It combines **best-in-class open-source analyzers** with **LLM-based reasoning** to provide actionable insights directly in Pull Requests or as build artifacts.

---

## 🚀 Key Capabilities

* 🔍 **Multi-language static analysis**
* 🔐 **Security & IaC scanning**
* 🤖 **AI-powered risk summarization**
* 💬 **Automatic PR comments**
* 📦 **Artifact reports for non-PR runs**
* 🧠 **Rate-limit safe LLM integration**
* 🧱 **CI-safe (never fails due to AI)**

---

## 🧰 Supported Languages & Tools

| Language / Area          | Tools Used                           |
| ------------------------ | ------------------------------------ |
| **Python**               | `ruff`, `pylint`, `bandit`           |
| **JavaScript / Node.js** | `eslint`                             |
| **Java**                 | `spotbugs`, `pmd`, `checkstyle`      |
| **Go**                   | `go vet`, `staticcheck`              |
| **Ruby**                 | `rubocop`                            |
| **PHP**                  | `phpcs`, `psalm`                     |
| **.NET**                 | Roslyn (`dotnet build /warnaserror`) |
| **Docker / Containers**  | `trivy`                              |
| **Terraform**            | `checkov`, `tfsec`                   |
| **Kubernetes YAML**      | `kube-linter`                        |
| **Multi-language**       | `semgrep`                            |

---

## 🏗️ Architecture Overview

```text
┌────────────┐
│ GitHub PR  │
└─────┬──────┘
      │
      ▼
┌────────────────────┐
│ GitHub Actions CI  │
└─────┬──────────────┘
      │
      ▼
┌──────────────────────────┐
│ Language Detection       │
│ (ai-agent/analyzers.py)  │
└─────┬────────────────────┘
      │
      ▼
┌──────────────────────────┐
│ Static & Security Scans  │
│ (All tools run locally) │
└─────┬────────────────────┘
      │
      ▼
┌──────────────────────────┐
│ AI Reasoning Layer       │
│ (OpenAI – rate-safe)     │
└─────┬────────────────────┘
      │
      ▼
┌───────────────┐   ┌────────────────┐
│ PR Comment    │   │ Artifacts JSON │
│ (PR mode)     │   │ (real/demo)    │
└───────────────┘   └────────────────┘
```

---

## ⚙️ Execution Modes

AI & GenOps Guardian supports **three execution modes**:

| Mode   | Trigger            | Behavior                           |
| ------ | ------------------ | ---------------------------------- |
| `pr`   | Pull Request       | Posts results as PR comments       |
| `real` | Manual / scheduled | Saves JSON reports as artifacts    |
| `demo` | Manual             | Same as `real` (no PR interaction) |

Mode selection priority:

1. `workflow_dispatch` input
2. `pull_request` event → `pr`
3. Default → `real`

---

## 🧪 Example PR Comment

```markdown
### 🤖 AI & GenOps Guardian Report

Mode: pr

Summary:
Potential security misconfigurations detected in Terraform
and inconsistent linting in Python modules.

Critical Issues:
- Terraform S3 bucket allows public access
- Hardcoded secret detected by Semgrep

Recommendations:
- Enable S3 Block Public Access
- Move secrets to GitHub Secrets or Vault
```

---

## 🛠️ Repository Structure

```text
.
├── .github/
│   └── workflows/
│       └── ai-genops.yml
│
├── ai-agent/
│   ├── agent.py        # Orchestrator (PR vs real mode)
│   ├── analyzers.py    # Tool execution & language detection
│   ├── llm.py          # LLM integration (rate-limit safe)
│   └── requirements.txt
│
└── analysis_results/   # Generated in real/demo mode
```

---

## 🔐 Required Secrets

Add the following secrets in your repository settings:

| Secret Name      | Description                     |
| ---------------- | ------------------------------- |
| `OPENAI_API_KEY` | OpenAI API key                  |
| `GITHUB_TOKEN`   | Auto-provided by GitHub Actions |

> ⚠️ **Do not** hardcode tokens or secrets in code.

---

## 🧠 LLM Safety & Reliability

The AI layer is **CI-safe by design**:

* 🧮 Prompt size capped to avoid token explosion
* 🔁 Automatic retry with exponential backoff
* ✂️ Analyzer output summarization
* 🧱 Hard fallback when rate-limited
* ❌ Pipeline **never fails due to AI**

If OpenAI is unavailable, **static analysis still completes**.

---

## 📦 Outputs

### PR Mode

* Comments posted directly on the Pull Request

### Real / Demo Mode

* `analysis_results/report.json`
* Uploaded as GitHub Action artifacts

---

## 🧩 Extensibility

Designed for easy extension:

* Add SARIF output
* Add policy gates (fail on Critical)
* Add diff-aware analysis (BASE vs HEAD)
* Plug in Bedrock / Azure OpenAI
* Split LLM analysis per language

---

## 🏆 Use Cases

* Secure CI/CD pipelines
* Enterprise DevSecOps automation
* Code quality enforcement
* IaC security governance
* AI-assisted code reviews

---

## 👤 Author

**Sourav Chandra**
DevSecOps • GenAI • Platform Engineering

---
