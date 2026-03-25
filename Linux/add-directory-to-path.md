# Add Directory to PATH

**Data:** 2024-08-04

---

**User:**

I get a notice
WARNING: The script fastapi is installed in '/home/kamil/.local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.

How to do it?

---

**Assistant:**

To resolve this issue, you need to add the directory `/home/kamil/.local/bin` to your PATH environment variable. This can be done by modifying your shell configuration file. Here are the steps to do it:

1. **Determine your shell**: First, identify which shell you are using. Common shells are `bash`, `zsh`, and `fish`. You can check your shell by running:
   ```sh
   echo $SHELL
   ```

2. **Modify the shell configuration file**: Based on your shell, you will need to edit the appropriate configuration file:

   - For `bash`, edit `~/.bashrc` or `~/.bash_profile`
   - For `zsh`, edit `~/.zshrc`
   - For `fish`, edit `~/.config/fish/config.fish`

3. **Add the directory to PATH**: Open the appropriate file in a text editor and add the following line:
   ```sh
   export PATH=$PATH:/home/kamil/.local/bin
   ```

   For `fish`, the syntax is slightly different:
   ```sh
   set -Ux PATH $PATH /home/kamil/.local/bin
   ```

4. **Apply the changes**: After editing the file, apply the changes by sourcing the file or restarting the terminal.

   - For `bash`:
     ```sh
     source ~/.bashrc
     ```
     or
     ```sh
     source ~/.bash_profile
     ```

   - For `zsh`:
     ```sh
     source ~/.zshrc
     ```

   - For `fish`:
     ```sh
     source ~/.config/fish/config.fish
     ```

By following these steps, the directory `/home/kamil/.local/bin` will be added to your PATH, and the warning should be suppressed.

---

**User:**

how to check ubuntu version?

---

**Assistant:**

To check the version of Ubuntu you are running, you can use several commands in the terminal. Here are a few common methods:

1. **Using `lsb_release` command**:
   ```sh
   lsb_release -a
   ```
   This will provide detailed information about the Ubuntu version, including the description, release number, and codename.

2. **Using `cat` to read the `/etc/os-release` file**:
   ```sh
   cat /etc/os-release
   ```
   This command outputs detailed information about the operating system, including the version number.

3. **Using `cat` to read the `/etc/issue` file**:
   ```sh
   cat /etc/issue
   ```
   This file typically contains a brief description of the OS, including the version number.

4. **Using `hostnamectl` command**:
   ```sh
   hostnamectl
   ```
   This command displays information about the system, including the OS and its version.

You can use any of these methods to check your Ubuntu version.

---

**User:**

on ubuntu  how to check if postgresql runs?

---

**Assistant:**

To check if PostgreSQL is running on an Ubuntu system, you can use several commands:

1. **Using `systemctl`**:
   ```sh
   sudo systemctl status postgresql
   ```
   This command will show the status of the PostgreSQL service. Look for lines indicating whether the service is active and running.

2. **Using `ps` command**:
   ```sh
   ps aux | grep postgres
   ```
   This will list all PostgreSQL processes if it is running.

3. **Using `pg_isready` command**:
   ```sh
   pg_isready
   ```
   This command checks the connection status of a PostgreSQL server.

4. **Checking open ports**:
   ```sh
   sudo netstat -plnt | grep postgres
   ```
   This command will show if PostgreSQL is listening on its default port (5432).

5. **Using `pg_ctlcluster`** (specific to Ubuntu/Debian):
   ```sh
   sudo pg_ctlcluster <version> main status
   ```
   Replace `<version>` with your PostgreSQL version (e.g., `12` for PostgreSQL 12). This command is specific to Ubuntu and Debian, which manage PostgreSQL instances using `pg_ctlcluster`.

Here's an example of using the `systemctl` command:

```sh
sudo systemctl status postgresql
```

The output will look something like this if PostgreSQL is running:

```
● postgresql.service - PostgreSQL RDBMS
   Loaded: loaded (/lib/systemd/system/postgresql.service; enabled; vendor preset: enabled)
   Active: active (exited) since Sun 2024-08-04 12:34:56 UTC; 5min ago
 Main PID: 1234 (code=exited, status=0/SUCCESS)
    Tasks: 0 (limit: 4915)
   Memory: 0B
   CGroup: /system.slice/postgresql.service
```

If it is not running, you can start it with:

```sh
sudo systemctl start postgresql
```

And to enable it to start on boot:

```sh
sudo systemctl enable postgresql
```

---

**User:**

how to check on what address it is accessible?

---

**Assistant:**

To check on which address PostgreSQL is accessible on an Ubuntu system, you can look at the configuration file and use network commands. Here are the steps:

1. **Check the PostgreSQL configuration file**:
   - The main configuration file for PostgreSQL is usually located at `/etc/postgresql/<version>/main/postgresql.conf`.
   - Open the file with a text editor, for example:
     ```sh
     sudo nano /etc/postgresql/<version>/main/postgresql.conf
     ```
   - Look for the `listen_addresses` directive. This setting determines which IP addresses PostgreSQL listens on. By default, it is set to `localhost`:
     ```conf
     listen_addresses = 'localhost'
     ```
   - If it is set to `'*'`, PostgreSQL will listen on all available IP addresses.

2. **Check the port**:
   - In the same configuration file (`postgresql.conf`), look for the `port` directive to see which port PostgreSQL is listening on. The default is `5432`:
     ```conf
     port = 5432
     ```

3. **Using `netstat` or `ss`**:
   - You can use `netstat` or `ss` to see the IP addresses and ports on which PostgreSQL is listening.
   ```sh
   sudo netstat -plnt | grep postgres
   ```
   Or:
   ```sh
   sudo ss -plnt | grep postgres
   ```
   This will show output similar to:
   ```
   tcp   LISTEN  0  128  127.0.0.1:5432  0.0.0.0:*  users:(("postgres",pid=1234,fd=5))
   tcp6  LISTEN  0  128  ::1:5432        :::*       users:(("postgres",pid=1234,fd=6))
   ```
   This indicates PostgreSQL is listening on `127.0.0.1` (localhost) and port `5432`.

4. **Using `pg_isready`**:
   - The `pg_isready` command can also provide information about the host and port PostgreSQL is listening on.
   ```sh
   pg_isready
   ```
   By default, this command checks `localhost` on port `5432` unless specified otherwise.

### Example

If you open the configuration file and see:
```conf
listen_addresses = '*'
port = 5432
```

And the `netstat` command shows:
```
tcp   LISTEN  0  128  0.0.0.0:5432  0.0.0.0:*  users:(("postgres",pid=1234,fd=5))
tcp6  LISTEN  0  128  :::5432       :::*       users:(("postgres",pid=1234,fd=6))
```

This indicates that PostgreSQL is listening on all available IP addresses (`0.0.0.0` for IPv4 and `::` for IPv6) on port `5432`.

These methods will help you determine on which address and port your PostgreSQL instance is accessible.

---

**User:**

sudo systemctl status postgresql
● postgresql.service - PostgreSQL RDBMS
     Loaded: loaded (/lib/systemd/system/postgresql.service; enabled; vendor preset: enabled)
     Active: active (exited) since Sun 2024-08-04 21:10:16 CEST; 9min ago
    Process: 52666 ExecStart=/bin/true (code=exited, status=0/SUCCESS)
   Main PID: 52666 (code=exited, status=0/SUCCESS)
        CPU: 2ms
Does it mean that postgresql is currently running?

---

**Assistant:**

The output indicates that the PostgreSQL service is in an `active (exited)` state. This means that the service itself is not currently running any processes. The line `ExecStart=/bin/true (code=exited, status=0/SUCCESS)` suggests that the service start command was `/bin/true`, which immediately exits with a success status, implying that no actual PostgreSQL processes are running.

Here’s a breakdown of what you see:

- **Loaded**: The service configuration is loaded.
- **Active (exited)**: The service is not currently running. It was started, but it exited right away.
- **Main PID**: The process ID associated with the service start command has exited.
- **CPU**: The service used very little CPU time, indicating it didn't do much before exiting.

To confirm if PostgreSQL is running and to start it if necessary, follow these steps:

1. **Check PostgreSQL cluster status**:
   On Ubuntu, PostgreSQL instances are often managed by `pg_ctlcluster`. To check the status of the specific PostgreSQL cluster, use:
   ```sh
   sudo pg_ctlcluster <version> main status
   ```
   Replace `<version>` with your PostgreSQL version, e.g., `12` for PostgreSQL 12.

2. **Start PostgreSQL service**:
   If the cluster is not running, start the PostgreSQL service:
   ```sh
   sudo systemctl start postgresql
   ```

3. **Enable PostgreSQL service at boot**:
   To ensure PostgreSQL starts automatically at boot, enable the service:
   ```sh
   sudo systemctl enable postgresql
   ```

4. **Check PostgreSQL processes**:
   To verify that PostgreSQL processes are running, use:
   ```sh
   ps aux | grep postgres
   ```
   This should list several PostgreSQL processes if the service is running.

### Example

Here’s an example sequence to start PostgreSQL and verify its status:

```sh
sudo systemctl start postgresql
sudo systemctl status postgresql
```

After starting the service, you should see output indicating that PostgreSQL is running, similar to:

```
● postgresql.service - PostgreSQL RDBMS
     Loaded: loaded (/lib/systemd/system/postgresql.service; enabled; vendor preset: enabled)
     Active: active (running) since Sun 2024-08-04 21:20:16 CEST; 1min ago
   Main PID: 52777 (postgres)
      Tasks: 5 (limit: 4915)
     Memory: 12.5M
     CGroup: /system.slice/postgresql.service
             ├─52777 /usr/lib/postgresql/12/bin/postgres -D /var/lib/postgresql/12/main -c config_file=/etc/postgresql/12/main/postgresql.conf
             ├─52779 postgres: checkpointer   
             ├─52780 postgres: background writer  
             ├─52781 postgres: walwriter  
             └─52782 postgres: autovacuum launcher  
```

This indicates that PostgreSQL is actively running.