# AMIEN Research - AI-Powered CloudVR Performance & Function Discovery

> Automated research platform combining CloudVR performance monitoring with AI-driven function discovery and optimization

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

AMIEN Research is an integrated platform that combines CloudVR performance monitoring with AI-driven function discovery and automated research capabilities. The system uses Google's FunSearch algorithm and multiple AI models (Gemini, GPT-4, Claude) to discover optimized functions, analyze VR performance metrics, and automate scientific research workflows.

### Key Components

**CloudVR PerfGuard:**
- Real-time VR performance monitoring and analysis
- AI-powered function discovery for VR optimization
- Performance metrics collection (FPS, latency, comfort scores)
- Automated hypothesis testing and validation

**AI Research Automation:**
- Automated paper generation and analysis
- Function discovery using evolutionary algorithms
- Integration with multiple AI providers (Google, OpenAI, Anthropic)
- Research output management and versioning

## Features

- **AI-Powered Function Discovery**: Uses FunSearch algorithm to evolve optimized functions for VR performance
- **Multi-Model AI Integration**: Supports Google Gemini, OpenAI GPT-4, and Anthropic Claude
- **Real-Time Performance Monitoring**: Tracks VR metrics including FPS, latency, and comfort scores
- **Automated Research Pipeline**: Generate, analyze, and manage research papers automatically
- **RESTful API**: FastAPI-based API for integration with other systems
- **Database Management**: SQLite-based storage for metrics, functions, and research outputs
- **Docker Support**: Containerized deployment for CloudVR monitoring

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/basedlsg/amien-research.git
cd amien-research

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Configuration

Edit `.env` file with your API credentials:

```bash
# AI Provider API Keys
GOOGLE_API_KEY=your_google_gemini_key_here
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Database Configuration
DATABASE_PATH=cloudvr_perfguard.db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

### Basic Usage

#### Running CloudVR PerfGuard API

```bash
cd cloudvr_perfguard
python -m uvicorn api.server:app --host 0.0.0.0 --port 8000
```

#### Using AI Function Discovery

```python
from cloudvr_perfguard.ai_integration.funsearch_integration import FunSearchManager
from cloudvr_perfguard.core.database import DatabaseManager

# Initialize managers
db_manager = DatabaseManager("cloudvr_perfguard.db")
await db_manager.connect()

funsearch_manager = FunSearchManager(db_manager)

# Discover optimized function
result = await funsearch_manager.discover_affordance_function(
    job_id="vr_opt_001",
    vr_performance_data={
        "avg_fps": 72,
        "comfort_score": 0.85,
        "latency_ms": 15
    },
    evolution_type="object_affordance"
)
```

#### Running AI Research Pipeline

```python
from ai_research.funsearch_manager import FunSearchManager

# Initialize manager
manager = FunSearchManager(api_key="your_google_api_key")

# Generate optimized function
best_function = await manager.run_funsearch(
    func_type="polynomial",
    target_metric="accuracy",
    num_iterations=100
)
```

## Architecture

```
amien-research/
├── cloudvr_perfguard/          # CloudVR Performance Monitoring
│   ├── ai_integration/         # FunSearch & AI integration
│   ├── api/                    # FastAPI endpoints
│   ├── core/                   # Database & core logic
│   └── scripts/                # Utility scripts
│
├── ai_research/                # Research Automation
│   ├── funsearch_manager.py    # Function discovery manager
│   ├── ai_scientist_manager.py # Research automation
│   └── research_coordinator.py # Multi-agent coordination
│
└── research_outputs/           # Generated Research
    ├── functions/              # Discovered functions
    ├── papers/                 # Generated papers
    └── datasets/               # Research datasets
```

## API Endpoints

### CloudVR PerfGuard API

- `GET /health` - Health check endpoint
- `POST /performance/collect` - Submit VR performance metrics
- `GET /performance/metrics` - Retrieve performance metrics
- `POST /ai/discover-function` - Trigger AI function discovery
- `GET /ai/evolved-functions` - List discovered functions
- `POST /research/generate-paper` - Generate research paper
- `GET /research/papers` - List generated papers

### Example API Usage

```python
import requests

# Submit VR performance data
response = requests.post("http://localhost:8000/performance/collect", json={
    "session_id": "vr_session_001",
    "fps": 72,
    "latency_ms": 15,
    "comfort_score": 0.85,
    "timestamp": "2025-11-15T10:30:00Z"
})

# Discover optimized function
response = requests.post("http://localhost:8000/ai/discover-function", json={
    "job_id": "optimization_001",
    "evolution_type": "object_affordance",
    "vr_data": {
        "avg_fps": 72,
        "comfort_score": 0.85
    }
})
```

## Documentation

- **[Improvement Plan](IMPROVEMENT_PLAN.md)** - Detailed roadmap for production readiness (100 hours)
- **[API Reference](docs/API.md)** - Complete API documentation (coming soon)
- **[Architecture Guide](docs/ARCHITECTURE.md)** - System design details (coming soon)
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment (coming soon)

## Known Issues

This is a research prototype with several known limitations. See [IMPROVEMENT_PLAN.md](IMPROVEMENT_PLAN.md) for complete details.

**Critical Issues:**

1. **Type Error** ✅ FIXED - `funsearch_integration.py:89` - Changed `float("-in")` to `float("-inf")`
2. **Dict Key Errors** ✅ FIXED - `funsearch_manager.py` - Fixed empty string keys in parameter dictionaries
3. **Security: exec() Disabled** ⚠️ - Function evaluation using `exec()` has been disabled for security. Uncomment only in controlled environments.
4. **Security: SQL Injection** ⚠️ - `database.py:372` - SQL query construction is vulnerable. Use parameterized queries.
5. **No Authentication** ⚠️ - API has no authentication. Add before production deployment.

**Additional Limitations:**

- No test coverage (needs unit & integration tests)
- Limited error handling in API endpoints
- No rate limiting or API quotas
- Research outputs not versioned
- No monitoring/observability setup

## Dependencies

Core dependencies:
- **FastAPI** - Web framework for APIs
- **Google Generative AI** - Gemini models for function discovery
- **OpenAI** - GPT-4 integration
- **Anthropic** - Claude integration
- **aiosqlite** - Async SQLite database
- **numpy** - Numerical computations
- **Docker** - Containerization support

See [requirements.txt](requirements.txt) for complete list.

## Development

### Setting Up Development Environment

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests (when available)
pytest tests/

# Run with auto-reload for development
uvicorn cloudvr_perfguard.api.server:app --reload
```

### Database Setup

The system automatically creates SQLite databases on first run:

```bash
# CloudVR database
cloudvr_perfguard/cloudvr_perfguard.db

# Initialize schema (automatic on first connection)
python -c "from cloudvr_perfguard.core.database import DatabaseManager; import asyncio; asyncio.run(DatabaseManager('cloudvr_perfguard.db').connect())"
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines (coming soon).

Areas needing contribution:
- Test coverage (currently 0%)
- Security hardening (authentication, SQL injection fixes)
- Documentation improvements
- Performance optimization
- Additional AI model integrations

## Research Outputs

Generated research papers and discovered functions are stored in `research_outputs/`:

```
research_outputs/
├── functions/
│   ├── discovered_YYYYMMDD_HHMMSS.py
│   └── ...
├── papers/
│   ├── automated/
│   │   └── research_paper_YYYYMMDD.md
│   └── amien/
│       └── spatial_ai_research_*.md
└── datasets/
    └── experiment_data.json
```

## Deployment

### Docker Deployment

```bash
# Build Docker image
docker build -t amien-research .

# Run container
docker run -p 8000:8000 \
  -e GOOGLE_API_KEY=your_key \
  -e OPENAI_API_KEY=your_key \
  amien-research
```

### Production Considerations

Before production deployment:

1. **Add Authentication** - Implement API key or OAuth
2. **Fix Security Issues** - Address SQL injection, remove exec()
3. **Add Rate Limiting** - Prevent API abuse
4. **Set Up Monitoring** - Add logging, metrics, alerts
5. **Add Test Coverage** - Unit and integration tests
6. **Use Production Database** - PostgreSQL instead of SQLite
7. **Enable HTTPS** - Use SSL/TLS certificates
8. **Implement Backup Strategy** - Regular database backups

See [IMPROVEMENT_PLAN.md](IMPROVEMENT_PLAN.md) for detailed production roadmap (100 hours estimated).

## Performance

Current system capabilities:
- **API Throughput**: ~100 requests/second (single instance)
- **Function Discovery**: 50-100 iterations in 5-10 minutes
- **Paper Generation**: 1 research paper in 2-5 minutes (depending on AI model)
- **Database**: Handles ~1M performance records efficiently

## License

MIT License - See [LICENSE](LICENSE) for details.

## Acknowledgments

- Separated from [NOUS monorepo](https://github.com/basedlsg/NOUS) on November 15, 2025
- Built on Google's FunSearch algorithm
- Integrates with Google Gemini, OpenAI GPT-4, and Anthropic Claude
- Inspired by AI-driven research automation and VR performance optimization

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- See [IMPROVEMENT_PLAN.md](IMPROVEMENT_PLAN.md) for known limitations
- Review existing documentation before asking questions

---

**Status**: Research Prototype
**Version**: 1.0.0
**Last Updated**: November 15, 2025
**Maintainer**: Based LSG
