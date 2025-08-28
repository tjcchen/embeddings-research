"""
Utility functions for the Chat with Documents system
"""

import os
import hashlib
import json
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging

def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('chat_with_docs.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def calculate_file_hash(file_path: str) -> str:
    """Calculate MD5 hash of a file"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def save_document_metadata(documents: List[Dict], metadata_file: str = "document_metadata.json"):
    """Save document metadata to JSON file"""
    try:
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(documents, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving metadata: {e}")

def load_document_metadata(metadata_file: str = "document_metadata.json") -> List[Dict]:
    """Load document metadata from JSON file"""
    try:
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading metadata: {e}")
    return []

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f}{size_names[i]}"

def validate_file_type(file_path: str, allowed_extensions: List[str]) -> bool:
    """Validate if file type is allowed"""
    file_ext = Path(file_path).suffix.lower()
    return file_ext in allowed_extensions

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    # Remove excessive whitespace
    text = ' '.join(text.split())
    
    # Remove special characters that might cause issues
    text = text.replace('\x00', '')  # Remove null bytes
    text = text.replace('\ufffd', '')  # Remove replacement characters
    
    return text.strip()

def create_directories(paths: List[str]):
    """Create directories if they don't exist"""
    for path in paths:
        os.makedirs(path, exist_ok=True)

def get_system_info() -> Dict[str, Any]:
    """Get system information for debugging"""
    import platform
    import psutil
    
    return {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "cpu_count": os.cpu_count(),
        "memory_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "disk_free_gb": round(psutil.disk_usage('.').free / (1024**3), 2)
    }

class PerformanceTimer:
    """Simple performance timer context manager"""
    
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.start_time = None
    
    def __enter__(self):
        import time
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        duration = time.time() - self.start_time
        print(f"⏱️  {self.operation_name}: {duration:.2f}s")

def estimate_tokens(text: str) -> int:
    """Rough estimation of token count"""
    # Simple approximation: ~4 characters per token
    return len(text) // 4

def truncate_text(text: str, max_length: int = 1000) -> str:
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."
