import { useState } from "react";
import CodeMirror from "@uiw/react-codemirror";
import { oneDark } from "@codemirror/theme-one-dark";

function TerminalOutput({ lines }) {
  return (
    <div className="terminal">
      <div className="terminal-scroll">
        {lines.length === 0 ? (
          <div style={{ color: "#888" }}>Aucune sortie pour l’instant...</div>
        ) : (
          lines.map((line, index) => (
            <div key={index}>
              <span style={{ color: "#22c55e" }}>{"> "}</span>{line}
            </div>
          ))
        )}
        <div className="blinking-cursor"></div>
      </div>
    </div>
  );
}

function App() {
  const [code, setCode] = useState("");
  const [output, setOutput] = useState([]);
  const [errors, setErrors] = useState([]);
  const [loading, setLoading] = useState(false);
  const [stars, setStars] = useState([]);
  const [fileName, setFileName] = useState("");

  const handleFileImport = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setFileName(file.name);
    const reader = new FileReader();
    reader.onload = (e) => setCode(e.target.result);
    reader.readAsText(file);
  };

  const handleExecute = async () => {
    if (!code.trim()) return alert("Le code est vide");

    const newStars = Array.from({ length: 20 }).map((_, i) => ({
      id: Date.now() + i,
      color: `hsl(${Math.random() * 360}, 100%, 70%)`,
      left: Math.random() * 140,
      top: Math.random() * 40,
    }));
    setStars(newStars);
    setTimeout(() => setStars([]), 1500);

    setOutput([]);
    setErrors([]);
    setLoading(true);

    try {
      const res = await fetch("/api/parse-json", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });

      const data = await res.json();
      setOutput(data.output || []);
      setErrors(data.errors || []);
    } catch (err) {
      console.error(err);
      setErrors(["Impossible de contacter le backend"]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      height: "100vh",
      width: "100%",
      maxWidth: "1000px",
      margin: "0 auto",
      padding: "1rem",
      boxSizing: "border-box",
      gap: "1rem",
      backgroundColor: "#0f0f0f",
      color: "white"
    }}>
      {/* 📂 Import fichier + Bouton Grammaire + Exécuter */}
      <div style={{
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  flexWrap: "wrap",
  gap: "1rem"
}}>
  <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
    <input
      type="file"
      accept=".pisc"
      onChange={handleFileImport}
      className="file-button"
    />

    <a
      href="https://github.com/AlexisLasselin/Piscine_Ecole-IT_2025/blob/main/docs/grammar.md"
      target="_blank"
      rel="noopener noreferrer"
      className="doc-button"
    >
      📘 Grammaire
    </a>
  </div>

  <div style={{ position: "relative" }}>
    <div className="star-container">
      {stars.map((s) => (
        <div
          key={s.id}
          className="star"
          style={{
            color: s.color,
            left: `${s.left}px`,
            top: `${s.top}px`,
          }}
        >
          ★
        </div>
      ))}
    </div>

    <button
      onClick={handleExecute}
      disabled={loading}
      className="execute-button"
    >
      🚀 {loading ? "Exécution..." : "Exécuter"}
    </button>
  </div>
</div>

      {fileName && (
        <div style={{ color: "#aaa", fontSize: "0.9rem" }}>
          📄 Fichier sélectionné : <strong>{fileName}</strong>
        </div>
      )}

      {/* ✍️ Éditeur CodeMirror */}
      <div style={{
        flexGrow: 1,
        borderRadius: "14px",
        border: "1px solid #6366f1",
        overflow: "hidden",
        boxShadow: "0 0 10px #6366f1"
      }}>
        <div style={{ height: "100%", overflowY: "auto", backgroundColor: "#0f0f0f" }}>
          <CodeMirror
            value={code}
            height="100%"
            theme={oneDark}
            onChange={(value) => setCode(value)}
            className="w-full"
          />
        </div>
      </div>

      {/* 🖥️ Terminal */}
      <TerminalOutput lines={output} />

      {/* ❌ Erreurs */}
      {errors.length > 0 && (
        <div style={{
          backgroundColor: "#fee2e2",
          color: "#b91c1c",
          padding: "1rem",
          borderRadius: "14px",
          fontSize: "0.9rem",
          whiteSpace: "pre-wrap"
        }}>
          {errors.join("\n")}
        </div>
      )}
    </div>
  );
}

export default App;