# Contributing to Proxmox CLI

Thank you for your interest in contributing to Proxmox CLI!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/rwgb/proxmox.cli.git
cd proxmox.cli
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
make install-dev
```

## Code Style

This project uses:
- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Run formatting:
```bash
make format
```

Run linting:
```bash
make lint
```

## Testing

Run tests with:
```bash
make test
```

Write tests for new features in the `tests/` directory.

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Commit Messages

Follow conventional commits format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Test changes
- `chore:` - Build/tooling changes

## Questions?

Feel free to open an issue for any questions or concerns.
