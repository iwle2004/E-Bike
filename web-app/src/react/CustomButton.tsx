import React from 'react';
import { Button, ButtonProps, Typography } from '@mui/material';
import { Link } from 'react-router-dom';

interface CustomButtonProps extends ButtonProps {
  icon: React.ReactElement;
  text: string;
  to?: string; // 追加: to プロパティ
}

const CustomButton: React.FC<CustomButtonProps> = ({ icon, text, to, ...props }) => {
  return (
    <Button
      {...props}
      component={to ? Link : 'button'}
      to={to}
      sx={{ 
        flexDirection: 'column', 
        padding: 2, 
        width: '100%', 
        maxWidth: 150,
        textAlign: 'center' // アイコンとテキストのセンタリング
      }}
    >
      {React.cloneElement(icon, { fontSize: 'large', sx: { fontSize: 48 } })}
      <Typography variant="h6" sx={{ marginTop: 1 }}>
        {text}
      </Typography>
    </Button>
  );
};

export default CustomButton;
