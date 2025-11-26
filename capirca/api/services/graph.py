# Copyright 2024 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Graph service for converting Capirca policies to React Flow format."""

from typing import Dict, List, Any, Tuple
from capirca.lib import policy

class GraphService:
    """Service to transform Capirca Policy objects into graph data."""

    def policy_to_graph(self, pol: policy.Policy) -> Dict[str, List[Dict[str, Any]]]:
        """Convert a parsed Policy object into React Flow nodes and edges.
        
        Args:
            pol: The parsed Capirca Policy object.
            
        Returns:
            A dictionary with 'nodes' and 'edges' lists.
        """
        nodes = []
        edges = []
        
        # Vertical spacing for initial layout (simple auto-layout)
        y_pos = 0
        x_pos = 250
        
        # We'll use a simple counter for unique IDs
        node_counter = 0
        
        if not hasattr(pol, 'filters'):
            return {"nodes": [], "edges": []}

        for i, filter_tuple in enumerate(pol.filters):
            # filter_tuple is (Header, List[Term])
            if not isinstance(filter_tuple, tuple) or len(filter_tuple) < 2:
                continue
                
            header = filter_tuple[0]
            terms = filter_tuple[1]
            
            # Create Header Node
            header_id = f"header-{i}"
            header_label = f"Filter: {header.target[0] if header.target else 'Unknown'}"
            
            nodes.append({
                "id": header_id,
                "type": "input", # Input node for the flow
                "data": {"label": header_label, "details": str(header.__dict__)},
                "position": {"x": x_pos, "y": y_pos}
            })
            
            y_pos += 100
            previous_node_id = header_id
            
            for j, term in enumerate(terms):
                term_id = f"term-{i}-{j}"
                term_name = term.name
                
                # Extract some term details for the label
                details = []
                if term.protocol:
                    details.append(f"Proto: {term.protocol}")
                if term.source_address:
                    details.append(f"Src: {len(term.source_address)} addrs")
                if term.destination_address:
                    details.append(f"Dst: {len(term.destination_address)} addrs")
                if term.destination_port:
                    details.append(f"Port: {len(term.destination_port)}")
                if term.action:
                    details.append(f"Action: {term.action}")
                
                label = f"Term: {term_name}\n" + "\n".join(details)
                
                # Determine node style based on action
                style = {}
                if 'accept' in term.action:
                    style = {'background': '#d4edda', 'border': '1px solid #c3e6cb'}
                elif 'deny' in term.action or 'reject' in term.action:
                    style = {'background': '#f8d7da', 'border': '1px solid #f5c6cb'}
                
                nodes.append({
                    "id": term_id,
                    "data": {
                        "label": label,
                        "term_name": term_name,
                        "action": term.action,
                        "protocol": term.protocol,
                        # Add more metadata as needed
                    },
                    "position": {"x": x_pos, "y": y_pos},
                    "style": style
                })
                
                # Edge from previous node to this term
                edges.append({
                    "id": f"e-{previous_node_id}-{term_id}",
                    "source": previous_node_id,
                    "target": term_id,
                    "animated": True
                })
                
                previous_node_id = term_id
                y_pos += 150
            
            # Reset Y for next filter (if any), maybe shift X
            y_pos = 0
            x_pos += 400

        return {"nodes": nodes, "edges": edges}
