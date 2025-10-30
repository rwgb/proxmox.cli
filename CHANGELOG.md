# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release preparation
- Version bumping automation

## [0.1.0] - 2025-10-30

### Added
- Initial release of Proxmox CLI
- Virtual machine management commands (list, start, stop, status)
- LXC container management commands (list, start, stop)
- Node management commands (list, status)
- Storage management commands (list)
- User management commands (create, delete, update, list, show, set-password)
- Group management commands (create, delete, update, list, show)
- Role management commands (create, delete, update, list, show)
- ACL/permissions management commands (list, add, remove)
- API token management commands (create, delete, update, list, show)
- JSON output format (default)
- Table output format support
- YAML output format support
- Plain text output format support
- Configuration file support (~/.config/proxmox-cli/config.yaml)
- SSL verification control
- API token authentication
- Password authentication
- Comprehensive documentation
- IAM documentation with examples
- API documentation
- Contributing guidelines

### Features
- Multi-format output (JSON, Table, YAML, Plain)
- Flexible authentication (password or API token)
- Path-based permissions (ACLs)
- Privilege separation for API tokens
- Offline node handling
- Error handling with JSON error responses
- Filtered output for cleaner tables
- User-friendly help messages

### Documentation
- README.md with installation and usage
- API.md with programmatic usage examples
- CONTRIBUTING.md with development guidelines
- IAM.md with identity and access management guide
- RELEASE.md with publishing instructions

[Unreleased]: https://github.com/rwgb/proxmox.cli/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/rwgb/proxmox.cli/releases/tag/v0.1.0
