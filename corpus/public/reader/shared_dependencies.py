"""Apply reviewed shared-proof relationships without changing proof or Lean scope."""
import json
from pathlib import Path


def apply_shared_dependencies(content, directory):
    path = Path(directory) / 'shared-dependencies.json'
    reviewed = json.loads(path.read_text())['results']
    for result in content['results']:
        dependencies = reviewed.get(result['id'])
        if dependencies is None:
            continue
        result['shared_proof_ids'] = [entry['id'] for entry in dependencies]
        result.pop('shared_proof_dependencies', None)
        result['translations']['en'].pop('shared_proof_dependencies', None)
        result['paper_adaptation_md'] = '\n\n'.join(
            entry['scope_md'] for entry in dependencies
        )
        result['translations']['en']['paper_adaptation_md'] = '\n\n'.join(
            entry['scope_en_md'] for entry in dependencies
        )
    return content
