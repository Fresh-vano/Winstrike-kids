import { useEffect, useState } from "react";
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";
import MDBox from "components/MDBox";
import MDTypography from "components/MDTypography";
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import { Button, TextField } from "@mui/material";import { useSearch } from "SearchContext";
;

function Notifications() {
  const { searchQuery, setSearchQuery } = useSearch();

  const marketplaces = [
    { name: "Ozon", color: "#005bff", url: "https://www.ozon.ru/search/?brand=26084989&from_global=true&text=" },
    { name: "Яндекс маркет", color: "#fc0", url: "https://market.yandex.ru/search?text=" },
    { name: "Wildberries", color: "#a73afd", url: "https://www.wildberries.ru/catalog/0/search.aspx?search=" },
    { name: "Мега маркет", color: "#8654cc", url: "https://megamarket.ru/catalog/?q=" },
  ];

  const renderMarketplaceButtons = () => {
  return marketplaces.map((marketplace, index) => (
    <Button
        key={index}
        href={`${marketplace.url}${encodeURIComponent(searchQuery)}`}
        target="_blank"
        sx={{ margin: 1, backgroundColor:`${marketplace.color}`, '&:hover': { transform: 'scale(1.05)', backgroundColor:`${marketplace.color}`},}}
      >
        <MDTypography variant="h5" color="white">{marketplace.name}</MDTypography>
      </Button>
    ));
  };

  return (
    <DashboardLayout>
      <MDBox pt={6} pb={3}>
        <Grid container spacing={6}>
          <Grid item xs={12}>
            <Card>
              <MDBox
                mx={2}
                mt={-3}
                py={3}
                px={2}
                variant="gradient"
                bgColor="info"
                borderRadius="lg"
                coloredShadow="info"
              >
                <MDTypography variant="h6" color="white">
                  Отзывы
                </MDTypography>
              </MDBox>
              <MDBox pt={2} px={2}>
                <MDTypography variant="h6">
                  Введите название интересующего вас товара и ознакомтесь с отзывами о нем в один клик на популярных маркетплейсах России.
                </MDTypography>
                <TextField
                    fullWidth
                    label="Введите название товара"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    variant="outlined"
                    margin="normal"
                  />
              </MDBox>
              <MDBox mt={2} sx={{ textAlign: 'center' }}>
                {renderMarketplaceButtons()}
              </MDBox>
            </Card>
          </Grid>
        </Grid>
      </MDBox>
    </DashboardLayout>
  );
}

export default Notifications;