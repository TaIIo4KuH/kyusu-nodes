# Kyusu-Nodes — 8-way Input Switches (Model / CLIP / Text) + a wrapping INT cycler
# SWITCH SET: pick one of 8 inputs via the Input integer (1-8).
# Drive all three switches from one CycleInt8way and queue with batch count 8
# to step through them; the cycler wraps 8 -> 1 so you never reset.
# Switch logic based on Comfyroll Studio's CR Input Switch nodes
# (RockOfFire and Akatsuzi, https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes)

CATEGORY = "Kyusu/logic"  # matches your pack; change if you like


class ModelInputSwitch8way:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {"Input": ("INT", {"default": 1, "min": 1, "max": 8})},
            "optional": {
                "model1": ("MODEL",), "model2": ("MODEL",),
                "model3": ("MODEL",), "model4": ("MODEL",),
                "model5": ("MODEL",), "model6": ("MODEL",),
                "model7": ("MODEL",), "model8": ("MODEL",),
            },
        }

    RETURN_TYPES = ("MODEL",)
    RETURN_NAMES = ("MODEL",)
    FUNCTION = "switch"
    CATEGORY = CATEGORY

    def switch(self, Input,
               model1=None, model2=None, model3=None, model4=None,
               model5=None, model6=None, model7=None, model8=None):
        models = [model1, model2, model3, model4,
                  model5, model6, model7, model8]
        return (models[Input - 1],)


class ClipInputSwitch8way:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {"Input": ("INT", {"default": 1, "min": 1, "max": 8})},
            "optional": {
                "clip1": ("CLIP",), "clip2": ("CLIP",),
                "clip3": ("CLIP",), "clip4": ("CLIP",),
                "clip5": ("CLIP",), "clip6": ("CLIP",),
                "clip7": ("CLIP",), "clip8": ("CLIP",),
            },
        }

    RETURN_TYPES = ("CLIP",)
    RETURN_NAMES = ("CLIP",)
    FUNCTION = "switch"
    CATEGORY = CATEGORY

    def switch(self, Input,
               clip1=None, clip2=None, clip3=None, clip4=None,
               clip5=None, clip6=None, clip7=None, clip8=None):
        clips = [clip1, clip2, clip3, clip4,
                 clip5, clip6, clip7, clip8]
        return (clips[Input - 1],)


class TextInputSwitch8way:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {"Input": ("INT", {"default": 1, "min": 1, "max": 8})},
            "optional": {
                "text1": ("STRING", {"forceInput": True}),
                "text2": ("STRING", {"forceInput": True}),
                "text3": ("STRING", {"forceInput": True}),
                "text4": ("STRING", {"forceInput": True}),
                "text5": ("STRING", {"forceInput": True}),
                "text6": ("STRING", {"forceInput": True}),
                "text7": ("STRING", {"forceInput": True}),
                "text8": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("STRING",)
    FUNCTION = "switch"
    CATEGORY = CATEGORY

    def switch(self, Input,
               text1=None, text2=None, text3=None, text4=None,
               text5=None, text6=None, text7=None, text8=None):
        texts = [text1, text2, text3, text4,
                 text5, text6, text7, text8]
        return (texts[Input - 1],)


class CycleInt8way:
    """Outputs start, start+1, ... end, then wraps back to start.
    Advances by one on every queued run. State is per-node and per-session
    (resets when ComfyUI restarts)."""

    _state = {}

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "start": ("INT", {"default": 1, "min": 0, "max": 1000000}),
                "end": ("INT", {"default": 8, "min": 1, "max": 1000000}),
            },
            "hidden": {"unique_id": "UNIQUE_ID"},
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("INT",)
    FUNCTION = "cycle"
    CATEGORY = CATEGORY

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # NaN never equals itself, so ComfyUI re-runs this node every queue
        # (instead of returning a cached value); that's what advances it.
        return float("nan")

    def cycle(self, start, end, unique_id=None):
        if end < start:
            end = start
        key = unique_id if unique_id is not None else "default"
        cur = CycleInt8way._state.get(key, start)
        if cur < start or cur > end:
            cur = start
        nxt = cur + 1 if cur < end else start
        CycleInt8way._state[key] = nxt
        return (cur,)


NODE_CLASS_MAPPINGS = {
    "ModelInputSwitch8way": ModelInputSwitch8way,
    "ClipInputSwitch8way": ClipInputSwitch8way,
    "TextInputSwitch8way": TextInputSwitch8way,
    "CycleInt8way": CycleInt8way,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ModelInputSwitch8way": "🔀 Model Input Switch (8 way)",
    "ClipInputSwitch8way": "🔀 Clip Input Switch (8 way)",
    "TextInputSwitch8way": "🔀 Text Input Switch (8 way)",
    "CycleInt8way": "🔢 Cycle Int (1-8)",
}
