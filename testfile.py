from py2neo import Graph
import wikipedia


user = "neo4j"
pswd = "0asNuYzn5LVJTyWfb3pJzbqwnkAT3x7HIIWF3WmbDi8"

# Make sure the database is started first, otherwise attempt to connect will fail
try:
    graph = Graph('neo4j+s://fea93aac.databases.neo4j.io', auth=(user, pswd))
    print('SUCCESS: Connected to the Neo4j Database.')
except Exception as e:
    print('ERROR: Could not connect to the Neo4j Database. See console for details.')
    raise SystemExit(e)

movies = graph.run("""MATCH (:Movie {title:"Iron Man 3"})<-[:Directed|Acted_in]-(p)-[:Directed|Acted_in]->(m) RETURN distinct(m)""").data()
for title in movies:
    print(title)