# Streams Patterns

## Collectors.flatMapping()
- **Since:** Java 9
- **Old approach:** Nested flatMap (Java 8)
- **Modern approach:** flatMapping() (Java 9+)
- **Summary:** Use flatMapping() to flatten inside a grouping collector.

### Before
```java
// Flatten within a grouping collector
// Required complex custom collector
Map<String, Set<String>> tagsByDept =
    // no clean way in Java 8
```

### After
```java
var tagsByDept = employees.stream()
    .collect(groupingBy(
        Emp::dept,
        flatMapping(
            e -> e.tags().stream(),
            toSet()
        )
    ));
```

### Why modern wins
- **Composable:** Works as a downstream collector inside groupingBy.
- **One pass:** Flatten and group in a single stream traversal.
- **Nestable:** Combine with other downstream collectors.

### References
- [Collectors.flatMapping()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/stream/Collectors.html#flatMapping(java.util.function.Function,java.util.stream.Collector))

---

## Optional.ifPresentOrElse()
- **Since:** Java 9
- **Old approach:** if/else on Optional (Java 8)
- **Modern approach:** ifPresentOrElse() (Java 9+)
- **Summary:** Handle both present and empty cases of Optional in one call.

### Before
```java
Optional<User> user = findUser(id);
if (user.isPresent()) {
    greet(user.get());
} else {
    handleMissing();
}
```

### After
```java
findUser(id).ifPresentOrElse(
    this::greet,
    this::handleMissing
);
```

### Why modern wins
- **Single expression:** Both cases handled in one method call.
- **No get():** Eliminates the dangerous isPresent() + get() pattern.
- **Fluent:** Chains naturally after findUser() or any Optional-returning method.

### References
- [Optional.ifPresentOrElse()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Optional.html#ifPresentOrElse(java.util.function.Consumer,java.lang.Runnable))

---

## Optional.or() fallback
- **Since:** Java 9
- **Old approach:** Nested Fallback (Java 8)
- **Modern approach:** .or() chain (Java 9+)
- **Summary:** Chain Optional fallbacks without nested checks.

### Before
```java
Optional<Config> cfg = primary();
if (!cfg.isPresent()) {
    cfg = secondary();
}
if (!cfg.isPresent()) {
    cfg = defaults();
}
```

### After
```java
Optional<Config> cfg = primary()
    .or(this::secondary)
    .or(this::defaults);
```

### Why modern wins
- **Chainable:** Stack fallbacks in a readable pipeline.
- **Lazy evaluation:** Fallback suppliers only execute if needed.
- **Declarative:** Reads as 'try primary, or secondary, or defaults'.

### References
- [Optional.or()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Optional.html#or(java.util.function.Supplier))

---

## Predicate.not() for negation
- **Since:** Java 11
- **Old approach:** Lambda negation (Java 8)
- **Modern approach:** Predicate.not() (Java 11+)
- **Summary:** Use Predicate.not() to negate method references cleanly instead of writing\ lambda wrappers.

### Before
```java
List<String> nonEmpty = list.stream()
    .filter(s -> !s.isBlank())
    .collect(Collectors.toList());
```

### After
```java
List<String> nonEmpty = list.stream()
    .filter(Predicate.not(String::isBlank))
    .toList();
```

### Why modern wins
- **Cleaner negation:** No need to wrap method references in lambdas just to negate them.
- **Composable:** Works with any Predicate, enabling clean predicate chains.
- **Reads naturally:** Predicate.not(String::isBlank) reads like English.

### References
- [Predicate.not()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/function/Predicate.html#not(java.util.function.Predicate))

---

## Stream gatherers
- **Since:** Java 24
- **Old approach:** Custom Collector (Java 8)
- **Modern approach:** gather() (Java 24+)
- **Summary:** Use gatherers for custom intermediate stream operations.

### Before
```java
// Sliding window: manual implementation
List<List<T>> windows = new ArrayList<>();
for (int i = 0; i <= list.size()-3; i++) {
    windows.add(
        list.subList(i, i + 3));
}
```

### After
```java
var windows = stream
    .gather(
        Gatherers.windowSliding(3)
    )
    .toList();
```

### Why modern wins
- **Composable:** Gatherers compose with other stream operations.
- **Built-in operations:** windowFixed, windowSliding, fold, scan out of the box.
- **Extensible:** Write custom gatherers for any intermediate transformation.

### References
- [Stream Gatherers (JEP 485)](https://openjdk.org/jeps/485)
- [Gatherers](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/stream/Gatherers.html)

---

## Stream.iterate() with predicate
- **Since:** Java 9
- **Old approach:** iterate + limit (Java 8)
- **Modern approach:** iterate(seed, pred, op) (Java 9+)
- **Summary:** Use a predicate to stop iteration — like a for-loop in stream form.

### Before
```java
Stream.iterate(1, n -> n * 2)
    .limit(10)
    .forEach(System.out::println);
// can't stop at a condition
```

### After
```java
Stream.iterate(
    1,
    n -> n < 1000,
    n -> n * 2
).forEach(IO::println);
// stops when n >= 1000
```

### Why modern wins
- **Natural termination:** Stop based on a condition, not an arbitrary limit.
- **For-loop equivalent:** Same semantics as for(seed; hasNext; next).
- **No infinite stream risk:** The predicate guarantees termination.

### References
- [Stream.iterate()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/stream/Stream.html#iterate(T,java.util.function.Predicate,java.util.function.UnaryOperator))

---

## Stream.mapMulti()
- **Since:** Java 16
- **Old approach:** flatMap + List (Java 8)
- **Modern approach:** mapMulti() (Java 16+)
- **Summary:** Emit zero or more elements per input without creating intermediate streams.

### Before
```java
stream.flatMap(order ->
    order.items().stream()
        .map(item -> new OrderItem(
            order.id(), item)
        )
);
```

### After
```java
stream.<OrderItem>mapMulti(
    (order, downstream) -> {
        for (var item : order.items())
            downstream.accept(
                new OrderItem(order.id(), item));
    }
);
```

### Why modern wins
- **Less allocation:** No intermediate Stream created per element.
- **Imperative style:** Use loops and conditionals directly.
- **Flexible:** Emit zero, one, or many elements with full control.

### References
- [Stream.mapMulti()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/stream/Stream.html#mapMulti(java.util.function.BiConsumer))

---

## Stream.ofNullable()
- **Since:** Java 9
- **Old approach:** Null Check (Java 8)
- **Modern approach:** ofNullable() (Java 9+)
- **Summary:** Create a zero-or-one element stream from a nullable value.

### Before
```java
Stream<String> s = val != null
    ? Stream.of(val)
    : Stream.empty();
```

### After
```java
Stream<String> s =
    Stream.ofNullable(val);
```

### Why modern wins
- **Concise:** One call replaces the ternary conditional.
- **Flatmap-friendly:** Perfect inside flatMap to skip null values.
- **Null-safe:** No NPE risk — null becomes empty stream.

### References
- [Stream.ofNullable()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/stream/Stream.html#ofNullable(T))

---

## Stream takeWhile / dropWhile
- **Since:** Java 9
- **Old approach:** Manual Loop (Java 8)
- **Modern approach:** takeWhile/dropWhile (Java 9+)
- **Summary:** Take or drop elements from a stream based on a predicate.

### Before
```java
List<Integer> result = new ArrayList<>();
for (int n : sorted) {
    if (n >= 100) break;
    result.add(n);
}
// no stream equivalent in Java 8
```

### After
```java
var result = sorted.stream()
    .takeWhile(n -> n < 100)
    .toList();
// or: .dropWhile(n -> n < 10)
```

### Why modern wins
- **Short-circuit:** Stops processing as soon as the predicate fails.
- **Pipeline-friendly:** Chain with other stream operations naturally.
- **Declarative:** takeWhile reads like English: 'take while less than 100'.

### References
- [Stream.takeWhile()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/stream/Stream.html#takeWhile(java.util.function.Predicate))
- [Stream.dropWhile()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/stream/Stream.html#dropWhile(java.util.function.Predicate))

---

## Stream.toList()
- **Since:** Java 16
- **Old approach:** Collectors.toList() (Java 8)
- **Modern approach:** .toList() (Java 16+)
- **Summary:** Terminal toList() replaces the verbose collect(Collectors.toList()).

### Before
```java
List<String> result = stream
    .filter(s -> s.length() > 3)
    .collect(Collectors.toList());
```

### After
```java
List<String> result = stream
    .filter(s -> s.length() > 3)
    .toList();
```

### Why modern wins
- **7 chars vs 24:** .toList() replaces .collect(Collectors.toList()).
- **Immutable:** The result list cannot be modified.
- **Fluent:** Reads naturally at the end of a pipeline.

### References
- [Stream.toList()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/stream/Stream.html#toList())

---

## Virtual thread executor
- **Since:** Java 21
- **Old approach:** Fixed Thread Pool (Java 8)
- **Modern approach:** Virtual Thread Executor (Java 21+)
- **Summary:** Use virtual thread executors for unlimited lightweight concurrency.

### Before
```java
ExecutorService exec =
    Executors.newFixedThreadPool(10);
try {
    futures = tasks.stream()
        .map(t -> exec.submit(t))
        .toList();
} finally {
    exec.shutdown();
}
```

### After
```java
try (var exec = Executors
        .newVirtualThreadPerTaskExecutor()) {
    var futures = tasks.stream()
        .map(exec::submit)
        .toList();
}
```

### Why modern wins
- **No sizing:** No pool size to tune — create as many threads as needed.
- **Lightweight:** Virtual threads use KB of memory, not MB.
- **Auto-closeable:** try-with-resources handles shutdown automatically.

### References
- [Executors.newVirtualThreadPerTaskExecutor()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/Executors.html#newVirtualThreadPerTaskExecutor())
- [Virtual Threads (JEP 444)](https://openjdk.org/jeps/444)

---
