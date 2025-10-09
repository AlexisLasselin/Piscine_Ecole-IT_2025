from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import Optional

from lexer import lexer, lexer_errors
from parser import parser
from interpreter import Interpreter

app = FastAPI()

# 🔓 Autoriser le frontend React (Vite tourne sur http://localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Route de test
@app.get("/health")
async def health():
    return {"status": "ok"}

# 📂 Route pour importer un fichier .pisc
@app.post("/parse", response_class=PlainTextResponse)
async def parse_file(file: Optional[UploadFile] = None, code: str = Form(None)):
    if file:
        content = await file.read()
        code = content.decode("utf-8")
    elif not code:
        return PlainTextResponse("No code provided", status_code=400)

    lexer_errors.clear()
    lexer.lineno = 1

    try:
        ast = parser.parse(code, lexer=lexer)
        if lexer_errors:
            return "\n".join(lexer_errors)

        interpreter = Interpreter()
        output = interpreter.run(ast)
        return "\n".join(map(str, output)) if output else ""

    except SyntaxError as e:
        return f"Syntax error: {str(e)}"

# 🧠 Route pour exécuter du code JSON depuis CodeMirror
class CodeInput(BaseModel):
    code: str

@app.post("/parse-json")
async def parse_json_code(input: CodeInput):
    code = input.code

    lexer_errors.clear()
    lexer.lineno = 1

    try:
        ast = parser.parse(code, lexer=lexer)
        if lexer_errors:
            return {"errors": lexer_errors}

        interpreter = Interpreter()
        output = interpreter.run(ast)

        return {
            "ast": str(ast),
            "output": output,
            "message": "Analyse réussie"
        }

    except SyntaxError as e:
        return {"errors": [f"Syntax error: {str(e)}"]}
