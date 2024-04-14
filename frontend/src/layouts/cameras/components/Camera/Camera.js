import { useState } from "react";
import Grid from "@mui/material/Grid";
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import { useDropzone } from "react-dropzone";
import serverUrl from 'config';
import axios from 'axios';
import { Box, Card, CircularProgress, Dialog, DialogContent, DialogTitle, Typography } from "@mui/material";
import MDBox from "components/MDBox";
import MDSnackbar from "components/MDSnackbar";
import MDDialog from "components/MDDialog";
import MDTypography from "components/MDTypography";
import HistoryDetailsDialog from "layouts/history/data/HistoryDetailsDialog";

function Cameras() {
  const [open, setOpen] = useState(false);
  const [dialogContent, setDialogContent] = useState("Подготовка к загрузке...");
  const [showSnackbar, setShowSnackbar] = useState(false);
  const [snackbarProps, setSnackbarProps] = useState({
    color: "info",
    title: "Загрузка",
    loadingProgress: 0,
    content: "",
  });
  const [elementDetails, setElementDetails] = useState(null); 
  const [openHistoryDetails, setOpenHistoryDetails] = useState(false); 

  const handleClose = () => {
    setOpen(false);
  };

  const toggleSnackbar = (open) => {
    setShowSnackbar(open);
    if (open) {
      setTimeout(() => {
        setShowSnackbar(false);
      }, 3000);
    }
  };

  const onDrop = async (acceptedFiles) => {
    setOpen(true);
    setDialogContent("Загрузка и анализ изображения...");

    const formData = new FormData();
    formData.append("file", acceptedFiles[0]); 

    const requestConfig = {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      onUploadProgress: (progressEvent) => {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        if (percentCompleted == 100) {
          setDialogContent("Анализ файла...");
        }
        else
          setDialogContent("Загрузка файла: " + percentCompleted + "%");
      }
    };

    try {
      const response = await axios.post(`${serverUrl}/upload-image`, formData, requestConfig);

      const detailsResponse = response.data;
      if (detailsResponse.data) {
        setSnackbarProps({
          color: "success",
          title: "Успешно",
          content: "Успешно загружено и распознано",
        });
        toggleSnackbar();
        handleClose();
        setElementDetails(detailsResponse.data); 
        setOpenHistoryDetails(true);
      }
    } catch (error) {
      handleClose();
      setSnackbarProps({
        color: "error",
        title: "Ошибка",
        content: "Ошибка при обработке файла",
      });
      toggleSnackbar();
    }
  };

  const { getRootProps, getInputProps } = useDropzone({ onDrop, accept: 'image/jpeg, image/png' });

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <MDBox pt={6} pb={3}>
        <Grid container spacing={6}>
          <Grid item xs={12}>
            <Grid
                {...getRootProps()}
                elevation={3}
                sx={{
                  padding: "20px",
                  border: "1px dashed #ccc",
                  borderRadius: "4px",
                  textAlign: "center",
                }}
              >
                <input {...getInputProps()} />
                <MDTypography variant="h6">Перетащите или выберите изображение для анализа</MDTypography>
              </Grid>
          </Grid>
        </Grid>
      </MDBox>
      <MDDialog
        open={open}
        onClose={handleClose}
        aria-labelledby="loading-dialog-title"
        aria-describedby="loading-dialog-description"
      >
        <DialogTitle id="loading-dialog-title" sx={{textAlign:'center'}}>{"Статус загрузки"}</DialogTitle>
        <DialogContent>
          <Box display="flex" flexDirection="column" alignItems="center">
            <CircularProgress />
            <MDTypography variant="body1" style={{ marginTop: 20 }}>
              {dialogContent}
            </MDTypography>
          </Box>
        </DialogContent>
      </MDDialog>
      <MDSnackbar
        color={snackbarProps.color}
        title={snackbarProps.title}
        loadingProgress={snackbarProps.loadingProgress}
        content={snackbarProps.content}
        open={showSnackbar}
        close={toggleSnackbar}
      />
      {openHistoryDetails && elementDetails && (
        <HistoryDetailsDialog 
          open={openHistoryDetails} 
          item={elementDetails} 
          onClose={() => setOpenHistoryDetails(false)}
        />
      )}
    </DashboardLayout>
  );
}

export default Cameras;
