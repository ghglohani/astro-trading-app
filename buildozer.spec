[app]

# (str) Title of your application
title = Astro Trading App

# (str) Package name
package.name = astrotradingapp

# (str) Package domain (needed for android packaging)
package.domain = org.astro

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (JSON, PNG, PY etc.)
source.include_exts = py,png,jpg,kv,atlas,json

# (list) Application requirements
# Note: cython, python3, kivy and pyswisseph are required
requirements = python3,kivy,pyswisseph

# (str) Application versioning
version = 1.0.0

# (list) Permissions
permissions = INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, skip updating NDK
android.skip_update = False

# (bool) Accept all SDK licenses automatically
android.accept_sdk_license = True

# (str) The Android arch to build for
android.archs = arm64-v8a

# (bool) Enable AndroidX
android.enable_androidx = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
