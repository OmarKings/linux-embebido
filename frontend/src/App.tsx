import { useEffect, useState } from "react";

function App() {
  const [files, setFiles] = useState<string[]>([]);
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const relays = [0, 1, 2, 3];

  // Apunta autom�ticamente al backend que sirvi� el frontend
  const API = window.location.origin;

  // Obtener la lista de archivos
  const fetchFiles = async () => {
    try {
      setLoading(true);
      const res = await fetch(`${API}/files`);
      if (!res.ok) {
        throw new Error(`Error ${res.status} al obtener archivos`);
      }
      const data = (await res.json()) as string[];
      setFiles(data);
    } catch (error) {
      console.error("Error al obtener la lista de archivos:", error);
      setFiles([]); 
      window.alert("No se pudo obtener la lista de archivos.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFiles();
  }, []);

  // Enviar comando para encender/apagar rel�
  const toggleRelay = async (index: number, state: "on" | "off") => {
    try {
      const res = await fetch(`${API}/relay/${index}/${state}`, { method: "POST" });
      if (!res.ok) {
        throw new Error(`Error ${res.status} al cambiar estado del rel�`);
      }
    } catch (error) {
      console.error("Error al cambiar estado del rel�:", error);
      window.alert(`No se pudo ${state === "on" ? "encender" : "apagar"} el rel� ${index}.`);
    }
  };

  // Subir el archivo seleccionado
  const handleUpload = async () => {
    console.log("?? handleUpload disparado, file =", file);
    if (!file) {
      console.warn("?? No hay ning�n archivo seleccionado");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      const res = await fetch(`${API}/upload`, {
        method: "POST",
        body: formData,
      });
      if (!res.ok) {
        throw new Error(`Error ${res.status} al subir el archivo`);
      }
      const json = await res.json();
      window.alert(`Archivo �${json.filename}� subido con �xito.`);
      setFile(null);
      fetchFiles();
    } catch (error) {
      console.error("Error al subir archivo:", error);
      window.alert("No se pudo subir el archivo.");
    } finally {
      setLoading(false);
    }
  };

  // Eliminar el archivo indicado
  const handleDelete = async (filename: string) => {
    if (!window.confirm(`�Eliminar �${filename}�?`)) return;

    try {
      setLoading(true);
      const res = await fetch(`${API}/files/${filename}`, { method: "DELETE" });
      if (!res.ok) {
        throw new Error(`Error ${res.status} al eliminar el archivo`);
      }
      window.alert(`Archivo �${filename}� eliminado.`);
      fetchFiles();
    } catch (error) {
      console.error("Error al eliminar archivo:", error);
      window.alert("No se pudo eliminar el archivo.");
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-200 via-purple-100 to-pink-200 p-8 text-center">
      <h1 className="text-3xl font-bold mb-6">Control de Rel�s</h1>

      <div className="grid grid-cols-2 gap-4 justify-center mb-12">
        {relays.map((i) => (
          <div key={i} className="bg-white/80 p-4 rounded shadow">
            <h2 className="text-xl font-semibold mb-2">Rel� {i}</h2>
            <button
              onClick={() => toggleRelay(i, "on")}
              className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded mr-2"
            >
              Encender
            </button>
            <button
              onClick={() => toggleRelay(i, "off")}
              className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
            >
              Apagar
            </button>
          </div>
        ))}
      </div>

      <h1 className="text-3xl font-bold mb-6">Gesti�n de Archivos</h1>
      <div className="bg-white/80 p-6 rounded shadow mb-6">
        <input
          type="file"
          onChange={(e) => {
            console.log("?? onChange, e.target.files =", e.target.files);
            setFile(e.target.files?.[0] || null);
          }}
          className="block mb-4"
        />
        <button
          onClick={handleUpload}
          className={`bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded ${
            !file || loading ? "opacity-50 cursor-not-allowed" : ""
          }`}
          disabled={!file || loading}
        >
          {loading ? "Procesando�" : "Subir archivo"}
        </button>
      </div>

      <div className="bg-white/80 p-6 rounded shadow">
        <h2 className="text-xl font-semibold mb-4">Archivos disponibles</h2>
        {loading && <p className="mb-4 text-gray-600">Cargando�</p>}
        {!loading && files.length === 0 && (
          <p className="mb-4 text-gray-600">No hay archivos subidos.</p>
        )}
        {!loading && files.length > 0 && (
          <ul>
            {files.map((name) => (
              <li key={name} className="mb-2 flex items-center justify-center">
                <a
                  href={`${API}/files/${name}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 underline mr-4"
                >
                  {name}
                </a>
                <button
                  onClick={() => handleDelete(name)}
                  className="bg-red-400 hover:bg-red-500 text-white px-2 py-1 rounded"
                >
                  Eliminar
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default App;
