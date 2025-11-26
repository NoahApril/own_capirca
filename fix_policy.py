import sys
import os
sys.path.append(os.getcwd())

from capirca.db.base import SessionLocal
from capirca.db import models

# Fixed policy content (without destination-port standalone)
fixed_content = """
header {
  target:: cisco_acl test-filter
}

term allow-ssh {
  protocol:: tcp
  action:: accept
  comment:: "Allow SSH traffic"
}

term allow-http {
  protocol:: tcp
  action:: accept
  comment:: "Allow HTTP traffic"
}

term deny-all {
  action:: deny
  comment:: "Deny all other traffic"
}
"""

db = SessionLocal()
policy = db.query(models.Policy).filter(models.Policy.id == 1).first()
if policy:
    policy.content = fixed_content
    db.commit()
    print("Policy updated successfully")
else:
    print("Policy not found")
db.close()
