from generate_nodes import Node
from queue import Queue
import timeit
import networkx as nx
import matplotlib.pyplot as plt


G_dfs = nx.Graph()

initial_state = [3, 3, 0]
def dfs(initial_state):
    i_node = Node(None, initial_state)
    if i_node.goal_test():
        return i_node.find_path()

    visited = []
    s = []
    s.append(i_node)
    while s:
        node = s.pop()
        if node.state not in visited:
            visited.append(node.state)

        G_dfs.add_node(str(node.state), color='Killed Node')

        if node.parent:
            G_dfs.add_edge(str(node.parent.state), str(node.state))

        if not node.is_killed():
            G_dfs.nodes[str(node.state)]['color'] = 'Traversed Node'
            children = node.generate_child()
            for child in children:
                if child.state not in visited:
                    if child.goal_test():
                        G_dfs.add_node(str(child.state), color='Goal Node')
                        G_dfs.add_edge(str(child.parent.state), str(child.state))
                        # print("returned")
                        return child.find_path()

                    else:
                        # print(f"{node.state} is not a goal state")
                        visited.append(child.state)
                        s.append(child)
    return None

dfs_start = timeit.default_timer()
b= dfs(initial_state)
dfs_end = timeit.default_timer()
dfs_total_time =  dfs_end-dfs_start
print(dfs_total_time)

x=dfs(initial_state)
x.reverse()
print(f"Total Time taken for traversal using dfs algorithm is: {dfs_total_time}")
print(f"Required traversal solution is:{x}")

def optimize_graph(G):
    e = list(G.edges)
    for i in range(len(e)-1):
        for j in range(i+1, len(e)-1):
            if e[i][1] == e[j][1]:
                if G.has_edge(e[j][0], e[j][1]):
                    G.remove_edge(e[j][0], e[j][1])
    return G


G_dfs_optimized = optimize_graph(G_dfs)


# determining nodes position for hierarchial structure
def nodes_pos(G, root, width=1, vert_gap=0.1, vert_pos=0, xcenter=0, pos=None, parent=None):
    if pos is None:
        pos = {root: (xcenter, vert_pos)}
    else:
        pos[root] = (xcenter, vert_pos)

    children = list(G.neighbors(root))

    if parent is not None:
        children.remove(parent)

    if len(children) != 0:
        if len(children) == 4:
            width = 0.1
        if len(children) == 3:
            width = 1
        else:
            width = len(children) / 2
        dx = width / len(children)
        nextx = xcenter - width / 2 - dx / 2
        for child in children:
            nextx += dx
            pos = nodes_pos(G, child, width=dx, vert_gap=vert_gap,
                            vert_pos=vert_pos - vert_gap, xcenter=nextx,
                            pos=pos, parent=root)
    return pos

#defining the color dictionary
color_dict = {'Killed Node':'r','Traversed Node':'c', 'Goal Node':'y'}

#coloring dfs_tree nodes
dfs_pos = nodes_pos(G_dfs_optimized,str(initial_state))
dfs_color_list = [color_dict[i[1]] for i in G_dfs_optimized.nodes.data('color')]
plt.title("State Space Generation and Traversal using Depth First Search Algorithm")
nx.draw(G_dfs_optimized, pos=dfs_pos,node_color=dfs_color_list, with_labels=True, font_size= 16, font_weight='bold')
plt.savefig('dfs_tree.png')
plt.show()


