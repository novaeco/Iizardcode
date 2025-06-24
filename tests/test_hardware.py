import sys, os, types

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import hardware


class DummyPort:
    device = "COMX"


def patch_serial(monkeypatch, ports, serial_class):
    lp = types.SimpleNamespace(comports=lambda: ports)
    tools = types.SimpleNamespace(list_ports=lp)
    serial_mod = types.SimpleNamespace(Serial=serial_class, tools=tools)
    monkeypatch.setitem(sys.modules, "serial", serial_mod)
    monkeypatch.setitem(sys.modules, "serial.tools", tools)
    monkeypatch.setitem(sys.modules, "serial.tools.list_ports", lp)


class DummySerial:
    def __init__(self, port, baud, timeout):
        self.written = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass

    def write(self, data):
        self.written.append(data)


def test_send_serial_command_ok(monkeypatch):
    serial_inst = DummySerial("COMX", 9600, 2)

    class _Serial(DummySerial):
        def __new__(cls, *a, **kw):
            return serial_inst

    patch_serial(monkeypatch, [DummyPort()], _Serial)
    assert hardware.send_serial_command("AT") is True
    assert serial_inst.written == [b"AT\n"]


def test_send_serial_command_no_port(monkeypatch):
    patch_serial(monkeypatch, [], DummySerial)
    assert hardware.send_serial_command("AT") is False


def test_send_serial_command_with_port(monkeypatch):
    serial_inst = DummySerial("COMZ", 9600, 2)

    class _Serial(DummySerial):
        def __new__(cls, *a, **kw):
            return serial_inst

    patch_serial(monkeypatch, [], _Serial)
    assert hardware.send_serial_command("AT", port="COMZ") is True
    assert serial_inst.written == [b"AT\n"]
