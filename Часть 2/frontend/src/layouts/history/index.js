import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";
import MDBox from "components/MDBox";
import MDTypography from "components/MDTypography";
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import HistoryItem from "layouts/history/data/HistoryItem";
import { useEffect, useState } from "react";
import axios from "axios";
import serverUrl from "config";
import { Box } from "@mui/material";
import HistoryDetailsDialog from "./data/HistoryDetailsDialog";
import MDButton from "components/MDButton";
import * as FileSaver from "file-saver";
import * as XLSX from "xlsx";

function History() {
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [items, setItems] = useState([]);
  
  const handleOpenDialog = (item) => {
    setSelectedItem(item);
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  useEffect(() => {
    axios.get(`${serverUrl}/history`)
      .then(response => {
        setItems(response.data);
      })
      .catch(error => {
        console.error('Ошибка при получении данных:', error);
      });
  }, []);

  const exportToCSV = (apiData, fileName) => {
    const fileType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8";
    const fileExtension = ".xlsx";

    const ws = XLSX.utils.json_to_sheet(apiData);
    const wb = { Sheets: { "data": ws }, SheetNames: ["data"] };
    const excelBuffer = XLSX.write(wb, { bookType: "xlsx", type: "array" });
    const data = new Blob([excelBuffer], { type: fileType });
    FileSaver.saveAs(data, fileName + fileExtension);
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
                  История
                </MDTypography>
              </MDBox>
              <Box pt={6} pb={3}>
                <Grid container spacing={2} justifyContent="center">
                  {items.map((item, index) => (
                    <Grid item key={index}>
                      <HistoryItem item={item} onOpen={handleOpenDialog} />
                    </Grid>
                  ))}
                </Grid>
              </Box>
            </Card>
            {selectedItem && (
              <HistoryDetailsDialog open={openDialog} item={selectedItem} onClose={handleCloseDialog} />
            )}
          </Grid>
        </Grid>
        <Box textAlign="center" mt={4}>
          <MDButton
            variant="contained"
            color="info"
            onClick={() => exportToCSV(items, "history_data")}
          >
            <MDTypography sx={{minHeight:'2rem', padding:'0.375rem 1.125rem'}} color="white">Экспортировать в excel</MDTypography>
          </MDButton>
        </Box>
      </MDBox>
    </DashboardLayout>
  );
}

export default History;
