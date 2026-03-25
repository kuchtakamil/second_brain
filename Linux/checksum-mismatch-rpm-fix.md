# Checksum Mismatch RPM Fix

**Data:** 2024-07-13

---

**User:**

I have two rpms dconnect-admin-menu-94.00.00.57.x86_64.rpm and dconnect-admin-menu-94.00.00.58.x86_64.rpm
While trying to install dconnect-admin-menu-94.00.00.57.x86_64.rpm I get
rpm -i dconnect-admin-menu-94.00.00.57.x86_64.rpm
package dconnect-admin-menu-0:94.00.00.57-.x86_64 does not verify: Payload SHA256 digest: BAD (Expected 19c5d081f00c4a792c977310b1626a64b4e3f31f8e8d17a85bb0c110da181f04 != cd48d6bca37af885d3dab6f6ecf10999fec85380661ecdcd91ccfd77b368db2b

Using sha256sum I checked the content of both rpms and the difference is in admin.whl file. 
Next using sha256sum, I checked the content of both admin.whl files and there the checsums are the same.
What causes the problem and how to fix it?

---

**Assistant:**

The issue you're encountering with the RPM installation is due to a mismatch in the SHA256 checksum of the RPM package, indicating that the integrity of the package has been compromised or modified. This mismatch can happen for various reasons, including file corruption during download, tampering, or errors in packaging.

Since the `admin.whl` files in both RPMs have the same checksum, it suggests that the issue might not be with the `admin.whl` file itself but rather with the RPM metadata or other contents of the RPM package.

Here are a few steps you can take to troubleshoot and potentially resolve the issue:

1. **Verify the RPM File Integrity**:
   Ensure that the RPM file itself is not corrupted. You can compare the checksum of the RPM file against a known good checksum if available.

   ```sh
   sha256sum dconnect-admin-menu-94.00.00.57.x86_64.rpm
   ```

2. **Re-download the RPM**:
   If you suspect the RPM file might be corrupted, try re-downloading it from a trusted source.

3. **Check RPM Metadata**:
   Sometimes the RPM metadata might be the cause of the issue. You can inspect the metadata using `rpm` command:

   ```sh
   rpm -Kv dconnect-admin-menu-94.00.00.57.x86_64.rpm
   ```

   This will provide more details about the verification process and where it might be failing.

4. **Rebuild the RPM**:
   If you have the source files and the spec file used to create the RPM, you can try rebuilding the RPM package. This process involves unpacking the RPM, inspecting the contents, and repackaging it.

   ```sh
   rpm2cpio dconnect-admin-menu-94.00.00.57.x86_64.rpm | cpio -idmv
   # Inspect the contents
   rpmbuild -bb your_spec_file.spec
   ```

5. **Compare RPM Contents**:
   Compare the contents of the two RPM packages to identify any differences apart from the `admin.whl` file. This can help pinpoint any discrepancies.

   ```sh
   rpm2cpio dconnect-admin-menu-94.00.00.57.x86_64.rpm | cpio -t
   rpm2cpio dconnect-admin-menu-94.00.00.58.x86_64.rpm | cpio -t
   ```

6. **Use the `--replacefiles` and `--force` Options**:
   If you are confident that the RPM package is safe and the issue is with the verification process, you can force the installation (not recommended for production systems):

   ```sh
   rpm -i --replacefiles --force dconnect-admin-menu-94.00.00.57.x86_64.rpm
   ```

   This option should be used with caution as it bypasses the integrity check.

By following these steps, you should be able to identify and potentially resolve the issue causing the checksum mismatch during the RPM installation.