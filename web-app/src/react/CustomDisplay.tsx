import React from 'react';
import { Typography, Box } from '@mui/material';

interface CustomDisplayProps {
  icon: React.ReactElement;
  text: string;
  iconColor?: string; // アイコンの色を指定するプロパティ
  textColor?: string; // テキストの色を指定するプロパティ
}

const CustomDisplay: React.FC<CustomDisplayProps> = ({ icon, text, iconColor, textColor }) => {
  return (
    <Box 
      sx={{ 
        display: 'flex', 
        flexDirection: 'column', 
        alignItems: 'center', 
        padding: 2, // `16px` を MUI のスペーシング単位に変更
        width: '100%', 
        maxWidth: 150, 
        textAlign: 'center' 
      }}
    >
      {React.cloneElement(icon, { sx: { fontSize: 48, color: iconColor } })} {/* `style` から `sx` に変更 */}
      <Typography variant="h6" sx={{ marginTop: 2, color: textColor }}>
        {text}
      </Typography>
    </Box>
  );
};

export default CustomDisplay;
