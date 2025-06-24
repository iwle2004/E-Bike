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

  const handleChange = (tagStr) => {
    setSelectedTags((prev) =>
      prev.includes(tagStr) ? prev.filter((t) => t !== tagStr) : [...prev, tagStr]
    );
  };

  const handleSubmit = () => {
    onRunNavigation(selectedTags);
  };

  return (
    <div>
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
                />
                {label}
              </label>
            );
          })}
        </fieldset>
      ))}
      <button onClick={handleSubmit}>ナビを開始する</button>
    </div>
  );
};

export default TagSelector;
