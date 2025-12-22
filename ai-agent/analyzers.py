import os
import subprocess

def run(cmd, cwd):
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
        return {
            "cmd": " ".join(cmd),
            "rc": p.returncode,
            "stdout": p.stdout[:15000],
            "stderr": p.stderr[:8000],
        }
    except Exception as e:
        return {"error": str(e)}

def detect(repo):
    found = set()
    for root, _, files in os.walk(repo):
        if "requirements.txt" in files or "pyproject.toml" in files:
            found.add("python")
        if "package.json" in files:
            found.add("javascript")
        if "pom.xml" in files or "build.gradle" in files:
            found.add("java")
        if "go.mod" in files:
            found.add("go")
        if "Gemfile" in files:
            found.add("ruby")
        if "composer.json" in files:
            found.add("php")
        if any(f.endswith(".csproj") for f in files):
            found.add("dotnet")
        if "Dockerfile" in files:
            found.add("docker")
        if any(f.endswith(".tf") for f in files):
            found.add("terraform")
        if any(f.endswith((".yaml", ".yml")) for f in files):
            found.add("k8s")
    return list(found)

def run_analyzers(repo, langs, run_semgrep=True):
    r = {}

    if "python" in langs:
        r["ruff"] = run(["ruff", "."], repo)
        r["pylint"] = run(["pylint", "--output-format=json", "."], repo)
        r["bandit"] = run(["bandit", "-r", ".", "-f", "json"], repo)

    if "javascript" in langs:
        r["eslint"] = run(["eslint", ".", "-f", "json"], repo)

    if "java" in langs:
        run(["mvn", "-q", "-DskipTests", "compile"], repo)
        r["spotbugs"] = run(["spotbugs", "-textui", "target/classes"], repo)
        r["pmd"] = run(["pmd", "-d", "src", "-R", "rulesets/java/quickstart.xml", "-f", "json"], repo)
        r["checkstyle"] = run(
            ["java", "-jar", "/usr/local/bin/checkstyle.jar", "-c", "google_checks.xml", "src"],
            repo
        )

    if "go" in langs:
        r["govet"] = run(["go", "vet", "./..."], repo)
        r["staticcheck"] = run(["staticcheck", "./..."], repo)

    if "ruby" in langs:
        r["rubocop"] = run(["rubocop", "-f", "json"], repo)

    if "php" in langs:
        r["phpcs"] = run(["phpcs", "--report=json", "."], repo)
        r["psalm"] = run(["psalm", "--output-format=json"], repo)

    if "dotnet" in langs:
        r["roslyn"] = run(["dotnet", "build", "/warnaserror"], repo)

    if "docker" in langs:
        r["trivy"] = run(["trivy", "config", "--format", "json", repo], repo)

    if "terraform" in langs:
        r["checkov"] = run(["checkov", "-d", repo, "-o", "json"], repo)
        r["tfsec"] = run(["tfsec", "--format", "json", repo], repo)

    if "k8s" in langs:
        r["kube-linter"] = run(["kube-linter", "lint", repo, "--format", "json"], repo)

    if run_semgrep:
        r["semgrep"] = run(["semgrep", "--config=auto", "--json"], repo)

    return r
