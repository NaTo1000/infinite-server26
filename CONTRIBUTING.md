# Contributing to Infinite Server26

Thank you for your interest in contributing to Infinite Server26! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists in [GitHub Issues](https://github.com/NaTo1000/infinite-server26/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - System information (OS, Docker version, etc.)
   - Relevant logs or screenshots

### Submitting Changes

1. **Fork the Repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/infinite-server26.git
   cd infinite-server26
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Make Your Changes**
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed
   - Test your changes thoroughly

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

5. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Provide clear description of changes
   - Reference any related issues

## 📋 Development Guidelines

### Code Style

**Python:**
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings for functions/classes
- Keep functions focused and small

**Bash:**
- Use `#!/bin/bash` shebang
- Add comments for complex logic
- Use functions for reusable code
- Handle errors appropriately

**Docker:**
- Keep Dockerfile clean and organized
- Use multi-stage builds when appropriate
- Minimize layers
- Document ENV variables

### Testing

Before submitting:

1. **Test Docker Build**
   ```bash
   docker build -t infinite-server26-test .
   ```

2. **Test Docker Compose**
   ```bash
   docker-compose up -d
   docker-compose ps
   docker-compose logs
   docker-compose down
   ```

3. **Test Scripts**
   ```bash
   bash -n your-script.sh  # Syntax check
   shellcheck your-script.sh  # Linting (if available)
   ```

4. **Test Deployment**
   ```bash
   ./quick-deploy.sh
   ./verify-deployment.sh
   ```

### Documentation

Update documentation when:
- Adding new features
- Changing configurations
- Modifying deployment process
- Adding new scripts or tools

Files to update:
- `README.md` - Main project documentation
- `DEPLOYMENT.md` - Deployment instructions
- `BUILD_AND_PUSH.md` - Build process
- Inline code comments

## 🎯 Areas for Contribution

### High Priority
- Bug fixes
- Security improvements
- Performance optimizations
- Documentation improvements
- Test coverage

### Features
- New AI capabilities
- Additional security tools
- Monitoring improvements
- Automation enhancements
- Integration with other tools

### Documentation
- Tutorials and guides
- Example configurations
- Troubleshooting tips
- Architecture diagrams

## 🔒 Security

### Reporting Security Issues

**DO NOT** create public issues for security vulnerabilities.

Instead:
1. Email security concerns to nato1000 (via GitHub)
2. Provide detailed description
3. Include steps to reproduce
4. Wait for response before public disclosure

### Security Best Practices

When contributing:
- Never commit secrets or credentials
- Use environment variables for sensitive data
- Follow principle of least privilege
- Validate and sanitize inputs
- Keep dependencies updated

## 📝 Commit Message Guidelines

Use clear, descriptive commit messages:

**Format:**
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```
feat: Add automated health check service

- Created health-check.py with multiple endpoints
- Added /health, /ready, and /live probes
- Integrated with Docker healthcheck

Closes #123
```

```
fix: Resolve docker-compose volume permission issue

- Changed volume permissions in docker-compose.yml
- Updated deployment documentation
- Tested on Ubuntu 22.04

Fixes #456
```

## 🧪 Testing Checklist

Before submitting PR:

- [ ] Code follows project style guidelines
- [ ] No syntax errors or warnings
- [ ] Docker build completes successfully
- [ ] Docker containers start and run
- [ ] Health checks pass
- [ ] Scripts execute without errors
- [ ] Documentation updated
- [ ] No hardcoded secrets
- [ ] Changes tested locally

## 📦 Release Process

Releases are managed by maintainers:

1. Version bump in relevant files
2. Update CHANGELOG
3. Create GitHub release
4. Build and push Docker images
5. Update documentation

## 🌟 Recognition

Contributors will be:
- Listed in project contributors
- Credited in release notes
- Appreciated by the community!

## 📞 Getting Help

Need help contributing?

- Check existing documentation
- Review closed issues and PRs
- Ask questions in new issue
- Contact project maintainer

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## Quick Reference

```bash
# Setup
git clone https://github.com/YOUR_USERNAME/infinite-server26.git
cd infinite-server26
git checkout -b feature/my-feature

# Develop
# ... make changes ...

# Test
docker build -t test .
docker-compose up -d
./verify-deployment.sh

# Commit
git add .
git commit -m "feat: Add awesome feature"
git push origin feature/my-feature

# Create PR on GitHub
```

---

**Thank you for contributing to Infinite Server26!**

**Built by the Community | For the Community**

*"Together we build an impenetrable fortress."*
