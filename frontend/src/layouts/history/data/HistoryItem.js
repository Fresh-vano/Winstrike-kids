import React from "react";
import { Box, Card, CardMedia, CardContent, Typography, CardActions, Button } from '@mui/material';
import MDTypography from "components/MDTypography";
import MDButton from "components/MDButton";
import serverUrl from "config";
import { useNavigate } from "react-router-dom"; 
import { useSearch } from "SearchContext";

function HistoryItem({ item, onOpen }) {
  const { setSearchQuery } = useSearch();
  const navigate = useNavigate();

  const handleReviewsClick = () => {
    setSearchQuery(`${item.name}`); 
    navigate('/feedback');
  };

  return (
    <Card sx={{ maxWidth: 345, m: 2, '&:hover': { transform: 'scale(1.03)', transition: 'transform 0.3s' } }}>
      <CardMedia
        component="img"
        height="140"
        image={`${serverUrl}/images/${item.imageUrl}`}
        alt={item.name}
      />
      <CardContent>
        <MDTypography gutterBottom variant="h5" component="div">
          {item.name}
        </MDTypography>
        <MDTypography variant="body2">
          {item.category}
        </MDTypography>
        <Box display="flex" alignItems="center">
          <MDTypography variant="subtitle1">{item.date}</MDTypography>
        </Box>
      </CardContent>
      <CardActions>
        <MDButton size="small" sx={{minHeight:'2rem', padding:'0.375rem 1.125rem'}} color="info" onClick={() => onOpen(item)}>Подробнее</MDButton>
        <MDButton size="small" sx={{minHeight:'2rem', padding:'0.375rem 1.125rem'}} color="primary" onClick={handleReviewsClick}>Отзывы</MDButton>
      </CardActions>
    </Card>
  );
}

export default HistoryItem;