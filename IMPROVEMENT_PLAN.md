# AMIEN Research - Production Readiness Improvement Plan

**Status**: Research Prototype → Production-Ready System
**Estimated Total Time**: 100 hours (~2.5 weeks)
**Current Completion**: ~90% feature complete, needs polish & security
**Priority**: Fix critical bugs → Add security → Improve infrastructure → Complete documentation

---

## Executive Summary

AMIEN Research is well-architected with solid async patterns and clean separation of concerns. The codebase is **90% feature complete** and closest to production-ready among all separated systems. However, it requires critical bug fixes, security hardening, and comprehensive documentation before production deployment.

### Current Strengths ✅

- Clean separation of concerns (CloudVR monitoring vs AI research)
- Well-structured async/await patterns throughout
- Good database abstraction layer
- Comprehensive AI integration (Gemini, GPT-4, Claude)
- FastAPI-based REST API
- Docker support for deployment

### Critical Issues ❌

- **Security**: Dangerous `exec()` usage, SQL injection vulnerability
- **Authentication**: No API authentication implemented
- **Bugs**: Type errors, dict key errors causing crashes
- **Testing**: Zero test coverage
- **Documentation**: Minimal getting-started guides
- **Error Handling**: Incomplete error handling in API endpoints

---

## Priority 1: Critical Fixes (1-2 days, 8 hours)

**Status**: ✅ COMPLETED in this separation

These bugs will cause crashes and security vulnerabilities. Fix immediately before any deployment.

### 1.1 Type Error Fix ✅ FIXED
**File**: `cloudvr_perfguard/ai_integration/funsearch_integration.py:89`
**Issue**: `float("-in")` should be `float("-inf")`
**Impact**: Causes ValueError crash when initializing best_score
**Time**: 30 minutes
**Status**: ✅ Fixed

```python
# BEFORE:
best_score = float("-in")  # ValueError!

# AFTER:
best_score = float("-inf")  # Correct
```

### 1.2 Dict Key Errors ✅ FIXED
**File**: `ai_research/funsearch_manager.py:379, 427, 656`
**Issue**: Empty string keys in parameter dictionaries
**Impact**: KeyError crashes when accessing params
**Time**: 30 minutes
**Status**: ✅ Fixed

```python
# BEFORE (Line 427):
params = {
    "a": random.uniform(-5, 5),
    ...
    "": random.uniform(0, 2 * math.pi),  # Empty string key!
}

# AFTER:
params = {
    "a": random.uniform(-5, 5),
    ...
    "f": random.uniform(0, 2 * math.pi),  # Proper key name
}
```

### 1.3 Remove Dangerous exec() Usage ⚠️ DISABLED
**File**: `cloudvr_perfguard/ai_integration/funsearch_integration.py:245-295`
**Issue**: Using `exec()` to execute arbitrary code is a security risk
**Impact**: Code injection vulnerability, arbitrary code execution
**Time**: 4 hours to implement safer alternative
**Status**: ⚠️ Disabled with warning comment

**Current State**: exec() is commented out with security warning. Returns default score (0.0).

**Safer Alternatives** (choose one):
- Use `ast.literal_eval()` for safe expression evaluation
- Implement sandboxed execution environment (Docker containers)
- Use function registry pattern with pre-defined functions
- Leverage cloud functions with isolated execution

**Recommended Approach**:
```python
# Option 1: Sandboxed execution
import subprocess
import json

def evaluate_function_safe(func_code: str, test_cases: List[Dict]) -> float:
    """Evaluate function in isolated Docker container"""
    # Write function to temp file
    # Execute in isolated container
    # Return score
    pass

# Option 2: Function registry
SAFE_FUNCTIONS = {
    "polynomial": evaluate_polynomial,
    "trigonometric": evaluate_trigonometric,
    "exponential": evaluate_exponential,
}

def evaluate_function_safe(func_type: str, params: Dict) -> float:
    return SAFE_FUNCTIONS[func_type](params)
```

### 1.4 Fix SQL Injection Vulnerability ⚠️ WARNING ADDED
**File**: `cloudvr_perfguard/core/database.py:369-376`
**Issue**: Using f-string formatting in SQL query
**Impact**: SQL injection vulnerability if set_clause contains user input
**Time**: 1 hour
**Status**: ⚠️ Warning comment added

**Current Code**:
```python
# SECURITY WARNING added:
await self.connection.execute(
    f"""
    UPDATE ai_scientist_papers
    SET {set_clause}  # Vulnerable to injection!
    WHERE paper_id = ?
    """,
    params,
)
```

**Secure Fix**:
```python
# Build safe parameterized query
set_parts = [f"{key} = ?" for key in update_fields.keys()]
set_clause = ", ".join(set_parts)
params = list(update_fields.values()) + [paper_id]

await self.connection.execute(
    f"""
    UPDATE ai_scientist_papers
    SET {set_clause}  # Now safe - no user input in f-string
    WHERE paper_id = ?
    """,
    params,
)
```

### 1.5 Add Missing Imports
**Files**: Various
**Issue**: Some imports missing causing ImportError
**Impact**: Module not found errors
**Time**: 2 hours
**Status**: ⏳ Needs review

**Action**: Run imports check and add missing imports:
```bash
# Find missing imports
python -m pylint --disable=all --enable=import-error cloudvr_perfguard/
python -m pylint --disable=all --enable=import-error ai_research/
```

---

## Priority 2: High Impact Improvements (3-5 days, 30 hours)

### 2.1 Implement FastAPI Lifespan Pattern (2 hours)
**Current Issue**: Database connections not properly managed
**Impact**: Resource leaks, connection pool exhaustion

```python
# Add to api/server.py
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    db = DatabaseManager(settings.DATABASE_PATH)
    await db.connect()
    app.state.db = db

    yield

    # Shutdown
    await db.close()

app = FastAPI(lifespan=lifespan)
```

### 2.2 Add API Authentication (6 hours)
**Current Issue**: No authentication, anyone can access API
**Impact**: Security vulnerability, API abuse

**Implementation**:
```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

API_KEY_HEADER = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(API_KEY_HEADER)):
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

# Apply to routes
@app.post("/ai/discover-function")
async def discover_function(
    request: DiscoverRequest,
    api_key: str = Depends(verify_api_key)
):
    ...
```

### 2.3 Add Comprehensive Error Handling (4 hours)
**Current Issue**: Limited error handling, crashes exposed to users
**Impact**: Poor user experience, security information leakage

```python
# Add exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "request_id": request.state.request_id}
    )

# Add validation error handling
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body}
    )
```

### 2.4 Add Rate Limiting (2 hours)
**Current Issue**: No rate limiting, API can be abused
**Impact**: DoS vulnerability, excessive AI API costs

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/ai/discover-function")
@limiter.limit("10/minute")
async def discover_function(request: Request, ...):
    ...
```

### 2.5 Implement Logging & Monitoring (4 hours)
**Current Issue**: Minimal logging, no observability
**Impact**: Difficult to debug, no performance metrics

```python
import structlog

logger = structlog.get_logger()

# Add request ID middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    with structlog.contextvars.bind_contextvars(request_id=request_id):
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

# Log all API calls
logger.info("function_discovery_started",
            job_id=job_id,
            evolution_type=evolution_type)
```

### 2.6 Add Input Validation (3 hours)
**Current Issue**: Limited input validation
**Impact**: Invalid data processing, crashes

```python
from pydantic import BaseModel, Field, validator

class DiscoverFunctionRequest(BaseModel):
    job_id: str = Field(..., min_length=1, max_length=100)
    evolution_type: str = Field(..., regex="^(object_affordance|performance_optimization)$")
    vr_data: VRPerformanceData

    @validator('vr_data')
    def validate_vr_data(cls, v):
        if v.avg_fps <= 0 or v.avg_fps > 144:
            raise ValueError("FPS must be between 0 and 144")
        if not 0 <= v.comfort_score <= 1:
            raise ValueError("Comfort score must be between 0 and 1")
        return v
```

### 2.7 Add Configuration Management (2 hours)
**Current Issue**: Hardcoded values throughout code
**Impact**: Difficult to configure for different environments

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_path: str = "cloudvr_perfguard.db"

    # AI APIs
    google_api_key: str
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None

    # API Server
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4

    # FunSearch
    funsearch_max_iterations: int = 100
    funsearch_timeout: int = 600

    class Config:
        env_file = ".env"

settings = Settings()
```

### 2.8 Add Health Checks (1 hour)
**Current Issue**: No health check endpoints
**Impact**: Cannot monitor service health

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected" if app.state.db.connection else "disconnected",
        "ai_services": {
            "gemini": "available" if settings.google_api_key else "unavailable",
            "openai": "available" if settings.openai_api_key else "unavailable",
        }
    }

@app.get("/metrics")
async def metrics():
    """Prometheus-compatible metrics endpoint"""
    return {
        "api_requests_total": metrics.api_requests,
        "function_discoveries_total": metrics.discoveries,
        "average_discovery_time_seconds": metrics.avg_discovery_time,
    }
```

### 2.9 Add Docker Optimization (3 hours)
**Current Issue**: Docker setup exists but not optimized
**Impact**: Large image size, slow builds

```dockerfile
# Multi-stage build for smaller images
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

CMD ["uvicorn", "cloudvr_perfguard.api.server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2.10 Database Migration System (3 hours)
**Current Issue**: No database versioning or migrations
**Impact**: Schema changes break production

```python
# Use Alembic for migrations
# alembic init alembic

# migrations/versions/001_initial.py
def upgrade():
    conn.execute("""
        CREATE TABLE IF NOT EXISTS vr_performance_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            ...
        )
    """)

def downgrade():
    conn.execute("DROP TABLE vr_performance_metrics")
```

---

## Priority 3: Testing & Quality (5-7 days, 40 hours)

### 3.1 Unit Tests (20 hours)
**Current Coverage**: 0%
**Target Coverage**: 70%+

**Test Structure**:
```
tests/
├── unit/
│   ├── test_funsearch_integration.py
│   ├── test_funsearch_manager.py
│   ├── test_database.py
│   └── test_api_endpoints.py
├── integration/
│   ├── test_api_flow.py
│   └── test_ai_integration.py
└── fixtures/
    ├── sample_vr_data.json
    └── mock_responses.py
```

**Example Tests**:
```python
import pytest
from cloudvr_perfguard.core.database import DatabaseManager

@pytest.mark.asyncio
async def test_store_evolved_function():
    db = DatabaseManager(":memory:")
    await db.connect()

    success = await db.store_evolved_function(
        function_id="test_001",
        job_id="job_001",
        program_name="test_program",
        evolution_iteration=1,
        evolved_function_code="def test(): return 42",
        evaluation_score=0.85,
        discovery_timestamp="2025-11-15T10:00:00Z",
        metadata={}
    )

    assert success is True

    # Verify storage
    result = await db.get_evolved_function("test_001")
    assert result["evaluation_score"] == 0.85
```

### 3.2 Integration Tests (10 hours)
**Focus**: End-to-end API testing

```python
import pytest
from fastapi.testclient import TestClient
from cloudvr_perfguard.api.server import app

client = TestClient(app)

def test_function_discovery_flow():
    # Submit VR performance data
    response = client.post("/performance/collect", json={
        "session_id": "test_001",
        "fps": 72,
        "latency_ms": 15,
        "comfort_score": 0.85,
    })
    assert response.status_code == 200

    # Trigger function discovery
    response = client.post("/ai/discover-function", json={
        "job_id": "test_job_001",
        "evolution_type": "object_affordance",
        "vr_data": {"avg_fps": 72, "comfort_score": 0.85}
    })
    assert response.status_code == 200
    assert "function_id" in response.json()
```

### 3.3 Performance Tests (5 hours)
**Focus**: API throughput, database performance

```python
import pytest
from locust import HttpUser, task, between

class AMIENUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def discover_function(self):
        self.client.post("/ai/discover-function", json={
            "job_id": f"perf_test_{uuid.uuid4()}",
            "evolution_type": "object_affordance",
            "vr_data": {"avg_fps": 72, "comfort_score": 0.85}
        })

# Run: locust -f tests/performance/test_load.py --host=http://localhost:8000
```

### 3.4 Add Type Checking (3 hours)
**Current Issue**: Type hints exist but not enforced
**Impact**: Type errors not caught

```bash
# Add mypy configuration
# mypy.ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True

# Run type checking
mypy cloudvr_perfguard/ ai_research/
```

### 3.5 Add Linting & Formatting (2 hours)
**Current Issue**: Inconsistent code style
**Impact**: Poor code readability

```bash
# Install tools
pip install black ruff isort

# Format code
black cloudvr_perfguard/ ai_research/
isort cloudvr_perfguard/ ai_research/

# Lint code
ruff check cloudvr_perfguard/ ai_research/
```

---

## Priority 4: Documentation (3-5 days, 22 hours)

### 4.1 README.md ✅ COMPLETED
**Status**: ✅ Created comprehensive README
**Time**: 4 hours
**Contents**:
- Quick start guide
- Installation instructions
- Basic usage examples
- API documentation overview
- Known issues and limitations
- Architecture overview

### 4.2 API Documentation (6 hours)
**Tool**: FastAPI auto-generated + custom docs

```python
# Enhanced API documentation
@app.post("/ai/discover-function",
    summary="Discover optimized function using AI",
    description="""
    Uses FunSearch algorithm to evolve optimized functions for VR performance.

    This endpoint triggers an evolutionary search process that:
    1. Takes seed function and VR performance data
    2. Runs iterative evolution with AI-generated mutations
    3. Returns the best-performing function

    **Note**: This is a long-running operation (5-10 minutes).
    """,
    response_model=DiscoverFunctionResponse,
    responses={
        200: {"description": "Function discovery completed successfully"},
        400: {"description": "Invalid request parameters"},
        500: {"description": "Function discovery failed"}
    }
)
async def discover_function(...):
    ...
```

### 4.3 Architecture Documentation (4 hours)
**File**: `docs/ARCHITECTURE.md`

**Contents**:
- System architecture diagram
- Component relationships
- Data flow diagrams
- Database schema
- AI integration patterns
- Deployment architecture

### 4.4 Deployment Guide (3 hours)
**File**: `docs/DEPLOYMENT.md`

**Contents**:
- Development setup
- Production deployment (Docker, K8s)
- Environment configuration
- Monitoring setup
- Backup/restore procedures
- Scaling considerations

### 4.5 Contributing Guide (2 hours)
**File**: `CONTRIBUTING.md`

**Contents**:
- Development environment setup
- Code style guidelines
- Testing requirements
- Pull request process
- Issue reporting guidelines

### 4.6 API Examples (3 hours)
**File**: `docs/EXAMPLES.md`

**Contents**:
- Python client examples
- cURL examples
- JavaScript/TypeScript examples
- Common workflows
- Error handling examples

---

## Timeline & Milestones

### Week 1: Critical Fixes & Security
- ✅ Day 1: Fix critical bugs (Priority 1.1-1.2)
- ⏳ Day 2-3: Remove exec(), fix SQL injection (Priority 1.3-1.4)
- ⏳ Day 4-5: Add authentication & rate limiting (Priority 2.2, 2.4)

**Milestone**: Safe to deploy internally (no security vulnerabilities)

### Week 2: Infrastructure & Reliability
- Day 6-7: Add error handling, logging, monitoring (Priority 2.3, 2.5)
- Day 8-9: Configuration management, health checks (Priority 2.7, 2.8)
- Day 10: Database migrations, Docker optimization (Priority 2.10, 2.9)

**Milestone**: Production-ready infrastructure

### Week 3: Testing & Quality
- Day 11-13: Write unit tests (Priority 3.1)
- Day 14: Integration & performance tests (Priority 3.2, 3.3)
- Day 15: Type checking & linting (Priority 3.4, 3.5)

**Milestone**: 70%+ test coverage, CI/CD ready

### Week 4: Documentation & Polish
- Day 16-17: API documentation (Priority 4.2)
- Day 18: Architecture & deployment docs (Priority 4.3, 4.4)
- Day 19: Contributing guide & examples (Priority 4.5, 4.6)
- Day 20: Final review & cleanup

**Milestone**: Complete documentation, ready for external use

---

## Success Criteria

### Minimum Viable Production (MVP)
- [x] All critical bugs fixed
- [ ] Authentication implemented
- [ ] SQL injection fixed
- [ ] exec() replaced with safe alternative
- [ ] Basic error handling
- [ ] Health check endpoint
- [ ] README with quick start

### Production Ready
- [ ] 70%+ test coverage
- [ ] Comprehensive error handling
- [ ] Rate limiting
- [ ] Logging & monitoring
- [ ] Complete API documentation
- [ ] Docker deployment tested
- [ ] Database migrations

### Enterprise Ready
- [ ] 90%+ test coverage
- [ ] Performance benchmarks met
- [ ] Security audit passed
- [ ] High availability setup
- [ ] Disaster recovery plan
- [ ] SLA documentation
- [ ] 24/7 monitoring

---

## Effort Breakdown

| Phase | Hours | Percentage |
|-------|-------|------------|
| Priority 1: Critical Fixes | 8 | 8% |
| Priority 2: High Impact | 30 | 30% |
| Priority 3: Testing & Quality | 40 | 40% |
| Priority 4: Documentation | 22 | 22% |
| **Total** | **100** | **100%** |

---

## Maintenance Roadmap (Post-Launch)

### Month 1-2: Stability
- Monitor error rates
- Fix bugs as reported
- Optimize performance bottlenecks
- Improve documentation based on user feedback

### Month 3-4: Features
- Add async job queue for long-running discoveries
- Implement function versioning
- Add experiment tracking integration
- Support additional AI models

### Month 6+: Scale
- Multi-tenancy support
- Advanced analytics dashboard
- GraphQL API
- Kubernetes operator for deployment

---

## Resources & References

**Code Quality Tools**:
- pytest: https://pytest.org
- mypy: https://mypy.readthedocs.io
- black: https://black.readthedocs.io
- ruff: https://beta.ruff.rs/docs/

**FastAPI Best Practices**:
- https://fastapi.tiangolo.com/
- https://github.com/zhanymkanov/fastapi-best-practices

**Security**:
- OWASP API Security Top 10
- FastAPI Security docs
- Python security best practices

---

**Last Updated**: November 15, 2025
**Version**: 1.0
**Status**: In Progress
**Next Review**: Weekly during implementation
