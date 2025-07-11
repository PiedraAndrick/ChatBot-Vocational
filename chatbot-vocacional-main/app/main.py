from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from app.routes.chat import chat
from app.routes.preguntas import pregunta
from app.routes.respuestas import respuesta
from app.routes.auth import auth
from app.middlewares.validate import validate_request_body, dispatch
#INICIAR LA APLICACION
app = FastAPI(docs_url=None, redoc_url=None)#Configuraciones seguras por defecto:

# Middleware para redirigir todas las solicitudes HTTP a HTTPS
#app.add_middleware(HTTPSRedirectMiddleware)

# Registrar el middleware
@app.middleware("http")
async def validate_request_body_middleware(request: Request, call_next):
    return await validate_request_body(request, call_next)

@app.middleware("http")
async def SQLInjectionMiddleware(request: Request, call_next):
    return await dispatch(request, call_next)

# Middleware para añadir headers de seguridad
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'"
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=()'
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Permite todas las origins
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)




#INCLUIR LAS RUTAS
app.include_router(chat,prefix="/api")
app.include_router(pregunta,prefix="/api")
app.include_router(respuesta,prefix="/api")
app.include_router(auth,prefix="/api")
