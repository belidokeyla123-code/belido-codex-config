#!/usr/bin/env python3
"""mcp-dropbox — MCP Dropbox Keyla com refresh automático (stdlib only, zero dependências)"""
import sys, json, os, base64, io, urllib.request, urllib.parse

# ── Credenciais: env vars primeiro, depois ~/.dropbox-keyla.env ──
APP_KEY = os.environ.get('DROPBOX_APP_KEY')
APP_SECRET = os.environ.get('DROPBOX_APP_SECRET')
REFRESH_TOKEN = os.environ.get('DROPBOX_REFRESH_TOKEN')
ACCESS_TOKEN = os.environ.get('DROPBOX_TOKEN')

if not all([APP_KEY, APP_SECRET, REFRESH_TOKEN]):
    env_path = os.path.expanduser('~/.dropbox-keyla.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith('DROPBOX_APP_KEY='):
                    APP_KEY = APP_KEY or line.split('=', 1)[1]
                elif line.startswith('DROPBOX_APP_SECRET='):
                    APP_SECRET = APP_SECRET or line.split('=', 1)[1]
                elif line.startswith('DROPBOX_REFRESH_TOKEN='):
                    REFRESH_TOKEN = REFRESH_TOKEN or line.split('=', 1)[1]

def refresh_access_token():
    global ACCESS_TOKEN
    data = urllib.parse.urlencode({
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN,
        'client_id': APP_KEY,
        'client_secret': APP_SECRET
    }).encode()
    req = urllib.request.Request(
        'https://api.dropboxapi.com/oauth2/token',
        data=data,
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    resp = urllib.request.urlopen(req)
    body = json.loads(resp.read())
    ACCESS_TOKEN = body['access_token']

def dropbox_api(endpoint, args=None, content=None):
    if not ACCESS_TOKEN:
        refresh_access_token()
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    if content is not None:
        headers['Content-Type'] = 'application/octet-stream'
        headers['Dropbox-API-Arg'] = json.dumps(args)
        data = content
    elif args is not None:
        headers['Content-Type'] = 'application/json'
        data = json.dumps(args).encode()
    else:
        data = b'{}'
        headers['Content-Type'] = 'application/json'
    url = f'https://api.dropboxapi.com/2/{endpoint}'
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        resp = urllib.request.urlopen(req)
        raw = resp.read()
        if content is not None:
            result_arg = resp.headers.get('Dropbox-API-Result', '{}')
            return json.loads(result_arg), raw
        return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        if e.code == 401:
            refresh_access_token()
            headers['Authorization'] = f'Bearer {ACCESS_TOKEN}'
            req = urllib.request.Request(url, data=data, headers=headers)
            resp = urllib.request.urlopen(req)
            raw = resp.read()
            return json.loads(raw) if raw else {}
        raise Exception(f'Dropbox API error {e.code}: {err}')

def send(msg):
    sys.stdout.write(json.dumps(msg) + '\n')
    sys.stdout.flush()

def recv():
    line = sys.stdin.readline()
    return json.loads(line) if line else None

def handle_call(params):
    name = params.get('name')
    args = params.get('arguments', {})
    if not all([APP_KEY, APP_SECRET, REFRESH_TOKEN]):
        return {'content': [{'type': 'text', 'text': 'Dropbox nao configurado (faltam credenciais)'}]}
    try:
        if name == 'list_folder':
            path = args.get('path', '')
            result = dropbox_api('files/list_folder', {'path': path, 'include_deleted': False})
            items = []
            for e in result.get('entries', []):
                tipo = '[PASTA]' if e.get('.tag') == 'folder' else '[ARQUIVO]'
                items.append(f'{tipo} {e["name"]}')
            return {'content': [{'type': 'text', 'text': '\n'.join(items) if items else '(vazia)'}]}

        elif name == 'download':
            path = args['path']
            meta, raw = dropbox_api('files/download', {'path': path}, content=b'')
            local = args.get('local', os.path.basename(path))
            with open(local, 'wb') as f:
                f.write(raw)
            return {'content': [{'type': 'text', 'text': f'Download: {local} ({len(raw)} bytes)'}]}

        elif name == 'upload':
            local = args['local']
            remote = args.get('remote', '/' + os.path.basename(local))
            with open(local, 'rb') as f:
                data = f.read()
            dropbox_api('files/upload', {
                'path': remote, 'mode': {'.tag': 'overwrite'}
            }, content=data)
            return {'content': [{'type': 'text', 'text': f'Upload: {local} -> {remote} ({len(data)} bytes)'}]}

        elif name == 'search':
            query = args['query']
            result = dropbox_api('files/search_v2', {'query': query, 'max_results': 20})
            items = []
            for m in result.get('matches', []):
                meta = m.get('metadata', {}).get('metadata', {})
                items.append(meta.get('name', '?'))
            return {'content': [{'type': 'text', 'text': '\n'.join(items) if items else '(sem resultados)'}]}

        else:
            return {'content': [{'type': 'text', 'text': f'Ferramenta desconhecida: {name}'}]}
    except Exception as e:
        return {'content': [{'type': 'text', 'text': f'Erro: {str(e)}'}]}

TOOLS = [
    {'name': 'list_folder', 'description': 'Listar conteudo de uma pasta no Dropbox', 'inputSchema': {'type': 'object', 'properties': {'path': {'type': 'string', 'description': 'Caminho da pasta (ex: /Public/IA)'}}}},
    {'name': 'download', 'description': 'Baixar arquivo do Dropbox', 'inputSchema': {'type': 'object', 'properties': {'path': {'type': 'string', 'description': 'Caminho remoto'}, 'local': {'type': 'string', 'description': 'Destino local (opcional)'}}, 'required': ['path']}},
    {'name': 'upload', 'description': 'Enviar arquivo para o Dropbox', 'inputSchema': {'type': 'object', 'properties': {'local': {'type': 'string', 'description': 'Arquivo local'}, 'remote': {'type': 'string', 'description': 'Caminho remoto (opcional)'}}, 'required': ['local']}},
    {'name': 'search', 'description': 'Buscar arquivos no Dropbox', 'inputSchema': {'type': 'object', 'properties': {'query': {'type': 'string', 'description': 'Termo de busca'}}, 'required': ['query']}},
]

def main():
    send({'jsonrpc': '2.0', 'method': 'initialized'})
    while True:
        msg = recv()
        if not msg:
            break
        req_id = msg.get('id')
        method = msg.get('method', '')
        if method == 'ping':
            send({'jsonrpc': '2.0', 'id': req_id, 'result': {'status': 'ok'}})
        elif method == 'tools/list':
            send({'jsonrpc': '2.0', 'id': req_id, 'result': {'tools': TOOLS}})
        elif method == 'tools/call':
            result = handle_call(msg.get('params', {}))
            send({'jsonrpc': '2.0', 'id': req_id, 'result': result})
        elif method == 'initialize':
            send({'jsonrpc': '2.0', 'id': req_id, 'result': {'protocolVersion': '2024-11-05', 'capabilities': {'tools': {}}}})
        else:
            send({'jsonrpc': '2.0', 'id': req_id, 'result': {'status': 'ignored'}})

if __name__ == '__main__':
    main()
