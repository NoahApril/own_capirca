
import sys
import os
import json

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from capirca.lib import policy
from capirca.lib import naming
from capirca.api.services.graph import GraphService

def verify_graph_service():
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
        
        service = GraphService()
        graph_data = service.policy_to_graph(pol)
        
        print(json.dumps(graph_data, indent=2))
        
        # Basic assertions
        nodes = graph_data.get('nodes', [])
        edges = graph_data.get('edges', [])
        
        print(f"\nNodes: {len(nodes)}")
        print(f"Edges: {len(edges)}")
        
        # Expect 3 nodes: 1 Header + 2 Terms
        if len(nodes) != 3:
            print("FAIL: Expected 3 nodes")
        else:
            print("PASS: Node count correct")
            
        # Expect 2 edges: Header->Term1, Term1->Term2
        if len(edges) != 2:
            print("FAIL: Expected 2 edges")
        else:
            print("PASS: Edge count correct")

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    verify_graph_service()
