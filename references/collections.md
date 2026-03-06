# Collections Patterns

## Collectors.teeing()
- **Since:** Java 12
- **Old approach:** Two Passes (Java 8)
- **Modern approach:** teeing() (Java 12+)
- **Summary:** Compute two aggregations in a single stream pass.

### Before
```java
long count = items.stream().count();
double sum = items.stream()
    .mapToDouble(Item::price)
    .sum();
var result = new Stats(count, sum);
```

### After
```java
var result = items.stream().collect(
    Collectors.teeing(
        Collectors.counting(),
        Collectors.summingDouble(Item::price),
        Stats::new
    )
);
```

### Why modern wins
- **Single pass:** Process the stream once instead of twice.
- **Composable:** Combine any two collectors with a merger function.
- **Immutable result:** Merge into a record or value object directly.

### References
- [Collectors.teeing()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/stream/Collectors.html#teeing(java.util.stream.Collector,java.util.stream.Collector,java.util.function.BiFunction))

---

## Copying collections immutably
- **Since:** Java 10
- **Old approach:** Manual Copy + Wrap (Java 8)
- **Modern approach:** List.copyOf() (Java 10+)
- **Summary:** Create an immutable copy of any collection in one call.

### Before
```java
List<String> copy =
    Collections.unmodifiableList(
        new ArrayList<>(original)
    );
```

### After
```java
List<String> copy =
    List.copyOf(original);
```

### Why modern wins
- **Smart copy:** Skips the copy if the source is already immutable.
- **One call:** No manual ArrayList construction + wrapping.
- **Defensive copy:** Changes to the original don't affect the copy.

### References
- [List.copyOf()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/List.html#copyOf(java.util.Collection))

---

## Immutable list creation
- **Since:** Java 9
- **Old approach:** Verbose Wrapping (Java 8)
- **Modern approach:** List.of() (Java 9+)
- **Summary:** Create immutable lists in one clean expression.

### Before
```java
List<String> list =
    Collections.unmodifiableList(
        new ArrayList<>(
            Arrays.asList("a", "b", "c")
        )
    );
```

### After
```java
List<String> list =
    List.of("a", "b", "c");
```

### Why modern wins
- **One call:** Replace three nested calls with a single factory method.
- **Truly immutable:** Not just a wrapper — the list itself is immutable.
- **Null-safe:** Rejects null elements at creation time, failing fast.

### References
- [List.of()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/List.html#of())
- [Collections Factory Methods (JEP 269)](https://openjdk.org/jeps/269)

---

## Immutable map creation
- **Since:** Java 9
- **Old approach:** Map Builder Pattern (Java 8)
- **Modern approach:** Map.of() (Java 9+)
- **Summary:** Create immutable maps inline without a builder.

### Before
```java
Map<String, Integer> map = new HashMap<>();
map.put("a", 1);
map.put("b", 2);
map.put("c", 3);
map = Collections.unmodifiableMap(map);
```

### After
```java
Map<String, Integer> map =
    Map.of("a", 1, "b", 2, "c", 3);
```

### Why modern wins
- **Inline creation:** No temporary mutable map needed.
- **Immutable result:** The map cannot be modified after creation.
- **No null keys/values:** Null entries are rejected immediately.

### References
- [Map.of()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Map.html#of())
- [Map.ofEntries()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Map.html#ofEntries(java.util.Map.Entry...))

---

## Immutable set creation
- **Since:** Java 9
- **Old approach:** Verbose Wrapping (Java 8)
- **Modern approach:** Set.of() (Java 9+)
- **Summary:** Create immutable sets with a single factory call.

### Before
```java
Set<String> set =
    Collections.unmodifiableSet(
        new HashSet<>(
            Arrays.asList("a", "b", "c")
        )
    );
```

### After
```java
Set<String> set =
    Set.of("a", "b", "c");
```

### Why modern wins
- **Concise:** One line instead of three nested calls.
- **Detects duplicates:** Throws if you accidentally pass duplicate elements.
- **Immutable:** No add/remove possible after creation.

### References
- [Set.of()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Set.html#of())
- [Collections Factory Methods (JEP 269)](https://openjdk.org/jeps/269)

---

## Map.entry() factory
- **Since:** Java 9
- **Old approach:** SimpleEntry (Java 8)
- **Modern approach:** Map.entry() (Java 9+)
- **Summary:** Create map entries with a clean factory method.

### Before
```java
Map.Entry<String, Integer> e =
    new AbstractMap.SimpleEntry<>(
        "key", 42
    );
```

### After
```java
var e = Map.entry(\"key\", 42);
```

### Why modern wins
- **Concise:** One line instead of three with a clearer intent.
- **Immutable:** The returned entry cannot be modified.
- **Composable:** Works perfectly with Map.ofEntries() for large maps.

### References
- [Map.entry()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Map.html#entry(K,V))

---

## Reverse list iteration
- **Since:** Java 21
- **Old approach:** Manual ListIterator (Java 8)
- **Modern approach:** reversed() (Java 21+)
- **Summary:** Iterate over a list in reverse order with a clean for-each loop.

### Before
```java
for (ListIterator<String> it =
        list.listIterator(list.size());
    it.hasPrevious(); ) {
    String element = it.previous();
    System.out.println(element);
}
```

### After
```java
for (String element : list.reversed()) {
    IO.println(element);
}
```

### Why modern wins
- **Natural syntax:** Enhanced for loop instead of verbose ListIterator.
- **No copying:** reversed() returns a view — no performance overhead.
- **Consistent API:** Works on List, Deque, SortedSet uniformly.

### References
- [SequencedCollection (Java 21)](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/SequencedCollection.html)
- [JEP 431: Sequenced Collections](https://openjdk.org/jeps/431)

---

## Sequenced collections
- **Since:** Java 21
- **Old approach:** Index Arithmetic (Java 8)
- **Modern approach:** getFirst/getLast (Java 21+)
- **Summary:** Access first/last elements and reverse views with clean API methods.

### Before
```java
// Get last element
var last = list.get(list.size() - 1);
// Get first
var first = list.get(0);
// Reverse iteration: manual
```

### After
```java
var last = list.getLast();
var first = list.getFirst();
var reversed = list.reversed();
```

### Why modern wins
- **Self-documenting:** getLast() is clearer than get(size()-1).
- **Reversed view:** reversed() gives a view — no copying needed.
- **Uniform API:** Works the same on List, Deque, SortedSet.

### References
- [Sequenced Collections (JEP 431)](https://openjdk.org/jeps/431)
- [SequencedCollection](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/SequencedCollection.html)

---

## Typed stream toArray
- **Since:** Java 8
- **Old approach:** Manual Array Copy (Pre-Streams)
- **Modern approach:** toArray(generator) (Java 8+)
- **Summary:** Convert streams to typed arrays with a method reference.

### Before
```java
List<String> list = getNames();
String[] arr = new String[list.size()];
for (int i = 0; i < list.size(); i++) {
    arr[i] = list.get(i);
}
```

### After
```java
String[] arr = getNames().stream()
    .filter(n -> n.length() > 3)
    .toArray(String[]::new);
```

### Why modern wins
- **Type-safe:** No Object[] cast — the array type is correct.
- **Chainable:** Works at the end of any stream pipeline.
- **Concise:** One expression replaces the manual loop.

### References
- [Stream.toArray()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/stream/Stream.html#toArray(java.util.function.IntFunction))

---

## Unmodifiable collectors
- **Since:** Java 16
- **Old approach:** collectingAndThen (Java 8)
- **Modern approach:** stream.toList() (Java 16+)
- **Summary:** Collect directly to an unmodifiable list with stream.toList().

### Before
```java
List<String> list = stream.collect(
    Collectors.collectingAndThen(
        Collectors.toList(),
        Collections::unmodifiableList
    )
);
```

### After
```java
List<String> list = stream.toList();
```

### Why modern wins
- **Shortest yet:** stream.toList() needs no collect() or Collectors import at all.
- **Immutable:** Result cannot be modified — no accidental mutations.
- **Readable:** Reads naturally as the terminal step of any stream pipeline.

### References
- [Stream.toList()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/stream/Stream.html#toList())
- [Collectors.toUnmodifiableList()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/stream/Collectors.html#toUnmodifiableList())

---
