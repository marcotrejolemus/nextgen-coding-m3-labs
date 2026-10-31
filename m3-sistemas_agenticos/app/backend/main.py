"""Punto de entrada de la API de gestión de empleados."""
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from database import Base, engine
from rutas_empleados import router as router_empleados

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gestión de empleados")


def _mensaje_error_validacion(errores: list[dict]) -> str:
    primero = errores[0]
    mensaje = primero["msg"]
    if mensaje.startswith("Value error, "):
        return mensaje[len("Value error, "):]
    campo = primero["loc"][-1] if primero["loc"] else "campo"
    return f"Revisa el campo '{campo}'"


@app.exception_handler(RequestValidationError)
async def manejar_error_validacion(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"detail": _mensaje_error_validacion(exc.errors())},
    )


@app.get("/api/salud")
def salud() -> dict[str, str]:
    return {"estado": "ok"}


app.include_router(router_empleados, prefix="/api")
