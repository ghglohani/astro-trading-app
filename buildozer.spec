[app]
title = AstroTrading
package.name = astrotrading
package.domain = org.astro
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Pure Python library flatlib - Zero C-compilation error
requirements = python3,kivy,flatlib

orientation = portrait
osx.kivy_version = 2.0.0
fullscreen = 0

# Android Target Settings
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
