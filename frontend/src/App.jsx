import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleExecute = async () => {
    if (!file) return alert("Choisis un fichier .pisc");

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/parse", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setResult({ errors: ["Impossible de contacter le backend"] });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-6">
      <h1 className="text-3xl font-bold text-blue-600 mb-6">
        Analyseur Piscine 🏊‍♂️
      </h1>

      {/* Upload input */}
      <input
        type="file"
        accept=".pisc"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-4 border p-2 rounded bg-white shadow"
      />

      {/* Execute button */}
      <button
        onClick={handleExecute}
        disabled={loading}
        className="px-4 py-2 bg-blue-500 text-white rounded shadow hover:bg-blue-600 disabled:bg-gray-400"
      >
        {loading ? "Exécution en cours..." : "Exécuter"}
      </button>

      {/* Result */}
      {result && (
        <div className="mt-6 w-full max-w-2xl">
          <h2 className="text-xl font-semibold mb-2">Résultat :</h2>
          <pre className="bg-gray-900 text-green-400 p-4 rounded overflow-x-auto whitespace-pre-wrap text-sm">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}

export default App;
