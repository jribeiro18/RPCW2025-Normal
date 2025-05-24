import json
from pathlib import Path
from rdflib import Graph, Namespace, URIRef, RDF, Literal, XSD
from rdflib.namespace import OWL
from collections import defaultdict

def carregar_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def uri(name):
    return name.strip().replace(" ", "_").replace(",", "").replace(".", "")

if __name__ == "__main__":
    n = Namespace("http://www.semanticweb.org/rpcw.di.uminho.pt/2025/2025/sapientia#")
    g = Graph()
    g.parse("sapientia_base.ttl", format="turtle")

    conceitos = carregar_json("conceitos.json")["conceitos"]
    disciplinas = carregar_json("disciplinas.json")["disciplinas"]
    mestres = carregar_json("mestres.json")["mestres"]
    obras = carregar_json("obras.json")["obras"]
    aprendizes = carregar_json("pg57565.json")

    # Conceitos
    for c in conceitos:
        cid = URIRef(n + uri(c["nome"]))
        g.add((cid, RDF.type, n.Conceito))
        g.add((cid, n.nome, Literal(c["nome"])))
        if "períodoHistórico" in c:
            phid = URIRef(n + uri(c["períodoHistórico"]))
            g.add((phid, RDF.type, n.PeríodoHistorico))
            g.add((phid, n.nome, Literal(c["períodoHistórico"])))
            g.add((cid, n.surgeEm, phid))
        for a in c.get("aplicações", []):
            aid = URIRef(n + uri(a))
            g.add((aid, RDF.type, n.Aplicação))
            g.add((aid, n.nome, Literal(a)))
            g.add((cid, n.temAplicaçãoEm, aid))
        for r in c.get("conceitosRelacionados", []):
            rid = URIRef(n + uri(r))
            g.add((rid, RDF.type, n.Conceito))
            g.add((rid, n.nome, Literal(r)))
            g.add((cid, n.estáRelacionadoCom, rid))

    # Disciplinas
    for d in disciplinas:
        did = URIRef(n + uri(d["nome"]))
        g.add((did, RDF.type, n.Disciplina))
        g.add((did, n.nome, Literal(d["nome"])))
        for tk in d.get("tiposDeConhecimento", []):
            tkid = URIRef(n + uri(tk))
            g.add((tkid, RDF.type, n.TipoDeConhecimento))
            g.add((tkid, n.nome, Literal(tk)))
            g.add((did, n.pertenceA, tkid))
        for c in d.get("conceitos", []):
            cid = URIRef(n + uri(c))
            g.add((cid, RDF.type, n.Conceito))
            g.add((cid, n.nome, Literal(c)))
            g.add((cid, n.éEstudadoEm, did))

    # Mestres
    for m in mestres:
        mid = URIRef(n + uri(m["nome"]))
        g.add((mid, RDF.type, n.Mestre))
        g.add((mid, n.nome, Literal(m["nome"])))
    
        phid = URIRef(n + uri(m["períodoHistórico"]))
        g.add((phid, RDF.type, n.PeríodoHistorico))
        g.add((phid, n.nome, Literal(m["períodoHistórico"])))
        g.add((mid, n.temPeriodoHistorico, phid))  # <-- associação do mestre ao período
    
        for d in m.get("disciplinas", []):
            did = URIRef(n + uri(d))
            g.add((did, RDF.type, n.Disciplina))
            g.add((did, n.nome, Literal(d)))
            g.add((mid, n.ensina, did))


    # Obras
    for o in obras:
        oid = URIRef(n + uri(o["titulo"]))
        g.add((oid, RDF.type, n.Obra))
        g.add((oid, n.titulo, Literal(o["titulo"])))
        mid = URIRef(n + uri(o["autor"]))
        g.add((oid, n.foiEscritoPor, mid))
        for c in o.get("conceitos", []):
            cid = URIRef(n + uri(c))
            g.add((cid, RDF.type, n.Conceito))
            g.add((cid, n.nome, Literal(c)))
            g.add((oid, n.explica, cid))

    # Aprendizes
    for a in aprendizes:
        aid = URIRef(n + uri(a["nome"]))
        g.add((aid, RDF.type, n.Aprendiz))
        g.add((aid, n.nome, Literal(a["nome"])))
        g.add((aid, n.idade, Literal(a["idade"], datatype=XSD.integer)))
        for d in a.get("disciplinas", []):
            did = URIRef(n + uri(d))
            g.add((did, RDF.type, n.Disciplina))
            g.add((did, n.nome, Literal(d)))
            g.add((aid, n.aprende, did))

    # Serializar com ordenação e agrupamento visual
    ttl = g.serialize(format="turtle")
    with open("sapientia_ind.ttl", "w", encoding="utf-8") as f:
        f.write(ttl)

    print("Ficheiro sapientia_final.ttl gerado com sucesso.")
