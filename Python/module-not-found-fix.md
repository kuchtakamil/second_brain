# Module Not Found Fix

**Data:** 2024-03-20

---

**User:**

I have activated venv. 
I run pip install -r requirements.txt 
where  inside requirements.txt is
requests==2.28.1
python-dotenv==1.0.1

When I run python3 main.py I get ModuleNotFoundError: No module named 'requests'

---

**Assistant:**

If you're encountering a `ModuleNotFoundError` after activating your virtual environment and installing the requirements listed in your `requirements.txt` file, there could be a few reasons for this:

1. **Activation Issue**: Ensure that you have properly activated your virtual environment before running `pip install -r requirements.txt` and `python3 main.py`. You should see the name of your virtual environment in your terminal prompt after activation.

2. **Installation Error**: Check that the packages were installed correctly. After running `pip install -r requirements.txt`, ensure there were no errors reported during the installation process. Sometimes, dependencies might fail to install due to network issues or other reasons.

3. **Check Virtual Environment**: Make sure you're running `main.py` within the same virtual environment where you installed the dependencies. If you activated another environment or are running the script without activating any environment, it might not recognize the installed packages.

4. **Path Issue**: Double-check that your Python script `main.py` is not trying to import the module `requests` before activating the virtual environment. If you're running the script without activating the environment, it will use the global Python environment, which might not have the necessary packages installed.

5. **Version Compatibility**: Rarely, a package might have compatibility issues with your Python version or other installed packages. However, this is less likely if you're using commonly used packages like `requests` and `python-dotenv`.

To debug:

- Confirm that you've activated the virtual environment correctly.
- Check if there were any errors during installation.
- Ensure `main.py` is being executed within the activated virtual environment.
- Verify that `main.py` doesn't attempt to import `requests` before activation.
- If the issue persists, consider reinstalling the packages within the virtual environment or recreating the virtual environment altogether.