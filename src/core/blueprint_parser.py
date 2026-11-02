"""
src/core/blueprint_parser.py
Pydantic data models and loader for declarative Discord blueprints.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
import yaml
import os


class RoleSchema(BaseModel):
    name: str
    color: Optional[str] = "#99AAB5"
    hoist: bool = False
    mentionable: bool = False
    permissions: Dict[str, bool] = Field(default_factory=dict)


class ChannelSchema(BaseModel):
    name: str
    type: str = "text"  # text, voice, forum, stage
    topic: Optional[str] = None
    slowmode: int = 0
    read_only: bool = False
    user_limit: Optional[int] = None


class CategorySchema(BaseModel):
    name: str
    private: bool = False
    allowed_roles: List[str] = Field(default_factory=list)
    channels: List[ChannelSchema] = Field(default_factory=list)


class AutoModSchema(BaseModel):
    name: str
    trigger_type: str  # keyword, regex, mention_spam
    keyword_filter: List[str] = Field(default_factory=list)
    regex_patterns: List[str] = Field(default_factory=list)
    mention_limit: int = 5
    actions: List[str] = Field(default_factory=list)


class BlueprintMetadata(BaseModel):
    name: str
    description: Optional[str] = None
    version: str = "1.0.0"
    author: Optional[str] = "HelixCore Community"


class BlueprintSchema(BaseModel):
    metadata: BlueprintMetadata
    roles: List[RoleSchema] = Field(default_factory=list)
    categories: List[CategorySchema] = Field(default_factory=list)
    automod: List[AutoModSchema] = Field(default_factory=list)


def load_blueprint(path: str) -> BlueprintSchema:
    """Loads, parses, and validates a YAML or JSON blueprint file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Blueprint file not found at: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return BlueprintSchema.model_validate(data)
