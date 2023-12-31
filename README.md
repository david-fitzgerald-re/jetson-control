# Description

# Requirements

- `node` - `v18.19.0`
- `python` - `3.11`

# Quickstart

To install backend requirements:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To install frontend requirements:

```bash
npm install
```

To run the backend application:

```bash
python backend/app.py
```

To run the frontend application:

```bash
npm run dev -- --open
```

To update required properties from `config-manager`:

```bash
docker exec -it config-manager bash
/app/entrypoint.sh
```