"""Thin, auditable wrapper around the Anthropic Messages API.

Design rules (these matter for a compliance tool):
  * The SDK is imported lazily, so the package — and the deterministic
    ``--dry-run`` path — works with no ``anthropic`` install and no API key.
  * Model id and token budget are explicit and logged into the artifact, so an
    assessor can see exactly which model produced which evidence.
  * No hidden retries that could silently change output; one call, surfaced
    errors. Determinism is a feature here, not a limitation.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

# Authoritative model ids (see docs/architecture.md "Model policy").
MODEL_DEFAULT = "claude-sonnet-4-6"      # cost/quality sweet spot for this analysis
MODEL_HIGH_STAKES = "claude-opus-4-8"    # ASIL C/D sign-off material
MAX_TOKENS_DEFAULT = 8000


@dataclass
class ClaudeResponse:
    text: str
    model: str
    input_tokens: int | None = None
    output_tokens: int | None = None


def api_key_present() -> bool:
    """True if an Anthropic API key is available in the environment."""
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def complete(
    system: str,
    user: str,
    *,
    model: str = MODEL_DEFAULT,
    max_tokens: int = MAX_TOKENS_DEFAULT,
) -> ClaudeResponse:
    """Run one Messages API call. Raises if the SDK or key is unavailable.

    Callers that want a no-network path must check ``api_key_present()`` first
    and use the pipeline's dry-run branch instead of calling this.
    """
    try:
        import anthropic
    except ImportError as exc:  # pragma: no cover - exercised only without the dep
        raise RuntimeError(
            "The 'anthropic' package is not installed. Run `pip install anthropic`, "
            "or use --dry-run to assemble the prompt without calling the API."
        ) from exc

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )

    text = "".join(block.text for block in message.content if block.type == "text")
    usage = getattr(message, "usage", None)
    return ClaudeResponse(
        text=text,
        model=model,
        input_tokens=getattr(usage, "input_tokens", None),
        output_tokens=getattr(usage, "output_tokens", None),
    )
