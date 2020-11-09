# Compare info tables
"match (n:Game)-[:INFO]->(info:Info)-[*]-(connected) return n,info, connected"
# Compare valoraciones
"match (n:Game)-[:has_scores]->(scores:Scores)-[*]-(connected) return n,scores, connected"
# Get commentaries
"match (n:Game)-[:has_commentaries]->(comments:Commentaries)-[*]-(connected) return n, comments, connected"
# Get all languages
"match (n:Game)-[:has_languages]->(language:Language)-[*]-(connected) return n, language, connected"
# Get licencias

# Get SM comparison

# Table comparisons