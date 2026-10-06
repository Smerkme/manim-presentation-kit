"""Download fonts and create a machine-local Fontconfig configuration."""
from pathlib import Path
from urllib.request import urlopen
from xml.sax.saxutils import escape
import shutil, subprocess
ROOT = Path(__file__).resolve().parents[1]
assets = ROOT / "assets"
assets.mkdir(exist_ok=True)
fonts = {
 "Inter.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/Inter%5Bopsz,wght%5D.ttf",
 "JetBrainsMono.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf",
 "Inter-OFL.txt": "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/OFL.txt",
 "JetBrainsMono-OFL.txt": "https://raw.githubusercontent.com/google/fonts/main/ofl/jetbrainsmono/OFL.txt",
}
for filename, url in fonts.items():
 target = assets / filename
 if not target.exists():
  with urlopen(url, timeout=60) as response:
   target.write_bytes(response.read())
configs = [Path("/etc/fonts/fonts.conf"), Path("/opt/homebrew/etc/fonts/fonts.conf"), Path("/usr/local/etc/fonts/fonts.conf")]
if shutil.which("brew"):
 prefix = subprocess.check_output(["brew", "--prefix"], text=True).strip()
 configs.insert(0, Path(prefix) / "etc/fonts/fonts.conf")
config = next((p for p in configs if p.exists()), None)
if config is None:
 raise SystemExit("Install Fontconfig first; see README.md")
local = ROOT / ".local"
local.mkdir(exist_ok=True)
(local / "fonts.conf").write_text('<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd"><fontconfig><include>' + escape(str(config)) + '</include><dir>' + escape(str(assets)) + '</dir></fontconfig>')
print("Fonts ready:", assets)
