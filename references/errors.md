# Errors Patterns

## Helpful NullPointerExceptions
- **Since:** Java 14
- **Old approach:** Cryptic NPE (Java 8)
- **Modern approach:** Detailed NPE (Java 14+)
- **Summary:** JVM automatically tells you exactly which variable was null.

### Before
```java
// Old NPE message:
// "NullPointerException"
// at MyApp.main(MyApp.java:42)
// Which variable was null?!
```

### After
```java
// Modern NPE message:
// Cannot invoke "String.length()"
// because "user.address().city()"
// is null
// Exact variable identified!
```

### Why modern wins
- **Exact variable:** The message names the null variable in the chain.
- **Faster debugging:** No more guessing which of 5 chained calls was null.
- **Free upgrade:** No code changes — just run on JDK 14+.

### References
- [Helpful NullPointerExceptions (JEP 358)](https://openjdk.org/jeps/358)

---

## Multi-catch exception handling
- **Since:** Java 7
- **Old approach:** Separate Catch Blocks (Pre-Java 7)
- **Modern approach:** Multi-catch (Java 7+)
- **Summary:** Catch multiple exception types in a single catch block.

### Before
```java
try {
    process();
} catch (IOException e) {
    log(e);
} catch (SQLException e) {
    log(e);
} catch (ParseException e) {
    log(e);
}
```

### After
```java
try {
    process();
} catch (IOException
    | SQLException
    | ParseException e) {
    log(e);
}
```

### Why modern wins
- **DRY:** Same handling logic written once instead of three times.
- **Rethrowable:** The caught exception can be rethrown with its precise type.
- **Scannable:** All handled types are visible in one place.

### References
- [Catching and Handling Exceptions (dev.java)](https://dev.java/learn/exceptions/catching-handling/)

---

## Null case in switch
- **Since:** Java 21
- **Old approach:** Guard Before Switch (Java 8)
- **Modern approach:** case null (Java 21+)
- **Summary:** Handle null directly as a switch case — no separate guard needed.

### Before
```java
// Must check before switch
if (status == null) {
    return "unknown";
}
return switch (status) {
    case ACTIVE  -> "active";
    case PAUSED  -> "paused";
    default      -> "other";
};
```

### After
```java
return switch (status) {
    case null    -> "unknown";
    case ACTIVE  -> "active";
    case PAUSED  -> "paused";
    default      -> "other";
};
```

### Why modern wins
- **Explicit:** null handling is visible right in the switch.
- **No NPE:** Switch on a null value won't throw NullPointerException.
- **All-in-one:** All cases including null in a single switch expression.

### References
- [Pattern Matching for switch (JEP 441)](https://openjdk.org/jeps/441)

---

## Optional chaining
- **Since:** Java 9
- **Old approach:** Nested Null Checks (Java 8)
- **Modern approach:** Optional Pipeline (Java 9+)
- **Summary:** Replace nested null checks with an Optional pipeline.

### Before
```java
String city = null;
if (user != null) {
    Address addr = user.getAddress();
    if (addr != null) {
        city = addr.getCity();
    }
}
if (city == null) city = "Unknown";
```

### After
```java
String city = Optional.ofNullable(user)
    .map(User::address)
    .map(Address::city)
    .orElse("Unknown");
```

### Why modern wins
- **Chainable:** Each .map() step handles null transparently.
- **Linear flow:** Read left-to-right instead of nested if-blocks.
- **NPE-proof:** null is handled at each step — no crash possible.

### References
- [Optional](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Optional.html)

---

## Optional.orElseThrow() without supplier
- **Since:** Java 10
- **Old approach:** get() or orElseThrow(supplier) (Java 8)
- **Modern approach:** orElseThrow() (Java 10+)
- **Summary:** Use Optional.orElseThrow() as a clearer, intent-revealing alternative to\ get().

### Before
```java
// Risky: get() throws if empty, no clear intent
String value = optional.get();

// Verbose: supplier just for NoSuchElementException
String value = optional
    .orElseThrow(NoSuchElementException::new);
```

### After
```java
// Clear intent: throws NoSuchElementException if empty
String value = optional.orElseThrow();
```

### Why modern wins
- **Self-documenting:** orElseThrow() clearly signals that absence is unexpected.
- **Avoids get():** Static analysis tools flag get() as risky; orElseThrow() is idiomatic.
- **Less boilerplate:** No need to pass a supplier for the default NoSuchElementException.

### References
- [Optional.orElseThrow()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Optional.html#orElseThrow())

---

## Record-based error responses
- **Since:** Java 16
- **Old approach:** Map or Verbose Class (Java 8)
- **Modern approach:** Error Records (Java 16+)
- **Summary:** Use records for concise, immutable error response types.

### Before
```java
// Verbose error class
public class ErrorResponse {
    private final int code;
    private final String message;
    // constructor, getters, equals,
    // hashCode, toString...
}
```

### After
```java
public record ApiError(
    int code,
    String message,
    Instant timestamp
) {
    public ApiError(int code, String msg) {
        this(code, msg, Instant.now());
    }
}
```

### Why modern wins
- **Concise:** Define error types in 3 lines instead of 30.
- **Immutable:** Error data can't be accidentally modified after creation.
- **Auto toString:** Perfect for logging — shows all fields automatically.

### References
- [Records (JEP 395)](https://openjdk.org/jeps/395)
- [Record class](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Record.html)

---

## Objects.requireNonNullElse()
- **Since:** Java 9
- **Old approach:** Ternary Null Check (Java 8)
- **Modern approach:** requireNonNullElse() (Java 9+)
- **Summary:** Get a non-null value with a clear default, no ternary needed.

### Before
```java
String name = input != null
    ? input
    : "default";
// easy to get the order wrong
```

### After
```java
String name = Objects
    .requireNonNullElse(
        input, "default"
    );
```

### Why modern wins
- **Clear intent:** Method name describes exactly what it does.
- **Null-safe default:** The default value is also checked for null.
- **Readable:** Better than ternary for simple null-or-default logic.

### References
- [Objects.requireNonNullElse()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Objects.html#requireNonNullElse(T,T))
- [Objects.requireNonNullElseGet()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Objects.html#requireNonNullElseGet(T,java.util.function.Supplier))

---
