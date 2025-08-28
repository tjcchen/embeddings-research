#!/usr/bin/env python3
"""
Quick Start Guide for Chat with Documents System
Run this script to set up and test the system quickly
"""

import os
import sys
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed"""
    required_packages = [
        'langchain', 'openai', 'faiss', 'streamlit', 
        'PyPDF2', 'python-docx', 'beautifulsoup4', 'requests'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_').lower())
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def setup_environment():
    """Guide user through environment setup"""
    print("🚀 Chat with Documents - Quick Start")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    
    print("✅ Python version check passed")
    
    # Check packages
    missing = check_requirements()
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("📦 Please install requirements:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ All required packages installed")
    
    # Check API key
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  OpenAI API key not found")
        print("📝 Please set up your API key:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your OpenAI API key to .env")
        print("   3. Or set environment variable: export OPENAI_API_KEY=your_key")
        return False
    
    print("✅ OpenAI API key configured")
    return True

def run_demo():
    """Run a quick demo"""
    print("\n🎯 Running Quick Demo")
    print("-" * 20)
    
    try:
        from sample_test import test_system
        test_system()
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("💡 Try running the CLI version: python cli_demo.py")

def show_usage_options():
    """Show different ways to use the system"""
    print("\n📋 Usage Options")
    print("-" * 20)
    print("1. 🌐 Web Interface (Recommended):")
    print("   streamlit run main.py")
    print()
    print("2. 💻 Command Line Interface:")
    print("   python cli_demo.py")
    print()
    print("3. 🧪 Run Tests:")
    print("   python sample_test.py")
    print()
    print("4. 📚 Read Documentation:")
    print("   cat README.md")

def main():
    """Main setup function"""
    if setup_environment():
        print("\n🎉 Setup completed successfully!")
        
        choice = input("\n❓ Run quick demo? (y/N): ").strip().lower()
        if choice == 'y':
            run_demo()
        
        show_usage_options()
        
        print("\n🚀 Ready to start chatting with documents!")
    else:
        print("\n❌ Setup incomplete. Please fix the issues above.")

if __name__ == "__main__":
    main()
