# SSL Certificates Lab Notes

## Mainline Progress

### Step 1: Root CA
- ✅ Generated RSA 4096-bit private key
- ✅ Created self-signed certificate (CA:TRUE, pathlen=1)
- ✅ Verified with Python + OpenSSL (`openssl x509 -in root.cert.pem -noout -text`)
- Next: build Intermediate CA generator

---

## Curiosity Detours

### 🌱 On OIDs
- OIDs = Object Identifiers, unique dotted numbers.
- Example: `2.5.4.3` = Common Name (CN).
- Appear not only in certificates but also in LDAP, SNMP, healthcare IT.

### 🌱 On Hash Functions
- SHA-256 chosen over SHA-1/MD5 for certificate signatures.
- SHA-256 also widely used for file checksums.
- Internal MD5 is OK for corruption checks, but SHA-256 is the modern default.

### 🌱 On RSA Primes
- A 2048-bit RSA key uses two ~2048-bit primes.
- There are ~10^613 such primes.
- Keys are random → effectively unique.

### 🌱 On Serial Numbers
- Each X.509 certificate must have a unique serial number per issuer.
- `x509.random_serial_number()` generates a 159-bit random integer.
- Probability of collision is astronomically low (~10^47 possibilities).
- Real CAs also track issued certs in a database to avoid duplicates.
- RFC 5280: serial must be positive and ≤ 20 bytes.

---

## Next Steps
- Implement Intermediate CA (`make_intermediate_ca.py`).
- Issue a server certificate from Intermediate CA.
- Verify certificate chain with OpenSSL and Python.

