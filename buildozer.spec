[app]
title = AstroTrading
package.name = astrotrading
package.domain = org.astro
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Swiss Ephemeris ke C-extension compilation ke liye hostpython3 zaroori hai
requirements = python3,kivy,pyswisseph,hostpython3

orientation = portrait
osx.kivy_version = 2.0.0
fullscreen = 0

# Stable NDK and API target
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
