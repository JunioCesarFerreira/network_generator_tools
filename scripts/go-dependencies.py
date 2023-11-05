import os
import re
import json
import networkx as nx

def convert_and_save(G, file_name):
    """Converte rede complexa e registra arquivo json"""
    # Formato compatível com visualização no NetViewJS
    data = {
        "nodes": [{"id": n, "label": G.nodes[n]["label"]} for n in G.nodes],
        "links": [{"source": u, "target": v, "weight": w['weight']} for u, v, w in G.edges(data=True)]
    }
    
    # Salvando os dados em um arquivo JSON indentado
    with open(file_name, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def format_graph(G):
    """Formata grafo gerado para padrão utilizado no visualizador NetViewJS"""
    # Novo grafo
    new_graph = nx.DiGraph()
    
    # Mapeamento dos IDs originais para inteiros
    id_mapping = {}

    # Adiciona vértices com os novos IDs
    for new_id, old_id in enumerate(G.nodes()):
        new_graph.add_node(new_id)
        id_mapping[old_id]=new_id

    # Adiciona arestas com os novos IDs
    for old_source, old_target in G.edges():
        new_source = id_mapping[old_source]
        new_target = id_mapping[old_target]
        new_graph.add_edge(new_source, new_target, weight=1)

    # Mapeamento reverso para usar como labels
    label_mapping = {new_id: old_id for old_id, new_id in id_mapping.items()}
    
    # Adicionando labels aos nós no novo grafo
    for new_id, old_id in label_mapping.items():
        new_graph.nodes[new_id]['label'] = old_id
    
    return new_graph

def extract_package_name(file_content):
    package_match = re.search(r'package (\w+)', file_content)
    if package_match:
        return package_match.group(1)
    return None

def find_go_file_dependencies(directory):
    go_files = [os.path.join(root, file) for root, _, files in os.walk(directory) for file in files if file.endswith(".go")]
    
    package_names = {}
    dependencies = {}
    
    for go_file in go_files:
        with open(go_file, 'r', encoding='utf-8') as f:
            content = f.read()
            package_name = extract_package_name(content)
            if package_name:
                package_names[go_file] = package_name
            dependencies[go_file] = set()
    
    for go_file in go_files:
        with open(go_file, 'r', encoding='utf-8') as f:
            content = f.read()
            import_statements = re.findall(r'import \(\n([\s\S]+?)\n\)', content)
            for imports in import_statements:
                referenced_packages = re.findall(r'"([^"]+)"', imports)
                for referenced_package in referenced_packages:
                    for file, package_name in package_names.items():
                        if f'/{package_name}' in referenced_package:
                            dependencies[go_file].add(package_name)
    
    with open('go-dependencies.txt', 'w') as f:
        for go_file_name, dependent_packages in dependencies.items():
            f.write(f'{package_names[go_file_name]} depends on:\n')
            for dependent_package in dependent_packages:
                f.write(f'  - {dependent_package}\n')
               
    G = nx.DiGraph()
    for go_file_name, dependent_packages in dependencies.items():
        for dependent_package in dependent_packages:
            G.add_edge(package_names[go_file_name], dependent_package)

    G = format_graph(G)
    convert_and_save(G, 'go-dependencies.json')

if __name__ == '__main__':
    analysis_directory = '.'  # Diretório do projeto a ser analisado.

    find_go_file_dependencies(analysis_directory)