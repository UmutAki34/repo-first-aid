from pathlib import Path

from .models import Finding


README_NAMES = {"readme", "readme.md", "readme.rst", "readme.txt"}
LICENSE_NAMES = {"license", "license.md", "license.txt", "copying"}


def _finding(check_id: str, title: str, status: str, message: str, suggestion: str) -> Finding:
    return Finding(check_id, title, status, message, suggestion)


def _has_any(root: Path, names: set[str]) -> bool:
    return any(item.name.lower() in names for item in root.iterdir())


def check_readme(root: Path) -> Finding:
    readme = next((item for item in root.iterdir() if item.name.lower() in README_NAMES), None)
    if readme is None:
        return _finding("docs.readme", "README", "error", "README file not found / README dosyası bulunamadı.", "Add README.md with installation, usage and tests / Kurulum, kullanım ve testleri anlatan README.md ekle.")

    text = readme.read_text(encoding="utf-8", errors="ignore").lower()
    missing = []
    if not any(word in text for word in ("install", "installation", "kurulum")):
        missing.append("kurulum")
    if not any(word in text for word in ("usage", "kullanım", "how to use")):
        missing.append("kullanım")
    if not any(word in text for word in ("test", "testing", "testler")):
        missing.append("test")
    if missing:
        return _finding("docs.readme", "README", "warning", f"README exists, but these sections are missing / README mevcut ancak şu bölümler eksik: {', '.join(missing)}.", "Complete the missing sections with commands / Eksik bölümleri komut örnekleriyle tamamla.")
    return _finding("docs.readme", "README", "ok", "README includes installation, usage and test guidance / README kurulum, kullanım ve test bilgisi içeriyor.", "Keep README current with examples / README'yi örnek çıktılarla güncel tut.")


def check_file(root: Path, check_id: str, title: str, names: set[str], missing_message: str, suggestion: str, required: bool = False) -> Finding:
    if _has_any(root, names):
        return _finding(check_id, title, "ok", f"{title} file found / {title} dosyası bulundu.", "Keep the file current / Dosyayı güncel tut.")
    return _finding(check_id, title, "error" if required else "warning", missing_message, suggestion)


def check_project_metadata(root: Path) -> Finding:
    metadata = {"pyproject.toml", "setup.py", "package.json", "go.mod", "cargo.toml", "pom.xml", "build.gradle"}
    if any(item.name.lower() in metadata for item in root.iterdir()):
        return _finding("project.metadata", "Project metadata / Proje metadata'sı", "ok", "A known project metadata file was found / Bilinen bir proje metadata dosyası bulundu.", "Also document the run command in README / Çalıştırma komutunu README'de de belirt.")
    return _finding("project.metadata", "Project metadata / Proje metadata'sı", "warning", "No known project metadata file was found / Bilinen proje metadata dosyası bulunamadı.", "Add pyproject.toml, package.json or an equivalent / Ekosisteme uygun pyproject.toml, package.json veya eşdeğerini ekle.")


def check_environment_example(root: Path) -> Finding:
    names = {".env.example", ".env.sample", ".env.template"}
    if _has_any(root, names):
        return _finding("security.env-example", "Environment example / Ortam değişkeni örneği", "ok", "An environment example file was found / Örnek ortam değişkeni dosyası bulundu.", "Never put real secrets in the example / Örnekte gerçek secret tutma.")
    return _finding("security.env-example", "Environment example / Ortam değişkeni örneği", "warning", "No environment example file was found / Ortam değişkenleri için örnek dosya bulunamadı.", "Add .env.example and keep real secrets in local .env / .env.example ekle ve gerçek secret'ları yalnızca yerel .env dosyasında tut.")


def check_secret_files(root: Path) -> Finding:
    risky_names = {".env", "id_rsa", "id_dsa", "server.key"}
    risky_suffixes = {".pem", ".key"}
    found = [item.name for item in root.rglob("*") if item.is_file() and (item.name.lower() in risky_names or item.suffix.lower() in risky_suffixes)]
    if found:
        return _finding("security.secret-files", "Secret files / Secret dosyaları", "error", f"Risky file names found / Riskli dosya adları bulundu: {', '.join(sorted(found))}.", "Add them to .gitignore and check git history / .gitignore'a ekle ve geçmişte commit edilip edilmediğini kontrol et.")
    return _finding("security.secret-files", "Secret files / Secret dosyaları", "ok", "No common secret-file pattern was found / Yaygın secret dosyası paterni bulunamadı.", "Never commit new secret files / Yeni secret dosyalarını commit etme.")


def check_contributing(root: Path) -> Finding:
    return check_file(root, "community.contributing", "Contributing guide / Katkı rehberi", {"contributing.md", "contributing.rst"}, "CONTRIBUTING file not found / CONTRIBUTING dosyası bulunamadı.", "Add CONTRIBUTING.md with setup, tests and PR flow / Kurulum, test ve PR akışını anlatan CONTRIBUTING.md ekle.")


def check_license(root: Path) -> Finding:
    return check_file(root, "legal.license", "License / Lisans", LICENSE_NAMES, "License file not found / Lisans dosyası bulunamadı.", "Choose a license and add LICENSE; do not copy license text without permission / Lisans seçip LICENSE ekle; lisans metnini izinsiz kopyalama.", required=True)


def check_gitignore(root: Path) -> Finding:
    return check_file(root, "project.gitignore", ".gitignore", {".gitignore"}, ".gitignore not found / .gitignore bulunamadı.", "Ignore build outputs, caches and secret files / Build çıktıları, cache klasörleri ve secret dosyaları için .gitignore ekle.")


def check_ci(root: Path) -> Finding:
    workflows = root / ".github" / "workflows"
    if workflows.is_dir() and any(workflows.iterdir()):
        return _finding("automation.ci", "CI workflow", "ok", "A GitHub Actions workflow was found / GitHub Actions workflow bulundu.", "Keep test and lint steps in CI / CI'da test ve lint adımlarını koru.")
    return _finding("automation.ci", "CI workflow", "warning", "No GitHub Actions workflow was found / GitHub Actions workflow bulunamadı.", "Add .github/workflows/ci.yml that runs tests / Testleri çalıştıran .github/workflows/ci.yml ekle.")


def run_checks(root: Path) -> list[Finding]:
    return [
        check_readme(root),
        check_project_metadata(root),
        check_file(root, "docs.code-of-conduct", "Code of Conduct / Davranış kuralları", {"code_of_conduct.md", "code-of-conduct.md"}, "CODE_OF_CONDUCT file not found / CODE_OF_CONDUCT dosyası bulunamadı.", "Add community behavior guidelines / Topluluk davranış kurallarını ekle."),
        check_contributing(root),
        check_license(root),
        check_gitignore(root),
        check_environment_example(root),
        check_secret_files(root),
        check_ci(root),
    ]
