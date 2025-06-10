import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Polyline, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import axios from 'axios';
import { Button } from '@mui/material';
import { Link } from 'react-router-dom';
import './Map.css';
import akarenga from '../images/akarenga.png';
import akarenga2 from '../images/akarenga2.png';
import hikiage from '../images/hikiage.png';
import hikiage2 from '../images/hikiage2.png';
import skyTower from '../images/sky-tower.png';
import skyTower2 from '../images/sky-tower2.png';
import toretore from '../images/toretore.png';
import toretore2 from '../images/toretore2.png';
// アイコンの定義
const currentIcon = new L.Icon({
  iconUrl: 'https://img.icons8.com/ios-filled/50/map-pin.png',
  iconSize: [40, 40],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

const searchIcon = new L.Icon({
  iconUrl: 'https://img.icons8.com/nolan/64/map-pin.png',
  iconSize: [40, 40],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

const tourIcon = new L.Icon({
  iconUrl: 'https://img.icons8.com/officel/16/marker.png',
  iconSize: [40, 40],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

const MarkerPosition = [
  {name: '舞鶴赤レンガパーク', position: new L.LatLng(35.4757, 135.3830),
    description: '舞鶴の歴史を感じることができる赤れんが倉庫群が立ち並ぶエリア。文化イベントや展示会が開催され、多くの観光客で賑わいます。',
    photos: [akarenga, akarenga2],
  },
  {name: '五老スカイタワー', position: new L.LatLng(35.464892077102, 135.34366891233),
    description: '舞鶴湾を一望できる絶景スポットで、高さ約50メートルの展望タワー。360度のパノラマビューが魅力です。',
    photos: [skyTower, skyTower2],
  },
  {name: '舞鶴港とれとれセンター', position: new L.LatLng(35.450318486205, 135.3145082609),
    description: '新鮮な海産物や地元特産品が揃う市場。舞鶴港で水揚げされた魚介類を楽しむことができます。',
    photos: [toretore, toretore2],
  },
  {name: '舞鶴引揚記念館', position: new L.LatLng(35.5095085, 135.3966057),
    description: '戦後の引揚者の歴史を伝える資料館。貴重な展示物や資料を通じて、戦争の悲惨さと平和の大切さを学べます。',
    photos: [hikiage, hikiage2],
  },
];

const SearchBox: React.FC<{ onSearch: (position: L.LatLng) => void }> = ({ onSearch }) => {
  const [query, setQuery] = useState('');

  const handleSearch = async () => {
    if (!query) return;

    const url = `https://nominatim.openstreetmap.org/search?format=json&q=${query}`;
    try {
      const response = await axios.get(url);
      if (response.data.length > 0) {
        const { lat, lon } = response.data[0];
        const position = new L.LatLng(lat, lon);
        onSearch(position);
      }
    } catch (error) {
      console.error('Error fetching location:', error);
    }
  };

  return (
    <div className="search-box">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="場所を入力"
      />
      <Button variant="contained" onClick={handleSearch}>検索</Button>
    </div>
  );
};

const MapComponent: React.FC = () => {
  const [searchPosition, setSearchPosition] = useState<L.LatLng | null>(null);
  const [route, setRoute] = useState<L.LatLng[]>([]);
  const [currentPosition, setCurrentPosition] = useState<L.LatLng | null>(null);
  const [showMap, setShowMap] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        setCurrentPosition(new L.LatLng(latitude, longitude));
        setShowMap(true);
        setLoading(false);
      },
      (error) => {
        console.error('Failed to get current position:', error);
        setLoading(false);
      }
    );
  }, []);

  const handleSearch = async (position: L.LatLng) => {
    setSearchPosition(position);
    getRoute(position);
  };

  const getRoute = async (destination: L.LatLng) => {
    if (!currentPosition) return;

    const url = `https://router.project-osrm.org/route/v1/driving/${currentPosition.lng},${currentPosition.lat};${destination.lng},${destination.lat}?overview=full&geometries=geojson`;
    try {
      const response = await axios.get(url);
      const coordinates = response.data.routes[0].geometry.coordinates;
      const route = coordinates.map((coord: [number, number]) => new L.LatLng(coord[1], coord[0]));
      setRoute(route);
    } catch (error) {
      console.error('Error fetching route:', error);
    }
  };

  if (loading) {
    return (
      <div className="map-container">
        <p>位置情報を取得しています...</p>
      </div>
    );
  }

  if (!showMap) {
    return (
      <div className="map-container">
        <p>位置情報の使用を許可してください。</p>
        <Button variant="contained" onClick={() => navigator.geolocation.getCurrentPosition(() => {}, () => {})}>位置情報を許可する</Button>
      </div>
    );
  }

  return (
    <>
      <Link to="/" style={{ textDecoration: 'none' }}>
        <Button
          variant="contained"
          style={{ position: 'absolute', bottom: '20px', left: '20px', zIndex: 1000 }}
        >
          戻る
        </Button>
      </Link>
      <div className="map-container">
        <SearchBox onSearch={handleSearch} />
        {currentPosition && (
          <MapContainer center={[currentPosition.lat, currentPosition.lng]} zoom={13} style={{ height: '100vh', width: '100%' }}>
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            {searchPosition && <Marker position={[searchPosition.lat, searchPosition.lng]} icon={searchIcon} />}
            {route.length > 0 && <Polyline positions={route} color="blue" />}
            <Marker position={[currentPosition.lat, currentPosition.lng]} icon={currentIcon} />
            {MarkerPosition.map((spot, index) => (
              <Marker key={index} position={spot.position} icon={tourIcon}>
                <Popup>
                  <div className='popup-content'>
                    <h3>{spot.name}</h3>
                    <p>{spot.description}</p>
                    {spot.photos.map((photo, idx) => (
                      <img key={idx} src={photo} alt={`${spot.name} photo ${idx + 1}`} />
                    ))}
                  </div>
                </Popup>
              </Marker>
            ))}
          </MapContainer>
        )}
      </div>
    </>
  );
};

export default MapComponent;
