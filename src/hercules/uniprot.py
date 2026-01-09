# hercules/uniprot.py
import requests

def fetch_sequence(uniprot_id: str) -> str:
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.fasta"
    r = requests.get(url)
    r.raise_for_status()
    return "".join(r.text.splitlines()[1:])
