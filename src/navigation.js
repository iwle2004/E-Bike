import React, { useState, useEffect } from "react";
import TagSelector from "./assets/TagSelector";

function App() {
  const [mapUrl, setMapUrl] = useState(null);
  const [currentLocation, setCurrentLocation] = useState(null);

  // ✅ 現在地取得：マウント時に1度だけ実行
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          setCurrentLocation({ lat: latitude, lon: longitude });
        },
        (error) => {
          console.error("現在地の取得に失敗:", error);
          alert("位置情報の取得に失敗しました");
        }
      );
    } else {
      alert("このブラウザではGeolocationがサポートされていません");
    }
  }, []);

  const runNavigation = async (tags) => {
    const apiUrl = process.env.REACT_APP_API_URL;
    const baseUrl = apiUrl || "http://localhost:5000";

    try {
      const res = await fetch(`${baseUrl}/run-navigation`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tags, currentLocation }), // ✅ 位置情報も一緒に送信可能
      });
      const json = await res.json();
      alert(currentLocation);
      if (json.status === "success") {
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
