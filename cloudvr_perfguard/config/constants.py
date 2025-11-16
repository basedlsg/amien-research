"""
Configuration constants for CloudVR-PerfGuard
Centralizes hardcoded values for easy configuration
"""

import os
from typing import List

# Database Configuration
DEFAULT_DB_PATH = os.getenv("DATABASE_PATH", "cloudvr_perfguard.db")

# VR Performance Thresholds
VR_FPS_THRESHOLD_PERCENT = float(os.getenv("VR_FPS_THRESHOLD", "0.05"))  # 5%
VR_FRAME_TIME_THRESHOLD_PERCENT = float(os.getenv("VR_FRAME_TIME_THRESHOLD", "0.05"))  # 5%
VR_COMFORT_SCORE_THRESHOLD = float(os.getenv("VR_COMFORT_THRESHOLD", "0.10"))  # 10%
VR_TRACKING_LATENCY_THRESHOLD_MS = float(os.getenv("VR_LATENCY_THRESHOLD_MS", "2.0"))  # 2ms
VR_DROPPED_FRAMES_THRESHOLD_PERCENT = float(os.getenv("VR_DROPPED_FRAMES_THRESHOLD", "0.15"))  # 15%

# Regression Detection Sensitivity
REGRESSION_SEVERITY_CRITICAL = float(os.getenv("REGRESSION_CRITICAL", "0.20"))  # 20%
REGRESSION_SEVERITY_HIGH = float(os.getenv("REGRESSION_HIGH", "0.15"))  # 15%
REGRESSION_SEVERITY_MEDIUM = float(os.getenv("REGRESSION_MEDIUM", "0.10"))  # 10%
REGRESSION_SEVERITY_LOW = float(os.getenv("REGRESSION_LOW", "0.05"))  # 5%

# Test Configuration
DEFAULT_TEST_DURATION_SECONDS = int(os.getenv("DEFAULT_TEST_DURATION", "60"))
DEFAULT_GPU_TYPES: List[str] = os.getenv("DEFAULT_GPU_TYPES", "T4,L4,A100").split(",")
DEFAULT_TEST_SCENES: List[str] = ["main_menu", "gameplay_scene"]

# Platform Configuration
SUPPORTED_PLATFORMS: List[str] = ["windows", "linux", "android"]
SUPPORTED_VR_RUNTIMES: List[str] = ["steamvr", "oculus", "openxr"]

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_WORKERS = int(os.getenv("API_WORKERS", "1"))

# Storage Configuration
BUILD_STORAGE_PATH = os.getenv("BUILD_STORAGE_PATH", "/tmp/cloudvr_builds")
RESEARCH_OUTPUT_PATH = os.getenv("RESEARCH_OUTPUT_PATH", "./research_outputs")

# AI Configuration
FUNSEARCH_MAX_ITERATIONS = int(os.getenv("FUNSEARCH_MAX_ITERATIONS", "100"))
FUNSEARCH_POPULATION_SIZE = int(os.getenv("FUNSEARCH_POPULATION_SIZE", "50"))
FUNSEARCH_MUTATION_RATE = float(os.getenv("FUNSEARCH_MUTATION_RATE", "0.1"))

# Retry Configuration
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
RETRY_BASE_DELAY_SECONDS = float(os.getenv("RETRY_BASE_DELAY", "2.0"))
RETRY_MAX_DELAY_SECONDS = float(os.getenv("RETRY_MAX_DELAY", "60.0"))

# Timeout Configuration
DEFAULT_TIMEOUT_SECONDS = int(os.getenv("DEFAULT_TIMEOUT", "30"))
AI_API_TIMEOUT_SECONDS = int(os.getenv("AI_API_TIMEOUT", "120"))
TEST_EXECUTION_TIMEOUT_SECONDS = int(os.getenv("TEST_TIMEOUT", "600"))

# Health Check Configuration
HEALTH_CHECK_INTERVAL_SECONDS = int(os.getenv("HEALTH_CHECK_INTERVAL", "30"))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", None)
LOG_JSON_FORMAT = os.getenv("LOG_JSON_FORMAT", "false").lower() == "true"
