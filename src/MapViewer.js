import React, { useState } from "react";

const MapViewer = () => {
  const [mapUrl, setMapUrl] = useState(null);

  const handleRunNavigation = async () => {
    try {
      const res = await fetch("http://localhost:5000/run-navigation");
      const json = await res.json();
      if (json.status === "success") {
        setMapUrl("http://localhost:5000/get-map");
      } else {
        alert("ナビゲーション実行に失敗しました");
      }
    } catch (error) {
      console.error(error);
      alert("通信エラーが発生しました");
    }
  };

  return (
    <div>
      <button onClick={handleRunNavigation}>ナビゲーション実行</button>
      {mapUrl && (
        <iframe
          title="TSP Map"
          src={mapUrl}
          width="100%"
          height="600px"
          style={{ border: "none", marginTop: 20 }}
        />
      )}
    </div>
  );
};

export default MapViewer;
