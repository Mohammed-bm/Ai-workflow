import { Handle, Position } from "reactflow";
import { useState } from "react";

export default function KnowledgeBaseNode({ data }) {
  const [uploading, setUploading] = useState(false);
  const [uploaded, setUploaded] = useState(false);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/documents/upload", {
        method: "POST",
        body: formData,
      });

      const result = await res.json();

      // Save upload result into node data
      data?.onUpload?.({
        fileName: file.name,
        documentId: result.documentId || result.id,
      });

      setUploaded(true);
    } catch (err) {
      alert("Upload failed");
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="bg-white border rounded p-3 w-56 shadow text-black">
      <div className="font-semibold text-sm mb-2">Knowledge Base</div>

      <input
        type="file"
        accept=".pdf"
        onChange={handleFileUpload}
        className="text-xs"
      />

      {uploading && (
        <div className="text-xs mt-2 text-blue-600">Uploading...</div>
      )}

      {uploaded && (
        <div className="text-xs mt-2 text-green-600">✅ Uploaded</div>
      )}

      <Handle type="target" position={Position.Left} />
      <Handle type="source" position={Position.Right} />
    </div>
  );
}