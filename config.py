from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectConfig:
    root_dir: Path = Path(__file__).resolve().parent
    data_dir: Path = root_dir / "data"
    docs_dir: Path = root_dir / "docs"
    ml_service_dir: Path = root_dir / "ml-service"
    backend_dir: Path = root_dir / "backend"
    frontend_dir: Path = root_dir / "frontend"


config = ProjectConfig()
