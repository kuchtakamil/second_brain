# Check PostgreSQL Installation

**Data:** 2024-08-04

---

**User:**

I have Ubuntu 22.04. Do I have already installed postgresql?

---

**Assistant:**

To check if PostgreSQL is installed on your Ubuntu 22.04 system, you can use the following steps:

1. **Open a terminal**: You can do this by pressing `Ctrl+Alt+T`.

2. **Check if PostgreSQL is installed**: Run the following command to see if PostgreSQL is installed and to find its version:

   ```sh
   psql --version
   ```

   If PostgreSQL is installed, this command will return the version of PostgreSQL installed. If it is not installed, you will see an error message indicating that `psql` is not found.

3. **Check for the PostgreSQL service**: You can also check if the PostgreSQL service is running by using the following command:

   ```sh
   sudo systemctl status postgresql
   ```

   This command will show the status of the PostgreSQL service if it is installed.

If PostgreSQL is not installed, you can install it by following these steps:

1. **Update your package list**:

   ```sh
   sudo apt update
   ```

2. **Install PostgreSQL**:

   ```sh
   sudo apt install postgresql postgresql-contrib
   ```

3. **Verify the installation**: After the installation is complete, you can verify it by checking the version again using:

   ```sh
   psql --version
   ```

By following these steps, you can determine if PostgreSQL is installed on your system and install it if necessary.

---

**User:**

sudo systemctl status postgresql shows
postgresql.service - PostgreSQL RDBMS
     Loaded: loaded (/lib/systemd/system/postgresql.service; enabled; vendor preset: enabled)
     Active: active (exited) since Sun 2024-08-04 21:39:33 CEST; 34min ago
   Main PID: 851 (code=exited, status=0/SUCCESS)
        CPU: 615us

sie 04 21:39:33 kamil-Legion-Pro-5-16IRX8 systemd[1]: Starting PostgreSQL RDBMS...
sie 04 21:39:33 kamil-Legion-Pro-5-16IRX8 systemd[1]: Finished PostgreSQL RDBMS.


---

**Assistant:**

Based on the output from the `systemctl status postgresql` command, PostgreSQL is installed and its service is running on your Ubuntu 22.04 system. Here’s a breakdown of the output:

- **Loaded**: The PostgreSQL service is enabled and loaded from `/lib/systemd/system/postgresql.service`.
- **Active**: The service is active, though it shows `active (exited)`, meaning the service itself is not currently running in the foreground but has successfully started.
- **Main PID**: The main process ID has exited successfully with status `0/SUCCESS`.

To interact with PostgreSQL and ensure it is working correctly, you can perform a few additional checks:

1. **Switch to the PostgreSQL user**:
   ```sh
   sudo -i -u postgres
   ```

2. **Access the PostgreSQL prompt**:
   ```sh
   psql
   ```

   This should take you to the PostgreSQL interactive terminal.

3. **Check the PostgreSQL version**:
   ```sh
   SELECT version();
   ```

4. **Exit the PostgreSQL prompt**:
   ```sh
   \q
   ```

By following these steps, you can confirm that PostgreSQL is not only installed but also operational on your system.

---

**User:**

how can I list all schemas?

---

**Assistant:**

To list all schemas in your PostgreSQL database, you can use the `psql` interactive terminal. Here's how you can do it:

1. **Open the terminal** and switch to the PostgreSQL user if you haven't already:

   ```sh
   sudo -i -u postgres
   ```

2. **Access the PostgreSQL prompt**:

   ```sh
   psql
   ```

3. **Connect to your specific database** (if you are not using the default `postgres` database):

   ```sh
   \c your_database_name
   ```

4. **List all schemas**:

   ```sh
   \dn
   ```

   Alternatively, you can use an SQL query to retrieve the list of schemas:

   ```sql
   SELECT schema_name
   FROM information_schema.schemata;
   ```

5. **Exit the PostgreSQL prompt**:

   ```sh
   \q
   ```

These commands will give you a list of all schemas in your PostgreSQL database.

---

**User:**

how to list all databases?

---

**Assistant:**

To list all databases in your PostgreSQL instance, you can use the `psql` interactive terminal. Here's how to do it:

1. **Open the terminal** and switch to the PostgreSQL user if you haven't already:

   ```sh
   sudo -i -u postgres
   ```

2. **Access the PostgreSQL prompt**:

   ```sh
   psql
   ```

3. **List all databases**:

   ```sh
   \l
   ```

   Alternatively, you can use an SQL query to retrieve the list of databases:

   ```sql
   SELECT datname FROM pg_database;
   ```

4. **Exit the PostgreSQL prompt**:

   ```sh
   \q
   ```

These steps will give you a list of all databases in your PostgreSQL instance.