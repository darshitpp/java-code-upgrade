# Pattern Index

Quick lookup table for all Java modernization patterns.
**Total patterns: 135**


## Collections

| Slug | Title | JDK Version | Difficulty |
|------|-------|-------------|------------|
| collection-bulk-operations | Collection bulk operations instead of mutation loops | 8 | beginner |
| collectors-teeing | Collectors.teeing() | 12 | intermediate |
| comparator-factories | Comparator factories and fluent ordering | 8 | beginner |
| copying-collections-immutably | Copying collections immutably | 10 | beginner |
| immutable-list-creation | Immutable list creation | 9 | beginner |
| immutable-map-creation | Immutable map creation | 9 | beginner |
| immutable-set-creation | Immutable set creation | 9 | beginner |
| legacy-synchronized-collections | Legacy synchronized collections to modern alternatives | 5 | intermediate |
| map-compute-and-merge | Atomic map updates with compute and merge | 8 | intermediate |
| map-entry-factory | Map.entry() factory | 9 | beginner |
| reverse-list-iteration | Reverse list iteration | 21 | beginner |
| sequenced-collections | Sequenced collections | 21 | beginner |
| stack-to-deque | Stack to Deque and ArrayDeque | 6 | beginner |
| stream-toarray-typed | Typed stream toArray | 8 | beginner |
| unmodifiable-collectors | Unmodifiable collectors | 16 | intermediate |

## Concurrency

| Slug | Title | JDK Version | Difficulty |
|------|-------|-------------|------------|
| completablefuture-chaining | CompletableFuture chaining | 8 | intermediate |
| concurrent-http-virtual | Concurrent HTTP with virtual threads | 21 | intermediate |
| executor-try-with-resources | ExecutorService auto-close | 19 | beginner |
| lock-free-lazy-init | Lock-free lazy initialization | 25 | advanced |
| process-api | Modern Process API | 9 | intermediate |
| scoped-values | Scoped values | 25 | advanced |
| stable-values | Stable values | 25 | advanced |
| structured-concurrency | Structured concurrency | 25 | advanced |
| thread-sleep-duration | Thread.sleep with Duration | 19 | beginner |
| thread-stop-to-cooperative-cancellation | Unsafe thread termination to cooperative cancellation | 5 | advanced |
| timer-task-to-scheduled-executor | Timer tasks to scheduled executors | 5 | intermediate |
| virtual-threads | Virtual threads | 21 | beginner |
| wait-notify-to-blocking-queue | Wait and notify queues to BlockingQueue | 5 | intermediate |

## Datetime

| Slug | Title | JDK Version | Difficulty |
|------|-------|-------------|------------|
| date-formatting | Date formatting | 8 | beginner |
| duration-and-period | Duration and Period | 8 | beginner |
| hex-format | HexFormat | 17 | intermediate |
| instant-precision | Instant with nanosecond precision | 9 | intermediate |
| java-time-basics | java.time API basics | 8 | beginner |
| locale-of | Locale constructors to Locale.of() | 19 | beginner |
| math-clamp | Math.clamp() | 21 | beginner |

## Enterprise

| Slug | Title | JDK Version | Difficulty |
|------|-------|-------------|------------|
| ejb-timer-vs-jakarta-scheduler | EJB Timer vs Jakarta Scheduler | 11 | intermediate |
| ejb-vs-cdi | EJB versus CDI | 11 | intermediate |
| jdbc-resultset-vs-jpa-criteria | JDBC ResultSet Mapping vs JPA Criteria API | 11 | advanced |
| jdbc-vs-jooq | JDBC versus jOOQ | 11 | intermediate |
| jdbc-vs-jpa | JDBC versus JPA | 11 | intermediate |
| jndi-lookup-vs-cdi-injection | JNDI Lookup vs CDI Injection | 11 | intermediate |
| jpa-vs-jakarta-data | JPA versus Jakarta Data | 21 | intermediate |
| jsf-managed-bean-vs-cdi-named | JSF Managed Bean vs CDI Named Bean | 11 | intermediate |
| manual-transaction-vs-declarative | Manual JPA Transaction vs Declarative @Transactional | 11 | intermediate |
| mdb-vs-reactive-messaging | Message-Driven Bean vs Reactive Messaging | 11 | advanced |
| servlet-vs-jaxrs | Servlet versus JAX-RS | 11 | intermediate |
| singleton-ejb-vs-cdi-application-scoped | Singleton EJB vs CDI @ApplicationScoped | 11 | intermediate |
| soap-vs-jakarta-rest | SOAP Web Services vs Jakarta REST | 11 | intermediate |
| spring-api-versioning | Spring Framework 7 API Versioning | 17 | intermediate |
| spring-boot-mvc-config | Spring Boot MVC Configuration | 17 | beginner |
| spring-null-safety-jspecify | Spring Null Safety with JSpecify | 17 | intermediate |
| spring-xml-config-vs-annotations | Spring XML Bean Config vs Annotation-Driven | 17 | intermediate |

## Errors

| Slug | Title | JDK Version | Difficulty |
|------|-------|-------------|------------|
| helpful-npe | Helpful NullPointerExceptions | 14 | beginner |
| multi-catch | Multi-catch exception handling | 7 | beginner |
| null-in-switch | Null case in switch | 21 | beginner |
| optional-chaining | Optional chaining | 9 | beginner |
| optional-orelsethrow | Optional.orElseThrow() without supplier | 10 | beginner |
| record-based-errors | Record-based error responses | 16 | intermediate |
| require-nonnull-else | Objects.requireNonNullElse() | 9 | beginner |

## Io

| Slug | Title | JDK Version | Difficulty |
|------|-------|-------------|------------|
| deserialization-filters | Deserialization filters | 9 | advanced |
| explicit-charset-file-io | Default-charset file I/O to explicit StandardCharsets | 7 | beginner |
| file-memory-mapping | File memory mapping | 22 | advanced |
| files-mismatch | Files.mismatch() | 12 | beginner |
| finalizers-to-resource-cleanup | Finalizers to deterministic resource cleanup | 9 | advanced |
| http-client | Modern HTTP client | 11 | beginner |
| http-websocket-client | WebSocket clients with java.net.http | 11 | intermediate |
| inputstream-transferto | InputStream.transferTo() | 9 | beginner |
| io-class-console-io | IO class for console I/O | 25 | beginner |
| path-of | Path.of() factory | 11 | beginner |
| reading-files | Reading files | 11 | beginner |
| try-with-resources-effectively-final | Try-with-resources improvement | 9 | beginner |
| url-constructors-to-uri | Deprecated URL constructors to URI | 20 | intermediate |
| writing-files | Writing files | 11 | beginner |

## Language

| Slug | Title | JDK Version | Difficulty |
|------|-------|-------------|------------|
| anonymous-classes-to-lambdas | Anonymous classes to lambdas and method references | 8 | beginner |
| call-c-from-java | Calling out to C code from Java | 22 | advanced |
| compact-canonical-constructor | Compact canonical constructor | 16 | intermediate |
| compact-source-files | Compact source files | 25 | beginner |
| default-interface-methods | Default interface methods | 8 | intermediate |
| diamond-operator | Diamond with anonymous classes | 9 | beginner |
| exhaustive-switch | Exhaustive switch without default | 21 | intermediate |
| flexible-constructor-bodies | Flexible constructor bodies | 25 | intermediate |
| guarded-patterns | Guarded patterns with when | 21 | intermediate |
| markdown-javadoc-comments | Markdown in Javadoc comments | 23 | beginner |
| module-import-declarations | Module import declarations | 25 | intermediate |
| pattern-matching-instanceof | Pattern matching for instanceof | 16 | beginner |
| pattern-matching-switch | Pattern matching in switch | 21 | intermediate |
| primitive-types-in-patterns | Primitive types in patterns | 25 | advanced |
| private-interface-methods | Private interface methods | 9 | intermediate |
| raw-collections-to-generics | Raw collections to generic types | 5 | beginner |
| record-patterns | Record patterns (destructuring) | 21 | intermediate |
| records-for-data-classes | Records for data classes | 16 | beginner |
| sealed-classes | Sealed classes for type hierarchies | 17 | intermediate |
| static-members-in-inner-classes | Static members in inner classes | 16 | intermediate |
| static-methods-in-interfaces | Static methods in interfaces | 8 | beginner |
| switch-expressions | Switch expressions | 14 | beginner |
| text-blocks-for-multiline-strings | Text blocks for multiline strings | 15 | beginner |
| type-inference-with-var | Type inference with var | 10 | beginner |
| unnamed-variables | Unnamed variables with _ | 22 | beginner |

## Security

| Slug | Title | JDK Version | Difficulty |
|------|-------|-------------|------------|
| key-derivation-functions | Key Derivation Functions | 25 | advanced |
| pem-encoding | PEM encoding/decoding | 25 | advanced |
| random-generator | RandomGenerator interface | 17 | intermediate |
| security-manager-migration | SecurityManager checks to explicit authorization | 24 | advanced |
| standard-base64 | Standard Base64 encoding and decoding | 8 | beginner |
| strong-random | Strong random generation | 9 | beginner |
| tls-default | TLS 1.3 by default | 11 | intermediate |

## Streams

| Slug | Title | JDK Version | Difficulty |
|------|-------|-------------|------------|
| collectors-flatmapping | Collectors.flatMapping() | 9 | intermediate |
| optional-ifpresentorelse | Optional.ifPresentOrElse() | 9 | beginner |
| optional-or | Optional.or() fallback | 9 | intermediate |
| predicate-not | Predicate.not() for negation | 11 | beginner |
| stream-gatherers | Stream gatherers | 24 | advanced |
| stream-iterate-predicate | Stream.iterate() with predicate | 9 | intermediate |
| stream-mapmulti | Stream.mapMulti() | 16 | intermediate |
| stream-of-nullable | Stream.ofNullable() | 9 | beginner |
| stream-takewhile-dropwhile | Stream takeWhile / dropWhile | 9 | beginner |
| stream-tolist | Stream.toList() | 16 | beginner |
| virtual-thread-executor | Virtual thread executor | 21 | intermediate |

## Strings

| Slug | Title | JDK Version | Difficulty |
|------|-------|-------------|------------|
| string-chars-stream | String chars as stream | 9 | beginner |
| string-formatted | String.formatted() | 15 | beginner |
| string-indent-transform | String.indent() and transform() | 12 | beginner |
| string-isblank | String.isBlank() | 11 | beginner |
| string-lines | String.lines() for line splitting | 11 | beginner |
| string-repeat | String.repeat() | 11 | beginner |
| string-strip | String.strip() vs trim() | 11 | beginner |

## Tooling

| Slug | Title | JDK Version | Difficulty |
|------|-------|-------------|------------|
| aot-class-preloading | AOT class preloading | 25 | advanced |
| built-in-http-server | Built-in HTTP server | 18 | beginner |
| class-file-api | Class-file parsing with the standard API | 24 | advanced |
| class-newinstance-to-constructor | Class.newInstance() to constructor reflection | 9 | intermediate |
| compact-object-headers | Compact object headers | 25 | advanced |
| jfr-profiling | JFR for profiling | 9 | intermediate |
| jshell-prototyping | JShell for prototyping | 9 | beginner |
| junit6-with-jspecify | JUnit 6 with JSpecify null safety | 17 | intermediate |
| multi-file-source | Multi-file source launcher | 22 | intermediate |
| runtime-exec-to-process-builder | Runtime.exec(String) to ProcessBuilder arguments | 5 | intermediate |
| single-file-execution | Single-file execution | 11 | beginner |
| stack-walker | Lazy stack inspection with StackWalker | 9 | intermediate |
