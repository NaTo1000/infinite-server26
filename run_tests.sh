#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║  INFINITE SERVER26 - TEST RUNNER                                 ║"
echo "║  Version: 26.2                                                   ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Run tests
echo "Running unit tests..."
python3 -m unittest discover -s tests -p "test_*.py" -v

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo ""
    echo "✅ All tests passed!"
else
    echo ""
    echo "❌ Some tests failed!"
fi

exit $exit_code
