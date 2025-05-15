# Contract to Neo4j Integration

This module extracts comprehensive contract information and generates Neo4j Cypher commands for graph database integration.

## Features

The enhanced extraction pipeline extracts and stores:

- Contract metadata (title, type, effective date)
- Parties and signatories
- Articles and sections
- Key legal provisions
- Financial mentions with context
- Key dates with context
- Legal terms with examples
- Named entities (people, organizations, places)

## Graph Schema

The Neo4j graph schema includes the following node types:

- `Contract`: The main contract document node
- `Party`: Contract parties (organizations, individuals)
- `Person`: Signatories who represent parties
- `Article`: Contract articles/sections
- `Section`: Subsections within articles
- `KeyProvision`: Important contract provisions
- `Financial`: Financial amounts mentioned with context
- `Date`: Important dates mentioned with context
- `Term`: Key legal terms with example contexts
- `Entity`: Named entities organized by type (people, organizations, places, etc.)

## Data Presentation

The extracted information is presented in Neo4j using:

- **Tables**: For structured information like contract metadata, articles, etc.
- **Bullet Points**: For lists of entities, term examples, etc.
- **Context Preservation**: Financial amounts, dates, and terms include surrounding context

## Requirements

- Neo4j Database (local or remote)
- Python 3.9 with packages in `requirements-3.9.txt`
- `cypher-shell` for executing the generated commands (included with Neo4j)

## Usage

### Using the Shell Script

```bash
./extract_to_neo4j.sh <json_file> [execute]
```

Arguments:
- `json_file`: Path to the JSON file containing contract data
- `execute`: Optional. If specified, the script will execute the Cypher commands immediately

Examples:
```bash
# Generate Cypher commands only
./extract_to_neo4j.sh data/sample_contract.json

# Generate and execute Cypher commands
./extract_to_neo4j.sh data/sample_contract.json execute
```

### Manually Executing Generated Cypher

```bash
cypher-shell -u neo4j -p your_password -f sample_contract.cypher
```

## Sample Neo4j Queries

After importing your contract data, you can use these Cypher queries:

1. View contract metadata:
```cypher
MATCH (c:Contract {documentId: 'sample_contract'}) RETURN c
```

2. Find all parties in a contract:
```cypher
MATCH (p:Party)-[:PARTY_TO]->(c:Contract {documentId: 'sample_contract'})
RETURN p.name, p.type
```

3. Find key provisions about termination:
```cypher
MATCH (c:Contract)-[:HAS_KEY_PROVISION]->(p:KeyProvision)
WHERE p.title CONTAINS 'termination' OR p.summary CONTAINS 'termination'
RETURN c.title, p.title, p.summary
```

4. Find all financial mentions with context:
```cypher
MATCH (c:Contract)-[:HAS_FINANCIAL]->(f:Financial)
RETURN c.title, f.amount, f.context
```

5. Explore all key dates:
```cypher
MATCH (c:Contract)-[:HAS_DATE]->(d:Date)
RETURN c.title, d.value, d.context
```

6. View all legal terms with examples:
```cypher
MATCH (c:Contract)-[:HAS_TERM]->(t:Term)
RETURN t.name, t.contexts
```

7. Find all named entities by type:
```cypher
MATCH (c:Contract)-[:HAS_ENTITY]->(e:Entity)
RETURN e.type, e.values
```

8. Show contract structure:
```cypher
MATCH (c:Contract {documentId: 'sample_contract'})-[:CONTAINS]->(a:Article)
RETURN c.title, a.number, a.title ORDER BY a.number
```
