from neo4j import GraphDatabase, basic_auth

URI="bolt://localhost:7687"
USER_NAME = "neo4j"
PASSWORD = "0000"

driver = GraphDatabase.driver(
    # bolt protocol로 내 DB의 IP에 BOLT_PORT로 접근하고 
    uri=f"{URI}", 
    # 주어진 USER_ID와 패스워드로 들어감.
    
    auth=basic_auth(
        user=USER_NAME, 
        password=PASSWORD)
    )

def run_query_extraction(input_query):
    data=[]
    with driver.session() as session:
        for record in session.run(input_query):
            data.append(record)
        
        return data
def run_query(input_query):
    with driver.session() as session:
        session.run(input_query)