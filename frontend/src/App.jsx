import { useState } from "react";
import CodeMirror from "@uiw/react-codemirror";
import { oneDark } from "@codemirror/theme-one-dark";

function TerminalOutput({ lines }) {
  return (
    <div className="bg-black text-green-400 font-mono p-4 rounded w-full h-32 overflow-y-auto border border-green-700 mt-4">
      {lines.length === 0 ? (
        <div className="text-gray-500">Aucune sortie pour l’instant...</div>
      ) : (
        lines.map((line, index) => (
          <div key={index} className="whitespace-pre-wrap">
            <span className="text-green-600">{"> "}</span>{line}
          </div>
        ))
      )}
      <div className="blinking-cursor"></div>
    </div>
  );
}

function App() {
  const [code, setCode] = useState("");
  const [output, setOutput] = useState([]);
  const [errors, setErrors] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFileImport = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => setCode(e.target.result);
    reader.readAsText(file);
  };

  const handleExecute = async () => {
    if (!code.trim()) return alert("Le code est vide");

    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/parse-json", {
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
    <div className="w-screen h-screen flex flex-col p-4 space-y-4 bg-[#1e1e1e] text-white">
      {/* 📂 Import fichier */}
      <div className="flex items-center gap-4">
        <input
          type="file"
          accept=".pisc"
          onChange={handleFileImport}
          className="border p-2 rounded bg-white text-black shadow"
        />
        <button
          onClick={handleExecute}
          disabled={loading}
        >
          {loading ? "Exécution en cours..." : "Exécuter"}
        </button>
      </div>

      {/* ✍️ Éditeur */}
      <div className="flex-grow rounded border border-gray-700 overflow-hidden">
        <div style={{ height: "50vh", overflowY: "auto", backgroundColor: "#1e1e1e" }}>
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
      <div>
        <h2 className="text-xl font-semibold text-green-400 mb-2">Terminal :</h2>
        <TerminalOutput lines={output} />
      </div>

      {/* ❌ Erreurs */}
      {errors.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold mb-2 text-red-600">Erreurs :</h2>
          <pre className="bg-red-100 text-red-800 p-4 rounded whitespace-pre-wrap text-sm">
            {errors.join("\n")}
          </pre>
        </div>
      )}
    </div>
  );
}

export default App;
