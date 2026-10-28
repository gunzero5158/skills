"""Read-only archive/PE inspection; verified lossless ZIP packing. Standard library only."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import struct
import zipfile

MACHINES = {0x14C: 'x86 (32位)', 0x8664: 'x64 (64位)', 0xAA64: 'ARM64'}

def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def pe(stream):
    start = stream.read(64)
    if len(start) < 64 or start[:2] != b'MZ':
        return None
    offset = struct.unpack_from('<I', start, 60)[0]
    if offset > 4 * 1024 * 1024:
        return {'error': 'PE offset exceeds inspection bound'}
    stream.seek(offset)
    signature = stream.read(6)
    if len(signature) != 6 or signature[:4] != b'PE\0\0':
        return None
    machine = struct.unpack_from('<H', signature, 4)[0]
    return {'machine': hex(machine), 'architecture': MACHINES.get(machine, 'unknown')}

def inspect(path, crc=False):
    path = Path(path).resolve()
    result = {'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)}
    with path.open('rb') as f:
        magic = f.read(8)
    if zipfile.is_zipfile(path):
        result['format'] = 'PE executable with appended ZIP' if magic[:2] == b'MZ' else 'ZIP'
        if magic[:2] == b'MZ':
            with path.open('rb') as f:
                result['outer_PE'] = pe(f)
        with zipfile.ZipFile(path) as z:
            result['members'] = len(z.infolist())
            result['sample_paths'] = z.namelist()[:30]
            if crc:
                bad = z.testzip()
                if bad:
                    raise ValueError('CRC failure: ' + bad)
                result['crc'] = 'passed'
            result['PE'] = []
            for name in z.namelist():
                if name.lower().endswith(('.exe', '.dll')):
                    with z.open(name) as f:
                        info = pe(f)
                    if info:
                        result['PE'].append({'entry': name, **info})
            result['lfs_pointer_candidates'] = []
            for item in z.infolist():
                if not item.is_dir() and item.file_size <= 1024:
                    if z.read(item).startswith(b'version https://git-lfs.github.com/spec/v1'):
                        result['lfs_pointer_candidates'].append(item.filename)
    elif magic.startswith(b'Rar!\x1a\x07'):
        result['format'] = 'RAR5' if magic[6:7] == b'\x01' else 'RAR'
    elif magic[:2] == b'MZ':
        result['format'] = 'PE/executable'
        with path.open('rb') as f:
            result['PE'] = pe(f)
    elif magic[:4] == b'\x00asm':
        result['format'] = 'WebAssembly'
    else:
        result['format'] = 'unrecognized; use an appropriate archive reader'
    return result

def pack(source, output, prefix='source'):
    source, output = Path(source).resolve(), Path(output).resolve()
    if not source.is_dir() or output.is_relative_to(source):
        raise ValueError('Input must be a directory; output must be outside it')
    if output.exists():
        raise FileExistsError(output)
    prefix = prefix.replace('\\', '/').strip('/')
    if '..' in PurePosixPath(prefix).parts:
        raise ValueError('Unsafe prefix')
    temporary = output.with_name(output.name + '.part')
    if temporary.exists():
        raise FileExistsError('Review incomplete output: ' + str(temporary))
    output.parent.mkdir(parents=True, exist_ok=True)
    files, empty = [], []
    for base, dirs, names in os.walk(source, followlinks=False):
        base = Path(base)
        for name in dirs + names:
            if (base / name).is_symlink():
                raise ValueError('Review symlink: ' + str(base / name))
        if not dirs and not names:
            empty.append(base)
        files.extend(base / name for name in names)
    if not files:
        raise ValueError('No input files')
    def arc(path):
        return (prefix + '/' if prefix else '') + path.relative_to(source).as_posix()
    manifest = {}
    with zipfile.ZipFile(temporary, 'w', zipfile.ZIP_DEFLATED, compresslevel=6, allowZip64=True) as z:
        for path in sorted(files):
            manifest[arc(path)] = {'bytes': path.stat().st_size, 'sha256': digest(path)}
            z.write(path, arc(path))
        for path in empty:
            name = arc(path).rstrip('/') + '/'
            if name not in ('./', '/'):
                z.writestr(name, b'')
        z.writestr('归档校验/文件SHA256.json', json.dumps(manifest, ensure_ascii=False, separators=(',', ':')))
    with zipfile.ZipFile(temporary) as z:
        for name, expected in manifest.items():
            h = hashlib.sha256()
            with z.open(name) as f:
                for chunk in iter(lambda: f.read(1024 * 1024), b''):
                    h.update(chunk)
            if z.getinfo(name).file_size != expected['bytes'] or h.hexdigest() != expected['sha256']:
                raise ValueError('Preservation failure: ' + name)
        if json.loads(z.read('归档校验/文件SHA256.json')) != manifest:
            raise ValueError('Internal manifest mismatch')
    os.replace(temporary, output)
    record = {'archive': output.name, 'source_directory': str(source), 'files': len(files),
              'empty_directories': len(empty), 'original_bytes': sum(x['bytes'] for x in manifest.values()),
              'bytes': output.stat().st_size, 'sha256': digest(output),
              'validation': 'all original files read back with matching SHA256 and CRC; no inputs deleted'}
    output.with_name(output.name + '.校验.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    return record

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    ins = commands.add_parser('inspect'); ins.add_argument('path'); ins.add_argument('--crc', action='store_true')
    pkg = commands.add_parser('pack'); pkg.add_argument('source'); pkg.add_argument('output'); pkg.add_argument('--prefix', default='source')
    args = parser.parse_args()
    result = inspect(args.path, args.crc) if args.command == 'inspect' else pack(args.source, args.output, args.prefix)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
