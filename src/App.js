import React, { useState } from "react";
import TagSelector from "./TagSelector";

function App() {
  const [mapUrl, setMapUrl] = useState(null);

  const runNavigation = async (tags, locations) => {
    try { 
      const res = await fetch("http://localhost:5000/run-navigation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tags, locations }),
      });
      const json = await res.json();
      if (json.status === "success") {
        setMapUrl("http://localhost:5000/get-map");
      } else {
        alert(locations)
        //alert("ナビ生成に失敗しました: " + (json.message || ""));
      }
    } catch {
      alert("通信エラーが発生しました");
    }
  };

  return (
    <div>
      <h1>東舞鶴観光ナビ</h1>
      <TagSelector
        onRunNavigation={runNavigation}
      />
      {mapUrl && (
        <iframe
          title="マップ"
          src={mapUrl}
          width="100%"
          height="600px"
          style={{ marginTop: "20px", border: "none" }}
        />
      )}
    </div>
  );
}

export default App;
