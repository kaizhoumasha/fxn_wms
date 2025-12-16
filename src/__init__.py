"""P9 WES backend scaffold.

This package intentionally follows a modular-monolith + hexagonal architecture:
- `src.app`: FastAPI northbound adapter (HTTP API)
- `src.core`: framework-agnostic core domain & use cases
- `src.infra`: infrastructure adapters (DB/Redis/Outbox/Workers)
- `src.southbound`: plugin adapters for hardware protocols (UHI)
"""

