# JVM Error: Missing Modules

**Data:** 2023-12-03

---

**User:**

w .jvmopts mam
--add-exports java.base/sun.nio.ch=ALL-UNNAMED

dostaje błąd
Error: --add-exports requires modules to be specified

---

**Assistant:**

Looks like you are trying to use the `--add-exports` option in the Java Virtual Machine (JVM) configuration, but you are missing the module specification. The `--add-exports` option requires you to specify the module from which you want to export a package and the module to which the package should be exported.

In your case, you need to specify the relevant modules for the `java.base/sun.nio.ch` package. For example, if you want to export this package to all unnamed modules, you can use the following syntax:

```bash
--add-exports java.base/sun.nio.ch=ALL-UNNAMED
```

However, if you are facing an error, it might be because this syntax is not supported in your Java version. Starting from Java 9, modules were introduced, and you need to ensure that the modules involved support the `--add-exports` option.

Here is an example of how you might specify modules:

```bash
--add-exports java.base/sun.nio.ch=your_module_name
```

Replace `your_module_name` with the actual name of the module you are working with.

Please note that this answer assumes you are using a Java version that supports modules. If you are using an older version of Java, you might want to consider updating to a newer version that supports modules.