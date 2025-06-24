import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import json
import pytest
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


class DummyResp:
    def __init__(self, content="dummy"):
        self.choices = [
            type("c", (), {"message": type("m", (), {"content": content})()})()
        ]


class DummyChatCompletion:
    @staticmethod
    def create(model, messages):
        return DummyResp()


class DummyOpenAI:
    api_key = None
    ChatCompletion = DummyChatCompletion


def test_ask_openai_env_fallback(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump({}, f)
    monkeypatch.setattr(project_utils, "openai", DummyOpenAI)
    monkeypatch.setenv("OPENAI_API_KEY", "ENVKEY")
    resp = project_utils.ask_openai("Hello")
    assert resp == "dummy"
    assert DummyOpenAI.api_key == "ENVKEY"


def test_ask_openai_missing_key(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump({}, f)
    monkeypatch.setattr(project_utils, "openai", DummyOpenAI)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(RuntimeError):
        project_utils.ask_openai("Hello")


def _patch_serial(monkeypatch, ports):
    import types

    lp = types.SimpleNamespace(comports=lambda: ports)
    tools = types.SimpleNamespace(list_ports=lp)
    serial_mod = types.SimpleNamespace(tools=tools)
    monkeypatch.setitem(sys.modules, "serial", serial_mod)
    monkeypatch.setitem(sys.modules, "serial.tools", tools)
    monkeypatch.setitem(sys.modules, "serial.tools.list_ports", lp)


def test_detect_com_found(monkeypatch):
    class Port:
        device = "COM1"

    _patch_serial(monkeypatch, [Port()])
    port, msg = project_utils.detect_com()
    assert port == "COM1"
    assert "[OK] Port détecté : COM1" == msg


def test_detect_com_missing(monkeypatch):
    _patch_serial(monkeypatch, [])
    port, msg = project_utils.detect_com()
    assert port is None
    assert msg.startswith("[ERR] Aucun port COM")


def test_flash_esp32(monkeypatch):
    class Port:
        device = "COM3"

    _patch_serial(monkeypatch, [Port()])
    res = project_utils.flash_esp32()
    assert res == "[FLASH] (Fake) Flash ESP32 sur COM3"


def test_flash_esp32_no_port(monkeypatch):
    _patch_serial(monkeypatch, [])
    res = project_utils.flash_esp32()
    assert res.startswith("[ERR] Aucun port COM")


def test_reset_git(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    calls = []
    monkeypatch.setattr(os, "system", lambda cmd: calls.append(cmd))
    msg = project_utils.reset_git()
    assert msg == "[GIT] Dépôt Git réinitialisé."
    assert calls == ["git init"]


def test_push_github(monkeypatch):
    calls = []
    monkeypatch.setattr(os, "system", lambda cmd: calls.append(cmd))
    msg = project_utils.push_github()
    assert msg.startswith("[GIT] Simu push")
    assert calls == []


def test_open_github_repo(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump({"github_repo_url": "http://ex"}, f)
    opened = []
    monkeypatch.setattr(
        project_utils.webbrowser, "open", lambda url: opened.append(url)
    )
    msg = project_utils.open_github_repo()
    assert msg == "[GIT] Ouverture page GitHub."
    assert opened == ["http://ex"]


def test_ask_openai_success(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump({"openai_api_key": "KEY"}, f)

    class Dummy(DummyOpenAI):
        pass

    called = []

    def create(model, messages):
        called.append(messages[0]["content"])
        return DummyResp("resp")

    Dummy.ChatCompletion.create = staticmethod(create)
    monkeypatch.setattr(project_utils, "openai", Dummy)
    resp = project_utils.ask_openai("Hi")
    assert resp == "resp"
    assert Dummy.api_key == "KEY"
    assert called == ["Hi"]
