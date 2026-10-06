"""Render the five-scene example using local dependencies and fonts."""
import os, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
env = os.environ.copy()
fontconfig = ROOT / ".local/fonts.conf"
if not fontconfig.exists():
 raise SystemExit("Run python scripts/setup.py first")
env["FONTCONFIG_FILE"] = str(fontconfig)
quality = "-ql" if "--draft" in sys.argv else "-qh"
args = [sys.executable, "-m", "manim", quality]
if quality == "-qh": args += ["--fps", "60"]
args += ["--media_dir", str(ROOT / "media"), str(ROOT / "examples/reactive-feed/scene.py"), "ReactiveFeed"]
subprocess.run(args, cwd=ROOT, env=env, check=True)
