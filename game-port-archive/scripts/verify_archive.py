"""Read-only archive gate. Prints JSON; exit 1 means failed/incomplete verification."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

VERSION = '1.1.0'


def audit(root, cloud=None):
    root = Path(root).resolve()
    errors, hashes, expected = [], {}, {}

    def fail(message):
        errors.append(message)

    def read(path):
        return json.loads(path.read_text(encoding='utf-8-sig'))

    def resolve(name):
        p = (root / name.replace('\\', '/')).resolve()
        if not p.is_relative_to(root) or p == root:
            raise ValueError('path escapes archive: ' + name)
        return p

    def check(entry, prefix=''):
        p = resolve(prefix + entry['file'])
        key = p.relative_to(root).as_posix()
        if not p.is_file():
            fail('missing: ' + key)
            return key
        if key not in hashes:
            h = hashlib.sha256()
            with p.open('rb') as f:
                for block in iter(lambda: f.read(4 * 1024 * 1024), b''):
                    h.update(block)
            hashes[key] = h.hexdigest()
        if not entry.get('sha256') or hashes[key] != entry['sha256'].lower():
            fail('SHA256 mismatch/missing: ' + key)
        if int(entry.get('bytes', -1)) != p.stat().st_size:
            fail('size mismatch/missing: ' + key)
        return key

    management = root / '_归档记录/当前管理记录'
    central = read(management / '校验结果.json')['archives']
    central_keys = [check(e) for e in central]
    if len(central_keys) != len(set(central_keys)):
        fail('duplicate central paths')
    manifest = read(management / 'manifest.json')
    repos = [j['repository'] for j in manifest]
    if len(repos) != len(set(repos)):
        fail('duplicate manifest repositories')
    indexed = {j['repository']: j for j in manifest}
    project_repos = []
    for record in sorted(root.glob('*/项目记录.json')):
        j = read(record)
        repo = j['repository']
        project_repos.append(repo)
        other = indexed.get(repo, {})
        for key in ('commit', 'runtime_versions', 'downloads'):
            if j.get(key) != other.get(key):
                fail('manifest differs: ' + repo + '/' + key)
        for e in j.get('downloads', []):
            key = check(e, record.parent.name + '/')
            expected[key] = e
            if key not in central_keys:
                fail('absent from central index: ' + key)
            if '源码' in e['file'] and e.get('commit'):
                if e['commit'] != j.get('commit'):
                    fail('source commit conflict: ' + repo)
                if 'codeload.github.com/' in e.get('url', '') and not e['url'].rstrip('/').endswith('/' + e['commit']):
                    fail('source URL commit conflict: ' + repo)
    if sorted(project_repos) != sorted(repos):
        fail('manifest/project repository sets differ')
    csv_path = management / '下载文件SHA256.csv'
    legacy_csv = root / '下载文件SHA256.csv'
    if csv_path.exists() and legacy_csv.exists():
        fail('duplicate current SHA256 CSV locations')
    if not csv_path.exists():
        csv_path = legacy_csv
    with csv_path.open(encoding='utf-8-sig', newline='') as f:
        csv_keys = [check(e) for e in csv.DictReader(f)]
    if sorted(csv_keys) != sorted(central_keys):
        fail('CSV/central path sets differ')
    # A cloud listing represents an explicit managed scope, not permission to delete extras.
    if cloud is not None:
        rows = read(Path(cloud))
        paths = [resolve(x['Path']).relative_to(root).as_posix() for x in rows]
        if len(paths) != len(set(paths)):
            fail('duplicate cloud paths')
        remote = dict(zip(paths, rows))
        for key in central_keys:
            if key not in remote:
                fail('cloud missing managed archive: ' + key)
                continue
            e = remote[key]
            digest = e.get('Hashes', {}).get('sha256') or e.get('Hashes', {}).get('SHA-256')
            if not digest or digest.lower() != hashes.get(key):
                fail('cloud SHA256 mismatch/unavailable: ' + key)
            p = resolve(key)
            if not p.is_file() or e.get('Size') != p.stat().st_size:
                fail('cloud size mismatch: ' + key)
    return {'version': VERSION, 'ok': not errors, 'projects': len(project_repos),
            'archives': len(central_keys), 'errors': errors,
            'scope': 'current records and indexed archives only; no game execution, submodule proof, document-link or full-tree cloud verification'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('--cloud-listing', type=Path, help='rclone lsjson --recursive --files-only --hash JSON')
    args = parser.parse_args()
    try:
        result = audit(args.root, args.cloud_listing)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        result = {'version': VERSION, 'ok': False, 'errors': [str(exc)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['ok'] else 1)


if __name__ == '__main__':
    main()
