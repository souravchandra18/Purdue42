#Author:Sourav Chandra
import os
import json
from github import Github
from analyzers import detect, run_analyzers
from llm import call_llm

def main():
    repo = os.getenv("GITHUB_WORKSPACE", ".")
    run_semgrep = os.getenv("INPUT_RUN_SEMGREP", "true") == "true"
    pr_number = os.getenv("PR_NUMBER")

    languages = detect(repo)
    analysis = run_analyzers(repo, languages, run_semgrep)

    prompt = f"""
You are an expert DevSecOps reviewer.

Return STRICT JSON:
{{
  "summary": "...",
  "critical_issues": [],
  "recommendations": []
}}

Detected languages: {languages}

Analyzer results:
{json.dumps(analysis, indent=2)}
"""

    result = call_llm(prompt)

    comment = f"""
### 🤖 AI & GenOps Guardian Report

**Summary**
{result.get("summary")}

**Critical Issues**
{json.dumps(result.get("critical_issues", []), indent=2)}

**Recommendations**
{json.dumps(result.get("recommendations", []), indent=2)}
"""

    if pr_number:
        gh = Github(os.getenv("GITHUB_TOKEN"))
        repo_obj = gh.get_repo(os.getenv("GITHUB_REPOSITORY"))
        repo_obj.get_pull(int(pr_number)).create_issue_comment(comment)
    else:
        os.makedirs("analysis_results", exist_ok=True)
        with open("analysis_results/report.json", "w") as f:
            json.dump(result, f, indent=2)

if __name__ == "__main__":
    main()
