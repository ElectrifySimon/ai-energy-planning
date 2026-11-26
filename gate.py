#!/usr/bin/env python3
"""Encrypt index.plain.html with Staticrypt and repaint the gate screen."""
import subprocess, pathlib, shutil, sys

ROOT = pathlib.Path(__file__).parent
PASS = "epw"

subprocess.run([
    "npx", "--yes", "staticrypt", "index.plain.html", "-d", "dist",
    "-p", PASS, "--remember", "0", "--short",
    "--template-title", "IRENA Expert Insight",
    "--template-instructions", "Draft article for Energy Planning Week 2026. Enter the passphrase to read it.",
    "--template-button", "Read the draft",
    "--template-placeholder", "Passphrase",
    "--template-color-primary", "#0073AB",
    "--template-color-secondary", "#04101a",
], cwd=ROOT, check=True)

src = ROOT / "dist" / "index.plain.html"
html = src.read_text()

SKIN = """
<link rel="stylesheet" href="fonts/fonts.css">
<style>
.staticrypt-html, body.staticrypt-body{background:#04101a !important;}
body.staticrypt-body{
  font-family:Inter,system-ui,sans-serif;
  display:grid !important;place-items:center;min-height:100svh;margin:0 !important;padding:0 !important;
  background:
    radial-gradient(70% 55% at 72% 12%, rgba(0,115,171,.30), transparent 62%),
    #04101a !important;
}
.staticrypt-page{width:100% !important;max-width:520px !important;padding:0 28px !important;margin:0 !important;box-sizing:border-box}
.staticrypt-page::before{
  content:"IRENA";display:block;font-family:Montserrat,sans-serif;font-weight:700;
  font-size:13px;letter-spacing:.22em;color:#fff;margin:0 0 44px;
}

.staticrypt-form{
  background:transparent !important;box-shadow:none !important;border:0 !important;
  max-width:none !important;margin:0 !important;padding:0 !important;text-align:left !important;
}
.staticrypt-title{
  font-family:Montserrat,sans-serif !important;font-weight:600 !important;color:#fff !important;
  font-size:clamp(26px,3.4vw,34px) !important;line-height:1.15 !important;letter-spacing:-.01em;
  margin:0 0 14px !important;
}
.staticrypt-instructions{color:#a7bdcb !important;font-size:14px !important;line-height:1.6 !important;margin:0 0 30px !important;max-width:34em}
.staticrypt-hr{border-top:1px solid rgba(255,255,255,.18) !important;margin:26px 0 !important}
.staticrypt-password-container{background:transparent !important;border:0 !important}
.staticrypt-password-container input, input[type="password"], input[type="text"]{
  background:transparent !important;border:0 !important;border-bottom:1px solid rgba(255,255,255,.34) !important;
  border-radius:0 !important;color:#fff !important;font-size:16px !important;padding:12px 34px 12px 0 !important;
  width:100% !important;box-shadow:none !important;
}
input::placeholder{color:#7f9aab !important}
.staticrypt-password-container input:focus{border-bottom-color:#3fa9e0 !important;outline:none}
.staticrypt-remember{display:none !important}
.staticrypt-form *{text-align:left}
.staticrypt-decrypt-button{
  background:#0073AB !important;border:0 !important;border-radius:0 !important;color:#fff !important;
  font-family:Inter,sans-serif !important;font-size:11.5px !important;font-weight:600 !important;
  letter-spacing:.16em !important;text-transform:uppercase !important;padding:16px 22px !important;
  margin-top:26px !important;width:100% !important;cursor:pointer;transition:background .25s ease;
}
.staticrypt-decrypt-button:hover{background:#0088c9 !important}
.staticrypt-error{color:#f0a97a !important;font-size:13px !important;margin-top:14px !important}
.staticrypt-toggle-visibility{filter:invert(1) opacity(.55)}
</style>
"""

html = html.replace("</head>", SKIN + "</head>", 1)
(ROOT / "index.html").write_text(html)
print("gated:", len(html), "bytes ->", ROOT / "index.html")
