import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './MapPage.css'
import React, { useState } from "react";
import TagSelector from "./assets/TagSelector";

function App() {
  const [mapUrl, setMapUrl] = useState(null);

  const runNavigation = async (tags) => {
    try {
      const res = await fetch("http://localhost:5000/run-navigation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tags }),
      });
      const json = await res.json();
      if (json.status === "success") {
        setMapUrl("http://localhost:5000/get-map");
      } else {
        alert("ナビ生成に失敗しました");
      }
    } catch {
      alert("通信エラーが発生しました");
    }
  };

  return (
    <div>
      <h1>東舞鶴観光ナビ</h1>
      <TagSelector onRunNavigation={runNavigation} />
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
