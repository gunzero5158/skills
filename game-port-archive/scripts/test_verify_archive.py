import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from verify_archive import audit


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.management = self.root / '_归档记录/当前管理记录'
        self.management.mkdir(parents=True)
        (self.root / 'Game').mkdir()
        (self.root / 'Game/run.zip').write_bytes(b'123')
        self.entry = {'file': 'run.zip', 'bytes': 3, 'sha256': hashlib.sha256(b'123').hexdigest()}
        self.record = {'repository': 'owner/game', 'commit': 'a'*40, 'downloads': [self.entry]}
        self.save()

    def save(self):
        def put(p, j):
            p.write_text(json.dumps(j), encoding='utf8')
        put(self.root / 'Game/项目记录.json', self.record)
        put(self.management / 'manifest.json', [self.record])
        put(self.management / '校验结果.json', {'archives': [dict(self.entry, file='Game/run.zip')]})
        (self.root / '下载文件SHA256.csv').write_text('file,bytes,sha256\nGame/run.zip,3,'+self.entry['sha256']+'\n', encoding='utf8')

    def test_valid_and_read_only(self):
        before = {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertTrue(audit(self.root)['ok'])
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_same_size_corruption(self):
        (self.root / 'Game/run.zip').write_bytes(b'456')
        self.assertFalse(audit(self.root)['ok'])

    def test_stale_central(self):
        p = self.management / '校验结果.json'
        j = json.loads(p.read_text()); j['archives'][0]['sha256'] = '0'*64
        p.write_text(json.dumps(j))
        self.assertFalse(audit(self.root)['ok'])

    def test_source_commit_conflict(self):
        (self.root / 'Game/源码.zip').write_bytes(b'123')
        self.entry.update(file='源码.zip', commit='b'*40)
        self.save()
        self.assertTrue(any('source commit conflict' in e for e in audit(self.root)['errors']))

    def test_cloud_duplicate_and_missing_hash(self):
        p = self.root / 'cloud.json'
        p.write_text(json.dumps([{'Path':'Game/run.zip','Size':3}]*2))
        errors = audit(self.root, p)['errors']
        self.assertIn('duplicate cloud paths', errors)
        self.assertTrue(any('unavailable' in e for e in errors))


if __name__ == '__main__':
    unittest.main()
