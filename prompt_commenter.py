"""
Kyusu-Nodes — Prompt Commenter
--------------------------------
Strips commented-out lines, blocks, and named sections from a prompt.

Supported comment syntax:
  # tag, tag           -> line ignored
  // tag, tag          -> line ignored
  ` tag, tag           -> line ignored
  /* tag, tag */       -> block ignored (multiline ok)
  [section_name]       -> starts a named section
  # [section_name]     -> entire section skipped
  ` [section_name]     -> entire section skipped
"""

import re

# Prefixes that mark a line (or section header) as commented out
COMMENT_PREFIXES = ('#', '//', '`')


def _is_commented_line(stripped: str) -> bool:
    return any(stripped.startswith(p) for p in COMMENT_PREFIXES)


def _is_commented_header(stripped: str) -> bool:
    """e.g.  # [name]  or  ` [name]"""
    return bool(re.match(r'^[#`]\s*\[.+\]\s*$', stripped))


def _is_active_header(stripped: str) -> bool:
    """e.g.  [name]"""
    return bool(re.match(r'^\[.+\]\s*$', stripped))


class PromptCommenter:
    CATEGORY = "Kyusu/prompt"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": (
                        "beautiful woman, long hair,\n"
                        "# open eyes, blue eyes,\n"
                        "closed eyes,\n"
                        "elegant dress\n\n"
                        "[face]\n"
                        "sharp features, defined jawline\n\n"
                        "# [extras]\n"
                        "detailed background, bokeh"
                    ),
                    "tooltip": (
                        "Comment syntax:\n"
                        "  # tag       -> line ignored\n"
                        "  // tag      -> line ignored\n"
                        "  ` tag       -> line ignored\n"
                        "  /* tag */   -> block ignored\n"
                        "  [name]      -> section header\n"
                        "  # [name]    -> whole section skipped\n"
                        "  ` [name]    -> whole section skipped"
                    ),
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "process"

    def process(self, prompt: str):
        # 1. Strip /* ... */ block comments (multiline)
        text = re.sub(r'/\*.*?\*/', '', prompt, flags=re.DOTALL)

        # 2. Walk lines
        output_tags = []
        skip_section = False

        for line in text.split('\n'):
            stripped = line.strip()

            if not stripped:
                continue

            if _is_commented_header(stripped):
                skip_section = True
                continue

            if _is_active_header(stripped):
                skip_section = False
                continue

            if skip_section:
                continue

            if _is_commented_line(stripped):
                continue

            output_tags.append(stripped)

        # 3. Flatten and clean
        full = ', '.join(output_tags)
        tags = [t.strip() for t in re.split(r'[,\n]+', full)]
        tags = [t for t in tags if t]
        return (', '.join(tags),)


NODE_CLASS_MAPPINGS = {"PromptCommenter": PromptCommenter}
NODE_DISPLAY_NAME_MAPPINGS = {"PromptCommenter": "Prompt Commenter"}
