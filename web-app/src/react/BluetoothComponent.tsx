import React, { useState } from 'react';
import { Box, Button, CircularProgress } from '@mui/material';

const BluetoothComponent: React.FC = () => {
    const [isConnecting, setIsConnecting] = useState<boolean>(false);

    const handleConnect = async () => {
        setIsConnecting(true);
        try {
            const device = await navigator.bluetooth.requestDevice({
                filters: [{ services: ['battery_service'] }]
            });

            const server = await device.gatt?.connect();

            if (!server) {
                throw new Error('Failed to connect to Bluetooth device');
            }

            const service = await server.getPrimaryService('battery_service');
            const characteristic = await service.getCharacteristic('battery_level');
            const value = await characteristic.readValue();

            console.log('Battery level:', value.getUint8(0));
        } catch (error) {
            console.error('Failed to connect to Bluetooth device:', error);
        } finally {
            setIsConnecting(false);
        }
    };

    return (
        <Box display="flex" flexDirection="column" alignItems="center">
            <Button
                variant="contained"
                color="primary"
                onClick={handleConnect}
                disabled={isConnecting}
                startIcon={isConnecting ? <CircularProgress size={24} /> : null}
            >
                {isConnecting ? '接続中...' : 'Me-BikeをBluetooth接続'}
            </Button>
        </Box>
    );
};

export default BluetoothComponent;
