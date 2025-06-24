import types
import main_gui


class DummyWidget:
    def __init__(self, master=None, **kw):
        self.children = []
        if isinstance(master, DummyWidget):
            master.children.append(self)

    def pack(self, *a, **kw):
        return self

    def grid(self, *a, **kw):
        return self

    def destroy(self):
        pass

    def winfo_children(self):
        return list(self.children)

    def pack_propagate(self, *a, **kw):
        pass


class DummyEntry(DummyWidget):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.value = ""
        DummyTB.last_entry = self

    def get(self):
        return self.value

    def insert(self, idx, text):
        self.value = text


class DummyCombobox(DummyEntry):
    def set(self, val):
        self.value = val


class DummyButton(DummyWidget):
    def __init__(self, master=None, command=None, **kw):
        super().__init__(master, **kw)
        self.command = command
        DummyTB.last_button = self


class DummyLabel(DummyWidget):
    pass


class DummyFrame(DummyWidget):
    pass


class DummyLabelframe(DummyFrame):
    pass


class DummyStringVar:
    def __init__(self, value=None):
        self.value = value

    def get(self):
        return self.value

    def set(self, val):
        self.value = val


class DummyToplevel(DummyFrame):
    def title(self, *a, **kw):
        pass


class DummyTB:
    Frame = DummyFrame
    Labelframe = DummyLabelframe
    Label = DummyLabel
    Button = DummyButton
    Entry = DummyEntry
    Combobox = DummyCombobox
    StringVar = DummyStringVar
    Toplevel = DummyToplevel
    last_button = None
    last_entry = None


def test_send_prompt_thread(monkeypatch):
    logs = []

    def add_log(msg):
        logs.append(msg)

    monkeypatch.setattr(main_gui, "tb", DummyTB)
    monkeypatch.setattr(
        main_gui,
        "messagebox",
        types.SimpleNamespace(showwarning=lambda *a, **k: None),
    )
    monkeypatch.setattr(main_gui, "load_agents", lambda: [])
    monkeypatch.setattr(main_gui, "save_agents", lambda a: None)
    monkeypatch.setattr(main_gui, "ask_openai", lambda p: "resp")

    events = {}

    class DummyThread:
        def __init__(self, target, args=(), kwargs=None, daemon=None):
            events["target"] = target
            events["daemon"] = daemon

        def start(self):
            events["started"] = True

    monkeypatch.setattr(
        main_gui, "threading", types.SimpleNamespace(Thread=DummyThread)
    )

    main_gui.ia_tab_panel(None, add_log)
    DummyTB.last_entry.value = "hello"
    DummyTB.last_button.command()

    assert events.get("started") is True
