# Receiving Device Updates

Test

## Description

Test

## Requirements

- `node` - `v18.19.0`
- `python` - `3.11`

## Quickstart

To install backend requirements:

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To install frontend requirements:

```bash
cd frontend
npm install
```

To run the backend application:

```bash
cd backend
python app.py
```

To run the frontend application:

```bash
cd frontend
npm run dev -- --open
```

To update required properties from `config-manager`:

```bash
docker exec -it config-manager bash
/app/entrypoint.sh
```
