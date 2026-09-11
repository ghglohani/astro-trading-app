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
# WARNING: pyswisseph is required for Swiss Ephemeris calculations
requirements = python3,kivy,pyswisseph

# (str) Application versioning
version = 1.0.0

# (list) Permissions
permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip building the ndk recipes
android.skip_update = False

# (bool) If True, accept all SDK licences
android.accept_sdk_license = True

# (str) The Android arch to build for
android.archs = arm64-v8a, armeabi-v7a

# (list) List of Java .jar files to add to the libs
# android.add_jars = foo.jar

# (list) List of Gradle dependencies to add
# android.gradle_dependencies =

# (bool) Enable AndroidX
android.enable_androidx = True

# (str) Custom source dir for p4a
# p4a.source_dir =

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = disable, 1 = enable)
warn_on_root = 1
