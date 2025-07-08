import 'leaflet/dist/leaflet.css';
import './MapPage.css';
import React, { useState, useEffect, useRef } from "react";
import TagSelector from "./TagSelector";

function MapPage() {
  const [mapUrl, setMapUrl] = useState(null);
  const [currentLocation, setCurrentLocation] = useState(null);
  const iframeRef = useRef(null); // 追加：iframe参照用

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
  const runNavigation = async (tags, endLocation, randomroute) => {
    const apiUrl = process.env.REACT_APP_API_URL;
    const baseUrl = apiUrl || "http://localhost:5000";

    try {
      const res = await fetch(`${baseUrl}/run-navigation`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tags,
          currentLocation,
          random_route: randomroute,
          endLocation
        }),
      });

      const json = await res.json();

      if (json.status === "success" && json.filename) {
        setMapUrl(`${baseUrl}/get-map/${json.filename}`);
      } else {
        alert("ナビ生成に失敗しました: " + (json.message || ""));
      }
    } catch (err) {
      console.error("通信エラー:", err);
      alert("通信エラーが発生しました: " + (err || ""));
    }
  };

  // 🔳 全画面表示処理
  const handleFullscreen = () => {
    const iframe = iframeRef.current;
    if (iframe.requestFullscreen) {
      iframe.requestFullscreen();
    } else if (iframe.webkitRequestFullscreen) {
      iframe.webkitRequestFullscreen();
    } else if (iframe.msRequestFullscreen) {
      iframe.msRequestFullscreen();
    } else {
      alert("このブラウザは全画面表示をサポートしていません。");
    }
  };

  return (
    <div className="map-wrapper">
      <h1 className="page-title">🌸 東舞鶴観光ナビ 🌊</h1>
      <TagSelector onRunNavigation={runNavigation} />
      {mapUrl && (
        <div className="map-container">
          <button className="fullscreen-button" onClick={handleFullscreen}>
            ⛶ 全画面表示
          </button>
          <iframe
            ref={iframeRef}
            title="マップ"
            src={mapUrl}
            width="100%"
            height="600"
            allowFullScreen
            style={{ border: "none" }}
          />
        </div>
      )}
    </div>
  );
}

export default MapPage;
