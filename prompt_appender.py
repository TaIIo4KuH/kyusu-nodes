"""
Kyusu-Nodes — Prompt Appender
-------------------------------
Prepends an incoming `prefix` string to this node's own text.
Chain multiple to build prompts in stages.
"""

import re


def _smart_join(prefix: str, text: str, separator: str) -> str:
    prefix = (prefix or "").strip()
    text = (text or "").strip()

    if not prefix:
        return text
    if not text:
        return prefix

    sep = separator
    if prefix.endswith(',') or prefix.endswith(';'):
        sep = ' '

    return f"{prefix}{sep}{text}"


class PromptAppender:
    CATEGORY = "Kyusu/prompt"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "This node's prompt text. Appended AFTER the prefix.",
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
        result = _smart_join(prefix, text, separator)
        result = re.sub(r'[ \t]+', ' ', result)
        return (result,)


NODE_CLASS_MAPPINGS = {"PromptAppender": PromptAppender}
NODE_DISPLAY_NAME_MAPPINGS = {"PromptAppender": "Prompt Appender"}
