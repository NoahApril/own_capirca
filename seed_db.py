
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add current directory to path
sys.path.append(os.getcwd())

from capirca.db import models
from capirca.db.base import Base, engine, SessionLocal

def seed_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Check if policy exists
    existing_policy = db.query(models.Policy).filter(models.Policy.id == 1).first()
    if existing_policy:
        print("Policy 1 already exists.")
        return

    # Create sample policy
    sample_content = """
header {
  target:: cisco_acl test-filter
}

term allow-ssh {
  destination-port:: 22
  protocol:: tcp
  action:: accept
}

term allow-http {
  destination-port:: 80
  protocol:: tcp
  action:: accept
}

term deny-all {
  action:: deny
}
"""
    policy = models.Policy(
        name="Sample Policy",
        description="A sample policy for visualization",
        content=sample_content,
        status="active",
        version=1
    )
    
    db.add(policy)
    db.commit()
    print("Created sample policy with ID 1")

if __name__ == "__main__":
    seed_db()
