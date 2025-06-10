import React, { useState } from "react";

const MapViewer = () => {
  const [mapUrl, setMapUrl] = useState(null);
  const [loading, setLoading] = useState(false); // ローディング状態

  const handleRunPython = async () => {
    setLoading(true);      // スピナー表示
    setMapUrl('');         // 出力クリア

    try {
      const res = await fetch('http://localhost:5000/run-navigation');
      const data = await res.json();

      if (data.status === "success") {
        setMapUrl("http://localhost:5000/get-map");
      }
    } catch (error) {
      setMapUrl('エラーが発生しました：' + error.message);
    } finally {
      setLoading(false);   // スピナー非表示
    }
  };

  return (
    <div style={{ textAlign: 'center', padding: '2rem' }}>
      
      <button onClick={handleRunPython} disabled={loading}>
        {loading ? 'ルート作成中...' : 'ルート案内開始'}
      </button>

      {/* スピナー表示 */}
      {loading && <div className="spinner" style={{ marginTop: '1rem' }}></div>}

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

      {/* スピナーのCSS */}
      <style>{`
        .spinner {
          width: 40px;
          height: 40px;
          border: 5px solid #ccc;
          border-top: 5px solid #3498db;
          border-radius: 50%;
          animation: spin 1s linear infinite;
          margin: auto;
        }

        @keyframes spin {
          0%   { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}

export default MapViewer;
