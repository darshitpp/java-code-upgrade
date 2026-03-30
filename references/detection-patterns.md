# Detection Patterns Reference

Maps old Java code signatures to modernization patterns.
Use this to identify which patterns apply when scanning source code.

_Auto-generated from upstream YAML data. Do not edit manually._

## Collections

- **collectors-teeing** (Java 12+): Old=`Two Passes` | Detect: `new Stats(`, `.stream().count()`, `items.stream()`
- **copying-collections-immutably** (Java 10+): Old=`Manual Copy + Wrap` | Detect: `Collections.unmodifiableList(`, `new ArrayList(`
- **immutable-list-creation** (Java 9+): Old=`Verbose Wrapping` | Detect: `Collections.unmodifiableList(`, `Arrays.asList(`, `new ArrayList(`
- **immutable-map-creation** (Java 9+): Old=`Map Builder Pattern` | Detect: `Collections.unmodifiableMap(`, `new HashMap(`
- **immutable-set-creation** (Java 9+): Old=`Verbose Wrapping` | Detect: `Collections.unmodifiableSet(`, `Arrays.asList(`, `new HashSet(`
- **map-entry-factory** (Java 9+): Old=`SimpleEntry` | Detect: `SimpleEntry`
- **reverse-list-iteration** (Java 21+): Old=`Manual ListIterator` | Detect: `System.out.println(`, `list.listIterator(list.size())`, `it.hasPrevious()`, `it.previous()`, `out.println(element)`
- **sequenced-collections** (Java 21+): Old=`Index Arithmetic` | Detect: `list.get(list.size() - 1)`, `list.get(0)`
- **stream-toarray-typed** (Java 8+): Old=`Manual Filter + Copy` | Detect: `new ArrayList(`, `n.length()`, `filtered.add(n)`
- **unmodifiable-collectors** (Java 16+): Old=`collectingAndThen` | Detect: `Collectors.collectingAndThen(`, `Collectors.toList(`

## Concurrency

- **completablefuture-chaining** (Java 8+): Old=`Blocking Future.get()` | Detect: `future.get()`
- **concurrent-http-virtual** (Java 21+): Old=`Thread Pool + URLConnection` | Detect: `Executors.newFixedThreadPool(`, `urls.stream()`
- **executor-try-with-resources** (Java 19+): Old=`Manual Shutdown` | Detect: `Executors.newCachedThreadPool(`, `exec.submit(task)`, `exec.shutdown()`
- **lock-free-lazy-init** (Java 25+): Old=`synchronized + volatile` | Detect: `synchronized + volatile`
- **process-api** (Java 9+): Old=`Runtime.exec()` | Detect: `Runtime.getRuntime(`, `p.waitFor()`
- **scoped-values** (Java 25+): Old=`ThreadLocal` | Detect: `CURRENT.set(`, `CURRENT.remove(`, `new ThreadLocal(`
- **stable-values** (Java 25+): Old=`Double-Checked Locking` | Detect: `Double-Checked Locking`
- **structured-concurrency** (Java 25+): Old=`Manual Thread Lifecycle` | Detect: `Executors.newFixedThreadPool(`, `exec.shutdown()`
- **thread-sleep-duration** (Java 19+): Old=`Milliseconds` | Detect: `Thread.sleep(`
- **virtual-threads** (Java 21+): Old=`Platform Threads` | Detect: `System.out.println(`, `new Thread(`, `thread.start()`, `thread.join()`

## Datetime

- **date-formatting** (Java 8+): Old=`SimpleDateFormat` | Detect: `new SimpleDateFormat(`, `sdf.format(date)`
- **duration-and-period** (Java 8+): Old=`Millisecond Math` | Detect: `date2.getTime()`, `date1.getTime()`
- **hex-format** (Java 17+): Old=`Manual Hex Conversion` | Detect: `String.format(`, `Integer.parseInt(`
- **instant-precision** (Java 9+): Old=`Milliseconds` | Detect: `System.currentTimeMillis(`
- **java-time-basics** (Java 8+): Old=`Date + Calendar` | Detect: `Calendar.getInstance(`, `cal.getTime()`
- **math-clamp** (Java 21+): Old=`Nested min/max` | Detect: `Nested min/max`

## Enterprise

- **ejb-timer-vs-jakarta-scheduler** (Java 11+): Old=`EJB TimerService` | Detect: `Service.createCalendarTimer(`, `new ScheduleExpression(`, `@Stateless`, `@Resource`, `@PostConstruct`, `@Timeout`
- **ejb-vs-cdi** (Java 11+): Old=`EJB` | Detect: `@Stateless`, `@EJB`, `inventory.reserve(order.getItem())`
- **jdbc-resultset-vs-jpa-criteria** (Java 11+): Old=`JDBC ResultSet` | Detect: `new ArrayList(`, `new User(`, `ds.getConnection()`, `con.prepareStatement(sql))`, `ps.executeQuery()`, `rs.next())`
- **jdbc-vs-jooq** (Java 11+): Old=`Raw JDBC` | Detect: `new ArrayList(`, `new User(`, `ds.getConnection()`, `con.prepareStatement(sql))`, `ps.executeQuery()`, `rs.next())`
- **jdbc-vs-jpa** (Java 11+): Old=`JDBC` | Detect: `Source.getConnection(`, `new User(`, `dataSource.getConnection()`, `con.prepareStatement(sql))`, `ps.executeQuery()`, `rs.next())`
- **jndi-lookup-vs-cdi-injection** (Java 11+): Old=`JNDI Lookup` | Detect: `new InitialContext(`, `java:comp/env/jdbc/OrderDB`, `ds.getConnection())`
- **jpa-vs-jakarta-data** (Java 21+): Old=`JPA EntityManager` | Detect: `@PersistenceContext`, `em.persist(user)`
- **jsf-managed-bean-vs-cdi-named** (Java 11+): Old=`@ManagedBean` | Detect: `@ManagedBean`, `@SessionScoped`, `@ManagedProperty`, `implements Serializable`
- **manual-transaction-vs-declarative** (Java 11+): Old=`Manual Transaction` | Detect: `@PersistenceContext`, `em.getTransaction()`, `tx.begin()`, `src.debit(amount)`, `dst.credit(amount)`, `tx.commit()`
- **mdb-vs-reactive-messaging** (Java 11+): Old=`Message-Driven Bean` | Detect: `@MessageDriven`, `@ActivationConfigProperty`, `@Override`, `implements MessageListener`, `txt.getText())`
- **servlet-vs-jaxrs** (Java 11+): Old=`HttpServlet` | Detect: `@WebServlet`, `@Override`, `extends HttpServlet`, `res.getWriter()`
- **singleton-ejb-vs-cdi-application-scoped** (Java 11+): Old=`@Singleton EJB` | Detect: `@Singleton`, `@Startup`, `@ConcurrencyManagement`, `@PostConstruct`, `@Lock`, `cache.get(key)`
- **soap-vs-jakarta-rest** (Java 11+): Old=`JAX-WS / SOAP` | Detect: `new UserResponse(`, `@WebService`, `@WebMethod`, `@WebParam`, `res.setId(user.getId())`, `res.setName(user.getName())`
- **spring-api-versioning** (Java 17+): Old=`Manual URL Path Versioning` | Detect: `@RestController`, `@RequestMapping`, `@GetMapping`, `@PathVariable`, `service.getV1(id)`, `service.getV2(id)`
- **spring-null-safety-jspecify** (Java 17+): Old=`Spring @NonNull/@Nullable` | Detect: `@Nullable`, `@NonNull`, `repository.findById(id)`, `repository.findAll()`, `repository.save(user)`
- **spring-xml-config-vs-annotations** (Java 17+): Old=`XML Bean Definitions` | Detect: `XML Bean Definitions`

## Errors

- **helpful-npe** (Java 14+): Old=`Cryptic NPE` | Detect: `MyApp.main(`
- **multi-catch** (Java 7+): Old=`Separate Catch Blocks` | Detect: `Separate Catch Blocks`
- **null-in-switch** (Java 21+): Old=`Guard Before Switch` | Detect: `Guard Before Switch`
- **optional-chaining** (Java 9+): Old=`Nested Null Checks` | Detect: `user.getAddress()`, `addr.getCity()`
- **optional-orelsethrow** (Java 10+): Old=`get() or orElseThrow(supplier)` | Detect: `optional.get()`
- **record-based-errors** (Java 16+): Old=`Map or Verbose Class` | Detect: `Map or Verbose Class`
- **require-nonnull-else** (Java 9+): Old=`Ternary Null Check` | Detect: `Ternary Null Check`

## Io

- **deserialization-filters** (Java 9+): Old=`Accept Everything` | Detect: `new ObjectInputStream(`, `ois.readObject()`
- **file-memory-mapping** (Java 22+): Old=`MappedByteBuffer` | Detect: `FileChannel.open(`, `channel.size())`
- **files-mismatch** (Java 12+): Old=`Manual Byte Compare` | Detect: `Files.readAllBytes(`, `Arrays.equals(`
- **http-client** (Java 11+): Old=`HttpURLConnection` | Detect: `new URL(`, `new BufferedReader(`, `new InputStreamReader(`, `url.openConnection()`, `con.getInputStream())`
- **inputstream-transferto** (Java 9+): Old=`Manual Copy Loop` | Detect: `input.read(buf))`
- **io-class-console-io** (Java 25+): Old=`System.out / Scanner` | Detect: `System.out.print(`, `System.out.println(`, `new Scanner(`, `sc.nextLine()`, `sc.close()`
- **path-of** (Java 11+): Old=`Paths.get()` | Detect: `Paths.get(`
- **reading-files** (Java 11+): Old=`BufferedReader` | Detect: `new StringBuilder(`, `new BufferedReader(`, `new FileReader(`, `br.readLine())`, `sb.append(line)`, `sb.toString()`
- **try-with-resources-effectively-final** (Java 9+): Old=`Re-declare Variable` | Detect: `Re-declare Variable`
- **writing-files** (Java 11+): Old=`FileWriter + BufferedWriter` | Detect: `new FileWriter(`, `new BufferedWriter(`, `bw.write(content)`

## Language

- **call-c-from-java** (Java 22+): Old=`JNI (Java Native Interface)` | Detect: `System.loadLibrary(`, `System.out.println(`
- **compact-canonical-constructor** (Java 16+): Old=`Explicit constructor validation` | Detect: `Objects.requireNonNull(`, `List.copyOf(`
- **compact-source-files** (Java 25+): Old=`Main Class Ceremony` | Detect: `System.out.println(`
- **default-interface-methods** (Java 8+): Old=`Abstract classes for shared behavior` | Detect: `System.out.println(`, `extends AbstractLogger`
- **diamond-operator** (Java 9+): Old=`Repeat Type Args` | Detect: `new Predicate(`
- **exhaustive-switch** (Java 21+): Old=`Mandatory default` | Detect: `new IAE(`
- **flexible-constructor-bodies** (Java 25+): Old=`Validate After super()` | Detect: `new IAE(`, `extends Shape`
- **guarded-patterns** (Java 21+): Old=`Nested if` | Detect: `c.radius()`
- **markdown-javadoc-comments** (Java 23+): Old=`HTML-based Javadoc` | Detect: `HTML-based Javadoc`
- **module-import-declarations** (Java 25+): Old=`Many Imports` | Detect: `Many Imports`
- **pattern-matching-instanceof** (Java 16+): Old=`instanceof + Cast` | Detect: `System.out.println(`, `out.println(s.length())`
- **pattern-matching-switch** (Java 21+): Old=`if-else Chain` | Detect: `if-else Chain`
- **primitive-types-in-patterns** (Java 25+): Old=`Manual Range Checks` | Detect: `Manual Range Checks`
- **private-interface-methods** (Java 9+): Old=`Duplicated Logic` | Detect: `System.out.println(`
- **record-patterns** (Java 21+): Old=`Manual Access` | Detect: `System.out.println(`
- **records-for-data-classes** (Java 16+): Old=`Verbose POJO` | Detect: `Verbose POJO`
- **sealed-classes** (Java 17+): Old=`Open Hierarchy` | Detect: `extends Shape`
- **static-members-in-inner-classes** (Java 16+): Old=`Must use static nested class` | Detect: `Library.Book(`
- **static-methods-in-interfaces** (Java 8+): Old=`Utility classes` | Detect: `ValidatorUtils.isBlank(`, `.trim().isEmpty()`
- **switch-expressions** (Java 14+): Old=`Switch Statement` | Detect: `Switch Statement`
- **text-blocks-for-multiline-strings** (Java 15+): Old=`String Concatenation` | Detect: `String Concatenation`
- **type-inference-with-var** (Java 10+): Old=`Explicit Types` | Detect: `map.entrySet())`
- **unnamed-variables** (Java 22+): Old=`Unused Variable` | Detect: `Unused Variable`

## Security

- **key-derivation-functions** (Java 25+): Old=`Manual PBKDF2` | Detect: `SecretKeyFactory.getInstance(`, `new PBEKeySpec(`, `factory.generateSecret(spec)`
- **pem-encoding** (Java 25+): Old=`Manual Base64 + Headers` | Detect: `Base64.getMimeEncoder(`, `cert.getEncoded())`
- **random-generator** (Java 17+): Old=`new Random() / ThreadLocalRandom` | Detect: `ThreadLocalRandom.current(`, `new Random(`, `rng.nextInt(100)`
- **strong-random** (Java 9+): Old=`new SecureRandom()` | Detect: `new SecureRandom(`, `random.nextBytes(bytes)`
- **tls-default** (Java 11+): Old=`Manual TLS Config` | Detect: `SSLContext.getInstance(`, `ctx.getSocketFactory()`

## Streams

- **collectors-flatmapping** (Java 9+): Old=`Nested flatMap` | Detect: `Nested flatMap`
- **optional-ifpresentorelse** (Java 9+): Old=`if/else on Optional` | Detect: `user.isPresent())`, `user.get())`
- **optional-or** (Java 9+): Old=`Nested Fallback` | Detect: `cfg.isPresent())`
- **predicate-not** (Java 11+): Old=`Lambda negation` | Detect: `Collectors.toList(`, `list.stream()`, `s.isBlank())`
- **stream-gatherers** (Java 24+): Old=`Custom Collector` | Detect: `new ArrayList(`, `list.size()`
- **stream-iterate-predicate** (Java 9+): Old=`iterate + limit` | Detect: `Stream.iterate(`
- **stream-mapmulti** (Java 16+): Old=`flatMap + List` | Detect: `new OrderItem(`, `.items().stream()`, `order.items()`, `order.id()`
- **stream-of-nullable** (Java 9+): Old=`Null Check` | Detect: `Stream.of(`, `Stream.empty(`
- **stream-takewhile-dropwhile** (Java 9+): Old=`Manual Loop` | Detect: `new ArrayList(`, `result.add(n)`
- **stream-tolist** (Java 16+): Old=`Collectors.toList()` | Detect: `Collectors.toList(`, `s.length()`
- **virtual-thread-executor** (Java 21+): Old=`Fixed Thread Pool` | Detect: `Executors.newFixedThreadPool(`, `tasks.stream()`, `exec.submit(t))`, `exec.shutdown()`

## Strings

- **string-chars-stream** (Java 9+): Old=`Manual Loop` | Detect: `Character.isDigit(`, `str.length()`, `str.charAt(i)`
- **string-formatted** (Java 15+): Old=`String.format()` | Detect: `String.format(`
- **string-indent-transform** (Java 12+): Old=`Manual Indentation` | Detect: `new StringBuilder(`, `sb.toString()`
- **string-isblank** (Java 11+): Old=`trim().isEmpty()` | Detect: `.trim().isEmpty()`, `.trim().length()`, `str.trim()`
- **string-lines** (Java 11+): Old=`split(\"\\\\n\")` | Detect: `System.out.println(`, `out.println(line)`
- **string-repeat** (Java 11+): Old=`StringBuilder Loop` | Detect: `new StringBuilder(`, `sb.toString()`
- **string-strip** (Java 11+): Old=`trim()` | Detect: `str.trim()`

## Tooling

- **aot-class-preloading** (Java 25+): Old=`Cold Start Every Time` | Detect: `Cold Start Every Time`
- **built-in-http-server** (Java 18+): Old=`External Server / Framework` | Detect: `HttpServer.create(`, `new InetSocketAddress(`, `server.start()`
- **compact-object-headers** (Java 25+): Old=`128-bit Headers` | Detect: `128-bit Headers`
- **jfr-profiling** (Java 9+): Old=`External Profiler` | Detect: `External Profiler`
- **jshell-prototyping** (Java 9+): Old=`Create File + Compile + Run` | Detect: `Create File + Compile + Run`
- **junit6-with-jspecify** (Java 17+): Old=`Unannotated API` | Detect: `@Test`, `result.name())`
- **multi-file-source** (Java 22+): Old=`Compile All First` | Detect: `Compile All First`
- **single-file-execution** (Java 11+): Old=`Two-Step Compile` | Detect: `Two-Step Compile`
