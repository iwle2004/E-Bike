import 'leaflet/dist/leaflet.css';
import './MapPage.css';
import React, { useState, useEffect } from "react";
import TagSelector from "./TagSelector";

function MapPage() {
  const [mapUrl, setMapUrl] = useState(null);
  const [currentLocation, setCurrentLocation] = useState(null);

  // 🌍 現在地を取得
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          setCurrentLocation({ lat: latitude, lon: longitude });
        },
        (error) => {
          console.error("現在地の取得に失敗:", error);
          alert("位置情報の取得に失敗：位置情報サービスをオンにしてください");
        }
      );
    } else {
      alert("このブラウザではGeolocationがサポートされていません");
    }
  }, []);

  // 📡 ナビゲーション開始リクエスト
  const runNavigation = async (tags, endLocation) => {
  const apiUrl = process.env.REACT_APP_API_URL;
  const baseUrl = apiUrl || "http://localhost:5000";

  try {
    const res = await fetch(`${baseUrl}/run-navigation`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        tags,
        currentLocation,
        endLocation
      }),
    });

    const json = await res.json();

    if (json.status === "success" && json.filename) {
      const fullUrl = `${baseUrl}/get-map/${json.filename}`;
      console.log("🌍 マップURL:", fullUrl);  // ← ここでログ確認
      setMapUrl(fullUrl);
    }
    else {
      alert("ナビ生成に失敗しましたmp: " + (json.message || ""));
    }
  } catch (err) {
    console.error("通信エラー:", err);
    alert("通信エラーが発生しましたa" + (err || ""));
  }
};

  return (
    <div className="map-wrapper">
      <h1 className="page-title">🌸 東舞鶴観光ナビ 🌊</h1>
      <TagSelector onRunNavigation={runNavigation} />
      {mapUrl && (
        <div className="map-container">
          <iframe
            title="マップ"
            src={mapUrl}
            width="100%"
            height="100%"
            style={{ border: "none" }}
          />
        </div>
      )}
    </div>
  );
}

export default MapPage;
