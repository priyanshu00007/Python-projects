import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import networkx as nx
import plotly.graph_objects as go

class BSTVisualizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Binary Search Tree Visualizer")

        # Create a binary search tree
        self.G = nx.DiGraph()
        self.G.add_edge(8, 3)
        self.G.add_edge(8, 10)
        self.G.add_edge(3, 1)
        self.G.add_edge(3, 6)
        self.G.add_edge(10, 14)
        self.G.add_edge(10, 13)

        # Define node positions (3D)
        self.pos = {
            8: (0, 0, 0),
            3: (-2, -1, 0),
            10: (2, -1, 0),
            1: (-3, -2, 0),
            6: (-1, -2, 0),
            14: (3, -2, 0),
            13: (1, -2, 0)
        }

        # Create 3D graph
        self.fig = Figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.draw_3d_graph()

        # Create Tkinter canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        # Create 2D graph button
        self.button = tk.Button(self.root, text="2D Graph", command=self.draw_2d_graph)
        self.button.pack()

        # Create Plotly 3D graph button
        self.plotly_button = tk.Button(self.root, text="Plotly 3D Graph", command=self.plotly_3d_graph)
        self.plotly_button.pack()

    def draw_3d_graph(self):
        self.ax.clear()
        self.ax.set_title('Binary Search Tree (3D)')
        nx.draw_networkx(self.G, self.pos, ax=self.ax, node_size=500, node_color='lightblue')

    def draw_2d_graph(self):
        self.ax.clear()
        self.ax.set_title('Binary Search Tree (2D)')
        pos_2d = {node: (x, y) for node, (x, y, z) in self.pos.items()}
        nx.draw_networkx(self.G, pos_2d, ax=self.ax, node_size=500, node_color='lightblue')

    def plotly_3d_graph(self):
        node_x = [self.pos[node][0] for node in self.G.nodes]
        node_y = [self.pos[node][1] for node in self.G.nodes]
        node_z = [self.pos[node][2] for node in self.G.nodes]

        edge_x = []
        edge_y = []
        edge_z = []
        for edge in self.G.edges:
            source, target = edge
            edge_x.extend([self.pos[source][0], self.pos[target][0], None])
            edge_y.extend([self.pos[source][1], self.pos[target][1], None])
            edge_z.extend([self.pos[source][2], self.pos[target][2], None])

        fig = go.Figure(data=[go.Scatter3d(
            x=edge_x,
            y=edge_y,
            z=edge_z,
            mode='lines',
            line=dict(colorscale=[[0, 'rgba(225,225,225,0.3)'], [1, 'rgba(225,225,225,0.3)']],
                      color=['rgba(225,225,225,0.3)']),
            hoverinfo='none'
        )])

        fig.add_trace(go.Scatter3d(
            x=node_x,
            y=node_y,
            z=node_z,
            mode='markers',
            hoverinfo='text',
            hovertext=list(self.G.nodes),
            marker=dict(size=10)
        ))

        fig.update_layout(
            showlegend=False,
            hovermode='x',
            scene=dict(
                xaxis=dict(nticks=4, range=[-4, 4]),
                yaxis=dict(nticks=4, range=[-4, 4]),
                zaxis=dict(nticks=4, range=[-4, 4])
            ),
            title='Binary Search Tree (Plotly 3D)',
            width=800,
            height=800
        )

        fig.show()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    visualizer = BSTVisualizer()
    visualizer.run()