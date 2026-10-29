"""
RepoGuard Academic Project Configuration Module.
Provides centralized, minimal settings for local LLM inference and the convergence loop.
"""
from pydantic import BaseModel, Field


class RepoGuardSettings(BaseModel):
    """Minimal settings for RepoGuard local execution."""
    model_name: str = "qwen2.5-coder:7b"
    temperature: float = 0.0
    seed: int = 42
    num_ctx: int = 4096
    max_iterations: int = 3


# Global configuration instance
settings = RepoGuardSettings()

# Backward-compatibility alias
MY_LOCAL_MODEL = settings.model_name
