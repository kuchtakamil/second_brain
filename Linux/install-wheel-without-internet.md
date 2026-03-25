# Install wheel without internet.

**Data:** 2024-05-24

---

**User:**

I want to install wheel using pip3 install wheel on a maching without internet access. I have installed package python3-setuptools-wheel-39.2.07.el8.noarch

---

**Assistant:**

To install the `wheel` package on a machine without internet access, you'll need to download the package files on a machine with internet access and then transfer them to the offline machine. Here's how you can do it:

1. **Download the wheel package and its dependencies** on a machine with internet access:
    ```sh
    mkdir wheel_download
    pip3 download wheel -d wheel_download
    ```

    This command will download the `wheel` package and its dependencies into the `wheel_download` directory.

2. **Transfer the downloaded files** to your offline machine. You can use a USB drive, external hard drive, or any other method to transfer the files.

3. **Install the downloaded files** on the offline machine:
    ```sh
    cd /path/to/wheel_download
    pip3 install --no-index --find-links=. wheel
    ```

    The `--no-index` option tells `pip` not to look for the packages on PyPI, and the `--find-links=.` option tells `pip` to look for packages in the current directory.

### Step-by-Step Summary

1. **On a machine with internet access:**
    ```sh
    mkdir wheel_download
    pip3 download wheel -d wheel_download
    ```

2. **Transfer `wheel_download` directory to the offline machine.**

3. **On the offline machine:**
    ```sh
    cd /path/to/wheel_download
    pip3 install --no-index --find-links=. wheel
    ```

By following these steps, you should be able to install the `wheel` package on your offline machine without any issues.

---

**User:**

I don't want to use pip download. I want to use already installed package python3-setuptools-wheel-39.2.07.el8.noarch

---

**Assistant:**

If you already have the `python3-setuptools-wheel-39.2.07.el8.noarch` package installed on your machine, it should provide the necessary functionality to use wheels with `setuptools`. However, if you specifically need to install a wheel file or manage wheels using `pip`, here’s how you can proceed without needing an internet connection:

### Using the `python3-setuptools-wheel` Package

The `python3-setuptools-wheel` package should already include the `wheel` module functionality. To verify and utilize it:

1. **Check if `wheel` is available**:
    ```sh
    python3 -c "import wheel; print(wheel.__version__)"
    ```

    This should print the version of the `wheel` module, indicating it's available.

2. **Using `pip` with local files**:
   Since you have `setuptools` and the `wheel` module from the `python3-setuptools-wheel` package, you can use `pip` to install local `.whl` files without needing an internet connection.

3. **Installing a `.whl` file locally**:
    If you have a wheel file (e.g., `example_package.whl`) you want to install, you can do it directly with `pip`:
    ```sh
    pip3 install /path/to/example_package.whl
    ```

### Creating a Local Package Repository

If you have multiple packages to install, creating a local repository might be helpful:

1. **Prepare a directory with all required `.whl` files**:
    - Collect all necessary `.whl` files and place them in a directory, for example, `local_repo`.

2. **Install packages from the local repository**:
    ```sh
    pip3 install --no-index --find-links=/path/to/local_repo package_name
    ```

    Replace `/path/to/local_repo` with the path to your directory containing the `.whl` files, and `package_name` with the name of the package you want to install.

### Summary

1. **Verify the availability of `wheel`**:
    ```sh
    python3 -c "import wheel; print(wheel.__version__)"
    ```

2. **Install a `.whl` file**:
    ```sh
    pip3 install /path/to/example_package.whl
    ```

3. **Create and use a local repository for multiple packages**:
    - Collect `.whl` files in `local_repo`.
    - Install from `local_repo`:
      ```sh
      pip3 install --no-index --find-links=/path/to/local_repo package_name
      ```

By following these steps, you can manage and install Python packages on your offline machine using the `python3-setuptools-wheel` package you already have.