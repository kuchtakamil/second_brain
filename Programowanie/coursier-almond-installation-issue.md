# Coursier Almond Installation Issue

**Data:** 2024-11-03

---

**User:**

./coursier launch --use-bootstrap almond:0.10.0 --scala 2.12.11 -- --install
Unrecognized argument: --use-bootstrap

---

**Assistant:**

It looks like the `--use-bootstrap` argument is not recognized by `coursier`. This option may have been deprecated or replaced. Try running the command without `--use-bootstrap`:

```bash
./coursier launch almond:0.10.0 --scala 2.12.11 -- --install
```

If this doesn’t work, here are a few suggestions:

1. **Update Coursier**: Ensure that you are using the latest version of `coursier`. You can update it by running:
   ```bash
   cs update
   ```

2. **Check Coursier Documentation**: Since arguments can change with newer versions, it’s worth checking the [Coursier documentation](https://get-coursier.io/docs/cli-overview) to confirm the current options.

3. **Alternative Command**: If you are trying to install the Almond Scala kernel, you could try using the installation script directly provided by Almond:

   ```bash
   SCALA_VERSION=2.12.11 ALMOND_VERSION=0.10.0 sh -c "$(curl -fsSL https://raw.githubusercontent.com/almond-sh/almond/main/scripts/download)"
   ```

This script should automatically install the Almond kernel with the specified Scala version.