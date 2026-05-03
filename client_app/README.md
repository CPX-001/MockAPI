# Service Desk

App cliente de ejemplo. Es independiente del backend: solo necesita una API HTTP
configurada con `CLIENT_API_BASE_URL`.

## Arrancar

```bash
CLIENT_API_BASE_URL=http://127.0.0.1:8000/api \
python3 -m uvicorn client_app.main:app --reload --port 8010
```

Abre:

```text
http://127.0.0.1:8010
```

## Contrato esperado

La app llama a estos endpoints:

- `GET /tickets`
- `POST /tickets`
- `GET /tickets/{id}`
- `PUT /tickets/{id}`
- `DELETE /tickets/{id}`

Body de crear/editar:

```json
{
  "title": "Error al iniciar sesion",
  "customer": "Acme",
  "priority": "high",
  "status": "open",
  "description": "El usuario recibe un 401."
}
```

La respuesta de `GET /tickets` puede ser una lista directa o un objeto con
`items`, `tickets`, `data` o `results`.
