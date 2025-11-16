"""
Pytest configuration and shared fixtures for CloudVR-PerfGuard tests
Provides mock objects, test data, and common setup/teardown
"""

import asyncio
import os
import tempfile
from typing import AsyncGenerator, Dict, Any
from unittest.mock import AsyncMock, MagicMock, Mock

import pytest
import aiosqlite

# Add parent directory to path for imports
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import DatabaseManager
from core.performance_tester import VRPerformanceTester
from core.regression_detector import RegressionDetector


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def temp_db_path() -> AsyncGenerator[str, None]:
    """Provide a temporary database path for testing"""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
        db_path = temp_file.name

    yield db_path

    # Cleanup
    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture
async def db_manager(temp_db_path: str) -> AsyncGenerator[DatabaseManager, None]:
    """Provide an initialized DatabaseManager for testing"""
    manager = DatabaseManager(db_path=temp_db_path)
    await manager.initialize()

    yield manager

    # Cleanup
    if manager.connection:
        await manager.close()


@pytest.fixture
def mock_db_manager() -> DatabaseManager:
    """Provide a mock DatabaseManager for unit tests"""
    mock = AsyncMock(spec=DatabaseManager)

    # Setup common mock methods
    mock.create_test_job = AsyncMock(return_value=True)
    mock.get_test_job = AsyncMock(return_value={
        "job_id": "test-job-123",
        "app_name": "TestApp",
        "build_version": "v1.0.0",
        "platform": "windows",
        "submission_type": "baseline",
        "status": "queued",
        "created_at": "2025-11-15T10:00:00Z"
    })
    mock.update_job_status = AsyncMock(return_value=True)
    mock.store_performance_results = AsyncMock(return_value=True)
    mock.get_performance_results = AsyncMock(return_value={
        "job_id": "test-job-123",
        "aggregated_metrics": {
            "avg_fps": 72.5,
            "p99_frame_time_ms": 13.8,
            "comfort_score": 0.85
        }
    })

    return mock


@pytest.fixture
async def performance_tester() -> AsyncGenerator[VRPerformanceTester, None]:
    """Provide a VRPerformanceTester instance for testing"""
    tester = VRPerformanceTester()
    await tester.initialize()

    yield tester

    await tester.cleanup()


@pytest.fixture
def mock_performance_tester() -> VRPerformanceTester:
    """Provide a mock VRPerformanceTester for unit tests"""
    mock = AsyncMock(spec=VRPerformanceTester)

    mock.run_test = AsyncMock(return_value={
        "test_id": "test-123",
        "total_duration": 60.0,
        "individual_results": [],
        "aggregated_metrics": {
            "avg_fps": 72.5,
            "p99_frame_time_ms": 13.8,
            "comfort_score": 0.85,
            "dropped_frames_percent": 0.02
        }
    })

    return mock


@pytest.fixture
async def regression_detector(db_manager: DatabaseManager) -> RegressionDetector:
    """Provide a RegressionDetector instance for testing"""
    return RegressionDetector(db_manager)


@pytest.fixture
def mock_regression_detector() -> RegressionDetector:
    """Provide a mock RegressionDetector for unit tests"""
    mock = AsyncMock(spec=RegressionDetector)

    mock.analyze_regression = AsyncMock(return_value={
        "regressions_detected": [],
        "overall_status": "PASS",
        "regression_score": 0.0
    })
    mock.generate_report = AsyncMock(return_value={
        "job_id": "test-job-123",
        "regressions": [],
        "status": "PASS"
    })

    return mock


@pytest.fixture
def sample_test_job() -> Dict[str, Any]:
    """Provide sample test job data"""
    return {
        "job_id": "test-job-123",
        "app_name": "TestVRApp",
        "build_version": "v1.2.3",
        "platform": "windows",
        "submission_type": "baseline",
        "baseline_version": None,
        "build_path": "/tmp/builds/test.zip",
        "test_config": {
            "gpu_types": ["T4"],
            "test_duration_seconds": 60,
            "test_scenes": ["main_menu"]
        },
        "status": "queued",
        "progress": 0,
        "created_at": "2025-11-15T10:00:00Z",
        "updated_at": "2025-11-15T10:00:00Z"
    }


@pytest.fixture
def sample_performance_results() -> Dict[str, Any]:
    """Provide sample performance test results"""
    return {
        "test_id": "perf-test-123",
        "build_path": "/tmp/builds/test.zip",
        "config": {
            "gpu_types": ["T4"],
            "test_duration_seconds": 60
        },
        "total_duration": 62.5,
        "individual_results": [
            {
                "gpu_type": "T4",
                "scene": "main_menu",
                "avg_fps": 72.5,
                "p99_frame_time_ms": 13.8,
                "comfort_score": 0.85
            }
        ],
        "aggregated_metrics": {
            "avg_fps": 72.5,
            "p99_frame_time_ms": 13.8,
            "comfort_score": 0.85,
            "tracking_latency_ms": 12.3,
            "dropped_frames_percent": 0.02
        },
        "timestamp": "2025-11-15T10:05:00Z"
    }


@pytest.fixture
def sample_regression_data() -> Dict[str, Any]:
    """Provide sample regression analysis data"""
    return {
        "regressions": [
            {
                "metric": "avg_fps",
                "baseline_value": 75.0,
                "current_value": 68.0,
                "change_percent": -9.33,
                "severity": "MEDIUM",
                "threshold": 5.0
            }
        ],
        "statistical_analysis": {
            "avg_fps": {
                "t_statistic": -2.5,
                "p_value": 0.03,
                "significant": True
            }
        },
        "comparison": {
            "baseline_job_id": "baseline-job-456",
            "current_job_id": "test-job-123"
        },
        "regression_score": 9.33,
        "overall_status": "REGRESSION_DETECTED",
        "analysis_timestamp": "2025-11-15T10:10:00Z"
    }


@pytest.fixture
def mock_ai_api_response() -> Dict[str, Any]:
    """Provide mock AI API response"""
    return {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "text": "def optimized_function(x):\n    return x * 2\n"
                        }
                    ]
                }
            }
        ]
    }


@pytest.fixture
def mock_google_genai():
    """Mock Google Generative AI client"""
    mock = MagicMock()
    mock.GenerativeModel.return_value.generate_content_async = AsyncMock(
        return_value=MagicMock(text="Generated content")
    )
    return mock


@pytest.fixture(autouse=True)
def reset_logging():
    """Reset logging configuration between tests"""
    import logging
    # Clear all handlers to avoid interference between tests
    logger = logging.getLogger("cloudvr_perfguard")
    logger.handlers.clear()
    yield
    logger.handlers.clear()


@pytest.fixture
def temp_build_file():
    """Create a temporary build file for upload tests"""
    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as temp_file:
        temp_file.write(b"fake build content")
        file_path = temp_file.name

    yield file_path

    # Cleanup
    if os.path.exists(file_path):
        os.unlink(file_path)
