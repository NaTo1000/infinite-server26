# Infinite Server26 - Multi-Edition Quick Start

## Version 26.2 - Now with Multiple Editions!

Infinite Server26 is now available in **three editions** to suit different needs:

---

## 🎯 Choose Your Edition

### 🌟 Lite Edition
**Perfect for:** Personal use, learning, testing
- **Resources**: 512 MB RAM, 1 CPU core
- **Features**: Basic AI orchestration, essential security
- **Install**: `pip install -r requirements-lite.txt`
- **Run**: `python3 server.py --edition=lite`

### 🚀 Standard Edition (Default)
**Perfect for:** Small teams, standard deployments
- **Resources**: 2 GB RAM, 2 CPU cores
- **Features**: Full AI + security + blockchain
- **Install**: `pip install -r requirements.txt`
- **Run**: `python3 server.py --edition=standard`

### 💼 Enterprise Edition
**Perfect for:** Large organizations, production
- **Resources**: 8+ GB RAM, 4+ CPU cores
- **Features**: All + API + plugins + HA
- **Install**: `pip install -r requirements-enterprise.txt`
- **Run**: `python3 server.py --edition=enterprise`

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/NaTo1000/infinite-server26.git
cd infinite-server26
```

### 2. Choose Edition & Install
```bash
# For Lite
pip install -r requirements-lite.txt

# For Standard (default)
pip install -r requirements.txt

# For Enterprise
pip install -r requirements-enterprise.txt
```

### 3. Run Server
```bash
# Lite edition
python3 server.py --edition=lite

# Standard edition
python3 server.py --edition=standard

# Enterprise edition
python3 server.py --edition=enterprise
```

---

## 📋 Feature Comparison

| Feature | Lite | Standard | Enterprise |
|---------|:----:|:--------:|:----------:|
| AI Orchestrator | ✅ Basic | ✅ Full | ✅ Enhanced |
| Security Monitoring | ✅ Basic | ✅ Full | ✅ Advanced |
| Blockchain Storage | ❌ | ✅ | ✅ |
| Auto-Healing | ❌ | ✅ | ✅ |
| Pattern Learning | ❌ | ✅ | ✅ |
| API Gateway | ❌ | ❌ | ✅ |
| Plugin System | ❌ | ❌ | ✅ |
| High Availability | ❌ | ❌ | ✅ |

See **[EDITIONS.md](EDITIONS.md)** for complete comparison.

---

## 🏗️ Build Distributions

Build standalone distributions for any edition:

```bash
# Build all editions
./build.sh lite
./build.sh standard
./build.sh enterprise

# Output: build/infinite-server26-26.2-{edition}.tar.gz
```

---

## 📚 Documentation

- **[VERSION.md](VERSION.md)** - Version history and edition overview
- **[EDITIONS.md](EDITIONS.md)** - Detailed feature comparison
- **[README_V2.md](README_V2.md)** - Full technical documentation
- **[CHANGELOG.md](CHANGELOG.md)** - Change history

---

## 🧪 Testing

Run the test suite:
```bash
./run_tests.sh
```

All editions share the same test suite.

---

## 🔧 Configuration

Each edition has its own config file:
- Lite: `config-lite.yaml`
- Standard: `config.yaml`
- Enterprise: `config-enterprise.yaml`

Override with: `--config=custom-config.yaml`

---

## 📦 What's New in v26.2

✨ **Multiple Editions**: Choose Lite, Standard, or Enterprise
✨ **Modular Architecture**: Clean separation of concerns
✨ **Configuration-Driven**: No hardcoded values
✨ **Security Hardened**: 0 vulnerabilities (CodeQL validated)
✨ **Fully Tested**: 7/7 tests passing
✨ **Well Documented**: Comprehensive guides

---

## 🎓 Examples

### Lite Edition (Personal Use)
```bash
# Install minimal dependencies
pip install -r requirements-lite.txt

# Run with lite config
python3 server.py --edition=lite

# Uses: config-lite.yaml
# Features: Basic AI + Security monitoring
# Resources: ~512 MB RAM
```

### Standard Edition (Teams)
```bash
# Install standard dependencies
pip install -r requirements.txt

# Run with standard config
python3 server.py --edition=standard

# Uses: config.yaml
# Features: Full AI + Security + Blockchain
# Resources: ~2 GB RAM
```

### Enterprise Edition (Organizations)
```bash
# Install enterprise dependencies
pip install -r requirements-enterprise.txt

# Run with enterprise config
python3 server.py --edition=enterprise

# Uses: config-enterprise.yaml
# Features: All + API + Plugins + HA
# Resources: ~8 GB RAM
```

---

## 🔄 Migration Between Editions

### Lite → Standard
```bash
pip install -r requirements.txt
python3 server.py --edition=standard
```

### Standard → Enterprise
```bash
pip install -r requirements-enterprise.txt
python3 server.py --edition=enterprise
```

---

## 💡 Tips

1. **Start with Lite** if you're learning
2. **Use Standard** for most deployments
3. **Choose Enterprise** when you need API/HA
4. **Check EDITIONS.md** for detailed comparison
5. **Build distributions** for easy deployment

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Write tests
4. Submit PR

---

## 📄 License

MIT License - Free for all editions

---

## 📞 Support

- **GitHub**: https://github.com/NaTo1000/infinite-server26
- **Issues**: Report bugs and request features
- **Docs**: Check documentation files

---

**Built with ❤️ by NaTo1000**  
**For the Security Community**  
**Version 26.2 - Multiple Editions**

---

*"One codebase, multiple editions, infinite possibilities."*
