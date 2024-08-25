from petlib.ec import EcGroup, EcPt
from petlib.bn import Bn

# Setup elliptic curve and group
group = EcGroup()

# Generate Alice's secret number
x = group.order().random()

# Generate Alice's public key
g = group.generator()
h = g * x

# Alice's secret
print("Alice's secret (x):", x)

# Alice creates a proof
r = group.order().random()
C = g * r
z = (r + x) % group.order()

# Bob verifies the proof
assert C == h * r + g * z
print("Proof verified successfully!")

# Let's consider fingerprint data for encryption/decryption
# Fingerprint data can be represented as a point on the elliptic curve
# For demonstration, let's assume the fingerprint data is represented as a point P on the curve

# Encrypt the fingerprint data using Alice's public key
P = g * 123  # Assuming 123 is the fingerprint data point
ciphertext = P + h  # Encrypted fingerprint data

# Decrypt the ciphertext using Alice's secret key
decrypted_point = ciphertext + (-x * g)  # Decrypted fingerprint data point

# Verify the decrypted data
assert decrypted_point == P
print("Decryption successful!")
