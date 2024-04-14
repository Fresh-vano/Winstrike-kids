import React from 'react';
import { DialogTitle, DialogContent, Box, Table, TableBody, TableCell, TableContainer, TableRow, Paper, Divider, TableHead } from '@mui/material';
import GaugeChart from 'react-gauge-chart';
import MDTypography from 'components/MDTypography';
import MDBox from 'components/MDBox';
import MDDialog from 'components/MDDialog';
import serverUrl from "config";

function HistoryDetailsDialog({ open, item, onClose }) {
  const getCharacteristicColor = (status) => {
    if (status == 'bad') return 'error.main'; // красный
    if (status == 'normal') return 'warning.main'; // оранжевый
    return 'success.main'; // зелёный
  };

  const getGaugeValue = () => {
      if (item.status === "bad") return 0.1;
      else if (item.status === "normal") return 0.5;
      return 0.9;
  };

  function getGaugeColor(percent) {
    if (percent <= 0.33) {
      return '#F44335';
    } else if (percent <= 0.66) {
      return '#fb8c00';
    } else {
      return '#4CAF50';
    }
  }
  
  function getGaugeRecommendation(percent) {
    if (percent <= 0.33) {
      return 'Не рекомендуется';
    } else if (percent <= 0.66) {
      return 'Частично рекомендуется';
    } else {
      return 'Рекомендуется';
    }
  }

  return (
    <MDDialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>{item.name}</DialogTitle>
      <DialogContent dividers>
      <MDBox sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 2 }}>
        <img src={`${serverUrl}/images/${item.imageUrl}`} alt={item.name} style={{ width: '100%', maxHeight: '400px', objectFit: 'contain' }} />
        <MDBox sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%', mt: 2 }}>
            <Box sx={{ display: 'flex', flexDirection: 'column', paddingLeft:'20px', flex: 1 }}>
            <MDTypography variant="subtitle1">{item.manufacturer ? `Производитель: ${item.manufacturer}` : ''}</MDTypography>
            <MDTypography variant="subtitle">{item.category}</MDTypography>
            <MDTypography variant="subtitle2">{`Дата анализа: ${item.date}`}</MDTypography>
            </Box>
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', flex: 1 }}>
                <GaugeChart id="gauge-chart" 
                    nrOfLevels={3} 
                    colors={["#F44335", "#fb8c00", "#4CAF50"]} 
                    arcWidth={0.2} 
                    hideText={true}
                    percent={getGaugeValue()} 
                    style={{ width: '50%' }} 
                />
                <MDTypography
                    variant="subtitle2"
                    style={{ 
                    color: getGaugeColor(getGaugeValue()), 
                    marginTop: '8px',
                    }}
                >
                    {getGaugeRecommendation(getGaugeValue())}
                </MDTypography>
            </Box>
        </MDBox>
        </MDBox>
        <Divider/>
        <TableContainer component={Paper} sx={{ marginTop: 2 }}>
            <Table sx={{ minWidth: 650 }} aria-label="simple table">
              <TableHead>
                <MDTypography variant="subtitle1">{`Характеристики`}</MDTypography>
              </TableHead>
              <TableBody>
                {item.characteristics.map((char, index) => (
                  <TableRow
                    key={index}
                    sx={{
                      'borderLeft': 10,
                      'borderLeftColor': getCharacteristicColor(char.status),
                      'borderLeftStyle': 'solid',
                    }}
                  >
                    <TableCell component="th" scope="row">
                      <MDTypography variant="subtitle2">{char.name}</MDTypography>
                    </TableCell>
                    <TableCell align="right">
                      {char.status === 'bad' && char.range && (
                        <MDTypography variant="caption" sx={{ color: 'error.main' }}>
                          Требуемый диапазон: {char.range}
                        </MDTypography>
                      )}
                    </TableCell>
                    <TableCell align="right">
                      <MDTypography variant="subtitle1" sx={{ color: getCharacteristicColor(char.status), fontWeight:'700' }}>{char.value}</MDTypography>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
      </DialogContent>
    </MDDialog>
  );
}

export default HistoryDetailsDialog;
