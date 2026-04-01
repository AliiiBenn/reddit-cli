# Contributing to Reddit CLI

We welcome contributions! Please follow these guidelines.

## How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/reddit-cli.git
cd reddit-cli

# Install dependencies
uv sync

# Run tests
uv run pytest

# Run CLI
uv run reddit <command>
```

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for public functions
- Add tests for new features

## Commit Messages

Follow the conventional commits format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for test changes
- `refactor:` for code refactoring

## Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Your PR will be reviewed by a maintainer

## Questions

For questions or discussions, please contact: support@nesalia.com
