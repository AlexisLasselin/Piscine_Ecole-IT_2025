from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from lexer import lexer, lexer_errors
from parser import parser, ast_to_dict

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

@app.post("/parse")
async def parse_code(file: Optional[UploadFile] = None, code: str = Form(None)):
    """
    Parse le code soit depuis un fichier uploadé, soit depuis une string envoyée.
    """
    if file:
        content = await file.read()
        code = content.decode("utf-8")
    elif not code:
        return JSONResponse(content={"error": "No code provided"}, status_code=400)

    # Reset lexer state
    lexer_errors.clear()
    lexer.lineno = 1

    try:
        ast = parser.parse(code, lexer=lexer)
        if lexer_errors:
            return {"errors": lexer_errors}
        return ast_to_dict(ast)
    except SyntaxError as e:
        return {"errors": [str(e)]}
