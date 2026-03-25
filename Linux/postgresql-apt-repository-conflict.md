# PostgreSQL APT Repository Conflict

**Data:** 2024-08-04

---

**User:**

 sudo apt update
E: Conflicting values set for option Signed-By regarding source https://apt.postgresql.org/pub/repos/apt/ jammy-pgdg: /usr/share/postgresql-common/pgdg/apt.postgresql.org.asc != /usr/share/postgresql-common/pgdg/apt.postgresql.org.gpg
E: The list of sources could not be read.


---

**Assistant:**

The error message you are seeing indicates that there is a conflict in the repository configuration for PostgreSQL on your Ubuntu system. Specifically, the `Signed-By` option for the PostgreSQL APT repository is set to different files, which is causing the update process to fail.

To resolve this issue, follow these steps:

1. **Edit the PostgreSQL APT source list**:
   Open the PostgreSQL APT source list file in a text editor with superuser privileges. This file is usually located at `/etc/apt/sources.list.d/pgdg.list`.

   ```sh
   sudo nano /etc/apt/sources.list.d/pgdg.list
   ```

2. **Identify and correct the conflicting `Signed-By` entries**:
   Ensure that all entries for the PostgreSQL APT repository use the same `Signed-By` file. You need to choose either `/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc` or `/usr/share/postgresql-common/pgdg/apt.postgresql.org.gpg` and make sure all lines in the file reference the same key.

   For example, your `pgdg.list` file should look like this (assuming you choose `.gpg`):

   ```sh
   deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.gpg] https://apt.postgresql.org/pub/repos/apt/ jammy-pgdg main
   ```

   Or if you choose `.asc`:

   ```sh
   deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc] https://apt.postgresql.org/pub/repos/apt/ jammy-pgdg main
   ```

3. **Save and exit**:
   Save the changes and exit the text editor. If you are using `nano`, you can do this by pressing `Ctrl+O` to write the changes, followed by `Ctrl+X` to exit.

4. **Update package lists**:
   Run the `sudo apt update` command to refresh the package lists.

   ```sh
   sudo apt update
   ```

If you continue to encounter issues, you may want to completely remove the existing PostgreSQL repository configuration and re-add it:

1. **Remove existing PostgreSQL repository**:
   
   ```sh
   sudo rm /etc/apt/sources.list.d/pgdg.list
   ```

2. **Add the PostgreSQL repository again**:

   ```sh
   wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo tee /etc/apt/trusted.gpg.d/postgresql.asc
   sudo sh -c 'echo "deb [signed-by=/etc/apt/trusted.gpg.d/postgresql.asc] https://apt.postgresql.org/pub/repos/apt/ jammy-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
   ```

3. **Update package lists**:

   ```sh
   sudo apt update
   ```

This should resolve the conflict and allow you to update your package lists successfully.

---

**User:**

This is content 
deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc] https://apt.postgresql.org/pub/repos/apt jammy-pgdg main

Is that ok?

---

**Assistant:**

The content you provided for the PostgreSQL APT repository configuration looks correct, but the format should be precise. Let's ensure it is correctly formatted and troubleshoot further if necessary.

Here's the line you provided:

```sh
deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc] https://apt.postgresql.org/pub/repos/apt jammy-pgdg main
```

This looks fine as long as the key file `/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc` exists and is correctly set up. Let's verify a few things to ensure everything is in order:

1. **Verify the existence of the key file**:

   Check if the key file `/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc` exists:

   ```sh
   ls -l /usr/share/postgresql-common/pgdg/apt.postgresql.org.asc
   ```

   If the file does not exist, you need to download it:

   ```sh
   sudo wget --quiet -O /usr/share/postgresql-common/pgdg/apt.postgresql.org.asc https://www.postgresql.org/media/keys/ACCC4CF8.asc
   ```

2. **Update package lists**:

   After ensuring the key file is present, update your package lists:

   ```sh
   sudo apt update
   ```

If you still encounter errors, it might be useful to remove and re-add the PostgreSQL repository as described previously to ensure there are no residual conflicts.

3. **Remove existing PostgreSQL repository**:

   ```sh
   sudo rm /etc/apt/sources.list.d/pgdg.list
   ```

4. **Add the PostgreSQL repository again**:

   ```sh
   sudo wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo tee /etc/apt/trusted.gpg.d/postgresql.asc
   sudo sh -c 'echo "deb [signed-by=/etc/apt/trusted.gpg.d/postgresql.asc] https://apt.postgresql.org/pub/repos/apt/ jammy-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
   ```

5. **Update package lists again**:

   ```sh
   sudo apt update
   ```

This process should help resolve any lingering conflicts and allow you to update your package lists without errors.