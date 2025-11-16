"""
CloudVR-PerfGuard: Automated Performance Regression Detection for VR Applications
Adapted from AMIEN infrastructure for VR performance testing
"""

import asyncio
import json
import os
import sys
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.logging_config import get_logger, setup_logging
from config.constants import (
    API_HOST,
    API_PORT,
    BUILD_STORAGE_PATH,
    DEFAULT_GPU_TYPES,
    SUPPORTED_PLATFORMS,
)
from core.database import DatabaseManager
from core.performance_tester import VRPerformanceTester
from core.regression_detector import RegressionDetector

# Initialize logger
logger = get_logger(__name__)

app = FastAPI(
    title="CloudVR-PerfGuard API",
    description="Automated Performance Regression Detection for VR Applications",
    version="1.0.0",
)

# Global instances
performance_tester: Optional[VRPerformanceTester] = None
regression_detector: Optional[RegressionDetector] = None
db_manager: Optional[DatabaseManager] = None

# --- Pydantic Models ---


class BuildSubmissionRequest(BaseModel):
    app_name: str = Field(..., example="MyVRGame")
    build_version: str = Field(..., example="v1.2.3")
    platform: str = Field(..., example="windows", description="windows, linux, android")
    submission_type: str = Field(
        ..., example="baseline", description="baseline or regression_test"
    )
    baseline_version: Optional[str] = Field(
        None, example="v1.2.2", description="Required for regression_test"
    )


class PerformanceTestConfig(BaseModel):
    gpu_types: List[str] = Field(default=["T4"], example=["T4", "L4"])
    test_duration_seconds: int = Field(default=60, example=60)
    test_scenes: List[str] = Field(
        default=["main_menu"], example=["main_menu", "gameplay_scene"]
    )


class RegressionTestResult(BaseModel):
    job_id: str
    app_name: str
    build_version: str
    baseline_version: str
    status: str  # "queued", "running", "completed", "failed"
    regressions_detected: Optional[List[Dict[str, Any]]] = None
    performance_data: Optional[Dict[str, Any]] = None
    created_at: str


# --- Startup/Shutdown Events ---


@app.on_event("startup")
async def startup_event():
    """Initialize application components on startup"""
    global performance_tester, regression_detector, db_manager

    try:
        # Setup logging first
        setup_logging()
        logger.info("Starting CloudVR-PerfGuard API initialization")

        # Initialize core components
        db_manager = DatabaseManager()
        await db_manager.initialize()
        logger.info("Database manager initialized")

        performance_tester = VRPerformanceTester()
        await performance_tester.initialize()
        logger.info("Performance tester initialized")

        regression_detector = RegressionDetector(db_manager)
        logger.info("Regression detector initialized")

        logger.info("CloudVR-PerfGuard API initialized successfully")

    except Exception as e:
        logger.critical("Failed to initialize CloudVR-PerfGuard", exc_info=True)
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup resources on shutdown"""
    logger.info("Starting CloudVR-PerfGuard API shutdown")

    try:
        if performance_tester:
            await performance_tester.cleanup()
            logger.info("Performance tester cleaned up")

        if db_manager:
            await db_manager.close()
            logger.info("Database connection closed")

        logger.info("CloudVR-PerfGuard API shutdown complete")

    except Exception as e:
        logger.error("Error during shutdown", exc_info=True)


# --- API Endpoints ---


@app.get("/health")
async def health_check():
    """
    Health check endpoint with actual service status
    Returns 200 if all services are healthy, 503 otherwise
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {}
    }

    is_healthy = True

    # Check database connection
    try:
        if db_manager and db_manager.connection:
            # Try a simple query
            await db_manager.connection.execute("SELECT 1")
            health_status["services"]["database"] = "healthy"
        else:
            health_status["services"]["database"] = "not_initialized"
            is_healthy = False
    except Exception as e:
        health_status["services"]["database"] = f"unhealthy: {str(e)}"
        is_healthy = False
        logger.error("Database health check failed", exc_info=True)

    # Check performance tester
    if performance_tester:
        health_status["services"]["performance_tester"] = "healthy"
    else:
        health_status["services"]["performance_tester"] = "not_initialized"
        is_healthy = False

    # Check regression detector
    if regression_detector:
        health_status["services"]["regression_detector"] = "healthy"
    else:
        health_status["services"]["regression_detector"] = "not_initialized"
        is_healthy = False

    if not is_healthy:
        health_status["status"] = "unhealthy"
        raise HTTPException(status_code=503, detail=health_status)

    return health_status


@app.get("/")
async def root():
    return {
        "message": "CloudVR-PerfGuard API is operational!",
        "version": "1.0.0",
        "description": "Automated Performance Regression Detection for VR Applications",
    }


@app.get("/status")
async def get_status():
    """Get detailed API and service status"""
    status = {
        "api_status": "OPERATIONAL",
        "services": {
            "performance_tester": (
                "initialized" if performance_tester else "not_initialized"
            ),
            "regression_detector": (
                "initialized" if regression_detector else "not_initialized"
            ),
            "database": "connected" if db_manager else "not_connected",
        },
        "supported_platforms": SUPPORTED_PLATFORMS,
        "supported_gpu_types": DEFAULT_GPU_TYPES,
        "timestamp": datetime.utcnow().isoformat(),
    }
    return status


@app.post("/submit_build", response_model=Dict[str, Any])
async def submit_build_for_testing(
    file: UploadFile = File(...),
    app_name: str = Form(...),
    build_version: str = Form(...),
    platform: str = Form(...),
    submission_type: str = Form(...),
    baseline_version: Optional[str] = Form(None),
    test_config: Optional[str] = Form(None),  # JSON string
):
    """Submit a VR application build for performance testing"""

    if not performance_tester or not db_manager:
        raise HTTPException(status_code=503, detail="Service not fully initialized")

    # Validate submission type
    if submission_type not in ["baseline", "regression_test"]:
        raise HTTPException(
            status_code=400,
            detail="submission_type must be 'baseline' or 'regression_test'",
        )

    if submission_type == "regression_test" and not baseline_version:
        raise HTTPException(
            status_code=400, detail="baseline_version required for regression_test"
        )

    # Parse test configuration
    config = PerformanceTestConfig()
    if test_config:
        try:
            config_dict = json.loads(test_config)
            config = PerformanceTestConfig(**config_dict)
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Invalid test_config JSON: {e}"
            )

    try:
        # Generate job ID
        job_id = str(uuid.uuid4())

        # Store build file (implement file storage logic)
        build_path = await store_build_file(file, app_name, build_version, job_id)

        # Create database record
        await db_manager.create_test_job(
            job_id=job_id,
            app_name=app_name,
            build_version=build_version,
            platform=platform,
            submission_type=submission_type,
            baseline_version=baseline_version,
            build_path=build_path,
            test_config=config.dict(),
        )

        # Queue performance test (implement async task queue)
        await queue_performance_test(job_id, build_path, config)

        return {
            "job_id": job_id,
            "status": "queued",
            "message": f"Build submitted for {submission_type} testing",
            "app_name": app_name,
            "build_version": build_version,
            "estimated_completion": "5-10 minutes",
        }

    except Exception as e:
        logger.error(f"Failed to submit build for {app_name} v{build_version}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to submit build. Please try again.")


@app.get("/job_status/{job_id}")
async def get_job_status(job_id: str):
    """Get the status of a performance test job"""

    if not db_manager:
        raise HTTPException(status_code=503, detail="Database not available")

    try:
        job_data = await db_manager.get_test_job(job_id)
        if not job_data:
            raise HTTPException(status_code=404, detail="Job not found")

        return {
            "job_id": job_id,
            "status": job_data["status"],
            "app_name": job_data["app_name"],
            "build_version": job_data["build_version"],
            "submission_type": job_data["submission_type"],
            "created_at": job_data["created_at"],
            "progress": job_data.get("progress", 0),
            "estimated_completion": job_data.get("estimated_completion"),
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get job status for {job_id}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="Failed to get job status. Please try again."
        )


@app.get("/regression_report/{job_id}")
async def get_regression_report(job_id: str):
    """Get detailed regression test report"""

    if not db_manager or not regression_detector:
        raise HTTPException(status_code=503, detail="Service not fully initialized")

    try:
        job_data = await db_manager.get_test_job(job_id)
        if not job_data:
            raise HTTPException(status_code=404, detail="Job not found")

        if job_data["status"] != "completed":
            return {
                "job_id": job_id,
                "status": job_data["status"],
                "message": "Report not ready yet",
            }

        # Get regression analysis
        report = await regression_detector.generate_report(job_id)

        return report

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to generate regression report for {job_id}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="Failed to generate report. Please try again."
        )


@app.get("/regression_report/{job_id}/html", response_class=HTMLResponse)
async def get_regression_report_html(job_id: str):
    """Get regression report as HTML"""

    try:
        report_data = await get_regression_report(job_id)

        # Generate HTML report (implement HTML template)
        html_content = generate_html_report(report_data)

        return HTMLResponse(content=html_content)

    except Exception as e:
        logger.error("Failed to generate HTML report", exc_info=True)
        raise HTTPException(
            status_code=500, detail="Failed to generate HTML report. Please try again."
        )


@app.get("/apps/{app_name}/baselines")
async def get_app_baselines(app_name: str):
    """Get available baseline versions for an app"""

    if not db_manager:
        raise HTTPException(status_code=503, detail="Database not available")

    try:
        baselines = await db_manager.get_app_baselines(app_name)
        return {"app_name": app_name, "baselines": baselines}

    except Exception as e:
        logger.error(f"Failed to get baselines for app {app_name}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="Failed to get baselines. Please try again."
        )


# --- Helper Functions ---


async def store_build_file(
    file: UploadFile, app_name: str, build_version: str, job_id: str
) -> str:
    """
    Store uploaded build file and return path

    Args:
        file: Uploaded file
        app_name: Application name
        build_version: Build version
        job_id: Unique job ID

    Returns:
        Path to stored file

    Raises:
        Exception: If file storage fails
    """
    try:
        # Sanitize filename to prevent path traversal
        safe_filename = os.path.basename(file.filename)

        # Use configured storage path
        storage_dir = os.path.join(BUILD_STORAGE_PATH, app_name, build_version)
        os.makedirs(storage_dir, exist_ok=True)

        file_path = os.path.join(storage_dir, safe_filename)

        # Write file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        logger.info(f"Stored build file: {file_path} (job_id: {job_id})")
        return file_path

    except Exception as e:
        logger.error(f"Failed to store build file for job {job_id}", exc_info=True)
        raise


async def queue_performance_test(job_id: str, build_path: str, config: Dict[str, Any]):
    """
    Queue performance test for execution

    Args:
        job_id: Unique job identifier
        build_path: Path to build file
        config: Test configuration
    """
    logger.info(f"Queuing performance test for job {job_id}")
    # TODO: Implement proper async task queue (Celery, Cloud Tasks, etc.)
    # For now, start background task
    asyncio.create_task(run_performance_test_background(job_id, build_path, config))


async def run_performance_test_background(
    job_id: str, build_path: str, config: Dict[str, Any]
):
    """
    Run performance test in background

    Args:
        job_id: Unique job identifier
        build_path: Path to build file
        config: Test configuration
    """
    try:
        logger.info(f"Starting performance test for job {job_id}")

        # Update job status
        await db_manager.update_job_status(job_id, "running")

        # Run performance test
        results = await performance_tester.run_test(build_path, config)
        logger.info(f"Performance test completed for job {job_id}")

        # Store results
        await db_manager.store_performance_results(job_id, results)

        # If this is a regression test, run regression analysis
        job_data = await db_manager.get_test_job(job_id)
        if job_data["submission_type"] == "regression_test":
            logger.info(f"Running regression analysis for job {job_id}")
            await regression_detector.analyze_regression(job_id)

        # Update job status
        await db_manager.update_job_status(job_id, "completed")
        logger.info(f"Job {job_id} completed successfully")

    except Exception as e:
        logger.error(f"Performance test failed for job {job_id}", exc_info=True)
        await db_manager.update_job_status(job_id, "failed", error=str(e))


def generate_html_report(report_data: Dict[str, Any]) -> str:
    """Generate HTML report from report data"""
    # TODO: Implement proper HTML template
    return """
    <html>
    <head><title>CloudVR-PerfGuard Report</title></head>
    <body>
        <h1>Performance Regression Report</h1>
        <pre>{json.dumps(report_data, indent=2)}</pre>
    </body>
    </html>
    """


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
