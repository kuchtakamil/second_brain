# Skrypt Bash do certyfikatów

**Data:** 2024-01-16

---

**User:**

Chcę następujące polecenia umieścić w skrypcie bash

echo Motorola1234 > passfile.txt
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 3650 -subj '/CN=motorola' -nodes
openssl pkcs12 -export -out keystore.p12 -inkey key.pem -in cert.pem -name "alias_certyfikatu" -passout file:./passfile.txt

---

**Assistant:**

To create a Bash script containing the commands you provided, follow these steps:

1. Open a text editor on your system (like Notepad, Nano, or Vim).
2. Copy and paste the following code into the editor:

```bash
#!/bin/bash

# Save password to a file
echo Motorola1234 > passfile.txt

# Generate a self-signed certificate
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 3650 -subj '/CN=motorola' -nodes

# Create a PKCS#12 keystore
openssl pkcs12 -export -out keystore.p12 -inkey key.pem -in cert.pem -name "alias_certyfikatu" -passout file:./passfile.txt
```

3. Save the file with a `.sh` extension, for example, `create_certificates.sh`.
4. To run the script, you'll need to make it executable. You can do this by running the following command in the terminal:

   ```bash
   chmod +x create_certificates.sh
   ```

5. Now, you can execute the script by typing:

   ```bash
   ./create_certificates.sh
   ```

Please ensure you have OpenSSL installed on your system to run these commands. Also, be aware that storing passwords in plaintext files (like `passfile.txt`) can be a security risk, so handle such files with care.