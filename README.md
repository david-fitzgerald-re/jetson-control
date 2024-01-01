# Receiving Device Updates

Test

## Description

Test

## Requirements

- `node` - `v18.19.0`
- `python` - `3.11`

## Quickstart

TODO - explain how to populate `.env`

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

# Notes

Anecdotadally, it regularly takes about 7 seconds for reported properties to 
get sent from the device through an azure service bus and into this app. It goes
without saying that this time can vary greatly and azure even document this 
themselves. If a device is disconnected we would not receive the reported properties
until the next time the device connects.