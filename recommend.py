import networkx as nx
import random
import matplotlib.pyplot as plt
from db_connect import DatabaseConnector

# MySQL database connection details
host = 'localhost'
username = 'root'
password = ''
database = 'DeMa'
port = '3308'


class recommend():
    def execute():
        # Create an instance of the DatabaseConnector
        db_connector = DatabaseConnector(
            host, username, password, database, port)
        db_connector.connect()

        # Retrieve usernames from the database
        query = "SELECT user_name FROM UserSongs"
        db_connector.execute_query(query)
        results = db_connector.fetchall()
        usernames = [row[0] for row in results]

        # Create an empty graph
        G = nx.Graph()

        # Generate a Barabasi-Albert graph with 100 nodes and preferential attachment parameter of 3
        G = nx.barabasi_albert_graph(len(usernames), 3)

        # Assign usernames as labels to the nodes
        labels = {node: username for node, username in zip(G.nodes, usernames)}
        G = nx.relabel_nodes(G, labels)

        # Function to recommend items to a user based on their known favorites
        def recommend_items(user, num_recommendations):
            user_neighbors = list(G.neighbors(user))

            # Find neighbors of neighbors (2nd degree connections)
            neighbors_of_neighbors = set()
            for neighbor in user_neighbors:
                neighbors_of_neighbors.update(G.neighbors(neighbor))

            # Remove user's direct connections from neighbors of neighbors
            neighbors_of_neighbors -= set(user_neighbors)

            # Calculate the popularity scores of items based on their neighbors
            item_scores = {}
            for item in neighbors_of_neighbors:
                neighbors = set(G.neighbors(item))
                common_neighbors = neighbors.intersection(user_neighbors)
                item_scores[item] = len(common_neighbors)

            # Sort the items based on their popularity scores in descending order
            sorted_items = sorted(item_scores.items(),
                                  key=lambda x: x[1], reverse=True)

            # Select the top recommended items
            recommendations = [item for item,
                               score in sorted_items[:num_recommendations]]

            return recommendations
        helper = ""
        for user in usernames:
            num_recommendations = 2
            flag = 0
            recommendations = recommend_items(user, num_recommendations)
            print(f"Recommended items for {user}:")
            for item in recommendations:
                if flag > 0:
                    name = item
                flag += 1
            query = f"SELECT song_name FROM UserSongs WHERE user_name= '{item}'"
            db_connector.execute_query(query)
            song_to_recommend = db_connector.fetch_one()
            print(type(song_to_recommend))
            query = f'''
        INSERT INTO Recommends (name,song,recommend_from_user) SELECT '{user}',song_name,'{item}' FROM UserSongs
        WHERE user_name = '{item}'
        '''
            # helper = song_to_recommend
            # test = helper.replace("'", "B")
            # query=f"INSERT INTO Recommends (name,song) VALUES ('{user}','{test}')"
            db_connector.execute_query(query)
            db_connector.commit_changes()

        # Plot the graph
        plt.figure(figsize=(10, 6))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='skyblue',
                node_size=300, font_size=8, edge_color='gray', width=0.5)
        plt.title('Barabasi-Albert Graph')
        plt.axis('off')
        plt.show()

        # Disconnect from the database
        db_connector.disconnect()
