#!/usr/bin/env python3
"""Aplica a marca L2Remote sobre o código do RustDesk antes do build.

Roda no CI (e pode rodar localmente) a partir da raiz do repositório:
    python3 l2remote/branding.py

Mantém o código original intacto no git: tudo é aplicado no momento do build,
o que facilita puxar atualizações do RustDesk.
"""
import os
import re
import shutil
import sys

APP_NAME = "L2Remote"
ORG = "br.com.l2automate"
COMPANY = "L2Automate"
DESCRIPTION = "L2Remote - Suporte remoto"
COPYRIGHT = "L2Automate. Baseado no RustDesk (AGPL-3.0)."
SERVER = os.environ.get("L2R_SERVER", "remote.l2automate.com.br")
PUB_KEY = os.environ.get("L2R_PUB_KEY", "KusPkmRPzCWRwpvg2YQjX6WBUvhJq+11xSVR1+OvUgI=")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "l2remote", "assets")


def patch(path, replacements):
    full = os.path.join(ROOT, path)
    with open(full, encoding="utf-8") as f:
        text = f.read()
    for pattern, repl in replacements:
        text, n = re.subn(pattern, lambda _m, r=repl: r, text, count=1, flags=re.M)
        if n != 1:
            sys.exit(f"ERRO: padrão não encontrado em {path}: {pattern}")
    with open(full, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"ok  {path}")


def copy(src, dst):
    shutil.copyfile(os.path.join(ASSETS, src), os.path.join(ROOT, dst))
    print(f"ok  {dst}")


patch("libs/hbb_common/src/config.rs", [
    (r'^pub const RENDEZVOUS_SERVERS: &\[&str\] = &\[.*\];$',
     f'pub const RENDEZVOUS_SERVERS: &[&str] = &["{SERVER}"];'),
    (r'^pub const RS_PUB_KEY: &str = ".*";$',
     f'pub const RS_PUB_KEY: &str = "{PUB_KEY}";'),
    (r'APP_NAME: RwLock<String> = RwLock::new\("RustDesk"\.to_owned\(\)\);',
     f'APP_NAME: RwLock<String> = RwLock::new("{APP_NAME}".to_owned());'),
    (r'ORG: RwLock<String> = RwLock::new\("com\.carriez"\.to_owned\(\)\);',
     f'ORG: RwLock<String> = RwLock::new("{ORG}".to_owned());'),
])

patch("Cargo.toml", [
    (r'^LegalCopyright = ".*"$', f'LegalCopyright = "{COPYRIGHT}"'),
    (r'^ProductName = "RustDesk"$', f'ProductName = "{APP_NAME}"'),
    (r'^FileDescription = ".*"$', f'FileDescription = "{DESCRIPTION}"'),
])

patch("flutter/windows/runner/Runner.rc", [
    (r'VALUE "CompanyName", ".*?"', f'VALUE "CompanyName", "{COMPANY}"'),
    (r'VALUE "FileDescription", ".*?"', f'VALUE "FileDescription", "{DESCRIPTION}"'),
    (r'VALUE "LegalCopyright", ".*?"', f'VALUE "LegalCopyright", "{COPYRIGHT}"'),
    (r'VALUE "ProductName", ".*?"', f'VALUE "ProductName", "{APP_NAME}"'),
])

for name in ("icon.ico", "icon.png", "tray-icon.ico", "32x32.png", "64x64.png",
             "128x128.png", "128x128@2x.png"):
    copy(name, f"res/{name}")
copy("icon.png", "res/mac-icon.png")
copy("icon.ico", "flutter/windows/runner/resources/app_icon.ico")
for name in ("icon.svg", "icon.png", "logo.png", "logo_light.png", "logo_dark.png"):
    copy(name, f"flutter/assets/{name}")

print(f"Marca {APP_NAME} aplicada. Servidor: {SERVER}")
