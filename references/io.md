# Io Patterns

## Deserialization filters
- **Since:** Java 9
- **Old approach:** Accept Everything (Java 8)
- **Modern approach:** ObjectInputFilter (Java 9+)
- **Summary:** Restrict which classes can be deserialized to prevent attacks.

### Before
```java
// Dangerous: accepts any class
ObjectInputStream ois =
    new ObjectInputStream(input);
Object obj = ois.readObject();
// deserialization attacks possible!
```

### After
```java
ObjectInputFilter filter =
    ObjectInputFilter.Config
    .createFilter(
        "com.myapp.*;!*"
    );
ois.setObjectInputFilter(filter);
Object obj = ois.readObject();
```

### Why modern wins
- **Security:** Prevent deserialization of unexpected/malicious classes.
- **Fine-grained:** Control depth, array size, references, and class patterns.
- **JVM-wide:** Set a global filter for all deserialization in the JVM.

### References
- [ObjectInputFilter](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/io/ObjectInputFilter.html)
- [Deserialization Filtering Guide](https://docs.oracle.com/en/java/javase/25/core/serialization-filtering1.html)

---

## File memory mapping
- **Since:** Java 22
- **Old approach:** MappedByteBuffer (Java 8)
- **Modern approach:** MemorySegment with Arena (Java 22+)
- **Summary:** Map files larger than 2GB with deterministic cleanup using MemorySegment.

### Before
```java
try (FileChannel channel =
    FileChannel.open(path,
        StandardOpenOption.READ,
        StandardOpenOption.WRITE)) {
    MappedByteBuffer buffer =
        channel.map(
            FileChannel.MapMode.READ_WRITE,
            0, (int) channel.size());
    // Limited to 2GB
    // Freed by GC, no control
}
```

### After
```java
FileChannel channel =
    FileChannel.open(path,
        StandardOpenOption.READ,
        StandardOpenOption.WRITE);
try (Arena arena = Arena.ofShared()) {
    MemorySegment segment =
        channel.map(
            FileChannel.MapMode.READ_WRITE,
            0, channel.size(), arena);
    // No size limit
    // ...
} // Deterministic cleanup
```

### Why modern wins
- **No size limit:** Map files larger than 2GB without workarounds.
- **Deterministic cleanup:** Arena ensures memory is freed at scope exit, not GC time.
- **Better performance:** Aligned with modern memory models and hardware.

### References
- [MemorySegment (Java 22)](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/foreign/MemorySegment.html)
- [Arena (Java 22)](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/foreign/Arena.html)
- [JEP 454: Foreign Function & Memory API](https://openjdk.org/jeps/454)

---

## Files.mismatch()
- **Since:** Java 12
- **Old approach:** Manual Byte Compare (Java 8)
- **Modern approach:** Files.mismatch() (Java 12+)
- **Summary:** Compare two files efficiently without loading them into memory.

### Before
```java
// Compare two files byte by byte
byte[] f1 = Files.readAllBytes(path1);
byte[] f2 = Files.readAllBytes(path2);
boolean equal = Arrays.equals(f1, f2);
// loads both files entirely into memory
```

### After
```java
long pos = Files.mismatch(path1, path2);
// -1 if identical
// otherwise: position of first difference
```

### Why modern wins
- **Memory-efficient:** Doesn't load entire files into byte arrays.
- **Pinpoints difference:** Returns the exact byte position of the first mismatch.
- **One call:** No manual byte array comparison logic.

### References
- [Files.mismatch()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/nio/file/Files.html#mismatch(java.nio.file.Path,java.nio.file.Path))

---

## Modern HTTP client
- **Since:** Java 11
- **Old approach:** HttpURLConnection (Java 8)
- **Modern approach:** HttpClient (Java 11+)
- **Summary:** Use the built-in HttpClient for clean, modern HTTP requests.

### Before
```java
URL url = new URL("https://api.com/data");
HttpURLConnection con =
    (HttpURLConnection) url.openConnection();
con.setRequestMethod("GET");
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
// read lines, close streams...
```

### After
```java
var client = HttpClient.newHttpClient();
var request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.com/data"))
    .build();
var response = client.send(
    request, BodyHandlers.ofString());
String body = response.body();
```

### Why modern wins
- **Builder API:** Fluent builder for requests, headers, and timeouts.
- **HTTP/2 support:** Built-in HTTP/2 with multiplexing and server push.
- **Async ready:** sendAsync() returns CompletableFuture.

### References
- [HttpClient (JEP 321)](https://openjdk.org/jeps/321)
- [HttpClient](https://docs.oracle.com/en/java/javase/25/docs/api/java.net.http/java/net/http/HttpClient.html)

---

## InputStream.transferTo()
- **Since:** Java 9
- **Old approach:** Manual Copy Loop (Java 8)
- **Modern approach:** transferTo() (Java 9+)
- **Summary:** Copy an InputStream to an OutputStream in one call.

### Before
```java
byte[] buf = new byte[8192];
int n;
while ((n = input.read(buf)) != -1) {
    output.write(buf, 0, n);
}
```

### After
```java
input.transferTo(output);
```

### Why modern wins
- **One line:** Replace the entire read/write loop with one method call.
- **Optimized:** Internal buffer size is tuned for performance.
- **No bugs:** No off-by-one errors in buffer management.

### References
- [InputStream.transferTo()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/io/InputStream.html#transferTo(java.io.OutputStream))

---

## IO class for console I/O
- **Since:** Java 25
- **Old approach:** System.out / Scanner (Java 8)
- **Modern approach:** IO class (Java 25+)
- **Summary:** The new IO class provides simple, concise methods for console input and\ output.

### Before
```java
import java.util.Scanner;

Scanner sc = new Scanner(System.in);
System.out.print("Name: ");
String name = sc.nextLine();
System.out.println("Hello, " + name);
sc.close();
```

### After
```java
String name = IO.readln("Name: ");
IO.println("Hello, " + name);
```

### Why modern wins
- **Dramatically simpler:** Two methods replace seven lines of Scanner setup, prompting, reading, and\ cleanup."
- **No resource leaks:** No Scanner to close — IO methods handle resource management internally.
- **Beginner-friendly:** New developers can do console I/O without learning Scanner, System.out, or\ import statements."

### References
- [Simple Source Files (JEP 495)](https://openjdk.org/jeps/495)
- [IO](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/IO.html)

---

## Path.of() factory
- **Since:** Java 11
- **Old approach:** Paths.get() (Java 8)
- **Modern approach:** Path.of() (Java 11+)
- **Summary:** Use Path.of() — the modern factory method on the Path interface.

### Before
```java
Path path = Paths.get("src", "main",
    "java", "App.java");
```

### After
```java
var path = Path.of("src", "main",
    "java", "App.java");
```

### Why modern wins
- **Consistent API:** Follows the .of() factory pattern like List.of(), Set.of().
- **Discoverable:** Found on the Path type itself, not a separate Paths class.
- **One less class:** No need to import the Paths utility class.

### References
- [Path.of()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/nio/file/Path.html#of(java.lang.String,java.lang.String...))

---

## Reading files
- **Since:** Java 11
- **Old approach:** BufferedReader (Java 8)
- **Modern approach:** Files.readString() (Java 11+)
- **Summary:** Read an entire file into a String with one line.

### Before
```java
StringBuilder sb = new StringBuilder();
try (BufferedReader br =
    new BufferedReader(
        new FileReader("data.txt"))) {
    String line;
    while ((line = br.readLine()) != null)
        sb.append(line).append("\n");
}
String content = sb.toString();
```

### After
```java
String content =
    Files.readString(Path.of("data.txt"));
```

### Why modern wins
- **One line:** Replace 8 lines of BufferedReader boilerplate.
- **Auto cleanup:** File handle is closed automatically.
- **UTF-8 default:** Correct encoding by default — no charset confusion.

### References
- [Files.readString()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/nio/file/Files.html#readString(java.nio.file.Path))
- [Files.readAllLines()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/nio/file/Files.html#readAllLines(java.nio.file.Path))

---

## Try-with-resources improvement
- **Since:** Java 9
- **Old approach:** Re-declare Variable (Java 8)
- **Modern approach:** Effectively Final (Java 9+)
- **Summary:** Use existing effectively-final variables directly in try-with-resources.

### Before
```java
Connection conn = getConnection();
// Must re-declare in try
try (Connection c = conn) {
    use(c);
}
```

### After
```java
Connection conn = getConnection();
// Use existing variable directly
try (conn) {
    use(conn);
}
```

### Why modern wins
- **No re-declaration:** Use the existing variable name directly.
- **Less confusion:** No separate variable name inside the try block.
- **Concise:** Fewer lines, same resource safety.

### References
- [Catching and Handling Exceptions (dev.java)](https://dev.java/learn/exceptions/catching-handling/)

---

## Writing files
- **Since:** Java 11
- **Old approach:** FileWriter + BufferedWriter (Java 8)
- **Modern approach:** Files.writeString() (Java 11+)
- **Summary:** Write a String to a file with one line.

### Before
```java
try (FileWriter fw =
        new FileWriter("out.txt");
    BufferedWriter bw =
        new BufferedWriter(fw)) {
    bw.write(content);
}
```

### After
```java
Files.writeString(
    Path.of("out.txt"),
    content
);
```

### Why modern wins
- **One line:** No writer wrapping or try-with-resources needed.
- **Safe defaults:** UTF-8 encoding, proper file handle cleanup.
- **Options:** Pass OpenOption flags for append, create, etc.

### References
- [Files.writeString()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/nio/file/Files.html#writeString(java.nio.file.Path,java.lang.CharSequence,java.nio.file.OpenOption...))

---
