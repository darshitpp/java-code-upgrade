# Language Patterns

## Calling out to C code from Java
- **Since:** Java 22
- **Old approach:** JNI (Java Native Interface) (Java 1.1+)
- **Modern approach:** FFM (Foreign Function & Memory API) (Java 22+)
- **Summary:** FFM lets Java call C libraries directly, without JNI boilerplate or C-side Java knowledge.

### Before
```java
public class CallCFromJava {
    static { System.loadLibrary("strlen-jni"); }
    public static native long strlen(String s);
    public static void main(String[] args) {
        long ret = strlen("Bambi");
        System.out.println("Return value " + ret); // 5
    }
}

// Run javac -h to generate the .h file, then write C:
// #include "CallCFromJava.h"
// #include <string.h>
// JNIEXPORT jlong JNICALL Java_CallCFromJava_strlen(
//     JNIEnv *env, jclass clazz, jstring str) {
//     const char* s = (*env)->GetStringUTFChars(env, str, NULL);
//     jlong len = (jlong) strlen(s);
//     (*env)->ReleaseStringUTFChars(env, str, s);
//     return len;
// }
```

### After
```java
void main() throws Throwable {
    try (var arena = Arena.ofConfined()) {
        // Use any system library directly — no C wrapper needed
        var stdlib = Linker.nativeLinker().defaultLookup();
        var foreignFuncAddr = stdlib.find("strlen").orElseThrow();
        var strlenSig = FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS);
        var strlenMethod = Linker.nativeLinker() .downcallHandle(foreignFuncAddr, strlenSig);
        var ret = (long) strlenMethod.invokeExact(arena.allocateFrom("Bambi"));
        System.out.println("Return value " + ret); // 5
    }
}

// Your own C library needs no special Java annotations:
// long greet(char* name) {
//     printf("Hello %s\n", name);
//     return 0;
// }
```

### Why modern wins
- **C code stays plain C:** The C function requires no JNI annotations or JNIEnv boilerplate — any existing C library can be called as-is.
- **More flexible:** Directly call most existing C/C++ libraries without writing adapter code or generating header files.
- **Easier workflow:** No need to stop, run javac -h, and implement the interface defined in the generated .h file.

### References
- [JEP 454: Foreign Function & Memory API](https://openjdk.org/jeps/454)
- [java.lang.foreign package (Java 22)](https://docs.oracle.com/en/java/javase/22/docs/api/java.base/java/lang/foreign/package-summary.html)

---

## Compact canonical constructor
- **Since:** Java 16
- **Old approach:** Explicit constructor validation (Java 16)
- **Modern approach:** Compact constructor (Java 16+)
- **Summary:** Validate and normalize record fields without repeating parameter lists.

### Before
```java
public record Person(String name,
                     List<String> pets) {
    // Full canonical constructor
    public Person(String name,
                  List<String> pets) {
        Objects.requireNonNull(name);
        this.name = name;
        this.pets = List.copyOf(pets);
    }
}
```

### After
```java
public record Person(String name,
                     List<String> pets) {
    // Compact constructor
    public Person {
        Objects.requireNonNull(name);
        pets = List.copyOf(pets);
    }
}
```

### Why modern wins
- **Less repetition:** No need to repeat parameter list or assign each field manually.
- **Validation:** Perfect for null checks, range validation, and defensive copies.
- **Clearer intent:** Compact syntax emphasizes validation, not boilerplate.

### References
- [Record (Java 21)](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Record.html)
- [JEP 395: Records](https://openjdk.org/jeps/395)

---

## Compact source files
- **Since:** Java 25
- **Old approach:** Main Class Ceremony (Java 8)
- **Modern approach:** void main() (Java 25)
- **Summary:** Write a complete program without class declaration or public static void\ main.

### Before
```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println(
            "Hello, World!");
    }
}
```

### After
```java
void main() {
    IO.println("Hello, World!");
}
```

### Why modern wins
- **Zero ceremony:** No class, no public static void main, no String[] args.
- **Beginner-friendly:** New programmers can write useful code from line 1.
- **Script-like:** Perfect for quick prototypes, scripts, and examples.

### References
- [Simple Source Files and Instance Main Methods (JEP 495)](https://openjdk.org/jeps/495)

---

## Default interface methods
- **Since:** Java 8
- **Old approach:** Abstract classes for shared behavior (Java 7)
- **Modern approach:** Default methods on interfaces (Java 8+)
- **Summary:** Add method implementations directly in interfaces, enabling multiple inheritance\ of behavior.

### Before
```java
// Need abstract class to share behavior
public abstract class AbstractLogger {
    public void log(String msg) {
        System.out.println(
            timestamp() + ": " + msg);
    }
    abstract String timestamp();
}

// Single inheritance only
public class FileLogger
    extends AbstractLogger { ... }
```

### After
```java
public interface Logger {
    default void log(String msg) {
        IO.println(
            timestamp() + ": " + msg);
    }
    String timestamp();
}

// Multiple interfaces allowed
public class FileLogger
    implements Logger, Closeable { ... }
```

### Why modern wins
- **Multiple inheritance:** Classes can implement many interfaces with default methods, unlike single\ abstract class inheritance."
- **API evolution:** Add new methods to interfaces without breaking existing implementations.
- **Composable behavior:** Mix and match capabilities from multiple interfaces freely.

### References
- [Evolving Interfaces (dev.java)](https://dev.java/learn/interfaces/examples/)

---

## Diamond with anonymous classes
- **Since:** Java 9
- **Old approach:** Repeat Type Args (Java 7/8)
- **Modern approach:** Diamond <> (Java 9+)
- **Summary:** Diamond operator now works with anonymous classes too.

### Before
```java
Map<String, List<String>> map =
    new HashMap<String, List<String>>();
// anonymous class: no diamond
Predicate<String> p =
    new Predicate<String>() {
        public boolean test(String s) {..}
    };
```

### After
```java
Map<String, List<String>> map =
    new HashMap<>();
// Java 9: diamond with anonymous classes
Predicate<String> p =
    new Predicate<>() {
        public boolean test(String s) {..}
    };
```

### Why modern wins
- **Consistent rules:** Diamond works everywhere — constructors and anonymous classes alike.
- **Less redundancy:** Type arguments are stated once on the left, never repeated.
- **DRY principle:** The compiler already knows the type — why write it twice?

### References
- [Diamond with Anonymous Classes (JEP 213)](https://openjdk.org/jeps/213)

---

## Exhaustive switch without default
- **Since:** Java 21
- **Old approach:** Mandatory default (Java 8)
- **Modern approach:** Sealed Exhaustiveness (Java 21+)
- **Summary:** Compiler verifies all sealed subtypes are covered — no default needed.

### Before
```java
// Must add default even though
// all cases are covered
double area(Shape s) {
    if (s instanceof Circle c)
        return Math.PI * c.r() * c.r();
    else if (s instanceof Rect r)
        return r.w() * r.h();
    else throw new IAE();
}
```

### After
```java
// sealed Shape permits Circle, Rect
double area(Shape s) {
    return switch (s) {
        case Circle c ->
            Math.PI * c.r() * c.r();
        case Rect r ->
            r.w() * r.h();
    }; // no default needed!
}
```

### Why modern wins
- **Compile-time safety:** Add a new subtype and the compiler shows every place to update.
- **No dead code:** No unreachable default branch that masks bugs.
- **Algebraic types:** Sealed + records + exhaustive switch = proper ADTs in Java.

### References
- [Pattern Matching for switch (JEP 441)](https://openjdk.org/jeps/441)
- [Sealed Classes (JEP 409)](https://openjdk.org/jeps/409)

---

## Flexible constructor bodies
- **Since:** Java 25
- **Old approach:** Validate After super() (Java 8)
- **Modern approach:** Code Before super() (Java 25+)
- **Summary:** Validate and compute values before calling super() or this().

### Before
```java
class Square extends Shape {
    Square(double side) {
        super(side, side);
        // can't validate BEFORE super!
        if (side <= 0)
            throw new IAE("bad");
    }
}
```

### After
```java
class Square extends Shape {
    Square(double side) {
        if (side <= 0)
            throw new IAE("bad");
        super(side, side);
    }
}
```

### Why modern wins
- **Fail fast:** Validate arguments before the superclass constructor runs.
- **Compute first:** Derive values and prepare data before calling super().
- **No workarounds:** No more static helper methods or factory patterns to work around the restriction.

### References
- [Flexible Constructor Bodies (JEP 492)](https://openjdk.org/jeps/492)

---

## Guarded patterns with when
- **Since:** Java 21
- **Old approach:** Nested if (Java 8)
- **Modern approach:** when Clause (Java 21+)
- **Summary:** Add conditions to pattern cases using when guards.

### Before
```java
if (shape instanceof Circle) {
    Circle c = (Circle) shape;
    if (c.radius() > 10) {
        return "large circle";
    } else {
        return "small circle";
    }
} else {
    return "not a circle";
}
```

### After
```java
return switch (shape) {
    case Circle c
        when c.radius() > 10
            -> "large circle";
    case Circle c
            -> "small circle";
    default -> "not a circle";
};
```

### Why modern wins
- **Precise matching:** Combine type + condition in a single case label.
- **Flat structure:** No nested if/else inside switch cases.
- **Readable intent:** The when clause reads like natural language.

### References
- [Pattern Matching for switch (JEP 441)](https://openjdk.org/jeps/441)

---

## Markdown in Javadoc comments
- **Since:** Java 23
- **Old approach:** HTML-based Javadoc (Java 8)
- **Modern approach:** Markdown Javadoc (Java 23+)
- **Summary:** Write Javadoc comments in Markdown instead of HTML for better readability.

### Before
```java
/**
 * Returns the {@code User} with
 * the given ID.
 *
 * <p>Example:
 * <pre>{@code
 * var user = findUser(123);
 * }</pre>
 *
 * @param id the user ID
 * @return the user
 */
public User findUser(int id) { ... }
```

### After
```java
/// Returns the `User` with
/// the given ID.
///
/// Example:
/// ```java
/// var user = findUser(123);
/// ```
///
/// @param id the user ID
/// @return the user
public User findUser(int id) { ... }
```

### Why modern wins
- **Natural syntax:** Use backticks for inline code and ``` for blocks instead of HTML tags.
- **Easier to write:** No need for {@code}, <pre>, <p> tags — just write Markdown.
- **Better in editors:** Markdown renders beautifully in modern IDEs and text editors.

### References
- [Markdown Documentation Comments (JEP 467)](https://openjdk.org/jeps/467)
- [JavaDoc Guide - Markdown](https://docs.oracle.com/en/java/javase/25/javadoc/using-markdown-documentation-comments.html)

---

## Module import declarations
- **Since:** Java 25
- **Old approach:** Many Imports (Java 8)
- **Modern approach:** import module (Java 25+)
- **Summary:** Import all exported packages of a module with a single declaration.

### Before
```java
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
```

### After
```java
import module java.base;

// All of java.util, java.io, java.nio
// etc. available in one line
```

### Why modern wins
- **One line:** Replace a wall of imports with a single module import.
- **Module-aware:** Leverages the module system to import coherent sets of packages.
- **Quick starts:** Perfect for scripts and prototypes where import lists are tedious.

### References
- [Module Import Declarations (JEP 494)](https://openjdk.org/jeps/494)

---

## Pattern matching for instanceof
- **Since:** Java 16
- **Old approach:** instanceof + Cast (Java 8)
- **Modern approach:** Pattern Variable (Java 16+)
- **Summary:** Combine type check and cast in one step with pattern matching.

### Before
```java
if (obj instanceof String) {
    String s = (String) obj;
    System.out.println(s.length());
}
```

### After
```java
if (obj instanceof String s) {
    IO.println(s.length());
}
```

### Why modern wins
- **No redundant cast:** Type check and variable binding happen in a single expression.
- **Fewer lines:** One line instead of two — the cast line disappears entirely.
- **Scope safety:** The pattern variable is only in scope where the type is guaranteed.

### References
- [Pattern Matching for instanceof (JEP 394)](https://openjdk.org/jeps/394)

---

## Pattern matching in switch
- **Since:** Java 21
- **Old approach:** if-else Chain (Java 8)
- **Modern approach:** Type Patterns (Java 21+)
- **Summary:** Replace if-else instanceof chains with clean switch type patterns.

### Before
```java
String format(Object obj) {
    if (obj instanceof Integer i)
        return "int: " + i;
    else if (obj instanceof Double d)
        return "double: " + d;
    else if (obj instanceof String s)
        return "str: " + s;
    return "unknown";
}
```

### After
```java
String format(Object obj) {
    return switch (obj) {
        case Integer i -> "int: " + i;
        case Double d  -> "double: " + d;
        case String s  -> "str: " + s;
        default        -> "unknown";
    };
}
```

### Why modern wins
- **Structured dispatch:** Switch makes the branching structure explicit and scannable.
- **Expression form:** Returns a value directly — no mutable variable needed.
- **Exhaustiveness:** The compiler ensures all types are handled.

### References
- [Pattern Matching for switch (JEP 441)](https://openjdk.org/jeps/441)

---

## Primitive types in patterns
- **Since:** Java 25
- **Old approach:** Manual Range Checks (Java 8)
- **Modern approach:** Primitive Patterns (Java 25 (Preview))
- **Summary:** Pattern matching now works with primitive types, not just objects.

### Before
```java
String classify(int code) {
    if (code >= 200 && code < 300)
        return "success";
    else if (code >= 400 && code < 500)
        return "client error";
    else
        return "other";
}
```

### After
```java
String classify(int code) {
    return switch (code) {
        case int c when c >= 200
            && c < 300 -> "success";
        case int c when c >= 400
            && c < 500 -> "client error";
        default -> "other";
    };
}
```

### Why modern wins
- **No boxing:** Match primitives directly — no Integer wrapper needed.
- **Pattern consistency:** Same pattern syntax for objects and primitives.
- **Better performance:** Avoid autoboxing overhead in pattern matching.

### References
- [Primitive Types in Patterns (JEP 488)](https://openjdk.org/jeps/488)

---

## Private interface methods
- **Since:** Java 9
- **Old approach:** Duplicated Logic (Java 8)
- **Modern approach:** Private Methods (Java 9+)
- **Summary:** Extract shared logic in interfaces using private methods.

### Before
```java
interface Logger {
    default void logInfo(String msg) {
        System.out.println(
            "[INFO] " + timestamp() + msg);
    }
    default void logWarn(String msg) {
        System.out.println(
            "[WARN] " + timestamp() + msg);
    }
}
```

### After
```java
interface Logger {
    private String format(String lvl, String msg) {
        return "[" + lvl + "] " + timestamp() + msg;
    }
    default void logInfo(String msg) {
        IO.println(format("INFO", msg));
    }
    default void logWarn(String msg) {
        IO.println(format("WARN", msg));
    }
}
```

### Why modern wins
- **Code reuse:** Share logic between default methods without duplication.
- **Encapsulation:** Implementation details stay hidden from implementing classes.
- **DRY interfaces:** No more copy-paste between default methods.

### References
- [Private Interface Methods](https://openjdk.org/jeps/213)

---

## Record patterns (destructuring)
- **Since:** Java 21
- **Old approach:** Manual Access (Java 8)
- **Modern approach:** Destructuring (Java 21+)
- **Summary:** Destructure records directly in patterns — extract fields in one step.

### Before
```java
if (obj instanceof Point) {
    Point p = (Point) obj;
    int x = p.getX();
    int y = p.getY();
    System.out.println(x + y);
}
```

### After
```java
if (obj instanceof Point(int x, int y)) {
    IO.println(x + y);
}
```

### Why modern wins
- **Direct extraction:** Access record components without calling accessors manually.
- **Nestable:** Patterns can nest — match inner records in a single expression.
- **Compact code:** Five lines become two — less ceremony, same clarity.

### References
- [Record Patterns (JEP 440)](https://openjdk.org/jeps/440)

---

## Records for data classes
- **Since:** Java 16
- **Old approach:** Verbose POJO (Java 8)
- **Modern approach:** record (Java 16+)
- **Summary:** One line replaces 30+ lines of boilerplate for immutable data carriers.

### Before
```java
public class Point {
    private final int x, y;
    public Point(int x, int y) { ... }
    public int getX() { return x; }
    public int getY() { return y; }
    // equals, hashCode, toString
}
```

### After
```java
public record Point(int x, int y) {}
```

### Why modern wins
- **One-line definition:** A single line replaces constructor, getters, equals, hashCode, toString.
- **Immutable by default:** All fields are final — no setter footguns.
- **Pattern-friendly:** Records work with destructuring patterns in switch and instanceof.

### References
- [Records (JEP 395)](https://openjdk.org/jeps/395)
- [Record class](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Record.html)

---

## Sealed classes for type hierarchies
- **Since:** Java 17
- **Old approach:** Open Hierarchy (Java 8)
- **Modern approach:** sealed permits (Java 17+)
- **Summary:** Restrict which classes can extend a type — enabling exhaustive switches.

### Before
```java
// Anyone can extend Shape
public abstract class Shape { }
public class Circle extends Shape { }
public class Rect extends Shape { }
// unknown subclasses possible
```

### After
```java
public sealed interface Shape
    permits Circle, Rect {}
public record Circle(double r)
    implements Shape {}
public record Rect(double w, double h)
    implements Shape {}
```

### Why modern wins
- **Controlled hierarchy:** Only permitted subtypes can extend — no surprise subclasses.
- **Exhaustive matching:** The compiler verifies switch covers all cases, no default needed.
- **Algebraic data types:** Model sum types naturally — sealed + records = ADTs in Java.

### References
- [Sealed Classes (JEP 409)](https://openjdk.org/jeps/409)

---

## Static members in inner classes
- **Since:** Java 16
- **Old approach:** Must use static nested class (Java 8)
- **Modern approach:** Static members in inner classes (Java 16+)
- **Summary:** Define static members in inner classes without requiring static nested classes.

### Before
```java
class Library {
    // Must be static nested class
    static class Book {
        static int globalBookCount;

        Book() {
            globalBookCount++;
        }
    }
}

// Usage
var book = new Library.Book();
```

### After
```java
class Library {
    // Can be inner class with statics
    class Book {
        static int globalBookCount;

        Book() {
            Book.globalBookCount++;
        }
    }
}

// Usage
var lib = new Library();
var book = lib.new Book();
```

### Why modern wins
- **More flexibility:** Inner classes can now have static members when needed.
- **Shared state:** Track shared state across instances of an inner class.
- **Design freedom:** No need to promote to static nested class just for one static field.

### References
- [JEP 395: Records](https://openjdk.org/jeps/395)
- [Inner Classes (JLS §8.1.3)](https://docs.oracle.com/javase/specs/jls/se25/html/jls-8.html#jls-8.1.3)

---

## Static methods in interfaces
- **Since:** Java 8
- **Old approach:** Utility classes (Java 7)
- **Modern approach:** Interface static methods (Java 8+)
- **Summary:** Add static utility methods directly to interfaces instead of separate utility\ classes.

### Before
```java
// Separate utility class needed
public class ValidatorUtils {
    public static boolean isBlank(
        String s) {
        return s == null ||
               s.trim().isEmpty();
    }
}

// Usage
if (ValidatorUtils.isBlank(input)) { ... }
```

### After
```java
public interface Validator {
    boolean validate(String s);

    static boolean isBlank(String s) {
        return s == null ||
               s.trim().isEmpty();
    }
}

// Usage
if (Validator.isBlank(input)) { ... }
```

### Why modern wins
- **Better organization:** Keep related utilities with the interface, not in a separate class.
- **Discoverability:** Factory and helper methods are found where you'd expect them.
- **API cohesion:** No need for separate *Utils or *Helper classes.

### References
- [Evolving Interfaces (dev.java)](https://dev.java/learn/interfaces/examples/)

---

## Switch expressions
- **Since:** Java 14
- **Old approach:** Switch Statement (Java 8)
- **Modern approach:** Switch Expression (Java 14+)
- **Summary:** Switch as an expression that returns a value — no break, no fall-through.

### Before
```java
String msg;
switch (day) {
    case MONDAY:
        msg = "Start";
        break;
    case FRIDAY:
        msg = "End";
        break;
    default:
        msg = "Mid";
}
```

### After
```java
String msg = switch (day) {
    case MONDAY  -> "Start";
    case FRIDAY  -> "End";
    default      -> "Mid";
};
```

### Why modern wins
- **Returns a value:** Assign the switch result directly — no temporary variable needed.
- **No fall-through:** Arrow syntax eliminates accidental fall-through bugs from missing break.
- **Exhaustiveness check:** The compiler ensures all cases are covered.

### References
- [Switch Expressions (JEP 361)](https://openjdk.org/jeps/361)

---

## Text blocks for multiline strings
- **Since:** Java 15
- **Old approach:** String Concatenation (Java 8)
- **Modern approach:** Text Blocks (Java 15+)
- **Summary:** Write multiline strings naturally with triple-quote text blocks.

### Before
```java
String json = "{\n" +
    "  \"name\": \"Duke\",\n" +
    "  \"age\": 30\n" +
    "}";
```

### After
```java
String json = """
    {
      "name": "Duke",
      "age": 30
    }""";
```

### Why modern wins
- **Readable as-is:** JSON, SQL, and HTML look like real JSON, SQL, and HTML in your source.
- **No escape hell:** Embedded quotes don't need backslash escaping.
- **Smart indentation:** Leading whitespace is trimmed automatically based on the closing delimiter\ position."

### References
- [Text Blocks (JEP 378)](https://openjdk.org/jeps/378)
- [Text Blocks Guide](https://docs.oracle.com/en/java/javase/25/language/text-blocks.html)

---

## Type inference with var
- **Since:** Java 10
- **Old approach:** Explicit Types (Java 8)
- **Modern approach:** var keyword (Java 10+)
- **Summary:** Use var for local variable type inference — less noise, same safety.

### Before
```java
Map<String, List<Integer>> map =
    new HashMap<String, List<Integer>>();
for (Map.Entry<String, List<Integer>> e
    : map.entrySet()) {
    // verbose type noise
}
```

### After
```java
var map = new HashMap<String, List<Integer>>();
for (var entry : map.entrySet()) {
    // clean and readable
}
```

### Why modern wins
- **Less boilerplate:** No need to repeat complex generic types on both sides of the assignment.
- **Better readability:** Focus on variable names and values, not type declarations.
- **Still type-safe:** The compiler infers and enforces the exact type at compile time.

### References
- [Local Variable Type Inference (JEP 286)](https://openjdk.org/jeps/286)
- [Style Guidelines for var](https://openjdk.org/projects/amber/guides/lvti-style-guide)

---

## Unnamed variables with _
- **Since:** Java 22
- **Old approach:** Unused Variable (Java 8)
- **Modern approach:** _ Placeholder (Java 22+)
- **Summary:** Use _ to signal intent when a variable is intentionally unused.

### Before
```java
try {
    parse(input);
} catch (Exception ignored) {
    log("parse failed");
}
map.forEach((key, value) -> {
    process(value); // key unused
});
```

### After
```java
try {
    parse(input);
} catch (Exception _) {
    log("parse failed");
}
map.forEach((_, value) -> {
    process(value);
});
```

### Why modern wins
- **Clear intent:** _ explicitly says 'this value is not needed here'.
- **No warnings:** IDEs and linters won't flag intentionally unused variables.
- **Cleaner lambdas:** Multi-param lambdas are cleaner when you only need some params.

### References
- [Unnamed Variables & Patterns (JEP 456)](https://openjdk.org/jeps/456)

---
