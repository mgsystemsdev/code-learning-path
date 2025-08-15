# Handles loading and switching roles
# agents/role_manager.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import os, glob

# Optional YAML support; app runs even if PyYAML isn’t installed
try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None

# ---- Data model ----
@dataclass
class RoleSpec:
    name: str
    instructions: str
    tools: List[str] = field(default_factory=list)
    knowledge: List[str] = field(default_factory=list)
    budget_usd: Optional[float] = None
    routing: Optional[dict] = None  # e.g., {"default":"qwen","boost_on_lines":200}

# ---- Built-in defaults (used when no YAML present) ----
DEFAULT_ROLES: Dict[str, RoleSpec] = {
    "General": RoleSpec(
        name="General",
        instructions=(
            "You are a practical assistant. Be concise, step-by-step, and actionable. "
            "Prefer clear bullets. Ask clarifying questions only when needed."
        ),
        tools=[],
    ),
    "Architect": RoleSpec(
        name="Architect",
        instructions=(
            "You are a software architect. Propose minimal, high-leverage designs with tradeoffs. "
            "Use brief diagrams-in-text and list risks & mitigations."
        ),
        tools=["search_repo", "read_file"],
    ),
    "Engineer": RoleSpec(
        name="Engineer",
        instructions=(
            "You are a senior Python engineer. Plan -> write minimal code -> explain key choices. "
            "Prefer unified diffs for edits. Keep functions small and tested."
        ),
        tools=["read_file", "write_file", "lint_format", "run_tests"],
    ),
    "Tester": RoleSpec(
        name="Tester",
        instructions=(
            "You are a QA engineer. Enumerate edge cases, write pytest snippets, and propose assertions. "
            "Be thorough but concise."
        ),
        tools=["run_tests"],
    ),
    "Doc Writer": RoleSpec(
        name="Doc Writer",
        instructions=(
            "You write developer docs. Use short sections, examples, and clear headings. "
            "Prefer Markdown. Keep a neutral, precise tone."
        ),
        tools=["render_markdown"],
    ),
    "Data Analyst": RoleSpec(
        name="Data Analyst",
        instructions=(
            "You analyze data. Clarify goals, outline steps, and show pandas/SQL examples when helpful. "
            "Validate assumptions and report caveats."
        ),
        tools=["parse_csv", "plot_data"],
    ),
}

# ---- YAML loader (data/agents/*.yaml) ----
def _merge_text(*parts: Optional[str]) -> str:
    return "\n".join(p.strip() for p in parts if isinstance(p, str) and p.strip())

def _load_yaml_roles(folder: str = "data/agents") -> Dict[str, RoleSpec]:
    roles: Dict[str, RoleSpec] = {}
    if not os.path.isdir(folder):
        return roles
    files = sorted(glob.glob(os.path.join(folder, "*.y*ml")))
    if not files or yaml is None:
        return roles

    for path in files:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
        except Exception:
            continue

        # Accept multiple common keys so you can paste from different templates
        name = data.get("name") or data.get("title") or data.get("id")
        if not name:
            # derive from filename
            name = os.path.splitext(os.path.basename(path))[0].replace("_", " ").title()

        # Instruction sources we support
        core = data.get("prompt_core") or data.get("core") or data.get("instructions")
        full = data.get("prompt") or data.get("system") or data.get("instruction")
        supplemental_list = data.get("prompt_supplemental") or data.get("supplemental") or []

        # Allow supplemental to be either list[str] or single str
        if isinstance(supplemental_list, str):
            supplemental_list = [supplemental_list]

        instructions = _merge_text(core, full, *supplemental_list)

        tools = data.get("tools") or []
        knowledge = data.get("knowledge") or []
        budget = data.get("budget_usd")
        routing = data.get("routing")

        roles[name] = RoleSpec(
            name=name,
            instructions=instructions or DEFAULT_ROLES.get(name, DEFAULT_ROLES["General"]).instructions,
            tools=list(tools) if isinstance(tools, list) else [],
            knowledge=list(knowledge) if isinstance(knowledge, list) else [],
            budget_usd=budget if isinstance(budget, (int, float)) else None,
            routing=routing if isinstance(routing, dict) else None,
        )
    return roles

def load_registry() -> Dict[str, RoleSpec]:
    yaml_roles = _load_yaml_roles()
    if yaml_roles:
        # Merge YAML over defaults (YAML wins; fill missing with defaults)
        merged = dict(DEFAULT_ROLES)
        merged.update(yaml_roles)
        return merged
    return dict(DEFAULT_ROLES)

# Public registry (loaded at import)
REGISTRY: Dict[str, RoleSpec] = load_registry()

# Convenience helpers
def get_role(name: str) -> RoleSpec:
    return REGISTRY.get(name, REGISTRY["General"])

def refresh_registry() -> None:
    """Reload roles from disk; call after editing files in data/agents/."""
    global REGISTRY
    REGISTRY = load_registry()
