from pyswip import Prolog

# Initialize a Prolog instance
prolog = Prolog()

# Consult the Prolog file (load the knowledge base)
prolog.consult("knowledge_base.pl")

# Query the knowledge base
query = "ancestor(alice, Y)"

# Execute the query and print the results
for result in prolog.query(query):
    print(result["Y"])
