import React, { useState } from "react";

const MapViewer = () => {
  const [mapUrl, setMapUrl] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleRunPython = async () => {
    setLoading(true);
    setMapUrl('');

    try {
      const res = await fetch('http://localhost:5000/run-navigation');
      const data = await res.json();

      if (data.status === "success") {
        setMapUrl("http://localhost:5000/get-map");
      }
    } catch (error) {
      setMapUrl('エラーが発生しました：' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ textAlign: 'center', padding: '2rem' }}>
      <button onClick={handleRunPython} disabled={loading}>
        {loading ? 'ルート作成中...' : 'ルート案内開始'}
      </button>

      {/* スピナー表示 */}
      {loading && (
        <div
          style={{
            width: 40,
            height: 40,
            border: "5px solid #ccc",
            borderTop: "5px solid #3498db",
            borderRadius: "50%",
            animation: "spin 1s linear infinite",
            margin: "1rem auto"
          }}
        />
      )}

      {/* 地図を表示 */}
      {!loading && mapUrl && (
        <iframe
          title="TSP Map"
          src={mapUrl}
          width="100%"
          height="600px"
          style={{ border: "none", marginTop: 20 }}
        />
      )}

      {/* スピナー用アニメーション */}
      <style>{`
        @keyframes spin {
          0%   { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default MapViewer;
