#!/bin/bash

# Modrinth Modpack Updater - Setup Script
# This script helps set up the environment for the modpack updater

echo "🚀 Setting up Modrinth Modpack Updater..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    echo "   Visit: https://www.python.org/downloads/"
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
min_version="3.8"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "❌ Python $python_version detected. Python 3.8+ is required."
    echo "   Current version: $python_version"
    echo "   Please upgrade Python: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python $python_version detected (compatible)"

# Create virtual environment (optional but recommended)
read -p "🔧 Create a virtual environment? (recommended) [y/N]: " create_venv
if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    
    # Activate virtual environment
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        # Windows
        source venv/Scripts/activate
    else
        # Unix-like (Linux, macOS)
        source venv/bin/activate
    fi
    
    echo "✅ Virtual environment created and activated"
    echo "   To activate it later, run: source venv/bin/activate"
fi

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Test installation
echo "🧪 Testing installation..."
python3 update_modpack.py --help > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Installation test passed"
else
    echo "❌ Installation test failed"
    exit 1
fi

# Success message
echo ""
echo "🎉 Setup complete! You can now use the Modrinth Modpack Updater."
echo ""
echo "📖 Quick start examples:"
echo "   python3 update_modpack.py --modpack-dir ./examples/fabric-example --client"
echo "   python3 update_modpack.py --modpack-dir path/to/modpack --client --server"
echo ""
echo "📚 For more information, see README.md or run:"
echo "   python3 update_modpack.py --help"
echo ""
echo "🌟 Don't forget to star the repository if you find it useful!"
