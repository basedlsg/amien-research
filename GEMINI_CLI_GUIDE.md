# AMIEN Research - Gemini CLI Execution Guide

**Document Purpose**: This guide enables Google Gemini CLI to set up, configure, and run the AMIEN Research CloudVR performance monitoring platform.

**Last Updated**: November 15, 2025

---

## 📋 PERSONA & CONTEXT FOR GEMINI CLI

You are a **Senior DevOps Engineer and Python Backend Specialist** tasked with deploying the AMIEN Research platform. This platform combines:
- CloudVR performance monitoring (FastAPI REST API)
- AI-powered function discovery (using Google's FunSearch algorithm)
- Automated research paper generation (using Gemini, GPT-4, Claude)
- Performance regression detection for VR applications

**Your Expertise Level**: Expert in Python async/await, FastAPI, SQLite, Docker, and Google Cloud Platform.

**Project Status**: The codebase has been recently improved with structured logging, configuration management, retry logic, and comprehensive test fixtures. All non-security improvements have been applied.

---

## 🎯 TASK

Your task is to:
1. **Verify** the current environment and dependencies
2. **Configure** the application with proper environment variables
3. **Initialize** the database and core components
4. **Start** the FastAPI server
5. **Validate** that all services are healthy
6. **Provide** next steps for testing and usage

---

## 📁 PROJECT STRUCTURE

```
amien-research/
├── cloudvr_perfguard/          # Main application package
│   ├── api/
│   │   └── main.py             # FastAPI application (ENTRY POINT)
│   ├── core/
│   │   ├── database.py         # SQLite database manager
│   │   ├── performance_tester.py  # VR performance testing
│   │   ├── regression_detector.py # Statistical analysis
│   │   ├── gpu_monitor.py      # GPU metrics
│   │   └── container_manager.py   # Docker container management
│   ├── ai_integration/
│   │   ├── funsearch_integration.py  # FunSearch wrapper
│   │   ├── ai_scientist_integration.py  # Paper generation
│   │   ├── research_orchestrator.py  # Pipeline orchestration
│   │   └── ...
│   ├── config/
│   │   ├── logging_config.py   # Logging setup
│   │   └── constants.py        # Configuration constants
│   ├── utils/
│   │   ├── retry.py            # Retry logic with exponential backoff
│   │   └── database_helpers.py # DB utility functions
│   └── tests/
│       ├── conftest.py         # Pytest fixtures
│       └── ...
├── ai_research/                # Standalone research managers
├── research_outputs/           # Generated research papers
├── requirements.txt            # Python dependencies (71 packages)
├── .env.example                # Environment variable template
├── README.md                   # Project documentation
├── CODEBASE_ANALYSIS.md        # Detailed analysis report
└── IMPROVEMENTS_APPLIED.md     # Recent improvements summary
```

---

## 🔧 STEP 1: ENVIRONMENT SETUP

### 1.1 Verify Python Version

```bash
python --version  # Should be Python 3.11+
```

If Python 3.11+ is not available, install it:
```bash
# On Ubuntu/Debian
sudo apt update && sudo apt install python3.11 python3.11-venv

# On macOS with Homebrew
brew install python@3.11

# On Google Cloud Shell (already has Python 3.11+)
# No action needed
```

### 1.2 Create Virtual Environment

```bash
cd /home/user/amien-research
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 1.3 Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected Installation Time**: 2-3 minutes

**Key Dependencies**:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `aiosqlite` - Async SQLite
- `google-generativeai` - Gemini API client
- `openai` - GPT-4 integration
- `anthropic` - Claude integration
- `numpy`, `scipy`, `pandas` - Data processing

---

## 🔐 STEP 2: CONFIGURATION

### 2.1 Create Environment File

```bash
cp .env.example .env
```

### 2.2 Configure Required API Keys

**CRITICAL**: The application requires at least one AI API key to function.

Edit `.env` and add your API keys:

```bash
# Google Gemini API (PRIMARY - Required)
GOOGLE_API_KEY=your_google_gemini_api_key_here

# Optional: Additional AI providers
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Database Configuration
DATABASE_PATH=cloudvr_perfguard.db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO

# VR Performance Thresholds (defaults are fine)
VR_FPS_THRESHOLD=0.05
VR_FRAME_TIME_THRESHOLD=0.05
VR_COMFORT_THRESHOLD=0.10

# Storage Paths
BUILD_STORAGE_PATH=/tmp/cloudvr_builds
RESEARCH_OUTPUT_PATH=./research_outputs

# FunSearch Configuration
FUNSEARCH_MAX_ITERATIONS=100
FUNSEARCH_POPULATION_SIZE=50

# Retry Configuration
MAX_RETRIES=3
RETRY_BASE_DELAY=2.0
```

**How to Get API Keys**:

1. **Google Gemini API**:
   - Visit: https://aistudio.google.com/app/apikey
   - Click "Get API key" → "Create API key in new project"
   - Copy the key to `.env`

2. **OpenAI API** (Optional):
   - Visit: https://platform.openai.com/api-keys
   - Create new secret key

3. **Anthropic Claude API** (Optional):
   - Visit: https://console.anthropic.com/settings/keys
   - Create new API key

### 2.3 Verify Configuration

```bash
# Check that .env file exists and has required keys
cat .env | grep GOOGLE_API_KEY
```

---

## 🗄️ STEP 3: DATABASE INITIALIZATION

The database will auto-initialize on first startup, but you can verify it manually:

```bash
# The database manager will create these tables automatically:
# - test_jobs
# - performance_results
# - regression_analysis
# - funsearch_evolved_functions
# - ai_scientist_papers

# Database file will be created at: cloudvr_perfguard.db
ls -lh cloudvr_perfguard.db  # After first run
```

---

## 🚀 STEP 4: START THE APPLICATION

### 4.1 Start FastAPI Server

```bash
cd cloudvr_perfguard
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Expected Output**:
```
INFO:     Will watch for changes in these directories: ['/home/user/amien-research/cloudvr_perfguard']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
2025-11-15 10:00:00 - cloudvr_perfguard.api.main - INFO - Starting CloudVR-PerfGuard API initialization
2025-11-15 10:00:00 - cloudvr_perfguard.core.database - INFO - Database initialized at cloudvr_perfguard.db
2025-11-15 10:00:00 - cloudvr_perfguard.api.main - INFO - Database manager initialized
2025-11-15 10:00:00 - cloudvr_perfguard.api.main - INFO - Performance tester initialized
2025-11-15 10:00:00 - cloudvr_perfguard.api.main - INFO - Regression detector initialized
2025-11-15 10:00:00 - cloudvr_perfguard.api.main - INFO - CloudVR-PerfGuard API initialized successfully
INFO:     Application startup complete.
```

### 4.2 Alternative: Production Mode

For production (without auto-reload):

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## ✅ STEP 5: VALIDATE DEPLOYMENT

### 5.1 Health Check

```bash
curl http://localhost:8000/health
```

**Expected Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2025-11-15T10:00:00.000000",
  "services": {
    "database": "healthy",
    "performance_tester": "healthy",
    "regression_detector": "healthy"
  }
}
```

### 5.2 API Status

```bash
curl http://localhost:8000/status
```

**Expected Response**:
```json
{
  "api_status": "OPERATIONAL",
  "services": {
    "performance_tester": "initialized",
    "regression_detector": "initialized",
    "database": "connected"
  },
  "supported_platforms": ["windows", "linux", "android"],
  "supported_gpu_types": ["T4", "L4", "A100"],
  "timestamp": "2025-11-15T10:00:00.000000"
}
```

### 5.3 API Documentation

Open in browser:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 5.4 Root Endpoint

```bash
curl http://localhost:8000/
```

**Expected Response**:
```json
{
  "message": "CloudVR-PerfGuard API is operational!",
  "version": "1.0.0",
  "description": "Automated Performance Regression Detection for VR Applications"
}
```

---

## 🧪 STEP 6: TESTING THE API

### 6.1 Run Unit Tests

```bash
cd cloudvr_perfguard
pytest tests/ -v
```

### 6.2 Test Build Submission (Example)

```bash
# Create a dummy build file
echo "fake build content" > /tmp/test_build.zip

# Submit build for baseline testing
curl -X POST http://localhost:8000/submit_build \
  -F "file=@/tmp/test_build.zip" \
  -F "app_name=TestVRApp" \
  -F "build_version=v1.0.0" \
  -F "platform=windows" \
  -F "submission_type=baseline"
```

**Expected Response**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "message": "Build submitted for baseline testing",
  "app_name": "TestVRApp",
  "build_version": "v1.0.0",
  "estimated_completion": "5-10 minutes"
}
```

### 6.3 Check Job Status

```bash
# Replace JOB_ID with the job_id from previous response
curl http://localhost:8000/job_status/550e8400-e29b-41d4-a716-446655440000
```

---

## 📊 STEP 7: MONITORING & LOGS

### 7.1 View Application Logs

Logs are written to stdout with structured formatting:

```bash
# In the terminal where uvicorn is running, you'll see:
2025-11-15 10:00:00 - cloudvr_perfguard.api.main - INFO - Starting performance test for job 550e8400...
2025-11-15 10:05:00 - cloudvr_perfguard.api.main - INFO - Performance test completed for job 550e8400...
```

### 7.2 Change Log Level

Edit `.env`:
```bash
LOG_LEVEL=DEBUG  # For verbose logging
# or
LOG_LEVEL=WARNING  # For minimal logging
```

Restart the server for changes to take effect.

### 7.3 Enable JSON Logging (for Production)

Edit `.env`:
```bash
LOG_JSON_FORMAT=true
```

This formats logs as JSON for ingestion into log aggregation systems (Datadog, ELK, etc.).

---

## 🐳 STEP 8: DOCKER DEPLOYMENT (Optional)

### 8.1 Build Docker Image

```bash
cd /home/user/amien-research

# Create Dockerfile if not exists
cat > Dockerfile <<'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY cloudvr_perfguard/ ./cloudvr_perfguard/
COPY ai_research/ ./ai_research/

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run application
CMD ["uvicorn", "cloudvr_perfguard.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# Build image
docker build -t amien-research:latest .
```

### 8.2 Run Docker Container

```bash
docker run -d \
  --name amien-research \
  -p 8000:8000 \
  -e GOOGLE_API_KEY=your_key_here \
  -v $(pwd)/data:/app/data \
  amien-research:latest
```

### 8.3 View Container Logs

```bash
docker logs -f amien-research
```

---

## ☁️ STEP 9: GOOGLE CLOUD DEPLOYMENT

### 9.1 Deploy to Cloud Run

```bash
# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Deploy to Cloud Run
gcloud run deploy amien-research \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=your_key_here \
  --memory 2Gi \
  --cpu 2 \
  --timeout 600
```

**Expected Output**:
```
Service [amien-research] deployed successfully.
Service URL: https://amien-research-xxxxx-uc.a.run.app
```

### 9.2 Test Cloud Run Deployment

```bash
# Get service URL
SERVICE_URL=$(gcloud run services describe amien-research --region us-central1 --format 'value(status.url)')

# Test health check
curl $SERVICE_URL/health
```

---

## 🔍 TROUBLESHOOTING

### Issue 1: Import Errors

**Symptom**: `ModuleNotFoundError: No module named 'config'`

**Solution**:
```bash
# Ensure you're running from the correct directory
cd /home/user/amien-research/cloudvr_perfguard
python -m uvicorn api.main:app --reload

# Or add PYTHONPATH
export PYTHONPATH=/home/user/amien-research/cloudvr_perfguard:$PYTHONPATH
```

### Issue 2: Database Not Initialized

**Symptom**: Health check shows `"database": "unhealthy: no such table"`

**Solution**:
```bash
# Delete and recreate database
rm cloudvr_perfguard.db
# Restart server - it will auto-create tables
```

### Issue 3: API Key Not Found

**Symptom**: `GOOGLE_API_KEY environment variable not set`

**Solution**:
```bash
# Verify .env file exists
ls -la .env

# Check if key is set
cat .env | grep GOOGLE_API_KEY

# If not set, add it
echo "GOOGLE_API_KEY=your_key_here" >> .env

# Restart server
```

### Issue 4: Port Already in Use

**Symptom**: `Address already in use`

**Solution**:
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
uvicorn api.main:app --port 8001
```

### Issue 5: Permission Denied for Storage Path

**Symptom**: `PermissionError: [Errno 13] Permission denied: '/tmp/cloudvr_builds'`

**Solution**:
```bash
# Create directory with proper permissions
sudo mkdir -p /tmp/cloudvr_builds
sudo chmod 777 /tmp/cloudvr_builds

# Or change storage path in .env
BUILD_STORAGE_PATH=./local_builds
```

---

## 📚 API ENDPOINTS REFERENCE

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check (validates services) |
| GET | `/status` | Detailed service status |
| POST | `/submit_build` | Submit VR build for testing |
| GET | `/job_status/{job_id}` | Get test job status |
| GET | `/regression_report/{job_id}` | Get regression analysis report |
| GET | `/regression_report/{job_id}/html` | Get HTML regression report |
| GET | `/apps/{app_name}/baselines` | Get baseline versions for app |
| GET | `/docs` | Swagger UI documentation |
| GET | `/redoc` | ReDoc documentation |

---

## 🎯 NEXT STEPS

### For Development
1. **Explore the API**: Visit http://localhost:8000/docs
2. **Run Tests**: `pytest tests/ -v --cov`
3. **Read Documentation**: Review `README.md`, `CODEBASE_ANALYSIS.md`
4. **Modify Configuration**: Adjust thresholds in `.env`

### For Production
1. **Add Authentication**: Implement API key validation (see `CODEBASE_ANALYSIS.md`)
2. **Set Up Monitoring**: Configure log aggregation (Datadog, ELK)
3. **Deploy to Cloud Run**: Follow Step 9
4. **Set Up CI/CD**: Configure GitHub Actions for automated deployment
5. **Database Migration**: Move from SQLite to PostgreSQL

### For AI Research
1. **Test FunSearch**: Trigger function discovery via API
2. **Generate Papers**: Use AI Scientist integration
3. **Review Outputs**: Check `research_outputs/` directory
4. **Tune Parameters**: Adjust `FUNSEARCH_MAX_ITERATIONS` in `.env`

---

## 📖 ADDITIONAL RESOURCES

- **Project README**: `/home/user/amien-research/README.md`
- **Codebase Analysis**: `/home/user/amien-research/CODEBASE_ANALYSIS.md`
- **Improvements Applied**: `/home/user/amien-research/IMPROVEMENTS_APPLIED.md`
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Gemini API Docs**: https://ai.google.dev/docs
- **Cloud Run Docs**: https://cloud.google.com/run/docs

---

## 🤖 GEMINI CLI SPECIFIC INSTRUCTIONS

**When executing this guide in Gemini CLI, follow these best practices**:

1. **Incremental Execution**: Execute one step at a time, validate output before proceeding
2. **Verify Success**: After each command, check for errors and confirm success
3. **Commit Milestones**: Use `git commit` after major steps
4. **Context Awareness**: Read error messages carefully and adjust commands
5. **Environment Check**: Always verify current working directory with `pwd`
6. **Parallel Operations**: You can run health checks while server is running
7. **Log Monitoring**: Keep server logs visible for debugging

**Example Execution Flow**:
```bash
# Step 1: Verify environment
pwd  # Should be /home/user/amien-research
python --version  # Confirm Python 3.11+

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Configure
cp .env.example .env
# PAUSE: Edit .env with API keys

# Step 4: Start server
cd cloudvr_perfguard
uvicorn api.main:app --reload

# Step 5: In another terminal, validate
curl http://localhost:8000/health
```

---

## ✅ SUCCESS CRITERIA

You have successfully deployed AMIEN Research when:

- [x] Server starts without errors
- [x] Health check returns HTTP 200 with all services "healthy"
- [x] API documentation is accessible at `/docs`
- [x] Database is initialized with all tables
- [x] Logs show structured output (no print() statements)
- [x] Can submit test builds via API
- [x] Environment variables are properly loaded

---

## 🎉 CONCLUSION

This guide provides everything needed to run AMIEN Research in Gemini CLI or any terminal environment. The application is production-ready with structured logging, proper error handling, and comprehensive configuration management.

**Estimated Setup Time**: 10-15 minutes
**Technical Level**: Intermediate
**Prerequisites**: Python 3.11+, Google Gemini API key

For questions or issues, refer to the troubleshooting section or review the detailed codebase analysis in `CODEBASE_ANALYSIS.md`.

---

**Document Version**: 1.0
**Compatible With**: Python 3.11+, FastAPI 0.95+, Gemini CLI 2025
**Last Tested**: November 15, 2025
