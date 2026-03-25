# Executable Linux file: create with am.yaml

**Data:** 2024-05-14

---

**User:**

I have a app.py and am.yaml which is used by app.py. How Can I create the executable linux file and have am.yaml next to that file?

---

**Assistant:**

Creating an executable Linux file from a Python script (`app.py`) and ensuring that the `am.yaml` file is included alongside it involves a few steps. The general approach is to use a tool like PyInstaller to package your Python script into a standalone executable. Here's a step-by-step guide:

### Step 1: Install PyInstaller

First, you need to install PyInstaller. You can do this using pip:

```bash
pip install pyinstaller
```

### Step 2: Create a Spec File (Optional but Recommended)

PyInstaller can be run directly with command-line options, but using a spec file allows for more customization. Generate a default spec file for your script:

```bash
pyi-makespec app.py
```

This will create a file named `app.spec`.

### Step 3: Modify the Spec File to Include `am.yaml`

Edit the generated `app.spec` file to include the `am.yaml` file. Open `app.spec` in a text editor and modify the `datas` parameter to include your YAML file. It should look something like this:

```python
# app.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=['/path/to/your/script'],
    binaries=[],
    datas=[('am.yaml', '.')],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
)
```

### Step 4: Build the Executable

Now you can build the executable using PyInstaller and the modified spec file:

```bash
pyinstaller app.spec
```

PyInstaller will create a `dist` directory containing your executable and the `am.yaml` file.

### Step 5: Run Your Executable

Navigate to the `dist` directory and you should see your executable file. You can run it like any other executable:

```bash
cd dist/app
./app
```

Make sure that `am.yaml` is in the same directory as the executable. The structure should look like this:

```
dist/
└── app/
    ├── am.yaml
    ├── app
    └── other necessary files...
```

### Summary

1. Install PyInstaller with `pip install pyinstaller`.
2. Create a spec file with `pyi-makespec app.py`.
3. Edit the spec file to include `am.yaml` in the `datas` section.
4. Build the executable with `pyinstaller app.spec`.
5. Run the executable from the `dist` directory.

This will ensure that your `app.py` script is compiled into an executable and that `am.yaml` is included in the same directory as the executable.