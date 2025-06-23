import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import json
import project_utils


def test_generate_project(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    msg = project_utils.generate_project()
    assert msg == "[OK] Projet ESP32/BPI généré."
    assert (tmp_path / "src" / "main.c").exists()
    assert (tmp_path / "README.md").exists()


def test_generate_readme(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    msg = project_utils.generate_readme()
    assert msg == "[OK] README.md généré."
    with open("README.md", "r", encoding="utf-8") as f:
        assert "Projet généré" in f.read()


def test_generate_workspace(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    msg = project_utils.generate_workspace()
    assert msg == "[OK] .code-workspace généré."
    with open(".code-workspace", "r", encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data.get("folders"), list)


def test_generate_openapi(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    msg = project_utils.generate_openapi()
    assert msg == "[OK] openapi.json généré."
    with open(project_utils.OPENAPI_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data.get("openapi") == "3.0.0"


def test_generate_changelog(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    msg = project_utils.generate_changelog()
    assert msg == "[OK] CHANGELOG et version.txt générés."
    assert (tmp_path / "CHANGELOG.md").exists()
    assert (tmp_path / "version.txt").exists()


def test_save_profile(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    msg = project_utils.save_profile("Test")
    assert "[PROFIL]" in msg
    with open(project_utils.PROFILES_FILE, "r", encoding="utf-8") as f:
        profiles = json.load(f)
    assert "Test" in profiles


def test_save_ia_history(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    project_utils.save_ia_history("p", "r")
    with open(project_utils.HIST_FILE, "r", encoding="utf-8") as f:
        hist = json.load(f)
    assert hist[0]["prompt"] == "p"
    assert hist[0]["response"] == "r"
