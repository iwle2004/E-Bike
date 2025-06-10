import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './MapPage.css'
function MapPage() {
    const position = [35.4501, 135.3339];
    return (
      <div className="map-container">
        <MapContainer center={position} zoom={13} className="leaflet-map">
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution="&copy; OpenStreetMap contributors"
          />
          <Marker position={position}>
            <Popup>Bike Station - Maizuru Port</Popup>
          </Marker>
        </MapContainer>
      </div>
    );
  }
  
  export default MapPage;