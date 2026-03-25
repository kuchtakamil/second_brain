# Java: Eager or Lazy?

**Data:** 2023-07-20

---

**User:**

In Future in Java eagar or lazy?

---

**Assistant:**

As of my last update in September 2021, Java is predominantly a "eager" language when it comes to evaluating expressions and performing computations. This means that Java typically evaluates expressions and computes values as soon as they are encountered in the code, without postponing the evaluation until it's strictly necessary.

For example, in Java, when you have an expression like this:

```java
int result = 5 + 3;
```

The addition operation `5 + 3` will be eagerly evaluated, and the result (`8`) will be stored in the variable `result`.

Similarly, when you call a method in Java, all the arguments to the method are evaluated before the method is invoked.

However, there are certain cases where Java can use "lazy evaluation" with the help of certain constructs like the short-circuit operators `&&` and `||` (logical AND and OR). These operators evaluate expressions from left to right and stop the evaluation as soon as the result can be determined.

For example:

```java
if (a == 5 && b == 10) {
    // Code block
}
```

In this case, if `a` is not equal to 5, the second condition (`b == 10`) will not be evaluated, as the result of the entire expression can already be determined to be `false`.

Overall, while Java is primarily an eager language, certain constructs allow for a degree of lazy evaluation, which can be useful in certain scenarios for optimizing performance and avoiding unnecessary computations. However, the core behavior of Java is mostly eager evaluation. If there have been any changes or updates to the language after my last update in September 2021, I would not be aware of them.

---

**User:**

But I asked about tasks put into Future. When executor produces a Future, does this Future is run at the moment when it was created or until the get method is called? 

---

**Assistant:**

Apologies for the confusion in my previous response. I understand your question now.

When you submit a task to an executor that returns a `Future` in Java, the task is typically executed asynchronously by the executor. The `Future` represents a result that will be available in the future, once the task has completed its execution. The task itself is not executed immediately when the `Future` is created; instead, it will be executed by the executor at some point in the future, usually as soon as a thread becomes available in the executor's thread pool.

The `Future` itself acts as a placeholder for the result of the computation and provides a way for you to interact with the task's outcome. You can use the `get()` method on the `Future` object to wait for the task to complete and obtain its result. If the task hasn't completed yet when you call `get()`, the method will block until the task finishes.

Here's an example of how you would typically use `Future` with an executor:

```java
ExecutorService executor = Executors.newFixedThreadPool(1); // Create an executor with one thread

Future<Integer> future = executor.submit(() -> {
    // Some time-consuming task
    return 42; // Result of the computation
});

// Other work can be done here concurrently

try {
    // Wait for the task to complete and get the result
    int result = future.get();
    System.out.println("Result: " + result);
} catch (InterruptedException | ExecutionException e) {
    e.printStackTrace();
}

executor.shutdown(); // Shutdown the executor when it's no longer needed
```

In this example, the task is submitted to the executor using the `submit()` method, which returns a `Future`. The task will be executed asynchronously by the executor, and you can retrieve its result by calling the `get()` method on the `Future` object. If the task hasn't completed yet, `get()` will block until the result is available.

So, to answer your question directly, the task represented by the `Future` is executed by the executor when it is submitted, not when you call `get()`. The `get()` method allows you to wait for the task to finish and retrieve its result.