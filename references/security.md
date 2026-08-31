# Security Patterns

## Key Derivation Functions
- **Since:** Java 25
- **Old approach:** Manual PBKDF2 (Java 8)
- **Modern approach:** KDF API (Java 25)
- **Summary:** Derive cryptographic keys using the standard KDF API.

### Before
```java
SecretKeyFactory factory =
    SecretKeyFactory.getInstance(
        "PBKDF2WithHmacSHA256");
KeySpec spec = new PBEKeySpec(
    password, salt, 10000, 256);
SecretKey key =
    factory.generateSecret(spec);
```

### After
```java
var kdf = KDF.getInstance("HKDF-SHA256");
SecretKey key = kdf.deriveKey(
    "AES",
    KDF.HKDFParameterSpec
        .ofExtract()
        .addIKM(inputKey)
        .addSalt(salt)
        .thenExpand(info, 32)
        .build()
);
```

### Why modern wins
- **Clean API:** Builder pattern instead of awkward KeySpec constructors.
- **HKDF support:** Modern HKDF algorithm alongside PBKDF2.
- **Standard:** Unified API for all key derivation algorithms.

### References
- [Key Derivation Functions (JEP 478)](https://openjdk.org/jeps/478)

---

## PEM encoding/decoding
- **Since:** Java 25
- **Old approach:** Manual Base64 + Headers (Java 8)
- **Modern approach:** PEM API (Java 25 (Preview))
- **Summary:** Encode and decode PEM-formatted cryptographic objects natively.

### Before
```java
String pem = "-----BEGIN CERTIFICATE-----\n"
    + Base64.getMimeEncoder()
        .encodeToString(
            cert.getEncoded())
    + "\n-----END CERTIFICATE-----";
```

### After
```java
// Encode to PEM
String pem = PEMEncoder.of()
    .encodeToString(cert);
// Decode from PEM
var cert = PEMDecoder.of()
    .decode(pemString);
```

### Why modern wins
- **No manual Base64:** PEM headers, line wrapping, and Base64 handled automatically.
- **Bidirectional:** Encode to PEM and decode from PEM with one API.
- **Standard format:** Produces RFC 7468-compliant PEM output.

### References
- [PEM Encodings of Certificates (JEP 470)](https://openjdk.org/jeps/470)

---

## RandomGenerator interface
- **Since:** Java 17
- **Old approach:** new Random() / ThreadLocalRandom (Java 8)
- **Modern approach:** RandomGenerator factory (Java 17+)
- **Summary:** Use the RandomGenerator interface to choose random number algorithms by\ name without coupling to a specific class.

### Before
```java
// Hard-coded to one algorithm
Random rng = new Random();
int value = rng.nextInt(100);

// Or thread-local, but still locked in
int value = ThreadLocalRandom.current()
    .nextInt(100);
```

### After
```java
// Algorithm-agnostic via factory
var rng = RandomGenerator.of("L64X128MixRandom");
int value = rng.nextInt(100);

// Or get a splittable generator
var rng = RandomGeneratorFactory
    .of("L64X128MixRandom").create();
```

### Why modern wins
- **Algorithm-agnostic:** Choose the best RNG algorithm by name without changing code structure.
- **Better algorithms:** Access to modern LXM generators with superior statistical properties.
- **Unified API:** One interface covers Random, ThreadLocalRandom, SplittableRandom, and more.

### References
- [RandomGenerator](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/random/RandomGenerator.html)
- [New Random Generator API (JEP 356)](https://openjdk.org/jeps/356)

---

## SecurityManager checks to explicit authorization
- **Since:** Java 24
- **Old approach:** SecurityManager checks (JDK 23 and earlier)
- **Modern approach:** Explicit authorization (JDK 24+)
- **Summary:** Replace disabled SecurityManager checks with explicit application authorization\ and deployment isolation.

### Before
```java
SecurityManager manager = System.getSecurityManager();
if (manager != null) {
    manager.checkRead(path.toString());
}
return Files.readString(path);
```

### After
```java
// Untrusted users must not be able to modify this tree
Path root = allowedRoot.toRealPath();
Path resolved = root.resolve(requested)
    .normalize()
    .toRealPath();
if (!resolved.startsWith(root)) {
    throw new SecurityException(
        "Path is outside the allowed root");
}
return Files.readString(resolved);
```

### Why modern wins
- **Explicit policy:** Authorization is visible and testable in application logic.
- **Real isolation:** Process, container, and operating-system boundaries protect the whole application.
- **Required migration:** Removes checks that can no longer enforce policy on JDK 24 and later.

### References
- [Permanently Disable the Security Manager (JEP 486)](https://openjdk.org/jeps/486)
- [SecureDirectoryStream](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/nio/file/SecureDirectoryStream.html)

---

## Standard Base64 encoding and decoding
- **Since:** Java 8
- **Old approach:** sun.misc encoder (Internal JDK API)
- **Modern approach:** Standard Base64 API (Java 8+)
- **Summary:** Use java.util.Base64 instead of internal JDK classes or third-party codecs.

### Before
```java
String encoded = new sun.misc.BASE64Encoder()
    .encode(data);
```

### After
```java
String encoded = Base64.getEncoder()
    .encodeToString(data);
```

### Why modern wins
- **Supported API:** Avoids inaccessible sun.misc implementation classes.
- **Complete variants:** Includes basic, URL-safe, and MIME encoders and decoders.
- **No dependency:** Encoding and decoding are built into the JDK.

### References
- [Base64](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Base64.html)

---

## Strong random generation
- **Since:** Java 9
- **Old approach:** new SecureRandom() (Java 8)
- **Modern approach:** getInstanceStrong() (Java 9+)
- **Summary:** Get the platform's strongest SecureRandom implementation.

### Before
```java
// Default algorithm — may not be
// the strongest available
SecureRandom random =
    new SecureRandom();
byte[] bytes = new byte[32];
random.nextBytes(bytes);
```

### After
```java
// Platform's strongest algorithm
SecureRandom random =
    SecureRandom.getInstanceStrong();
byte[] bytes = new byte[32];
random.nextBytes(bytes);
```

### Why modern wins
- **Strongest available:** Automatically selects the best algorithm for the platform.
- **Explicit intent:** Clearly communicates that strong randomness is required.
- **Configurable:** Administrators can change the strong algorithm via security properties.

### References
- [SecureRandom](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/security/SecureRandom.html)

---

## TLS 1.3 by default
- **Since:** Java 11
- **Old approach:** Manual TLS Config (Java 8)
- **Modern approach:** TLS 1.3 Default (Java 11+)
- **Summary:** TLS 1.3 is enabled by default — no explicit protocol configuration needed.

### Before
```java
SSLContext ctx =
    SSLContext.getInstance("TLSv1.2");
ctx.init(null, trustManagers, null);
SSLSocketFactory factory =
    ctx.getSocketFactory();
// Must specify protocol version
```

### After
```java
// TLS 1.3 is the default!
var client = HttpClient.newBuilder()
    .sslContext(SSLContext.getDefault())
    .build();
// Already using TLS 1.3
```

### Why modern wins
- **More secure:** TLS 1.3 removes obsolete cipher suites and handshake patterns.
- **Faster handshake:** TLS 1.3 completes in one round trip vs two.
- **Zero config:** Secure by default — no explicit protocol selection needed.

### References
- [SSLContext](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/javax/net/ssl/SSLContext.html)
- [Java Security Guide](https://docs.oracle.com/en/java/javase/25/security/java-security-overview1.html)

---
