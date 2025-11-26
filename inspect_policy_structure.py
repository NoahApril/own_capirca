
import sys
import os

# Add the current directory to sys.path to make sure we can import capirca
sys.path.append(os.getcwd())

from capirca.lib import policy
from capirca.lib import naming

def inspect_policy():
    sample_policy = """
header {
  target:: cisco_acl test-filter
}

term allow-tcp {
  protocol:: tcp
  action:: accept
}

term deny-all {
  action:: deny
}
"""
    defs = naming.Naming('./def')
    try:
        pol = policy.ParsePolicy(sample_policy, definitions=defs)
        print("Policy Object:", pol)
        print("Dir Policy:", dir(pol))
        
        if hasattr(pol, 'filters'):
            print("\nFilters Type:", type(pol.filters))
            for i, f in enumerate(pol.filters):
                print(f"  Filter {i} Type:", type(f))
                print(f"  Filter {i} Length:", len(f))
                for j, item in enumerate(f):
                    print(f"    Item {j} Type:", type(item))
                    print(f"    Item {j} Value:", item)
                    if hasattr(item, '__dict__'):
                         print(f"    Item {j} Dict:", item.__dict__)
                        
    except Exception as e:
        print("Error parsing policy:", e)

if __name__ == "__main__":
    inspect_policy()
