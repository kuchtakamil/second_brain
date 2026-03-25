# Create deterministic admin.whl

**Data:** 2024-07-13

---

**User:**

I have to builded files named admin.whl (wheel Python package) with the same content.
The SHA256 sums differs between those two files.
I checked the content of admin.whl files, so I checked every single file including *dist-info files, and every file in both admin.whl have the same SHA256.
However sha256 between two fles admin.whl differs. Why? How to fix it

---

**Assistant:**

The SHA256 sums of the two `admin.whl` files differ even though their contents are identical because the archive metadata, such as timestamps or compression levels, might differ between the two files. This discrepancy can occur due to:

1. **Timestamps**: Files within the wheel might have different timestamps, causing the overall hash to differ.
2. **Compression**: Different compression algorithms or levels might be used, resulting in different hashes.
3. **Order of files**: The order in which files are added to the archive can affect the hash.

To ensure that the SHA256 sums match, you need to standardize the process of creating the wheel files. Here are some steps to achieve this:

### Using `zipfile` module in Python
You can create a ZIP archive (wheel files are ZIP archives) with deterministic metadata using the `zipfile` module in Python.

```python
import zipfile
import os
import time

def deterministic_zip(zip_name, source_dir):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(source_dir):
            for file in sorted(files):
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                info = zipfile.ZipInfo(arcname)
                info.date_time = (1980, 1, 1, 0, 0, 0)  # Set fixed timestamp
                info.external_attr = 0o644 << 16  # Set permissions to -rw-r--r--
                with open(file_path, 'rb') as f:
                    zf.writestr(info, f.read())

# Usage example:
deterministic_zip('admin.whl', 'path/to/admin_wheel_content')
```

### Using `zip` command
Alternatively, you can use the `zip` command with options to strip timestamps and other metadata:

```sh
zip -X -r admin.whl .
```

- `-X` option creates a ZIP file without extra file attributes.
- `-r` option recursively adds files.

### Using `wheel` package with reproducible options
If you're using the `wheel` package to create your wheel files, you can pass the `--build-number` argument to ensure deterministic builds.

```sh
python setup.py bdist_wheel --build-number=1
```

Make sure to use the same build number each time.

### Verifying SHA256
After creating the wheels, you can verify the SHA256 sums to ensure they match.

```sh
sha256sum admin1.whl admin2.whl
```

By following these steps, you should be able to create wheel files with identical SHA256 sums.