import yaml
import json
import networkx as nx

# Atenção!
# O script deve ser executado no mesmo diretório onde está o arquivo docker-compose.yaml.
# Sua saída será registrada no mesmo diretório.

with open('docker-compose.yaml', 'r') as file:
    # Carregando o conteúdo do YAML para uma estrutura de dados Python
    docker_compose_data = yaml.safe_load(file)

def generate_docker_compose_network(docker_compose_data):
    G = nx.Graph()

    # Criando um dicionário para armazenar quais contêineres estão em quais redes
    network_container_map = {}

    count = 1
    # Preenchendo o dicionário com contêineres e redes
    for service_name, service_details in docker_compose_data['services'].items():
        G.add_node(count, label=service_name)
        for network in service_details.get('networks', []):
            if network not in network_container_map:
                network_container_map[network] = []
            network_container_map[network].append(count)
        count+=1

    # Adicionando os contêineres como nós e conectando-os com base nas redes compartilhadas
    for network, ids in network_container_map.items():
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                if G.has_edge(ids[i], ids[j]):
                    G[ids[i]][ids[j]]['weight']+=1
                else:
                    G.add_edge(ids[i], ids[j], weight=1)
    
    data = {
        "nodes": [{"id": n, "label": G.nodes[n]["label"]} for n in G.nodes],
        "links": [{"source": u, "target": v, "weight": w['weight']} for u, v, w in G.edges(data=True)]
    }
    
    # Salvando os dados em um arquivo JSON indentado
    with open('docker_compose_network.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Chamando a função com os dados do docker-compose para gerar o grafo
generate_docker_compose_network(docker_compose_data)