"""
Kyusu-Nodes — Prompt UltimaCHA
--------------------------------
Appender + Commenter fused into one node.

Order of operations:
  1. Strip comments from `text` (line structure preserved)
  2. Join upstream `prefix` with cleaned text
  3. Final whitespace tidy

Output is named `prefix` so nodes can be chained.
"""

import re

from .prompt_commenter import PromptCommenter
from .prompt_appender import _smart_join


class PromptUltimaCHA:
    CATEGORY = "Kyusu/prompt"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "default": (
                        "1girl, long hair,\n"
                        "# open eyes, blue eyes,\n"
                        "closed eyes,\n\n"
                        "[face]\n"
                        "sharp features\n\n"
                        "# [extras]\n"
                        "detailed background"
                    ),
                    "tooltip": (
                        "This node's prompt text. Comments supported:\n"
                        "  # tag       -> line ignored\n"
                        "  // tag      -> line ignored\n"
                        "  ` tag       -> line ignored\n"
                        "  /* tag */   -> block ignored\n"
                        "  [name]      -> section header\n"
                        "  # [name]    -> whole section skipped\n"
                        "  ` [name]    -> whole section skipped\n\n"
                        "If a `prefix` is connected, it is prepended BEFORE "
                        "this text is processed."
                    ),
                }),
            },
            "optional": {
                "prefix": ("STRING", {
                    "forceInput": True,
                    "tooltip": "Incoming string. Appears BEFORE this node's text.",
                }),
                "separator": ("STRING", {
                    "default": ", ",
                    "tooltip": "What to put between prefix and text. Default: ', '",
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prefix",)
    FUNCTION = "process"

    def process(self, text: str, prefix: str = "", separator: str = ", "):
        # Strip comments from text first, then join with prefix
        cleaned_text = PromptCommenter().process(text)[0]
        combined = _smart_join(prefix, cleaned_text, separator)
        combined = re.sub(r'[ \t]+', ' ', combined).strip()
        return (combined,)


NODE_CLASS_MAPPINGS = {"PromptUltimaCHA": PromptUltimaCHA}
NODE_DISPLAY_NAME_MAPPINGS = {"PromptUltimaCHA": "Prompt UltimaCHA"}
