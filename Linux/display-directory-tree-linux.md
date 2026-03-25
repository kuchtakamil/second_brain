# Display Directory Tree Linux

**Data:** 2024-05-20

---

**User:**

On linux how to display a tree of a catalog

---

**Assistant:**

To display a tree of a catalog (directory) in Linux, you can use the `tree` command. The `tree` command lists the contents of directories in a tree-like format, making it easier to visualize the directory structure.

Here's how to use it:

1. **Install the `tree` command** (if not already installed):
   - On Debian-based distributions (like Ubuntu):
     ```sh
     sudo apt-get install tree
     ```
   - On Red Hat-based distributions (like Fedora):
     ```sh
     sudo dnf install tree
     ```
   - On Arch-based distributions:
     ```sh
     sudo pacman -S tree
     ```

2. **Use the `tree` command**:
   - To display the tree of a directory, simply navigate to the directory or specify the directory path with the `tree` command.
     ```sh
     tree /path/to/directory
     ```
   - If you want to display the tree of the current directory, just run:
     ```sh
     tree
     ```

3. **Additional options**:
   - To include hidden files (those starting with a dot), use the `-a` option:
     ```sh
     tree -a
     ```
   - To limit the depth of the directory tree, use the `-L` option followed by the desired level:
     ```sh
     tree -L 2
     ```
   - To display file sizes, use the `-h` option (human-readable format):
     ```sh
     tree -h
     ```
   - To print the full path of each file, use the `-f` option:
     ```sh
     tree -f
     ```

### Example Usage

```sh
tree -L 2 -h /path/to/directory
```

This command will display the directory structure up to 2 levels deep, including the sizes of the files, for the specified path.

### Sample Output

```
/path/to/directory
├── file1.txt
├── file2.txt
└── subdirectory
    ├── file3.txt
    └── file4.txt

2 directories, 4 files
```

By using these commands and options, you can easily display and customize the tree view of any directory on your Linux system.