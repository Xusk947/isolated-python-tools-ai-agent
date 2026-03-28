import builtins
import os
import sys
import time
from typing import Optional


_WORKDIR: Optional[str] = None
_ARTIFACT_COUNTER = 0
_AUTO_HOOKS_INSTALLED = False
_ORIG_IMPORT = builtins.__import__


def _new_artifact_path(prefix: str, ext: str) -> str:
    global _ARTIFACT_COUNTER
    _ARTIFACT_COUNTER += 1
    workdir = _WORKDIR or "/workspace"
    name = f"{prefix}_{int(time.time() * 1000)}_{_ARTIFACT_COUNTER}.{ext}"
    return os.path.join(workdir, name)


def _patch_matplotlib():
    try:
        import matplotlib

        try:
            matplotlib.use("Agg", force=True)
        except Exception:
            pass
        import matplotlib.pyplot as plt
    except Exception:
        return

    if getattr(plt.show, "__croki_patched__", False):
        return

    orig_show = plt.show

    def show(*args, **kwargs):
        try:
            nums = list(plt.get_fignums())
            for num in nums:
                fig = plt.figure(num)
                path = _new_artifact_path("plot", "png")
                fig.savefig(path, bbox_inches="tight")
            plt.close("all")
            return None
        except Exception:
            return orig_show(*args, **kwargs)

    show.__croki_patched__ = True
    plt.show = show


def _patch_pil():
    try:
        from PIL import Image
    except Exception:
        return

    if getattr(Image.Image.show, "__croki_patched__", False):
        return

    orig_show = Image.Image.show

    def show(self, *args, **kwargs):
        path = _new_artifact_path("image", "png")
        try:
            self.save(path)
            return None
        except Exception:
            try:
                self.convert("RGB").save(path)
                return None
            except Exception:
                return orig_show(self, *args, **kwargs)

    show.__croki_patched__ = True
    Image.Image.show = show


def _patch_plotly():
    try:
        import plotly.basedatatypes as basedatatypes
    except Exception:
        return

    if getattr(basedatatypes.BaseFigure.show, "__croki_patched__", False):
        return

    orig_show = basedatatypes.BaseFigure.show

    def show(self, *args, **kwargs):
        path = _new_artifact_path("plotly", "html")
        try:
            self.write_html(path, include_plotlyjs="cdn", full_html=True)
            return None
        except Exception:
            return orig_show(self, *args, **kwargs)

    show.__croki_patched__ = True
    basedatatypes.BaseFigure.show = show


def _croki_import(name, globals=None, locals=None, fromlist=(), level=0):
    mod = _ORIG_IMPORT(name, globals, locals, fromlist, level)
    try:
        if name.startswith("matplotlib") or (name == "matplotlib" and "pyplot" in (fromlist or ())):
            _patch_matplotlib()
        if name.startswith("PIL"):
            _patch_pil()
        if name.startswith("plotly"):
            _patch_plotly()
    except Exception:
        pass
    return mod


def ensure_auto_artifact_hooks(workdir: str):
    global _AUTO_HOOKS_INSTALLED, _WORKDIR
    _WORKDIR = workdir

    if not _AUTO_HOOKS_INSTALLED:
        builtins.__import__ = _croki_import
        _AUTO_HOOKS_INSTALLED = True

    if "matplotlib.pyplot" in sys.modules:
        _patch_matplotlib()
    if "PIL.Image" in sys.modules or "PIL" in sys.modules:
        _patch_pil()
    if "plotly" in sys.modules:
        _patch_plotly()

