# Mocking Patterns

**Date:** 2026-03-31

## Mock os.getenv

```python
def test_env_variable(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "test-token-123")
    result = runner.invoke(app, ["config"])
    assert "Using token" in result.output
```

## Mock typer.launch()

```python
def test_launch_no_open(monkeypatch):
    opened_urls = []
    def mock_launch(url, browser=None, locate=False):
        opened_urls.append(url)

    with mock.patch("typer.launch", mock_launch):
        result = runner.invoke(app, ["docs"])

    assert "https://docs.example.com" in result.output
    assert len(opened_urls) == 1
```

## Mock Path.exists()

```python
def test_file_not_found(monkeypatch):
    fake_path = mock.MagicMock()
    fake_path.exists.return_value = False

    with mock.patch("pathlib.Path", return_value=fake_path):
        result = runner.invoke(app, ["process", "--config", "fake.txt"])

    assert result.exit_code != 0
```

## Mock datetime

```python
def test_timestamp(monkeypatch):
    fake_date = mock.Mock()
    fake_date.isoformat.return_value = "2024-01-15T10:30:00"

    with mock.patch("datetime.datetime") as mock_dt:
        mock_dt.now.return_value = fake_date
        result = runner.invoke(app, ["timestamp"])

    assert "2024-01-15" in result.output
```

## Mock requests

```python
def test_api_call(monkeypatch):
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "ok"}

    with mock.patch("requests.get", return_value=mock_response):
        result = runner.invoke(app, ["fetch", "--url", "https://api.example.com"])

    assert result.exit_code == 0
    assert "ok" in result.output
```

## Mock subprocess.run

```python
def test_external_command(monkeypatch):
    mock_run = mock.Mock()
    mock_run.return_value = mock.Mock(returncode=0, stdout="command output\n")

    with mock.patch("subprocess.run", mock_run):
        result = runner.invoke(app, ["run-external"])

    assert result.exit_code == 0
```

## Common Mocking Issues

### Mock Not Being Called

```python
# Problem: Mock not working
def test_mock_not_working(monkeypatch):
    mock_func = mock.Mock()
    # Make sure to patch the correct module path
    monkeypatch.setattr("myapp.module.func", mock_func)
    result = runner.invoke(app, ["call-func"])
    mock_func.assert_called_once()  # Will fail if wrong path

# Solution: Verify the correct import path
# from myapp.module import func  # Patch myapp.module.func
# import myapp.module; myapp.module.func  # Patch myapp.module.func
```

### monkeypatch vs mock.patch

```python
def test_monkeypatch_env(monkeypatch):
    monkeypatch.setenv("MY_VAR", "value")
    result = runner.invoke(app, ["config"])
    assert "value" in result.output

def test_mock_patch():
    with mock.patch("os.getenv", return_value="mocked"):
        result = runner.invoke(app, ["config"])
    assert "mocked" in result.output
```

## See Also

- [pytest-configuration.md](pytest-configuration.md) - pytest configuration
