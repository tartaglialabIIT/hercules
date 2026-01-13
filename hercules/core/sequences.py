# hercules/sequences.py
import requests

def fetch_sequence(uniprot_id: str) -> str:
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.fasta"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return "".join(r.text.splitlines()[1:])


def fetch_sequences(uniprot_ids):
    return {
        uid: fetch_sequence(uid)
        for uid in uniprot_ids
    }
