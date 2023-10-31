#!/usr/bin/env python3

def preprocess(s:str) -> list:
    s = s.lower().replace(".", "").split()
    stop_words = ["in", "is", "a", "of", "the", "but", "itself", "more", "like", "what", "does"]
    s = [word for word in s if word not in stop_words]
    return s

def make_trie(s:list) -> dict:
    trie = {}
    for word in s:
        node = trie
        for char in word:
            node = node.setdefault(char, {})
            node["is_word"] = False
        node["is_word"] = True
    return trie

def write_trie_to_graphviz(trie, parent='root', graph=None, edge_label='', file=None):
    # Initialize the file if it does not exist
    if file is None:
        file = open('trie.dot', 'w')
        file.write('digraph Trie {\n')
        file.write('    node [shape=circle]\n')  # Set the shape of nodes
        # No invisibility style is applied to the root here

    # Traverse the trie
    for char, next_node in trie.items():
        if char == "is_word":
            continue

        # Create a node identifier by appending the character to the parent identifier
        node_id = (parent if parent else '') + char

        # Define the background color for is_word nodes
        bg_color = 'yellow' if next_node.get("is_word", False) else 'white'

        # Write the node to the file
        file.write(f'    "{node_id}" [label="{char}", style=filled, fillcolor={bg_color}];\n')

        # Write an edge from the parent to the current node without applying invisibility style
        if parent:
            file.write(f'    "{parent}" -> "{node_id}" [label="{edge_label}"];\n')

        # Recursively write the children of the current node to the file
        write_trie_to_graphviz(next_node, node_id, graph, edge_label='', file=file)

    # Only close the file when at the root call to avoid partial writes
    if parent == 'root':
        file.write('}\n')
        file.close()

        # Use the Graphviz command-line tool to convert the .dot file to a PNG file
        import os
        os.system('dot -Tpng trie.dot -o trie.png')

def make_trie_to_tree(trie: dict) -> dict:
    tree = {}
    for char, next_node in trie.items():
        if char == "is_word":
            continue
        tree[char] = make_trie_to_tree(next_node)
    return tree



def main():
    s = "Intelligent behavior in people is a product of the mind. But the mind itself is more like what the human brain does."
    s = preprocess(s)
    s = {'intelligent': {
                'is_word': True
            },
            'b': {
                'is_word': False,
                'ehaviour': {
                'is_word': True
                },
                'rain': {
                'is_word': True
                }
            },
            'p': {
                'is_word': False,
                'eople': {
                'is_word': True
                },
                'roduct': {
                'is_word': True
                }
            },
            'mind': {
                'is_word': True
            },
            'human': {
                'is_word': True
            }
            }
    write_trie_to_graphviz(s)

if __name__ == "__main__":
    main()