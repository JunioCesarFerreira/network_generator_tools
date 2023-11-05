import os
import re
import json
import networkx as nx

# Ferramenta para análise de relações entre tabelas.

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


def extract_table_names(sql_file):
    """Extrai os nomes das tabelas de um arquivo de script SQL"""
    with open(sql_file, 'r', encoding='utf-8') as file:
        content = file.read()

    table_names = re.findall(r'CREATE TABLE\s+(\w+)', content, re.IGNORECASE)
    return table_names


def extract_foreign_keys(sql_file, table_name):
    """Extrai as chaves estrangeiras de uma tabela em um arquivo de script SQL"""
    foreign_keys = []
    on_table = False

    with open(sql_file, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('CREATE TABLE'):
                current_table = line.split()[2].strip()
                if current_table == table_name:
                    on_table = True
                else:
                    on_table = False

            if on_table:
                match = re.search(r'FOREIGN KEY.*?REFERENCES\s+(\w+)', line, re.IGNORECASE)
                if match:
                    foreign_key = match.group(1)
                    foreign_keys.append(foreign_key)

    return foreign_keys


def create_relationships(sql_files):
    """Cria os relacionamentos entre as tabelas com base nas chaves estrangeiras nos arquivos de script SQL"""
    relationships = set()
    nodes = []

    for file in sql_files:
        table_names = extract_table_names(file)
        nodes.append(table_names)

        for table_name in table_names:
            foreign_keys = extract_foreign_keys(file, table_name)
            print('table:', table_name)
            print('\tforeign keys:', foreign_keys)

            for foreign_key in foreign_keys:
                relationship = (table_name, foreign_key)
                relationships.add(relationship)

    return nodes, relationships
    

if __name__ == '__main__':
    sql_folder = '.' # Diretório onde estão os scripts a serem analisados
    
    sql_files = [os.path.join(sql_folder, file) for file in os.listdir(sql_folder) if file.endswith('.sql')]

    nodes, relationships = create_relationships(sql_files)

    G = nx.DiGraph()

    for node in nodes:
        G.add_nodes_from(node)
    G.add_edges_from(relationships)

    print('\nNumber of nodes:', G.number_of_nodes(),'\n')
    for pair in nx.degree(G):
        print(pair[0],':', pair[1])
        
    G = format_graph(G)

    convert_and_save(G, 'table_relations.json')
