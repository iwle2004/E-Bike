import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './MapPage.css'
import React, { useState } from "react";
import TagSelector from "./assets/TagSelector";

function App() {
  const [mapUrl, setMapUrl] = useState(null);

  const runNavigation = async (tags) => {
    // 環境変数からバックエンドのURLを取得
    const apiUrl = process.env.REACT_APP_API_URL;

    // もしapiUrlが未設定なら、ローカル用のURLを使う（開発時に便利）
    const baseUrl = apiUrl || "http://localhost:5000";

    try {
      // 🔽 変更点1
      const res = await fetch(`${baseUrl}/run-navigation`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tags }),
      });
      const json = await res.json();
      if (json.status === "success") {
        // 🔽 変更点2
        setMapUrl(`${baseUrl}/get-map`);
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