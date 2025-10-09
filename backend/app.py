from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from lexer import lexer, lexer_errors
from parser import parser
from interpreter import Interpreter

app = FastAPI()

# Autoriser le frontend React (Vite tourne par défaut sur http://localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/parse", response_class=PlainTextResponse)
async def parse_code(file: Optional[UploadFile] = None, code: str = Form(None)):
    """
    Parse et exécute le code, puis renvoie UNIQUEMENT la sortie des `print`.
    """
    # Charger le code
    if file:
        content = await file.read()
        code = content.decode("utf-8")
    elif not code:
        return PlainTextResponse("No code provided", status_code=400)

    # Reset lexer state
    lexer_errors.clear()
    lexer.lineno = 1

    try:
        # Parser en AST
        ast = parser.parse(code, lexer=lexer)
        if lexer_errors:
            return "\n".join(lexer_errors)

        # Exécuter avec l’interpréteur
        interpreter = Interpreter()
        output = interpreter.run(ast)

        # Retourner la sortie concaténée
        return "\n".join(map(str, output)) if output else ""

    except SyntaxError as e:
        return f"Syntax error: {str(e)}"
