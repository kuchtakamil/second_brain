# Checksum Error in RPM

**Data:** 2024-07-13

---

**User:**

Popraw następujący tekst po angielsku

When I build rpm with my app, from time to time I get an error connected with rpm's checksum. I will present the issue on the two examples versions 15 and 16. 
I have two built rpms calculator-15.x86_64.rpm and calculator-16.x86_64.rpm. The rpms were built using gradle plugin `gradle-ospackage-plugin`.
While trying to install calculator-15.x86_64.rpm I get
rpm -i calculator-15.x86_64.rpm
package calculator-15.x86_64.rpm does not verify: Payload SHA256 digest: BAD (Expected 19c5d081f00c4a792..... != cd48d6bca37af885d3dab6f6ecf1......)

Using the following command

    rpm -qp --qf '[%{FILENAMES} %{FILEDIGESTS}\n]' calculator.rpm > sums.txt

I checked the content of both rpms and a `calc.whl` file (wheel Python package) has different checksum in both rpms. `calc.whl` in rpm version 15 has a different checksum then calc.whl in rpm version 16.
Next after extracting calc.whl using unzip, I checked the sha256 for content of both calc.whl files and there the checsums are the same. The command which I used

    find calc-type f -exec sha256sum {} \; | sort -k 2 > whl_sums.txt

Also files in *dist-info were checked. It seems to be no difference between those two calc.whl

But still rpm version 15 cannot be installed because of checksum error.

---

**Assistant:**

Here is the corrected version of your text:

---

When I build an RPM for my app, I occasionally encounter an error related to the RPM's checksum. I will present the issue using two example versions: 15 and 16.

I have two built RPMs: `calculator-15.x86_64.rpm` and `calculator-16.x86_64.rpm`. These RPMs were built using the Gradle plugin `gradle-ospackage-plugin`. While trying to install `calculator-15.x86_64.rpm`, I get the following error:

```
rpm -i calculator-15.x86_64.rpm
package calculator-15.x86_64.rpm does not verify: Payload SHA256 digest: BAD (Expected 19c5d081f00c4a792..... != cd48d6bca37af885d3dab6f6ecf1......)
```

Using the following command:

```
rpm -qp --qf '[%{FILENAMES} %{FILEDIGESTS}\n]' calculator.rpm > sums.txt
```

I checked the content of both RPMs, and found that the `calc.whl` file (a Python wheel package) has different checksums in each RPM. The `calc.whl` in RPM version 15 has a different checksum than the `calc.whl` in RPM version 16.

Next, after extracting `calc.whl` using `unzip`, I checked the SHA256 checksums for the contents of both `calc.whl` files. The checksums were the same. The command I used was:

```
find calc-type f -exec sha256sum {} \; | sort -k 2 > whl_sums.txt
```

I also checked the files in `*dist-info` and found no differences between the two `calc.whl` files.

Despite this, RPM version 15 still cannot be installed due to a checksum error.