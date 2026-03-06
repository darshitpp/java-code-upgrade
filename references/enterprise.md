# Enterprise Patterns

## EJB Timer vs Jakarta Scheduler
- **Since:** Java 11
- **Old approach:** EJB TimerService (Java EE)
- **Modern approach:** ManagedScheduledExecutorService (Jakarta EE 10+)
- **Summary:** Replace heavyweight EJB timers with Jakarta Concurrency's ManagedScheduledExecutorService\ for simpler scheduling.

### Before
```java
@Stateless
public class ReportGenerator {
    @Resource
    TimerService timerService;

    @PostConstruct
    public void init() {
        timerService.createCalendarTimer(
            new ScheduleExpression()
                .hour("2").minute("0"));
    }

    @Timeout
    public void generateReport(Timer timer) {
        // runs every day at 02:00
        buildDailyReport();
    }
}
```

### After
```java
@ApplicationScoped
public class ReportGenerator {
    @Resource
    ManagedScheduledExecutorService scheduler;

    @PostConstruct
    public void init() {
        scheduler.scheduleAtFixedRate(
            this::generateReport,
            0, 24, TimeUnit.HOURS);
    }

    public void generateReport() {
        buildDailyReport();
    }
}
```

### Why modern wins
- **Reduced boilerplate:** No @Timeout callback or ScheduleExpression — use the standard ScheduledExecutorService\ API."
- **Better testability:** Plain methods and executor mocks make unit testing straightforward without\ EJB container."
- **Cloud-native friendly:** Managed executors integrate with container lifecycle and work in lightweight\ runtimes."

### References
- [Jakarta Concurrency Specification](https://jakarta.ee/specifications/concurrency/)
- [Jakarta Concurrency 3.0 API](https://jakarta.ee/specifications/concurrency/3.0/apidocs/)

---

## EJB versus CDI
- **Since:** Java 11
- **Old approach:** EJB (Java EE)
- **Modern approach:** CDI Bean (Jakarta EE 8+)
- **Summary:** Replace heavyweight EJBs with lightweight CDI beans for dependency injection\ and transactions.

### Before
```java
@Stateless
public class OrderEJB {
    @EJB
    private InventoryEJB inventory;

    public void placeOrder(Order order) {
        // container-managed transaction
        inventory.reserve(order.getItem());
    }
}
```

### After
```java
@ApplicationScoped
public class OrderService {
    @Inject
    private InventoryService inventory;

    @Transactional
    public void placeOrder(Order order) {
        inventory.reserve(order.getItem());
    }
}
```

### Why modern wins
- **Lightweight:** CDI beans are plain Java classes with no EJB-specific interfaces or descriptors.
- **Unified injection:** @Inject works for every managed bean, JAX-RS resources, and Jakarta EE components\ alike."
- **Easy unit testing:** Plain classes without EJB proxy overhead are straightforward to instantiate\ and mock."

### References
- [Jakarta CDI Specification](https://jakarta.ee/specifications/cdi/)
- [Jakarta Transactions — @Transactional](https://jakarta.ee/specifications/transactions/)

---

## JDBC ResultSet Mapping vs JPA Criteria API
- **Since:** Java 11
- **Old approach:** JDBC ResultSet (Java EE)
- **Modern approach:** JPA Criteria API (Jakarta EE 8+)
- **Summary:** Replace manual JDBC ResultSet mapping with JPA's type-safe Criteria API\ for dynamic queries.

### Before
```java
String sql = "SELECT * FROM users"
    + " WHERE status = ? AND age > ?";
try (Connection con = ds.getConnection();
     PreparedStatement ps =
             con.prepareStatement(sql)) {
    ps.setString(1, status);
    ps.setInt(2, minAge);
    ResultSet rs = ps.executeQuery();
    List<User> users = new ArrayList<>();
    while (rs.next()) {
        User u = new User();
        u.setId(rs.getLong("id"));
        u.setName(rs.getString("name"));
        u.setAge(rs.getInt("age"));
        users.add(u);
    }
}
```

### After
```java
@PersistenceContext
EntityManager em;

public List<User> findActiveAboveAge(
        String status, int minAge) {
    var cb = em.getCriteriaBuilder();
    var cq =
        cb.createQuery(User.class);
    var root = cq.from(User.class);
    cq.select(root).where(
        cb.equal(root.get("status"), status),
        cb.greaterThan(root.get("age"), minAge));
    return em.createQuery(cq).getResultList();
}
```

### Why modern wins
- **Type-safe queries:** The Criteria builder catches field name and type mismatches at compile time.
- **Automatic mapping:** JPA maps result rows to entity objects — no manual column-by-column extraction.
- **Composable predicates:** Dynamic where-clauses build cleanly with and(), or(), and reusable Predicate\ objects."

### References
- [Jakarta Persistence Specification](https://jakarta.ee/specifications/persistence/)
- [Jakarta Persistence 3.1 — Criteria API](https://jakarta.ee/specifications/persistence/3.1/apidocs/)

---

## JDBC versus jOOQ
- **Since:** Java 11
- **Old approach:** Raw JDBC (Raw JDBC)
- **Modern approach:** jOOQ SQL DSL (jOOQ)
- **Summary:** Replace raw JDBC string-based SQL with jOOQ's type-safe, fluent SQL DSL.

### Before
```java
String sql = "SELECT id, name, email FROM users "
           + "WHERE department = ? AND salary > ?";
try (Connection con = ds.getConnection();
     PreparedStatement ps =
             con.prepareStatement(sql)) {
    ps.setString(1, department);
    ps.setBigDecimal(2, minSalary);
    ResultSet rs = ps.executeQuery();
    List<User> result = new ArrayList<>();
    while (rs.next()) {
        result.add(new User(
            rs.getLong("id"),
            rs.getString("name"),
            rs.getString("email")));
    }
    return result;
}
```

### After
```java
DSLContext dsl = DSL.using(ds, SQLDialect.POSTGRES);

return dsl
    .select(USERS.ID, USERS.NAME, USERS.EMAIL)
    .from(USERS)
    .where(USERS.DEPARTMENT.eq(department)
        .and(USERS.SALARY.gt(minSalary)))
    .fetchInto(User.class);
```

### Why modern wins
- **Type-safe columns:** Column names are generated Java constants — typos and type mismatches become\ compiler errors instead of runtime failures."
- **SQL fluency:** The jOOQ DSL mirrors SQL syntax closely, so complex JOINs, subqueries, and\ CTEs stay readable."
- **Injection-free by design:** Parameters are always bound safely — no string concatenation means no SQL\ injection risk."

### References
- [jOOQ — Getting Started](https://www.jooq.org/doc/latest/manual/getting-started/)
- [jOOQ — DSL API Reference](https://www.jooq.org/javadoc/latest/)

---

## JDBC versus JPA
- **Since:** Java 11
- **Old approach:** JDBC (Java EE)
- **Modern approach:** JPA EntityManager (Jakarta EE 8+)
- **Summary:** Replace verbose JDBC boilerplate with JPA's object-relational mapping and\ EntityManager.

### Before
```java
String sql = "SELECT * FROM users WHERE id = ?";
try (Connection con = dataSource.getConnection();
     PreparedStatement ps =
             con.prepareStatement(sql)) {
    ps.setLong(1, id);
    ResultSet rs = ps.executeQuery();
    if (rs.next()) {
        User u = new User();
        u.setId(rs.getLong("id"));
        u.setName(rs.getString("name"));
    }
}
```

### After
```java
@PersistenceContext
EntityManager em;

public User findUser(Long id) {
    return em.find(User.class, id);
}

public List<User> findByName(String name) {
    return em.createQuery(
        "SELECT u FROM User u WHERE u.name = :name",
        User.class)
        .setParameter("name", name)
        .getResultList();
}
```

### Why modern wins
- **Object mapping:** Entities are plain annotated classes — no manual ResultSet-to-object translation.
- **Type-safe queries:** JPQL operates on entity types and fields rather than raw table and column\ strings."
- **Built-in caching:** First- and second-level caches reduce database round-trips automatically.

### References
- [Jakarta Persistence Specification](https://jakarta.ee/specifications/persistence/)
- [Jakarta Persistence 3.1 API](https://jakarta.ee/specifications/persistence/3.1/apidocs/)

---

## JNDI Lookup vs CDI Injection
- **Since:** Java 11
- **Old approach:** JNDI Lookup (Java EE)
- **Modern approach:** CDI @Inject (Jakarta EE 8+)
- **Summary:** Replace fragile JNDI string lookups with type-safe CDI injection for container-managed\ resources.

### Before
```java
public class OrderService {
    private DataSource ds;

    public void init() throws NamingException {
        InitialContext ctx = new InitialContext();
        ds = (DataSource) ctx.lookup(
            "java:comp/env/jdbc/OrderDB");
    }

    public List<Order> findAll()
            throws SQLException {
        try (Connection con = ds.getConnection()) {
            // query orders
        }
    }
}
```

### After
```java
@ApplicationScoped
public class OrderService {
    @Inject
    @Resource(name = "jdbc/OrderDB")
    DataSource ds;

    public List<Order> findAll()
            throws SQLException {
        try (Connection con = ds.getConnection()) {
            // query orders
        }
    }
}
```

### Why modern wins
- **Type-safe wiring:** Injection errors are caught at deployment time, not at runtime via string\ lookups."
- **No boilerplate:** Eliminates InitialContext creation, JNDI name strings, and NamingException\ handling."
- **Testable:** Dependencies are injected fields, easily replaced with mocks in unit tests.

### References
- [Jakarta CDI Specification](https://jakarta.ee/specifications/cdi/)
- [Jakarta Annotations — @Resource](https://jakarta.ee/specifications/annotations/)

---

## JPA versus Jakarta Data
- **Since:** Java 21
- **Old approach:** JPA EntityManager (Jakarta EE 8+)
- **Modern approach:** Jakarta Data Repository (Jakarta EE 11+)
- **Summary:** Declare a repository interface and let Jakarta Data generate the DAO implementation\ automatically.

### Before
```java
@PersistenceContext
EntityManager em;

public User findById(Long id) {
    return em.find(User.class, id);
}

public List<User> findByName(String name) {
    return em.createQuery(
        "SELECT u FROM User u WHERE u.name = :name",
        User.class)
        .setParameter("name", name)
        .getResultList();
}

public void save(User user) {
    em.persist(user);
}
```

### After
```java
@Repository
public interface Users extends CrudRepository<User, Long> {
    List<User> findByName(String name);
}
```

### Why modern wins
- **Zero boilerplate:** Declare the interface; the container generates the full DAO implementation\ at deploy time."
- **Derived queries:** Method names like findByNameAndStatus are parsed automatically — no JPQL\ or SQL needed."
- **Portable:** Any Jakarta EE 11 compliant runtime provides the repository implementation\ with no vendor lock-in."

### References
- [Jakarta Data 1.0 Specification](https://jakarta.ee/specifications/data/1.0/)
- [Jakarta Data 1.0 API](https://jakarta.ee/specifications/data/1.0/apidocs/)

---

## JSF Managed Bean vs CDI Named Bean
- **Since:** Java 11
- **Old approach:** @ManagedBean (Java EE)
- **Modern approach:** @Named + CDI (Jakarta EE 10+)
- **Summary:** Replace deprecated JSF @ManagedBean with CDI @Named for a unified dependency\ injection model.

### Before
```java
@ManagedBean
@SessionScoped
public class UserBean implements Serializable {
    @ManagedProperty("#{userService}")
    private UserService userService;

    private String name;

    public String getName() { return name; }
    public void setName(String name) {
        this.name = name;
    }

    public void setUserService(UserService svc) {
        this.userService = svc;
    }
}
```

### After
```java
@Named
@SessionScoped
public class UserBean implements Serializable {
    @Inject
    private UserService userService;

    private String name;

    public String getName() { return name; }
    public void setName(String name) {
        this.name = name;
    }
}
```

### Why modern wins
- **Unified model:** One CDI container manages all beans — JSF, REST, and service layers share\ the same injection."
- **Less boilerplate:** @Inject replaces @ManagedProperty and its required setter method.
- **Future-proof:** @ManagedBean is removed in Jakarta EE 10; @Named is the supported replacement.

### References
- [Jakarta Faces Specification](https://jakarta.ee/specifications/faces/)
- [Jakarta CDI Specification](https://jakarta.ee/specifications/cdi/)

---

## Manual JPA Transaction vs Declarative @Transactional
- **Since:** Java 11
- **Old approach:** Manual Transaction (Java EE)
- **Modern approach:** @Transactional (Jakarta EE 8+)
- **Summary:** Replace verbose begin/commit/rollback blocks with a single @Transactional\ annotation.

### Before
```java
@PersistenceContext
EntityManager em;

public void transferFunds(Long from, Long to,
                          BigDecimal amount) {
    EntityTransaction tx = em.getTransaction();
    tx.begin();
    try {
        Account src = em.find(Account.class, from);
        Account dst = em.find(Account.class, to);
        src.debit(amount);
        dst.credit(amount);
        tx.commit();
    } catch (Exception e) {
        tx.rollback();
        throw e;
    }
}
```

### After
```java
@ApplicationScoped
public class AccountService {
    @PersistenceContext
    EntityManager em;

    @Transactional
    public void transferFunds(Long from, Long to,
                              BigDecimal amount) {
        var src = em.find(Account.class, from);
        var dst = em.find(Account.class, to);
        src.debit(amount);
        dst.credit(amount);
    }
}
```

### Why modern wins
- **No boilerplate:** One annotation replaces repetitive begin/commit/rollback try-catch blocks.
- **Safer rollback:** The container guarantees rollback on unchecked exceptions — no risk of forgetting\ the catch block."
- **Declarative control:** Propagation, isolation, and rollback rules are expressed as annotation attributes.

### References
- [Jakarta Transactions Specification](https://jakarta.ee/specifications/transactions/)
- [Jakarta Transactions 2.0 API](https://jakarta.ee/specifications/transactions/2.0/apidocs/)

---

## Message-Driven Bean vs Reactive Messaging
- **Since:** Java 11
- **Old approach:** Message-Driven Bean (Java EE)
- **Modern approach:** Reactive Messaging (MicroProfile 4+)
- **Summary:** Replace JMS Message-Driven Beans with MicroProfile Reactive Messaging for\ simpler event processing.

### Before
```java
@MessageDriven(activationConfig = {
    @ActivationConfigProperty(
        propertyName = "destinationType",
        propertyValue = "jakarta.jms.Queue"),
    @ActivationConfigProperty(
        propertyName = "destination",
        propertyValue = "java:/jms/OrderQueue")
})
public class OrderMDB implements MessageListener {
    @Override
    public void onMessage(Message message) {
        TextMessage txt = (TextMessage) message;
        processOrder(txt.getText());
    }
}
```

### After
```java
@ApplicationScoped
public class OrderProcessor {
    @Incoming("orders")
    public void process(Order order) {
        // automatically deserialized from
        // the "orders" channel
        fulfillOrder(order);
    }
}
```

### Why modern wins
- **Minimal code:** A single @Incoming method replaces the MDB class, MessageListener interface,\ and activation config."
- **Broker-agnostic:** Swap Kafka, AMQP, or JMS connectors via configuration without changing application\ code."
- **Cloud-native fit:** Reactive streams backpressure and lightweight runtime make it ideal for containerised\ deployments."

### References
- [MicroProfile Reactive Messaging Specification](https://download.eclipse.org/microprofile/microprofile-reactive-messaging-3.0/microprofile-reactive-messaging-spec-3.0.html)
- [SmallRye Reactive Messaging Documentation](https://smallrye.io/smallrye-reactive-messaging/)

---

## Servlet versus JAX-RS
- **Since:** Java 11
- **Old approach:** HttpServlet (Java EE)
- **Modern approach:** JAX-RS Resource (Jakarta EE 8+)
- **Summary:** Replace verbose HttpServlet boilerplate with declarative JAX-RS resource\ classes.

### Before
```java
@WebServlet("/users")
public class UserServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req,
                         HttpServletResponse res)
            throws ServletException, IOException {
        String id = req.getParameter("id");
        res.setContentType("application/json");
        res.getWriter().write("{\"id\":\"" + id + "\"}");
    }
}
```

### After
```java
@Path("/users")
public class UserResource {
    @GET
    @Produces(MediaType.APPLICATION_JSON)
    public Response getUser(
            @QueryParam("id") String id) {
        return Response.ok(new User(id)).build();
    }
}
```

### Why modern wins
- **Declarative routing:** Annotations define HTTP method, path, and content type instead of imperative\ if/else dispatch."
- **Automatic marshalling:** Return POJOs directly; the runtime serialises them to JSON or XML based on\ @Produces."
- **Easier testing:** Resource classes are plain Java objects, testable without a servlet container.

### References
- [Jakarta RESTful Web Services Specification](https://jakarta.ee/specifications/restful-ws/)
- [Jakarta REST 3.1 API](https://jakarta.ee/specifications/restful-ws/3.1/apidocs/)

---

## Singleton EJB vs CDI @ApplicationScoped
- **Since:** Java 11
- **Old approach:** @Singleton EJB (Java EE)
- **Modern approach:** @ApplicationScoped CDI (Jakarta EE 8+)
- **Summary:** Replace Singleton EJBs with CDI @ApplicationScoped beans for simpler shared-state\ management.

### Before
```java
@Singleton
@Startup
@ConcurrencyManagement(
    ConcurrencyManagementType.CONTAINER)
public class ConfigCache {
    private Map<String, String> cache;

    @PostConstruct
    public void load() {
        cache = loadFromDatabase();
    }

    @Lock(LockType.READ)
    public String get(String key) {
        return cache.get(key);
    }

    @Lock(LockType.WRITE)
    public void refresh() {
        cache = loadFromDatabase();
    }
}
```

### After
```java
@ApplicationScoped
public class ConfigCache {
    private volatile Map<String, String> cache;

    @PostConstruct
    public void load() {
        cache = loadFromDatabase();
    }

    public String get(String key) {
        return cache.get(key);
    }

    public void refresh() {
        cache = loadFromDatabase();
    }
}
```

### Why modern wins
- **Less annotation noise:** No @ConcurrencyManagement, @Lock, or @Startup — just a single @ApplicationScoped\ annotation."
- **Flexible concurrency:** Use java.util.concurrent locks or volatile for exactly the thread-safety\ you need."
- **Easy testing:** Plain CDI beans can be instantiated directly in tests without an EJB container.

### References
- [Jakarta CDI Specification](https://jakarta.ee/specifications/cdi/)
- [Jakarta Enterprise Beans Specification](https://jakarta.ee/specifications/enterprise-beans/)

---

## SOAP Web Services vs Jakarta REST
- **Since:** Java 11
- **Old approach:** JAX-WS / SOAP (Java EE)
- **Modern approach:** Jakarta REST / JSON (Jakarta EE 8+)
- **Summary:** Replace heavyweight SOAP/WSDL endpoints with clean Jakarta REST resources\ returning JSON.

### Before
```java
@WebService
public class UserWebService {
    @WebMethod
    public UserResponse getUser(
            @WebParam(name = "id") String id) {
        User user = findUser(id);
        UserResponse res = new UserResponse();
        res.setId(user.getId());
        res.setName(user.getName());
        return res;
    }
}
```

### After
```java
@Path("/users")
@Produces(MediaType.APPLICATION_JSON)
public class UserResource {
    @Inject
    UserService userService;

    @GET
    @Path("/{id}")
    public User getUser(@PathParam("id") String id) {
        return userService.findById(id);
    }
}
```

### Why modern wins
- **Lighter payloads:** JSON is more compact than SOAP XML envelopes, reducing bandwidth and parsing\ overhead."
- **Simple annotations:** @GET, @Path, and @Produces replace WSDL, @WebService, and @WebMethod ceremony.
- **Microservice-ready:** REST/JSON is the standard for service-to-service communication in cloud-native\ architectures."

### References
- [Jakarta RESTful Web Services Specification](https://jakarta.ee/specifications/restful-ws/)
- [Jakarta JSON Binding Specification](https://jakarta.ee/specifications/jsonb/)

---

## Spring Framework 7 API Versioning
- **Since:** Java 17
- **Old approach:** Manual URL Path Versioning (Spring Boot 2/3)
- **Modern approach:** Native API Versioning (Spring Framework 7+)
- **Summary:** Replace duplicated version-prefixed controllers with Spring Framework 7's\ native API versioning support.

### Before
```java
// Version 1 controller
@RestController
@RequestMapping("/api/v1/products")
public class ProductControllerV1 {
    @GetMapping("/{id}")
    public ProductDtoV1 getProduct(
            @PathVariable Long id) {
        return service.getV1(id);
    }
}

// Version 2 — duplicated structure
@RestController
@RequestMapping("/api/v2/products")
public class ProductControllerV2 {
    @GetMapping("/{id}")
    public ProductDtoV2 getProduct(
            @PathVariable Long id) {
        return service.getV2(id);
    }
}
```

### After
```java
// Configure versioning once
@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void configureApiVersioning(
            ApiVersionConfigurer config) {
        config.useRequestHeader("X-API-Version");
    }
}

// Single controller, version per method
@RestController
@RequestMapping("/api/products")
public class ProductController {
    @GetMapping(value = "/{id}", version = "1")
    public ProductDtoV1 getV1(@PathVariable Long id) {
        return service.getV1(id);
    }

    @GetMapping(value = "/{id}", version = "2")
    public ProductDtoV2 getV2(@PathVariable Long id) {
        return service.getV2(id);
    }
}
```

### Why modern wins
- **No controller duplication:** All versions live in one controller class; only the individual handler methods\ carry a version attribute."
- **Centralised version strategy:** Switch from header to URL or query-param versioning in a single configureApiVersioning\ call."
- **Incremental evolution:** Add a new version to one method without touching unrelated endpoints or creating\ new controller files."

### References
- [Spring Framework 7.0 — API Versioning](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-requestmapping.html#mvc-ann-requestmapping-version)
- [Spring Framework 7.0 Migration Guide](https://github.com/spring-projects/spring-framework/wiki/Spring-Framework-7.0-Migration-Guide)

---

## Spring Null Safety with JSpecify
- **Since:** Java 17
- **Old approach:** Spring @NonNull/@Nullable (Spring 5/6)
- **Modern approach:** JSpecify @NullMarked (Spring 7)
- **Summary:** Spring 7 adopts JSpecify annotations, making non-null the default and reducing\ annotation noise.

### Before
```java
import org.springframework.lang.NonNull;
import org.springframework.lang.Nullable;

public class UserService {

    @Nullable
    public User findById(@NonNull String id) {
        return repository.findById(id).orElse(null);
    }

    @NonNull
    public List<User> findAll() {
        return repository.findAll();
    }

    @NonNull
    public User save(@NonNull User user) {
        return repository.save(user);
    }
}
```

### After
```java
import org.jspecify.annotations.NullMarked;
import org.jspecify.annotations.Nullable;

@NullMarked
public class UserService {

    public @Nullable User findById(String id) {
        return repository.findById(id).orElse(null);
    }

    public List<User> findAll() {
        return repository.findAll();
    }

    public User save(User user) {
        return repository.save(user);
    }
}
```

### Why modern wins
- **Non-null by default:** @NullMarked makes all unannotated types non-null, so only nullable exceptions\ need annotation."
- **Ecosystem standard:** JSpecify annotations are a cross-framework standard recognized by NullAway,\ Error Prone, and IDEs."
- **Richer tooling:** Modern static analyzers understand JSpecify's null model and report violations\ at compile time."

### References
- [Spring Framework 7 — Null Safety](https://docs.spring.io/spring-framework/reference/core/null-safety.html)
- [JSpecify Specification](https://jspecify.dev/docs/spec)

---

## Spring XML Bean Config vs Annotation-Driven
- **Since:** Java 17
- **Old approach:** XML Bean Definitions (Spring (XML))
- **Modern approach:** Annotation-Driven Beans (Spring Boot 3+)
- **Summary:** Replace verbose Spring XML bean definitions with concise annotation-driven\ configuration in Spring Boot.

### Before
```java
<!-- applicationContext.xml -->
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd">

    <bean id="userRepository"
          class="com.example.UserRepository">
        <property name="dataSource" ref="dataSource"/>
    </bean>

    <bean id="userService"
          class="com.example.UserService">
        <property name="repository" ref="userRepository"/>
    </bean>

</beans>
```

### After
```java
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}

@Repository
public class UserRepository {
    private final JdbcTemplate jdbc;

    public UserRepository(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }
}

@Service
public class UserService {
    private final UserRepository repository;

    public UserService(UserRepository repository) {
        this.repository = repository;
    }
}
```

### Why modern wins
- **No XML:** @SpringBootApplication triggers component scanning and auto-configuration,\ eliminating all XML wiring files."
- **Constructor injection:** Spring injects dependencies through constructors automatically, making beans\ easier to test and reason about."
- **Auto-configuration:** Spring Boot configures DataSource, JPA, and other infrastructure from the\ classpath with zero boilerplate."

### References
- [Spring Framework — Annotation-based Container Configuration](https://docs.spring.io/spring-framework/reference/core/beans/annotation-config.html)
- [Spring Boot — Auto-configuration](https://docs.spring.io/spring-boot/reference/using/auto-configuration.html)

---
