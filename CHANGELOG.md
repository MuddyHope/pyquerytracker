# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **New FastAPI endpoint `/metrics`** - Provides aggregated query tracking metrics
  - Returns total number of tracked queries
  - Returns average execution time in milliseconds
  - Returns details about the slowest query (function name, execution time, timestamp, event)
  - Located in `pyquerytracker/api/metrics.py`
  - Integrated with main FastAPI application

### Changed
- **Project structure refactor** - Renamed `pyquerytracker/api.py` to `pyquerytracker/app.py`
  - Resolves import ambiguity between `api` package and main app file
  - Updated all imports throughout the project to use new location
  - Maintains backward compatibility for existing functionality

### Added (Testing)
- **New test file `tests/test_metrics.py`**
  - Tests the `/metrics` endpoint functionality
  - Verifies correct JSON response structure
  - Ensures proper data types and required fields
  - Includes simulation of tracked queries for testing

### Technical Details
- **Database integration** - Uses existing `TrackedQuery` model and `SessionLocal`
- **SQLAlchemy queries** - Implements efficient aggregation using `func.count()` and `func.avg()`
- **Error handling** - Proper session management with try/finally blocks
- **Code quality** - PEP8 compliant with comprehensive docstrings
- **Router pattern** - Uses FastAPI's APIRouter for modular endpoint organization

### Files Modified
- `pyquerytracker/api/__init__.py` - Created package initialization
- `pyquerytracker/api/metrics.py` - New metrics endpoint implementation
- `pyquerytracker/app.py` - Renamed from `api.py`, includes metrics router
- `pyquerytracker/main.py` - Updated import to use new app location
- `tests/test_metrics.py` - New test file for metrics endpoint
- `tests/test_dashboard.py` - Updated import
- `tests/test_websocket.py` - Updated import

### Files Removed
- `pyquerytracker/api.py` - Renamed to `app.py` to avoid import conflicts

## [0.1.0] - Initial Release
- Initial implementation of pyquerytracker
- Basic query tracking functionality
- FastAPI dashboard and websocket support
- Database persistence with SQLAlchemy
- Export functionality (CSV, JSON) 