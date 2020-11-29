# Example queries

# Compare info tables
"match (n:Game)-[:HAS_INFO]->(info:Infos)-[*]-(connected) return n,info, connected"
# Compare valoraciones
"match (n:Game)-[:HAS_SCORES]->(scores:Scores)-[*]-(connected) return n,scores, connected"
# Get commentaries
"match (n:Game)-[:HAS_COMMENTARIES]->(comments:Commentaries)-[*]-(connected) return n, comments, connected"
# Get all languages (Audio and Interface info included)
"match (n:Game)-[:HAS_LANGUAGES]->(Languages)-[:IN]-(l:Language)-[:HAS]-(t) return l.name, t.name"
# Release dates
"match (g:Game)-[:RELEASED]->(d:Date) return g.name, d.name"
# Get licencias (show Nos y etc)
'''
MATCH (g:Game),
		(g)-[r1:LICENSES]->(l:Licenses)-[r2]-(s)-[r3]-(c:Country)-[r4]-(s3)
WHERE type(r4) = "LICENSED" OR type(r4) = "REAL_PLAYERS"
RETURN g.name as game,
		c.name as Country,
        type(r4) as rel,
        s3.name as licencia
'''
# PES COuntries that have no licenses
'''
MATCH (g:Game),
		(g)-[r1:LICENSES]->(l:Licenses)-[r2]-(s)-[r3]-(c:Country)-[r4]-(s3)
WHERE g.name = "eFootball PES 2020" and s3.name = "No"
RETURN g.name as game,
        c.name as Country
'''
# Pes Competitions licenses
'''
MATCH (g:Game),
		(g)-[r1:LICENSES]->(l:Licenses)-[r2]-(s)-[r3]-(c:Country)-[r4]-(s3)-[r5]-(s4)
WHERE g.name = "eFootball PES 2020" and type(r4) = "ITEM"
RETURN g.name as game,
        c.name as Country,
        s3.name as Competition,
        s4.name as License
'''
# Get SM comparison
'''
MATCH (g:Game),
		(g)-[r1]->(sm:SM)-[r2]-(s)
RETURN g.name as game,
		sm.name as social_media,
		type(r2) as rel,
		s.name as number
              '''

# Table comparisons

# Number of languages per game
'''
MATCH (g:Game)
RETURN g.name as game, 
       size((g)-[:HAS_LANGUAGES]->(:Languages)-[*]-(:Language)) as languages
ORDER BY languages DESC
LIMIT 5
'''

# Number of licenses per game
'''
MATCH (g:Game)
RETURN g.name as game, 
       size((g)-[:LICENSES]->(:Licenses)-[*]-()) as licencias
ORDER BY licencias DESC
LIMIT 5
'''

# All scores by game
'''
match (g:Game),
		(g)-[:HAS_SCORES]->(:Scores)-[r]-(s:Score)
return g.name as game,
		type(r) as review,
        s.name as score
order by review
'''

# Info table 
'''
match (g:Game),
		(g)-[:HAS_INFO]->(:Infos)-[r]-(s)
return g.name as game,
		type(r) as rel,
        s.name as str
'''