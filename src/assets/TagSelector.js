import React, { useState } from "react";

const tagGroups = {
  "観光・歴史": [
    { key: "historic", type: "monument", label: "<b>記念碑</b>（舞鶴重砲兵連隊跡 / 舞鶴東～小浜西 開通記念碑）" },
    { key: "historic", type: "memorial", label: "<b>慰霊碑</b>（四面山忠魂碑 / 舞鶴空襲学徒犠牲者慰霊碑 / 舞鶴海軍墓地）" },
    { key: "historic", type: "castle", label: "<b>城</b>（浜村城跡 / 溝尻城跡 / 行永城跡）" },
    { key: "tourism", type: "museum", label: "<b>博物館</b>（舞鶴の電気発祥の地 / 海軍記念館 / ルーシーちゃんの魔法の玩具博物館）" },
    { key: "tourism", type: "attraction", label: "<b>観光地</b>" },
  ],
  "飲食": [
    { key: "amenity", type: "restaurant", label: "<b>レストラン</b>（とと楽 / Cafe&Deli AZUR）" },
    { key: "amenity", type: "cafe", label: "<b>カフェ</b>（チャイム / こもれび / GOOD SOUND COFFEE / 木馬）" },
    { key: "amenity", type: "fast_food", label: "<b>ファストフード</b>" },
  ],
  "買い物・便利施設": [
    { key: "shop", type: "convenience", label: "<b>コンビニ</b>" },
    { key: "shop", type: "supermarket", label: "<b>スーパー</b>" },
    { key: "amenity", type: "pharmacy", label: "<b>薬局</b>" },
  ],
  "休憩・滞在": [
    { key: "leisure", type: "park", label: "<b>公園</b>（舞鶴公園 / 中舞鶴公園 / 舞鶴の森 / 青葉山ろく公園）" },
    { key: "tourism", type: "hotel", label: "<b>ホテル</b>" },
    { key: "amenity", type: "toilets", label: "<b>トイレ</b>" },
  ],
};

const endpointGroups = {
  "目的地": [
    { name: "<b>赤れんが博物館</b>", lat: 35.47608894530083, lon: 135.387461090522 },
    { name: "<b>赤レンガパーク</b>", lat: 35.474666114787986, lon: 135.38543573277403 },
  ],
};

const TagSelector = ({ onRunNavigation }) => {
  const [selectedTags, setSelectedTags] = useState([]);
  const [selectedEndpoint, setSelectedEndpoint] = useState(endpointGroups["目的地"][0]);
  const [loading, setLoading] = useState(false);
  const [randomroute, setRandomroute] = useState(false);

  const handleTagChange = (tagStr) => {
    setSelectedTags((prev) =>
      prev.includes(tagStr) ? prev.filter((t) => t !== tagStr) : [...prev, tagStr]
    );
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      await onRunNavigation(selectedTags, selectedEndpoint, randomroute);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "0.2rem", textAlign: "left" }}>
          <h2>ルート生成をランダムにしますか？</h2>
<div style={{ display: "flex", justifyContent: "center", marginBottom: "1em" }}>
  <label
    style={{
      display: "flex",
      flexDirection: "row",
      alignItems: "center",
      gap: "0.5em",
    }}
  >
    <input
      type="checkbox"
      checked={randomroute}
      onChange={(e) => setRandomroute(e.target.checked)}
      disabled={loading}
      style={{
        width: "16px",
        height: "16px",
        flexShrink: 0,
        marginTop: "0.2em",
      }}
    />
    <span
      className="tag-label"
      dangerouslySetInnerHTML={{ __html: "<b>ランダムに経由地を選択する</b>" }}
    />
  </label>
</div>
      <h2>行きたい場所のカテゴリを選んでください</h2>
      {Object.entries(tagGroups).map(([group, tags]) => (
      <fieldset key={group}>
        <legend><strong>{group}</strong></legend>
        {tags.map(({ key, type, label }) => {
          const tagStr = `${key}=${type}`;
          return (
            <label
              key={tagStr}
              style={{
                display: "flex",
                flexDirection: "row",
                alignItems: "flex-start",
                gap: "0.5em",
                width: "100%",
                marginBottom: "1em", // 行間
              }}
            >
              <input
                type="checkbox"
                checked={selectedTags.includes(tagStr)}
                onChange={() => handleTagChange(tagStr)}
                disabled={loading}
                style={{
                  width: "16px",
                  height: "16px",
                  flexShrink: 0,
                  marginTop: "0.2em",
                }}
              />
              <span
                className="tag-label"
                dangerouslySetInnerHTML={{ __html: label }}
              />
            </label>
          );
        })}
      </fieldset>
      ))}

      <h2>目的地を選択してください</h2>
      {Object.entries(endpointGroups).map(([group, endLocation]) => (
      <fieldset key={group}>
        <legend><strong>{group}</strong></legend>
        {endLocation.map((endpoint) => {
          return (
            <label
              key={endpoint.name}
              style={{
                display: "flex",
                flexDirection: "row",
                alignItems: "flex-start",
                gap: "0.5em",
                width: "100%",
                marginBottom: "1em", // 行間
              }}
            >
              <input
                type="radio"
                checked={selectedEndpoint?.name === endpoint.name}
                onChange={() => setSelectedEndpoint(endpoint)}
                disabled={loading}
                style={{
                  width: "16px",
                  height: "16px",
                  flexShrink: 0,
                  marginTop: "0.2em",
                }}
              />
              <span
                className="tag-label"
                dangerouslySetInnerHTML={{ __html: endpoint.name }}
              />
            </label>
          );
        })}
        </fieldset>
      ))}



      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "ナビ生成中..." : "ナビを開始する"}
      </button>

      {loading && <div className="spinner" />}

      <style>{`
        .spinner {
          width: 40px;
          height: 40px;
          border: 5px solid #ccc;
          border-top: 5px solid #3498db;
          border-radius: 50%;
          animation: spin 1s linear infinite;
          margin: 1rem auto;
        }
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }

        .tag-label {
          word-break: break-word;
          overflow-wrap: anywhere;
          white-space: normal;
          display: inline-block;
          max-width: 100%;
          line-height: 1.5;
        }

        @media (max-width: 600px) {
          .tag-label {
            word-break: keep-all;
            overflow-wrap: normal;
          }
        }
      `}</style>
    </div>
  );
};

export default TagSelector;
