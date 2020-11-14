# Compare info tables
"match (n:Game)-[:INFO]->(info:Info)-[*]-(connected) return n,info, connected"
# Compare valoraciones
"match (n:Game)-[:has_scores]->(scores:Scores)-[*]-(connected) return n,scores, connected"
# Get commentaries
"match (n:Game)-[:has_commentaries]->(comments:Commentaries)-[*]-(connected) return n, comments, connected"
# Get all languages
"match (n:Game)-[:has_languages]->(language:Language)-[*]-(connected) return n, language, connected"
# Release dates
"match (g:Game) return g.name as game, (g)-[:released]->(:Date) as release"
# Get licencias (show Nos y etc)
'''
MATCH (g:Game),
		(g)-[r1:licenses]->(l:Licencias)-[r2]-(s)-[r3]-(s2)-[r4]-(s3)
RETURN g.name as game,
		s.name as tipo,
        s2.name as item,
        type(r4) as rel,
        s3.name as licencia
'''
'''
MATCH (g:Game),
		(g)-[r1:licenses]->(l:Licencias)-[r2]-(s)-[r3]-(s2)-[r4]-(s3)
WHERE g.name = "eFootball PES 2020" and s3.name = "4"
RETURN g.name as game,
		s.name as tipo,
        s2.name as item,
        type(r4) as rel,
        s3.name as licencia
order by licencia
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
       size((g)-[:has_languages]->(:Language)-[*]-()) as languages
ORDER BY languages DESC
LIMIT 5
'''

# All lanuages add ons
'''
MATCH (g:Game),
		(g)-[:has_languages]->(:Language)-[:in]-(lang:Language)-[:has]-(s)
RETURN g.name as game, 
		lang.name as language,
       s.name as language_add
ORDER BY lang DESC
'''

# Number of licenses per game
'''
MATCH (g:Game)
RETURN g.name as game, 
       size((g)-[:licenses]->(:Licencias)-[*]-()) as licencias
ORDER BY licencias DESC
LIMIT 5
'''

# All scores by game
'''
match (g:Game),
		(g)-[:has_scores]->(:Scores)-[r]-(s:Score)
return g.name as game,
		type(r) as review,
        s.name as score
order by review
'''

# Info table 
'''
match (g:Game),
		(g)-[:INFO]->(:Info)-[r]-(s)
return g.name as game,
		type(r) as rel,
        s.name as str
'''