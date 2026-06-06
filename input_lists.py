# Kyusu-Nodes — 8-way List Emitters (Model / CLIP / Text)
# LIST SET: gather up to 8 inputs into a single list output.
# With OUTPUT_IS_LIST, ComfyUI runs everything downstream once per item, so a
# single Queue press sends all of them through one KSampler -> N images out.
# Wire ModelList / ClipList / TextList by matching index (model1<->text1 ...);
# connect the SAME number of inputs on each so they pair up 1:1.

CATEGORY = "Kyusu/list"  # separate category so this set groups on its own


class ModelList8way:

    @classmethod
    def INPUT_TYPES(cls):
        return {"optional": {f"model{i}": ("MODEL",) for i in range(1, 9)}}

    RETURN_TYPES = ("MODEL",)
    RETURN_NAMES = ("MODEL",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "make_list"
    CATEGORY = CATEGORY

    def make_list(self, **kwargs):
        out = [kwargs.get(f"model{i}") for i in range(1, 9)]
        out = [m for m in out if m is not None]
        return (out,)


class ClipList8way:

    @classmethod
    def INPUT_TYPES(cls):
        return {"optional": {f"clip{i}": ("CLIP",) for i in range(1, 9)}}

    RETURN_TYPES = ("CLIP",)
    RETURN_NAMES = ("CLIP",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "make_list"
    CATEGORY = CATEGORY

    def make_list(self, **kwargs):
        out = [kwargs.get(f"clip{i}") for i in range(1, 9)]
        out = [c for c in out if c is not None]
        return (out,)


class TextList8way:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                f"text{i}": ("STRING", {"forceInput": True}) for i in range(1, 9)
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("STRING",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "make_list"
    CATEGORY = CATEGORY

    def make_list(self, **kwargs):
        out = [kwargs.get(f"text{i}") for i in range(1, 9)]
        out = [t for t in out if t is not None]
        return (out,)


NODE_CLASS_MAPPINGS = {
    "ModelList8way": ModelList8way,
    "ClipList8way": ClipList8way,
    "TextList8way": TextList8way,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ModelList8way": "📜 Model List (8 -> list)",
    "ClipList8way": "📜 Clip List (8 -> list)",
    "TextList8way": "📜 Text List (8 -> list)",
}
