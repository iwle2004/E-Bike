import 'leaflet/dist/leaflet.css';
import './MapPage.css';
import React, { useState, useEffect, useRef } from "react";
import TagSelector from "./TagSelector";

function MapPage() {
  const [mapUrl, setMapUrl] = useState(null);
  const [currentLocation, setCurrentLocation] = useState(null);
  const [isFullscreen, setIsFullscreen] = useState(false); // 🌟 状態追加
  const iframeRef = useRef(null);

  // 現在地取得
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

    // 🔄 フルスクリーン変更監視
    const handleChange = () => {
      const fsElement =
        document.fullscreenElement ||
        document.webkitFullscreenElement ||
        document.mozFullScreenElement ||
        document.msFullscreenElement;
      setIsFullscreen(!!fsElement);
    };

    document.addEventListener("fullscreenchange", handleChange);
    document.addEventListener("webkitfullscreenchange", handleChange);
    document.addEventListener("mozfullscreenchange", handleChange);
    document.addEventListener("MSFullscreenChange", handleChange);

    return () => {
      document.removeEventListener("fullscreenchange", handleChange);
      document.removeEventListener("webkitfullscreenchange", handleChange);
      document.removeEventListener("mozfullscreenchange", handleChange);
      document.removeEventListener("MSFullscreenChange", handleChange);
    };
  }, []);

  // ナビ生成
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
          endLocation,
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

  // ✅ 全画面表示
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

  // ⛔️ 全画面解除
  const handleExitFullscreen = () => {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    } else if (document.msExitFullscreen) {
      document.msExitFullscreen();
    }
  };

  return (
    <div className="map-wrapper">
      <h1 className="page-title">🌸 東舞鶴観光ナビ 🌊</h1>
      <TagSelector onRunNavigation={runNavigation} />
      {mapUrl && (
        <div className="map-container">
          {!isFullscreen ? (
            <button className="fullscreen-button" onClick={handleFullscreen}>
              ⛶ 全画面表示
            </button>
          ) : (
            <button className="fullscreen-button" onClick={handleExitFullscreen}>
              ✕ 全画面をやめる
            </button>
          )}
          <iframe
            ref={iframeRef}
            title="マップ"
            src={mapUrl}
            width="100%"
            height="600"
            allowFullScreen
            webkitallowfullscreen="true"
            mozallowfullscreen="true"
            style={{ border: "none" }}
          />
        </div>
      )}
    </div>
  );
}

export default MapPage;
