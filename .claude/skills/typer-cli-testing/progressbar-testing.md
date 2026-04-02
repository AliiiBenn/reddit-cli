# Progress Bar Testing

**Date:** 2026-03-31

## Overview

Progress bars can cause tests to hang because they wait for completion.

## Basic Progress Bar Test

```python
def test_progressbar():
    result = runner.invoke(app, ["process", "--items", "a,b,c"])
    assert result.exit_code == 0
    # The test blocks until the progress bar finishes
```

## Mocking time.sleep to Speed Up

```python
def test_progressbar_quick():
    import unittest.mock as mock
    with mock.patch("time.sleep"):  # Mock sleep to go fast
        result = runner.invoke(app, ["process"])
    assert result.exit_code == 0
```

## Mocking tqdm Completely

```python
def test_progressbar_with_tqdm_mock():
    with mock.patch("tqdm.tqdm") as mock_tqdm:
        mock_tqdm.return_value.__enter__ = mock.Mock(return_value=mock_tqdm)
        mock_tqdm.return_value.__exit__ = mock.Mock(return_value=None)
        mock_tqdm.return_value.update = mock.Mock()
        result = runner.invoke(app, ["batch-process"])
    assert result.exit_code == 0
```

## Complete tqdm Mock

```python
def test_tqdm_complete():
    mock_tqdm_instance = mock.MagicMock()
    mock_tqdm_instance.__enter__ = mock.Mock(return_value=mock_tqdm_instance)
    mock_tqdm_instance.__exit__ = mock.Mock(return_value=None)
    mock_tqdm_instance.update = mock.Mock()

    with mock.patch("tqdm.tqdm", return_value=mock_tqdm_instance) as mock_tqdm_cls:
        result = runner.invoke(app, ["process"])
    assert result.exit_code == 0
    mock_tqdm_cls.assert_called()
```

## Troubleshooting

### Test Hangs or Times Out

If tests hang, you may have missed a prompt or the progress bar is waiting:

```python
# Problem: Test blocks forever waiting for progress bar
def test_slow_process():
    result = runner.invoke(app, ["process", "--items", "a,b,c"])
    # This will block!

# Solution: Mock time.sleep to speed up
def test_slow_process_fast():
    import unittest.mock as mock
    with mock.patch("time.sleep", return_value=None):
        result = runner.invoke(app, ["process", "--items", "a,b,c"])
    assert result.exit_code == 0
```

## See Also

- [rich-output-testing.md](rich-output-testing.md) - Rich output testing
