import { useState, useEffect } from "react";
import CodeMirror from "@uiw/react-codemirror";
import { oneDark } from "@codemirror/theme-one-dark";

function TerminalOutput({ lines }) {
  return (
    <div className="terminal">
      <div className="terminal-scroll">
        {lines.length === 0 ? (
          <div className="terminal-empty">Aucune sortie pour l’instant...</div>
        ) : (
          lines.map((line, index) => (
            <div key={index}>
              <span className="terminal-prefix">{"> "}</span>
              {line}
            </div>
          ))
        )}
        <div className="blinking-cursor"></div>
      </div>
    </div>
  );
}

function App() {
  // lecture du cache (localStorage) ou valeur par défaut
  const savedCode = localStorage.getItem("editorCode") || `print("Hello World")`;
  const [code, setCode] = useState(savedCode);

  const [output, setOutput] = useState([]);
  const [errors, setErrors] = useState([]);
  const [loading, setLoading] = useState(false);
  const [stars, setStars] = useState([]);
  const [fileName, setFileName] = useState("");
  const [theme, setTheme] = useState("dark");

  const toggleTheme = () => setTheme((t) => (t === "dark" ? "light" : "dark"));

  const handleCodeChange = (value) => {
    setCode(value);
    localStorage.setItem("editorCode", value);
  };

  const handleFileImport = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setFileName(file.name);
    const reader = new FileReader();
    reader.onload = (ev) => handleCodeChange(ev.target.result);
    reader.readAsText(file);
  };

  const handleExport = () => {
    if (!code.trim()) {
      alert("Aucun code à exporter");
      return;
    }
    const blob = new Blob([code], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = fileName || "code.pisc";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handleExecute = async () => {
    if (!code.trim()) return alert("Le code est vide");

    const newStars = Array.from({ length: 30 }).map((_, i) => ({
      id: Date.now() + i,
      color: `hsl(${Math.random() * 360}, 100%, 70%)`,
      left: 10 + Math.random() * 80,
      top: -10 + Math.random() * 40,
      size: 10 + Math.random() * 12,
      rotate: Math.random() * 360,
    }));
    setStars(newStars);
    setTimeout(() => setStars([]), 1200);

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

  useEffect(() => {
    // Exécute le code au premier rendu (Hello World ou code sauvegardé)
    handleExecute();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className={theme === "dark" ? "app-dark app-container" : "app-light app-container"}>
      {/* Toolbar (gauche: actions) */}
      <div className="toolbar">
        <div className="toolbar-left">
          <button onClick={toggleTheme} className="theme-toggle">
            {theme === "dark" ? "☀️ Mode clair" : "🌙 Mode sombre"}
          </button>

          <input type="file" accept=".pisc" onChange={handleFileImport} className="file-button" />
          <button onClick={handleExport} className="export-button">💾 Exporter</button>
          <a
            href="https://github.com/AlexisLasselin/Piscine_Ecole-IT_2025/blob/main/docs/grammar.md"
            target="_blank"
            rel="noopener noreferrer"
            className="doc-button"
          >
            📘 Grammaire
          </a>
        </div>
        {/* on garde l'espace droit si besoin, mais on ne met plus l'exécuter ici */}
        <div className="toolbar-right" />
      </div>

      {fileName && (
        <div className="file-info">
          📄 Fichier sélectionné : <strong>{fileName}</strong>
        </div>
      )}

      {/* Éditeur (Execute placé en overlay bottom-right sur grand écrans) */}
      <div className="editor-container">
        <CodeMirror
          value={code}
          height="100%"
          theme={oneDark}
          onChange={handleCodeChange}
          className="code-editor"
        />

        {/* Footer/overlay dans l'éditeur : particules + bouton Exécuter */}
        <div className="editor-footer" aria-hidden={loading ? "true" : "false"}>
          <div className="star-area" aria-hidden>
            {stars.map((s) => (
              <div
                key={s.id}
                className="particle"
                style={{
                  color: s.color,
                  left: `${s.left}%`,
                  top: `${s.top}%`,
                  fontSize: `${s.size}px`,
                  transform: `rotate(${s.rotate}deg)`,
                }}
              >
                ✦
              </div>
            ))}
          </div>

          <button onClick={handleExecute} disabled={loading} className="execute-button">
            🚀 {loading ? "Exécution..." : "Exécuter"}
          </button>
        </div>
      </div>

      {/* Terminal */}
      <TerminalOutput lines={output} />

      {/* Errors */}
      {errors.length > 0 && <div className="error-box">{errors.join("\n")}</div>}
    </div>
  );
}

export default App;
