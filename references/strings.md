# Strings Patterns

## String chars as stream
- **Since:** Java 9
- **Old approach:** Manual Loop (Java 8)
- **Modern approach:** chars() Stream (Java 9+)
- **Summary:** Process string characters as a stream pipeline.

### Before
```java
for (int i = 0; i < str.length(); i++) {
    char c = str.charAt(i);
    if (Character.isDigit(c)) {
        process(c);
    }
}
```

### After
```java
str.chars()
    .filter(Character::isDigit)
    .forEach(c -> process((char) c));
```

### Why modern wins
- **Chainable:** Use filter, map, collect on character streams.
- **Declarative:** Describe what to do, not how to loop.
- **Unicode-ready:** codePoints() correctly handles emoji and supplementary chars.

### References
- [String.chars()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/String.html#chars())
- [CharSequence.codePoints()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/CharSequence.html#codePoints())

---

## String.formatted()
- **Since:** Java 15
- **Old approach:** String.format() (Java 8)
- **Modern approach:** formatted() (Java 15+)
- **Summary:** Call formatted() on the template string itself.

### Before
```java
String msg = String.format(
    "Hello %s, you are %d",
    name, age
);
```

### After
```java
String msg =
    "Hello %s, you are %d"
    .formatted(name, age);
```

### Why modern wins
- **Reads naturally:** Template.formatted(args) flows better than String.format(template, args).
- **Chainable:** Can be chained with other string methods.
- **Less verbose:** Drops the redundant String.format() static call.

### References
- [String.formatted()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/String.html#formatted(java.lang.Object...))

---

## String.indent() and transform()
- **Since:** Java 12
- **Old approach:** Manual Indentation (Java 8)
- **Modern approach:** indent() / transform() (Java 12+)
- **Summary:** Indent text and chain string transformations fluently.

### Before
```java
String[] lines = text.split("\n");
StringBuilder sb = new StringBuilder();
for (String line : lines) {
    sb.append("    ").append(line)
      .append("\n");
}
String indented = sb.toString();
```

### After
```java
String indented = text.indent(4);

String result = text
    .transform(String::strip)
    .transform(s -> s.replace(" ", "-"));
```

### Why modern wins
- **Built-in:** Indentation is a common operation — now it's one call.
- **Chainable:** transform() enables fluent pipelines on strings.
- **Clean code:** No manual line splitting and StringBuilder loops.

### References
- [String.indent()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/String.html#indent(int))
- [String.transform()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/String.html#transform(java.util.function.Function))

---

## String.isBlank()
- **Since:** Java 11
- **Old approach:** trim().isEmpty() (Java 8)
- **Modern approach:** isBlank() (Java 11+)
- **Summary:** Check for blank strings with a single method call.

### Before
```java
boolean blank =
    str.trim().isEmpty();
// or: str.trim().length() == 0
```

### After
```java
boolean blank = str.isBlank();
// handles Unicode whitespace too
```

### Why modern wins
- **Self-documenting:** isBlank() says exactly what it checks.
- **Unicode-aware:** Handles all Unicode whitespace, not just ASCII.
- **No allocation:** No intermediate trimmed string is created.

### References
- [String.isBlank()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/String.html#isBlank())

---

## String.lines() for line splitting
- **Since:** Java 11
- **Old approach:** split(\"\\\\n\") (Java 8)
- **Modern approach:** lines() (Java 11+)
- **Summary:** Use String.lines() to split text into a stream of lines without regex overhead.

### Before
```java
String text = "one\ntwo\nthree";
String[] lines = text.split("\n");
for (String line : lines) {
    System.out.println(line);
}
```

### After
```java
String text = "one\ntwo\nthree";
text.lines().forEach(IO::println);
```

### Why modern wins
- **Lazy streaming:** Lines are produced on demand, not all at once like split().
- **Universal line endings:** Handles \\n, \\r, and \\r\\n automatically without regex.
- **Stream integration:** Returns a Stream for direct use with filter, map, collect.

### References
- [String.lines()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/String.html#lines())

---

## String.repeat()
- **Since:** Java 11
- **Old approach:** StringBuilder Loop (Java 8)
- **Modern approach:** repeat() (Java 11+)
- **Summary:** Repeat a string n times without a loop.

### Before
```java
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 3; i++) {
    sb.append("abc");
}
String result = sb.toString();
```

### After
```java
String result = "abc".repeat(3);
// "abcabcabc"
```

### Why modern wins
- **One-liner:** Replace 5 lines of StringBuilder code with one call.
- **Optimized:** Internal implementation is optimized for large repeats.
- **Clear intent:** repeat(3) immediately conveys the purpose.

### References
- [String.repeat()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/String.html#repeat(int))

---

## String.strip() vs trim()
- **Since:** Java 11
- **Old approach:** trim() (Java 8)
- **Modern approach:** strip() (Java 11+)
- **Summary:** Use Unicode-aware stripping with strip(), stripLeading(), stripTrailing().

### Before
```java
// trim() only removes ASCII whitespace
// (chars <= U+0020)
String clean = str.trim();
```

### After
```java
// strip() removes all Unicode whitespace
String clean = str.strip();
String left  = str.stripLeading();
String right = str.stripTrailing();
```

### Why modern wins
- **Unicode-correct:** Handles all whitespace characters from every script.
- **Directional:** stripLeading() and stripTrailing() for one-sided trimming.
- **Fewer bugs:** No surprise whitespace left behind in international text.

### References
- [String.strip()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/String.html#strip())

---
