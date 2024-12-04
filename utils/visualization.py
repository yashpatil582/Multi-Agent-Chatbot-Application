import plotly.graph_objects as go
from typing import Dict, List

def create_interactive_agent_visualization(agent_states: Dict = None):
    """Create an interactive visualization of agent interactions using Plotly"""
    
    # Node positions
    nodes = {
        'User Query': {'x': 0, 'y': 0},
        'Coordinator': {'x': 0, 'y': -1},
        'Wikipedia Agent': {'x': -1, 'y': -2},
        'Google Agent': {'x': 1, 'y': -2},
        'Response': {'x': 0, 'y': -3}
    }
    
    # Create edges
    edges = [
        ('User Query', 'Coordinator'),
        ('Coordinator', 'Wikipedia Agent'),
        ('Coordinator', 'Google Agent'),
        ('Wikipedia Agent', 'Response'),
        ('Google Agent', 'Response')
    ]
    
    # Create node traces
    node_x = []
    node_y = []
    node_text = []
    node_color = []
    
    for node, pos in nodes.items():
        node_x.append(pos['x'])
        node_y.append(pos['y'])
        node_text.append(node)
        # Set colors based on node type
        if 'Agent' in node:
            node_color.append('#FF9999')  # Red for agents
        elif node == 'Coordinator':
            node_color.append('#99FF99')  # Green for coordinator
        else:
            node_color.append('#9999FF')  # Blue for other nodes

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        textposition="bottom center",
        marker=dict(
            size=30,
            color=node_color,
            line=dict(width=2, color='#888'),
        )
    )

    # Create edge traces
    edge_x = []
    edge_y = []
    
    for edge in edges:
        x0, y0 = nodes[edge[0]]['x'], nodes[edge[0]]['y']
        x1, y1 = nodes[edge[1]]['x'], nodes[edge[1]]['y']
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace],
                   layout=go.Layout(
                       showlegend=False,
                       hovermode='closest',
                       margin=dict(b=0, l=0, r=0, t=0),
                       xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       plot_bgcolor='rgba(0,0,0,0)',
                       paper_bgcolor='rgba(0,0,0,0)',
                       width=600,
                       height=400
                   ))
    
    return fig 