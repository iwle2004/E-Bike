import React, { useState } from "react";

const tagGroups = {
  "観光・歴史": [
    { key: "historic", type: "monument", label: "記念碑(舞鶴重砲兵連隊跡、舞鶴東～小浜西 開通記念碑、)" },
    { key: "historic", type: "memorial", label: "慰霊碑(四面山忠魂碑、舞鶴空襲学徒犠牲者慰霊碑、舞鶴海軍墓地)" },
    { key: "historic", type: "castle", label: "城(浜村城跡、溝尻城跡、行永城跡)" },
    { key: "tourism", type: "museum", label: "博物館(舞鶴の電気発祥の地、海軍記念館、ルーシーちゃんの魔法の玩具博物館)" },
    { key: "tourism", type: "attraction", label: "観光地" },
  ],
  "飲食": [
    { key: "amenity", type: "restaurant", label: "レストラン" },
    { key: "amenity", type: "cafe", label: "カフェ" },
    { key: "amenity", type: "fast_food", label: "ファストフード" },
  ],
  "買い物・便利施設": [
    { key: "shop", type: "convenience", label: "コンビニ" },
    { key: "shop", type: "supermarket", label: "スーパー" },
    { key: "amenity", type: "pharmacy", label: "薬局" },
  ],
  "休憩・滞在": [
    { key: "leisure", type: "park", label: "公園(舞鶴公園、中舞鶴公園、舞鶴の森、青葉山ろく公園)" },
    { key: "tourism", type: "hotel", label: "ホテル" },
    { key: "amenity", type: "toilets", label: "トイレ" },
  ],
};

const endpointGroups = {
  "目的地": [
    { name: "赤れんが博物館", lat: 35.47608894530083, lon: 135.387461090522 },
    { name: "赤レンガパーク", lat: 35.474666114787986, lon: 135.38543573277403 },
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
    <div style={{ padding: "2rem", textAlign: "left" }}>
      <h2>行きたい場所のカテゴリを選んでください</h2>
      {Object.entries(tagGroups).map(([group, tags]) => (
        <fieldset key={group}>
          <legend><strong>{group}</strong></legend>
          {tags.map(({ key, type, label }) => {
            const tagStr = `${key}=${type}`;
            return (
              <label key={tagStr}
              style={{
                display: "flex",
    flexDirection: "row",
    alignItems: "flex-start",
    gap: "0.5em",
    marginBottom: "0.5em",
    maxWidth: "600px", // ← 横幅制限ここ
    width: "100%",
    wordBreak: "break-word",
    whiteSpace: "normal",
    overflowWrap: "break-word",  // 単語途中でも改行
    //writingMode: "horizontal-tb" // 横書き強制
              }}>
                <input
                  type="checkbox"
                  checked={selectedTags.includes(tagStr)}
                  onChange={() => handleTagChange(tagStr)}
                  disabled={loading}
                  style={{ flexShrink: 0 }}
                />
                {label}
              </label>
            );
          })}
        </fieldset>
      ))}

      <h2>目的地を選択してください</h2>
      {Object.entries(endpointGroups).map(([group, endLocation]) => (
        <fieldset key={group}>
          <legend><strong>{group}</strong></legend>
          {endLocation.map((endpoint) => (
            <label key={endpoint.name}
            style={{
                display: "flex",
                alignItems: "flex-start", // 長いテキストに合わせて上揃え
                justifyContent: "flex-start",
                marginBottom: "0.5em",
                gap: "0.5em",              // inputとテキストの間隔
                maxWidth: "100%",         // 横幅制限
                wordBreak: "break-word",  // テキストがはみ出ないように
                whiteSpace: "normal",     // 折り返しを許可
            }}>
              <input
                type="radio"
                name="endLocation"
                checked={selectedEndpoint?.name === endpoint.name}
                onChange={() => setSelectedEndpoint(endpoint)}
                disabled={loading}
                style={{ flexShrink: 0 }}
              />
              {endpoint.name}
            </label>
          ))}
        </fieldset>
      ))}

      <h2>ルート生成をランダムにしますか？</h2>
      <label
      style={{
        display: "flex",
        alignItems: "flex-start", // 長いテキストに合わせて上揃え
        justifyContent: "flex-start",
        marginBottom: "0.5em",
        gap: "0.5em",              // inputとテキストの間隔
        maxWidth: "100%",         // 横幅制限
        wordBreak: "break-word",  // テキストがはみ出ないように
        whiteSpace: "normal",     // 折り返しを許可
      }}>
        <input
          type="checkbox"
          checked={randomroute}
          onChange={(e) => setRandomroute(e.target.checked)}
          disabled={loading}
          style={{ flexShrink: 0 }}
        />
        ランダムに経由地を選択する
      </label>

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
      `}</style>
    </div>
  );
};

export default TagSelector;
