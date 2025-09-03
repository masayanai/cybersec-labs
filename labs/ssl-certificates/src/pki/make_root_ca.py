from pathlib import Path
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

OUT_DIR = Path(__file__).resolve().parents[2] / "pkidata" / "root"

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    key = rsa.generate_private_key(public_exponent=65537, key_size=4096)

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Demo Root CA"),
        x509.NameAttribute(NameOID.COMMON_NAME, "Demo Root CA"),
    ])

    now = datetime.utcnow()
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject).issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(days=1))
        .not_valid_after(now + timedelta(days=3650))
        .add_extension(x509.BasicConstraints(ca=True, path_length=1), critical=True)
        .add_extension(x509.KeyUsage(
            digital_signature=False, content_commitment=False,
            key_encipherment=False, data_encipherment=False,
            key_agreement=False, key_cert_sign=True, crl_sign=True,
            encipher_only=False, decipher_only=False
        ), critical=True)
        .sign(private_key=key, algorithm=hashes.SHA256())
    )

    (OUT_DIR / "root.key.pem").write_bytes(key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.TraditionalOpenSSL,
        serialization.NoEncryption(),   # demo only
    ))
    (OUT_DIR / "root.cert.pem").write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    print(f"Wrote {OUT_DIR/'root.key.pem'} and {OUT_DIR/'root.cert.pem'}")

if __name__ == "__main__":
    main()
