import React, { useState } from "react";

const tagGroups = {
  "観光・歴史": [
    { key: "historic", type: "monument", label: "記念碑" },
    { key: "historic", type: "memorial", label: "慰霊碑" },
    { key: "historic", type: "castle", label: "城" },
    { key: "tourism", type: "museum", label: "博物館" },
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
    { key: "leisure", type: "park", label: "公園" },
    { key: "tourism", type: "hotel", label: "ホテル" },
    { key: "amenity", type: "toilets", label: "トイレ" },
  ],
};

const TagSelector = ({ onRunNavigation }) => {
  const [selectedTags, setSelectedTags] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleChange = (tagStr) => {
    setSelectedTags((prev) =>
      prev.includes(tagStr) ? prev.filter((t) => t !== tagStr) : [...prev, tagStr]
    );
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      await onRunNavigation(selectedTags);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h2>行きたい場所を選んでください</h2>
      {Object.entries(tagGroups).map(([group, tags]) => (
        <fieldset key={group}>
          <legend><strong>{group}</strong></legend>
          {tags.map(({ key, type, label }) => {
            const tagStr = `${key}=${type}`;
            return (
              <label key={tagStr} style={{ display: "block" }}>
                <input
                  type="checkbox"
                  checked={selectedTags.includes(tagStr)}
                  onChange={() => handleChange(tagStr)}
                  disabled={loading}
                />
                {label}
              </label>
            );
          })}
        </fieldset>
      ))}

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? 'ナビ生成中...' : 'ナビを開始する'}
      </button>

      {/* スピナー表示 */}
      {loading && <div className="spinner" />}

      {/* スピナー用アニメーション CSS */}
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
          0%   { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default TagSelector;