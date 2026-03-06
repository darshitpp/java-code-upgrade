# Datetime Patterns

## Date formatting
- **Since:** Java 8
- **Old approach:** SimpleDateFormat (Pre-Java 8)
- **Modern approach:** DateTimeFormatter (Java 8+)
- **Summary:** Format dates with thread-safe, immutable DateTimeFormatter.

### Before
```java
// Not thread-safe!
SimpleDateFormat sdf =
    new SimpleDateFormat("yyyy-MM-dd");
String formatted = sdf.format(date);
// Must synchronize for concurrent use
```

### After
```java
DateTimeFormatter fmt =
    DateTimeFormatter.ofPattern(
        "uuuu-MM-dd");
String formatted =
    LocalDate.now().format(fmt);
// Thread-safe, immutable
```

### Why modern wins
- **Thread-safe:** Share formatters across threads without synchronization.
- **Built-in formats:** ISO_LOCAL_DATE, ISO_INSTANT, etc. for standard formats.
- **Immutable:** Store as static final constants safely.

### References
- [DateTimeFormatter](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/time/format/DateTimeFormatter.html)

---

## Duration and Period
- **Since:** Java 8
- **Old approach:** Millisecond Math (Pre-Java 8)
- **Modern approach:** Duration / Period (Java 8+)
- **Summary:** Calculate time differences with type-safe Duration and Period.

### Before
```java
// How many days between two dates?
long diff = date2.getTime()
    - date1.getTime();
long days = diff
    / (1000 * 60 * 60 * 24);
// ignores DST, leap seconds
```

### After
```java
long days = ChronoUnit.DAYS
    .between(date1, date2);
Period period = Period.between(
    date1, date2);
Duration elapsed = Duration.between(
    time1, time2);
```

### Why modern wins
- **Type-safe:** Duration for time, Period for dates — no confusion.
- **Correct math:** Handles DST transitions, leap years, and leap seconds.
- **Readable:** ChronoUnit.DAYS.between() reads like English.

### References
- [Duration](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/time/Duration.html)
- [Period](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/time/Period.html)

---

## HexFormat
- **Since:** Java 17
- **Old approach:** Manual Hex Conversion (Java 8)
- **Modern approach:** HexFormat (Java 17+)
- **Summary:** Convert between hex strings and byte arrays with HexFormat.

### Before
```java
// Pad to 2 digits, uppercase
String hex = String.format(
    "%02X", byteValue);
// Parse hex string
int val = Integer.parseInt(
    "FF", 16);
```

### After
```java
var hex = HexFormat.of()
    .withUpperCase();
String s = hex.toHexDigits(
    byteValue);
byte[] bytes =
    hex.parseHex("48656C6C6F");
```

### Why modern wins
- **Bidirectional:** Convert bytes→hex and hex→bytes with one API.
- **Configurable:** Delimiters, prefix, suffix, upper/lower case.
- **Array support:** Encode/decode entire byte arrays at once.

### References
- [HexFormat](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/HexFormat.html)

---

## Instant with nanosecond precision
- **Since:** Java 9
- **Old approach:** Milliseconds (Java 8)
- **Modern approach:** Nanoseconds (Java 9+)
- **Summary:** Get timestamps with microsecond or nanosecond precision.

### Before
```java
// Millisecond precision only
long millis =
    System.currentTimeMillis();
// 1708012345678
```

### After
```java
// Microsecond/nanosecond precision
Instant now = Instant.now();
// 2025-02-15T20:12:25.678901234Z
long nanos = now.getNano();
```

### Why modern wins
- **Higher precision:** Microsecond/nanosecond vs millisecond timestamps.
- **Type-safe:** Instant carries its precision — no ambiguous longs.
- **UTC-based:** Instant is always in UTC — no timezone confusion.

### References
- [Instant](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/time/Instant.html)
- [Clock](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/time/Clock.html)

---

## java.time API basics
- **Since:** Java 8
- **Old approach:** Date + Calendar (Pre-Java 8)
- **Modern approach:** java.time.* (Java 8+)
- **Summary:** Use immutable, clear date/time types instead of Date and Calendar.

### Before
```java
// Mutable, confusing, zero-indexed months
Calendar cal = Calendar.getInstance();
cal.set(2025, 0, 15); // January = 0!
Date date = cal.getTime();
// not thread-safe
```

### After
```java
LocalDate date = LocalDate.of(
    2025, Month.JANUARY, 15);
LocalTime time = LocalTime.of(14, 30);
Instant now = Instant.now();
// immutable, thread-safe
```

### Why modern wins
- **Immutable:** Date/time values can't be accidentally modified.
- **Clear API:** Month.JANUARY, not 0. DayOfWeek.MONDAY, not 2.
- **Thread-safe:** No synchronization needed — share freely across threads.

### References
- [LocalDate](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/time/LocalDate.html)
- [LocalTime](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/time/LocalTime.html)
- [LocalDateTime](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/time/LocalDateTime.html)

---

## Math.clamp()
- **Since:** Java 21
- **Old approach:** Nested min/max (Java 8)
- **Modern approach:** Math.clamp() (Java 21+)
- **Summary:** Clamp a value between bounds with a single clear call.

### Before
```java
// Clamp value between min and max
int clamped =
    Math.min(Math.max(value, 0), 100);
// or: min and max order confusion
```

### After
```java
int clamped =
    Math.clamp(value, 0, 100);
// value constrained to [0, 100]
```

### Why modern wins
- **Self-documenting:** clamp(value, min, max) is unambiguous.
- **Less error-prone:** No more swapping min/max order by accident.
- **All numeric types:** Works with int, long, float, and double.

### References
- [Math.clamp()](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Math.html#clamp(long,int,int))

---
