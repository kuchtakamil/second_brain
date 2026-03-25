# Spylon Kernel Installation Error

**Data:** 2024-11-03

---

**User:**

PS C:\Users\kamil> pip install spylon-kernel
Defaulting to user installation because normal site-packages is not writeable
Collecting spylon-kernel
  Using cached spylon-kernel-0.4.1.tar.gz (33 kB)
  Preparing metadata (setup.py) ... error
  error: subprocess-exited-with-error

  × python setup.py egg_info did not run successfully.
  │ exit code: 1
  ╰─> [18 lines of output]
      C:\Users\kamil\AppData\Local\Temp\pip-install-dv1c8rig\spylon-kernel_06b8ef4377c941a18696873d643be137\versioneer.py:418: SyntaxWarning: invalid escape sequence '\s'
        LONG_VERSION_PY['git'] = '''
      Traceback (most recent call last):
        File "<string>", line 2, in <module>
        File "<pip-setuptools-caller>", line 34, in <module>
        File "C:\Users\kamil\AppData\Local\Temp\pip-install-dv1c8rig\spylon-kernel_06b8ef4377c941a18696873d643be137\setup.py", line 14, in <module>
          version=versioneer.get_version(),
                  ^^^^^^^^^^^^^^^^^^^^^^^^
        File "C:\Users\kamil\AppData\Local\Temp\pip-install-dv1c8rig\spylon-kernel_06b8ef4377c941a18696873d643be137\versioneer.py", line 1476, in get_version
          return get_versions()["version"]
                 ^^^^^^^^^^^^^^
        File "C:\Users\kamil\AppData\Local\Temp\pip-install-dv1c8rig\spylon-kernel_06b8ef4377c941a18696873d643be137\versioneer.py", line 1408, in get_versions
          cfg = get_config_from_root(root)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "C:\Users\kamil\AppData\Local\Temp\pip-install-dv1c8rig\spylon-kernel_06b8ef4377c941a18696873d643be137\versioneer.py", line 342, in get_config_from_root
          parser = configparser.SafeConfigParser()
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      AttributeError: module 'configparser' has no attribute 'SafeConfigParser'. Did you mean: 'RawConfigParser'?
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.
error: metadata-generation-failed

× Encountered error while generating package metadata.
╰─> See above for output.

note: This is an issue with the package mentioned above, not pip.
hint: See above for details.

[notice] A new release of pip is available: 24.0 -> 24.3.1
[notice] To update, run: C:\Users\kamil\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\python.exe -m pip install --upgrade pip

---

**Assistant:**

The error you're encountering is due to the `spylon-kernel` package's setup script, which references `configparser.SafeConfigParser()`, an outdated method that is no longer available in recent versions of Python. Instead, Python now uses `configparser.ConfigParser()` instead of `SafeConfigParser()`.

Here's how you might address this:

### Option 1: Use a Python version compatible with the package

The `spylon-kernel` package might be outdated and not fully compatible with Python 3.10+ versions. You could try installing it in a virtual environment with an older Python version, like Python 3.8 or 3.9, which is more likely to be compatible with the package's dependencies.

### Option 2: Modify the Package Files

If you are comfortable doing so, you can manually modify the `spylon-kernel` package files:

1. **Download** the `spylon-kernel` package source code instead of installing directly with `pip`.
2. **Edit** the `versioneer.py` file located in the source code:
   - Replace `configparser.SafeConfigParser()` with `configparser.ConfigParser()`.
3. **Install the package locally**:
   - Navigate to the directory with the modified source files.
   - Run `pip install .` to install from the local files.

### Option 3: Use a Different Kernel for PySpark

If your primary goal is to use a Spark kernel in Jupyter, consider alternative kernels like `Apache Toree`, which is specifically designed for Spark and might be more actively maintained.

Let me know if you'd like guidance on any of these options.