# Tooling Patterns

## AOT class preloading
- **Since:** Java 25
- **Old approach:** Cold Start Every Time (Java 8)
- **Modern approach:** AOT Cache (Java 25)
- **Summary:** Cache class loading and compilation for instant startup.

### Before
```java
// Every startup:
// - Load 10,000+ classes
// - Verify bytecode
// - JIT compile hot paths
// Startup: 2-5 seconds
```

### After
```java
// Training run:
$ java -XX:AOTCacheOutput=app.aot \
    -cp app.jar com.App
// Production:
$ java -XX:AOTCache=app.aot \
    -cp app.jar com.App
```

### Why modern wins
- **Faster startup:** Skip class loading, verification, and linking.
- **Cached state:** Training run captures the ideal class state.
- **No code changes:** Works with existing applications — just add JVM flags.

### References
- [Ahead-of-Time Command-Line Ergonomics (JEP 514)](https://openjdk.org/jeps/514)
- [AOT Cache (JEP 515)](https://openjdk.org/jeps/515)

---

## Built-in HTTP server
- **Since:** Java 18
- **Old approach:** External Server / Framework (Java 8)
- **Modern approach:** jwebserver CLI (Java 18+)
- **Summary:** Java 18 includes a built-in minimal HTTP server for prototyping and file\ serving.

### Before
```java
// Install and configure a web server
// (Apache, Nginx, or embedded Jetty)

// Or write boilerplate with com.sun.net.httpserver
HttpServer server = HttpServer.create(
    new InetSocketAddress(8080), 0);
server.createContext("/", exchange -> { ... });
server.start();
```

### After
```java
// Terminal: serve current directory
$ jwebserver

// Or use the API (JDK 18+)
var server = SimpleFileServer.createFileServer(
    new InetSocketAddress(8080),
    Path.of("."),
    OutputLevel.VERBOSE);
server.start();
```

### Why modern wins
- **Zero setup:** Run jwebserver in any directory — no installation, config, or dependencies\ needed."
- **Built into the JDK:** Ships with every JDK 18+ installation, always available on any machine with\ Java."
- **Great for prototyping:** Serve static files instantly for testing HTML, APIs, or front-end development.

### References
- [Simple Web Server (JEP 408)](https://openjdk.org/jeps/408)
- [SimpleFileServer](https://docs.oracle.com/en/java/javase/25/docs/api/jdk.httpserver/com/sun/net/httpserver/SimpleFileServer.html)
- [jwebserver Tool](https://docs.oracle.com/en/java/javase/25/docs/specs/man/jwebserver.html)

---

## Compact object headers
- **Since:** Java 25
- **Old approach:** 128-bit Headers (Java 8)
- **Modern approach:** 64-bit Headers (Java 25)
- **Summary:** Cut object header size in half for better memory density and cache usage.

### Before
```java
// Default: 128-bit object header
// = 16 bytes overhead per object
// A boolean field object = 32 bytes!
// Mark word (64) + Klass pointer (64)
```

### After
```java
// -XX:+UseCompactObjectHeaders
// 64-bit object header
// = 8 bytes overhead per object
// 50% less header memory
// More objects fit in cache
```

### Why modern wins
- **50% smaller headers:** 8 bytes instead of 16 per object.
- **Better cache usage:** More objects fit in CPU cache lines.
- **Higher density:** Fit more objects in the same heap size.

### References
- [Compact Object Headers (JEP 519)](https://openjdk.org/jeps/519)

---

## JFR for profiling
- **Since:** Java 9
- **Old approach:** External Profiler (Java 8)
- **Modern approach:** Java Flight Recorder (Java 9+)
- **Summary:** Profile any Java app with the built-in Flight Recorder — no external tools.

### Before
```java
// Install VisualVM / YourKit / JProfiler
// Attach to running process
// Configure sampling
// Export and analyze
// External tool required
```

### After
```java
// Start with profiling enabled
$ java -XX:StartFlightRecording=
    filename=rec.jfr MyApp

// Or attach to running app:
$ jcmd <pid> JFR.start
```

### Why modern wins
- **Built-in:** No external profiler to install or license.
- **Low overhead:** ~1% performance impact — safe for production.
- **Rich events:** CPU, memory, GC, threads, I/O, locks, and custom events.

### References
- [JDK Flight Recorder](https://docs.oracle.com/en/java/javase/25/docs/specs/man/jfr.html)
- [Flight Recorder API (JEP 328)](https://openjdk.org/jeps/328)

---

## JShell for prototyping
- **Since:** Java 9
- **Old approach:** Create File + Compile + Run (Java 8)
- **Modern approach:** jshell REPL (Java 9+)
- **Summary:** Try Java expressions interactively without creating files.

### Before
```java
// 1. Create Test.java
// 2. javac Test.java
// 3. java Test
// Just to test one expression!
```

### After
```java
$ jshell
jshell> "hello".chars().count()
$1 ==> 5
jshell> List.of(1,2,3).reversed()
$2 ==> [3, 2, 1]
```

### Why modern wins
- **Instant feedback:** Type an expression, see the result immediately.
- **No files needed:** No .java files, no compilation step.
- **API exploration:** Tab completion helps discover methods and parameters.

### References
- [JShell Tool](https://docs.oracle.com/en/java/javase/25/jshell/introduction-jshell.html)
- [JShell (JEP 222)](https://openjdk.org/jeps/222)

---

## JUnit 6 with JSpecify null safety
- **Since:** Java 17
- **Old approach:** Unannotated API (JUnit 5)
- **Modern approach:** @NullMarked API (JUnit 6)
- **Summary:** JUnit 6 adopts JSpecify @NullMarked, making null contracts explicit across\ its assertion API.

### Before
```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class UserServiceTest {

    // JUnit 5: no null contracts on the API
    // Can assertEquals() accept null? Check source...
    // Does fail(String) allow null message? Unknown.

    @Test
    void findUser_found() {
        // Is result nullable? API doesn't say
        User result = service.findById("u1");
        assertNotNull(result);
        assertEquals("Alice", result.name());
    }

    @Test
    void findUser_notFound() {
        // Hope this returns null, not throws...
        assertNull(service.findById("missing"));
    }
}
```

### After
```java
import org.junit.jupiter.api.Test;
import org.jspecify.annotations.NullMarked;
import org.jspecify.annotations.Nullable;
import static org.junit.jupiter.api.Assertions.*;

@NullMarked  // all refs non-null unless @Nullable
class UserServiceTest {

    // JUnit 6 API is @NullMarked:
    // assertNull(@Nullable Object actual)
    // assertEquals(@Nullable Object, @Nullable Object)
    // fail(@Nullable String message)

    @Test
    void findUser_found() {
        // IDE warns: findById returns @Nullable User
        @Nullable User result = service.findById("u1");
        assertNotNull(result); // narrows type to non-null
        assertEquals("Alice", result.name()); // safe
    }

    @Test
    void findUser_notFound() {
        @Nullable User result = service.findById("missing");
        assertNull(result); // IDE confirms null expectation
    }
}
```

### Why modern wins
- **Explicit contracts:** @NullMarked on the JUnit 6 module documents null semantics directly in the\ API — no source-reading required."
- **Compile-time safety:** IDEs and analyzers warn when null is passed where non-null is expected, catching\ bugs before tests run."
- **Ecosystem standard:** JSpecify is adopted by Spring, Guava, and others — consistent null semantics\ across your whole stack."

### References
- [JUnit 6 Assertions API](https://docs.junit.org/current/api/org.junit.jupiter.api/org/junit/jupiter/api/Assertions.html)
- [JSpecify Nullness User Guide](https://jspecify.dev/docs/user-guide/)
- [Upgrading to JUnit 6.0](https://github.com/junit-team/junit-framework/wiki/Upgrading-to-JUnit-6.0/Core-Principles)

---

## Multi-file source launcher
- **Since:** Java 22
- **Old approach:** Compile All First (Java 8)
- **Modern approach:** Source Launcher (Java 22+)
- **Summary:** Launch multi-file programs without an explicit compile step.

### Before
```java
$ javac *.java
$ java Main
// Must compile all files first
// Need a build tool for dependencies
```

### After
```java
$ java Main.java
// Automatically finds and compiles
// other source files referenced
// by Main.java
```

### Why modern wins
- **Zero setup:** No build tool needed for small multi-file programs.
- **Auto-resolve:** Referenced classes are found and compiled automatically.
- **Script-like:** Run multi-file programs like scripts.

### References
- [Launch Multi-File Source-Code Programs (JEP 458)](https://openjdk.org/jeps/458)

---

## Single-file execution
- **Since:** Java 11
- **Old approach:** Two-Step Compile (Java 8)
- **Modern approach:** Direct Launch (Java 11+)
- **Summary:** Run single-file Java programs directly without javac.

### Before
```java
$ javac HelloWorld.java
$ java HelloWorld
// Two steps every time
```

### After
```java
$ java HelloWorld.java
// Compiles and runs in one step
// Also works with shebangs:
#!/usr/bin/java --source 25
```

### Why modern wins
- **One command:** java File.java compiles and runs in one step.
- **Script-like:** Add a shebang line to make .java files executable scripts.
- **Learning-friendly:** Newcomers run code immediately without learning build tools.

### References
- [Launch Single-File Source-Code Programs (JEP 330)](https://openjdk.org/jeps/330)

---
