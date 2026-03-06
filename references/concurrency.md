# Concurrency Patterns

## CompletableFuture chaining
- **Since:** Java 8
- **Old approach:** Blocking Future.get() (Pre-Java 8)
- **Modern approach:** CompletableFuture (Java 8+)
- **Summary:** Chain async operations without blocking, using CompletableFuture.

### Before
```java
Future<String> future =
    executor.submit(this::fetchData);
String data = future.get(); // blocks
String result = transform(data);
```

### After
```java
CompletableFuture.supplyAsync(
    this::fetchData
)
.thenApply(this::transform)
.thenAccept(IO::println);
```

### Why modern wins
- **Chainable:** Compose async steps into a readable pipeline.
- **Non-blocking:** No thread sits idle waiting for results.
- **Error handling:** exceptionally() and handle() for clean error recovery.

### References
- [CompletableFuture](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/CompletableFuture.html)

---

## Concurrent HTTP with virtual threads
- **Since:** Java 21
- **Old approach:** Thread Pool + URLConnection (Java 8)
- **Modern approach:** Virtual Threads + HttpClient (Java 21+)
- **Summary:** Fetch many URLs concurrently with virtual threads and HttpClient.

### Before
```java
ExecutorService pool =
    Executors.newFixedThreadPool(10);
List<Future<String>> futures =
    urls.stream()
    .map(u -> pool.submit(
        () -> fetchUrl(u)))
    .toList();
// manual shutdown, blocking get()
```

### After
```java
try (var exec = Executors
    .newVirtualThreadPerTaskExecutor()) {
    var results = urls.stream()
        .map(u -> exec.submit(
            () -> client.send(req(u),
                ofString()).body()))
        .toList().stream()
        .map(Future::join).toList();
}
```

### Why modern wins
- **Thread per request:** No pool sizing — one virtual thread per URL.
- **Simple code:** Write straightforward blocking code.
- **High throughput:** Thousands of concurrent requests with minimal resources.

### References
- [Virtual Threads (JEP 444)](https://openjdk.org/jeps/444)
- [HttpClient](https://docs.oracle.com/en/java/javase/25/docs/api/java.net.http/java/net/http/HttpClient.html)

---

## ExecutorService auto-close
- **Since:** Java 19
- **Old approach:** Manual Shutdown (Java 8)
- **Modern approach:** try-with-resources (Java 19+)
- **Summary:** Use try-with-resources for automatic executor shutdown.

### Before
```java
ExecutorService exec =
    Executors.newCachedThreadPool();
try {
    exec.submit(task);
} finally {
    exec.shutdown();
    exec.awaitTermination(
        1, TimeUnit.MINUTES);
}
```

### After
```java
try (var exec =
        Executors.newCachedThreadPool()) {
    exec.submit(task);
}
// auto shutdown + await on close
```

### Why modern wins
- **Auto cleanup:** Shutdown happens automatically when the block exits.
- **No leaks:** Executor always shuts down, even if exceptions occur.
- **Familiar pattern:** Same try-with-resources used for files, connections, etc.

### References
- [ExecutorService](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/ExecutorService.html)

---

## Lock-free lazy initialization
- **Since:** Java 25
- **Old approach:** synchronized + volatile (Java 8)
- **Modern approach:** StableValue (Java 25 (Preview))
- **Summary:** Replace double-checked locking with StableValue for lazy singletons.

### Before
```java
class Config {
    private static volatile Config inst;
    static Config get() {
        if (inst == null) {
            synchronized (Config.class) {
                if (inst == null)
                    inst = load();
            }
        }
        return inst;
    }
}
```

### After
```java
class Config {
    private static final
        StableValue<Config> INST =
            StableValue.of(Config::load);

    static Config get() {
        return INST.get();
    }
}
```

### Why modern wins
- **No boilerplate:** No volatile, synchronized, or double-null-check.
- **Faster reads:** JVM can constant-fold after initialization.
- **Provably correct:** No subtle ordering bugs — the JVM handles it.

### References
- [StableValue (JEP 502)](https://openjdk.org/jeps/502)
- [StableValue](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/StableValue.html)

---

## Modern Process API
- **Since:** Java 9
- **Old approach:** Runtime.exec() (Java 8)
- **Modern approach:** ProcessHandle (Java 9+)
- **Summary:** Inspect and manage OS processes with ProcessHandle.

### Before
```java
Process p = Runtime.getRuntime()
    .exec("ls -la");
int code = p.waitFor();
// no way to get PID
// no easy process info
```

### After
```java
ProcessHandle ph =
    ProcessHandle.current();
long pid = ph.pid();
ph.info().command()
    .ifPresent(IO::println);
ph.children().forEach(
    c -> IO.println(c.pid()));
```

### Why modern wins
- **Full info:** Access PID, command, arguments, start time, CPU usage.
- **Process tree:** Navigate parent, children, and descendants.
- **Monitoring:** onExit() returns a CompletableFuture for async monitoring.

### References
- [ProcessHandle](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/ProcessHandle.html)
- [Process API (JEP 102)](https://openjdk.org/jeps/102)

---

## Scoped values
- **Since:** Java 25
- **Old approach:** ThreadLocal (Java 8)
- **Modern approach:** ScopedValue (Java 25)
- **Summary:** Share data across call stacks safely without ThreadLocal pitfalls.

### Before
```java
static final ThreadLocal<User> CURRENT =
    new ThreadLocal<>();
void handle(Request req) {
    CURRENT.set(authenticate(req));
    try { process(); }
    finally { CURRENT.remove(); }
}
```

### After
```java
static final ScopedValue<User> CURRENT =
    ScopedValue.newInstance();
void handle(Request req) {
    ScopedValue.where(CURRENT,
        authenticate(req)
    ).run(this::process);
}
```

### Why modern wins
- **Immutable:** Callees can read but never modify the scoped value.
- **Auto cleanup:** No manual remove() — value is scoped to the block.
- **Virtual-thread safe:** Works efficiently with millions of virtual threads.

### References
- [Scoped Values (JEP 487)](https://openjdk.org/jeps/487)
- [ScopedValue](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/ScopedValue.html)

---

## Stable values
- **Since:** Java 25
- **Old approach:** Double-Checked Locking (Java 8)
- **Modern approach:** StableValue (Java 25 (Preview))
- **Summary:** Thread-safe lazy initialization without volatile or synchronized.

### Before
```java
private volatile Logger logger;
Logger getLogger() {
    if (logger == null) {
        synchronized (this) {
            if (logger == null)
                logger = createLogger();
        }
    }
    return logger;
}
```

### After
```java
private final StableValue<Logger> logger =
    StableValue.of(this::createLogger);

Logger getLogger() {
    return logger.get();
}
```

### Why modern wins
- **Zero boilerplate:** No volatile, synchronized, or null checks.
- **JVM-optimized:** The JVM can fold the value after initialization.
- **Guaranteed once:** The supplier runs exactly once, even under contention.

### References
- [Stable Values (JEP 502)](https://openjdk.org/jeps/502)
- [StableValue](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/StableValue.html)

---

## Structured concurrency
- **Since:** Java 25
- **Old approach:** Manual Thread Lifecycle (Java 8)
- **Modern approach:** StructuredTaskScope (Java 25 (Preview))
- **Summary:** Manage concurrent task lifetimes as a single unit of work.

### Before
```java
ExecutorService exec =
    Executors.newFixedThreadPool(2);
Future<User> u = exec.submit(this::fetchUser);
Future<Order> o = exec.submit(this::fetchOrder);
try {
    return combine(u.get(), o.get());
} finally { exec.shutdown(); }
```

### After
```java
try (var scope = new StructuredTaskScope
        .ShutdownOnFailure()) {
    var u = scope.fork(this::fetchUser);
    var o = scope.fork(this::fetchOrder);
    scope.join().throwIfFailed();
    return combine(u.get(), o.get());
}
```

### Why modern wins
- **No thread leaks:** All forked tasks complete before the scope closes.
- **Fast failure:** ShutdownOnFailure cancels siblings if one fails.
- **Clear structure:** Task lifetime matches the lexical scope in code.

### References
- [Structured Concurrency (JEP 499)](https://openjdk.org/jeps/499)
- [StructuredTaskScope](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/StructuredTaskScope.html)

---

## Thread.sleep with Duration
- **Since:** Java 19
- **Old approach:** Milliseconds (Java 8)
- **Modern approach:** Duration (Java 19+)
- **Summary:** Use Duration for self-documenting time values.

### Before
```java
// What unit is 5000? ms? us?
Thread.sleep(5000);

// 2.5 seconds: math required
Thread.sleep(2500);
```

### After
```java
Thread.sleep(
    Duration.ofSeconds(5)
);
Thread.sleep(
    Duration.ofMillis(2500)
);
```

### Why modern wins
- **Self-documenting:** Duration.ofSeconds(5) is unambiguous.
- **Unit-safe:** No accidentally passing microseconds as milliseconds.
- **Composable:** Duration math: plus(), multipliedBy(), etc.

### References
- [Thread.sleep(Duration)](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Thread.html#sleep(java.time.Duration))

---

## Virtual threads
- **Since:** Java 21
- **Old approach:** Platform Threads (Java 8)
- **Modern approach:** Virtual Threads (Java 21+)
- **Summary:** Create millions of lightweight virtual threads instead of heavy OS threads.

### Before
```java
Thread thread = new Thread(() -> {
    System.out.println("hello");
});
thread.start();
thread.join();
```

### After
```java
Thread.startVirtualThread(() -> {
    IO.println("hello");
}).join();
```

### Why modern wins
- **Lightweight:** Virtual threads use KB of memory, platform threads use MB.
- **Scalable:** Create millions of threads — no pool sizing needed.
- **Simple model:** Write blocking code that scales like async code.

### References
- [Virtual Threads (JEP 444)](https://openjdk.org/jeps/444)
- [Thread.ofVirtual()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Thread.html#ofVirtual())

---
