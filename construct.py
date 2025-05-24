from rdflib import Graph, Namespace, RDF, OWL

# Carrega a ontologia
g = Graph()
g.parse("sapientia_ind.ttl", format="turtle")

# Define o namespace da ontologia
n = Namespace("http://www.semanticweb.org/rpcw.di.uminho.pt/2025/2025/sapientia#")

# Declara as propriedades
g.add((n.estudaCom, RDF.type, OWL.ObjectProperty))
g.add((n.estudaCom, RDF.type, OWL.SymmetricProperty))
g.add((n.daBasesPara, RDF.type, OWL.ObjectProperty))

# -----------------------------
# CONSTRUCT para :estudaCom
# -----------------------------
q1 = """
PREFIX : <http://www.semanticweb.org/rpcw.di.uminho.pt/2025/2025/sapientia#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

CONSTRUCT {
  ?aprendiz :estudaCom ?mestre .
}
WHERE {
  ?aprendiz a :Aprendiz ;
            :aprende ?disciplina .

  ?mestre a :Mestre ;
          :ensina ?disciplina .
}
"""

# Executa e adiciona os triplos estudaCom
for triple in g.query(q1):
    g.add(triple)

# -----------------------------
# CONSTRUCT para :daBasesPara
# -----------------------------
q2 = """
PREFIX : <http://www.semanticweb.org/rpcw.di.uminho.pt/2025/2025/sapientia#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

CONSTRUCT {
  ?disciplina :daBasesPara ?aplicacao .
}
WHERE {
  ?conceito :éEstudadoEm ?disciplina ;
            :temAplicaçãoEm ?aplicacao .
}
"""

# Executa e adiciona os triplos daBasesPara
for triple in g.query(q2):
    g.add(triple)

# Serializa o grafo atualizado (para stdout ou ficheiro)
# print(g.serialize(format="turtle"))
# ou para ficheiro:
g.serialize(destination="sapientia_final.ttl", format="turtle")
