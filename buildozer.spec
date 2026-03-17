[app]
# Neuer Name der App
title = FLIP IT
package.name = flipit
package.domain = org.pixelart

source.dir = .
source.include_exts = py,png,jpg,kv,json,ttf

version = 0.1

# Anforderungen (sh und six helfen oft bei der Stabilität auf Android)
requirements = python3,kivy==2.3.1,pillow,sh,six

orientation = portrait
fullscreen = 1

# Das App Logo (Kopf Seite)
icon.filename = pixil-frame-0-startkopf.png
android.adaptive_icon_scale = 1.0

# Android API Einstellungen
android.api = 34
android.minapi = 21
android.sdk = 34
android.ndk = 25c
android.build_tools_version = 34.0.0

# Architekturen für moderne Handys
android.archs = arm64-v8a, armeabi-v7a
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
