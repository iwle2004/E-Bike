import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './MapPage.css'
function MapPage() {
<<<<<<< Updated upstream
    const position = [35.4501, 135.3339];
    return (
      <div className="map-container">
        <MapContainer center={position} zoom={13} className="leaflet-map">
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution="&copy; OpenStreetMap contributors"
=======
  const [mapUrl, setMapUrl] = useState(null);

  const runNavigation = async (tags) => {
    try {
      const res = await fetch("https://e-bike-vjxt.onrender.com/run-navigation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tags }),
      });

      const json = await res.json();
      if (json.status === "success") {
        setMapUrl("https://e-bike-vjxt.onrender.com/get-map");
      } else {
        alert("ナビ生成に失敗しました");
      }
    } catch {
      alert("通信エラーが発生しました");
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
>>>>>>> Stashed changes
          />
          <Marker position={position}>
            <Popup>Bike Station - Maizuru Port</Popup>
          </Marker>
        </MapContainer>
      </div>
    );
  }
  
  export default MapPage;