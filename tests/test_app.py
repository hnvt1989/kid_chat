import pytest
try:
    from app import app, load_memory, save_memory, MEMORY_LIMIT
except ModuleNotFoundError:
    pytest.skip("Required packages not installed", allow_module_level=True)
import os
import tempfile
import json

def test_index():
    tester = app.test_client()
    response = tester.get('/')
    assert response.status_code == 200

def test_tts_no_text():
    tester = app.test_client()
    response = tester.post('/tts', json={})
    assert response.status_code == 400


def test_memory_persistence(tmp_path, monkeypatch):
    mem_file = tmp_path / 'mem.json'
    monkeypatch.setattr('app.MEMORY_FILE', str(mem_file))
    monkeypatch.setattr('app.MEMORY_LIMIT', 5)

    # Save more items than the limit
    history = [{'role': 'user', 'content': f'm{i}'} for i in range(10)]
    save_memory(history)

    loaded = load_memory()
    assert len(loaded) == 5
    assert loaded == history[-5:]
