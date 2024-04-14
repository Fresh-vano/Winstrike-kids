import Grid from "@mui/material/Grid";
import MDBox from "components/MDBox";
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import ReportsBarChart from "examples/Charts/BarCharts/ReportsBarChart";
import ReportsLineChart from "examples/Charts/LineCharts/ReportsLineChart";
import ComplexStatisticsCard from "examples/Cards/StatisticsCards";
import { useEffect, useState } from "react";
import serverUrl from 'config';
import PriorityHighIcon from '@mui/icons-material/PriorityHigh';
import VerifiedIcon from '@mui/icons-material/Verified';
import CancelIcon from '@mui/icons-material/Cancel';
import MemoryIcon from '@mui/icons-material/Memory';
import axios from 'axios';

function Dashboard() {
  const [elementChartData, setElementChartData] = useState(
    {
      labels: ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
      datasets: { label: "Распознано товаров", data: [0, 0, 0, 0, 0, 0, 0] },
    }
  );
  const [recomendedChartData, setRecomendedChartData] = useState(
    {
      labels: ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
      datasets: { label: "Кол-во рекомендуемых товаров", data: [0, 0, 0, 0, 0, 0, 0] },
    }
  );
  const [notRecomendedChartData, setNotRecomendedChartData] = useState(
    {
      labels: ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
      datasets: { label: "Кол-во не рекомендуемых товаров", data: [0, 0, 0, 0, 0, 0, 0] },
    }
  );

  const [statisticsData, setStatisticsData] = useState({
    today_element: 0,
    partially_recommended: 0,
    recomended: 0,
    not_recomended: 0,
  });

  useEffect(() => {
    axios.get(`${serverUrl}/all`)
    .then(response => {
      setStatisticsData(prevData => ({
        ...prevData,
        today_element: response.data.count,
      }));
    })
    .catch(error => {
      console.error('Ошибка при получении данных:', error);
    });

    axios.get(`${serverUrl}/partially_recommended`)
      .then(response => {
        setStatisticsData(prevData => ({
          ...prevData,
          partially_recommended: response.data.count,
        }));
        setBarChartData(response.data.chartData);
      })
      .catch(error => {
        console.error('Ошибка при получении данных:', error);
      });

    axios.get(`${serverUrl}/recomended`)
      .then(response => {
        setStatisticsData(prevData => ({
          ...prevData,
          recomended: response.data.count,
        }));
        setSalesChartData(response.data.chartData);
      })
      .catch(error => {
        console.error('Ошибка при получении данных:', error);
      });

    axios.get(`${serverUrl}/not_recomended`)
      .then(response => {
        setStatisticsData(prevData => ({
          ...prevData,
          not_recomended: response.data.count,
        }));
        setTasksChartData(response.data.chartData);
      })
      .catch(error => {
        console.error('Ошибка при получении данных:', error);
      });

    axios.get(`${serverUrl}/chart/elements`)
      .then(response => {
        setElementChartData(response.data);
      })
      .catch(error => {
        console.error('Ошибка при получении данных:', error);
      });

    axios.get(`${serverUrl}/chart/recomended`)
      .then(response => {
        setRecomendedChartData(response.data);
      })
      .catch(error => {
        console.error('Ошибка при получении данных:', error);
      });

    axios.get(`${serverUrl}/chart/not_recomended`)
      .then(response => {
        setNotRecomendedChartData(response.data);
      })
      .catch(error => {
        console.error('Ошибка при получении данных:', error);
      });
  }, []);

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <MDBox py={3}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6} lg={3}>
            <MDBox mb={1.5}>
              <ComplexStatisticsCard
                color="dark"
                icon={<MemoryIcon/>}
                title="Обработано за сегодня"
                count={statisticsData.today_element}
              />
            </MDBox>
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <MDBox mb={1.5}>
              <ComplexStatisticsCard
                icon={<PriorityHighIcon/>}
                title="Частично рекомендуемые"
                count={statisticsData.partially_recommended}
              />
            </MDBox>
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <MDBox mb={1.5}>
              <ComplexStatisticsCard
                color="success"
                icon={<VerifiedIcon/>}
                title="Рекомендуемые товары"
                count={statisticsData.recomended}
              />
            </MDBox>
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <MDBox mb={1.5}>
              <ComplexStatisticsCard
                color="primary"
                icon={<CancelIcon/>}
                title="Не рекомендуемые товары"
                count={statisticsData.not_recomended}
              />
            </MDBox>
          </Grid>
        </Grid>
        <MDBox mt={4.5}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6} lg={4}>
              <MDBox mb={3}>
                <ReportsBarChart
                  color="dark"
                  title="Записей за день"
                  description="Количество обработанных записей по дням"
                  chart={elementChartData}
                />
              </MDBox>
            </Grid>
            <Grid item xs={12} md={6} lg={4}>
              <MDBox mb={3}>
                <ReportsLineChart
                  color="success"
                  title="Рекомендуемые товары"
                  description="Число рекомендуемых товаров в соответствии с рекомендациями ВОЗ за последнюю неделю"
                  chart={recomendedChartData}
                />
              </MDBox>
            </Grid>
            <Grid item xs={12} md={6} lg={4}>
              <MDBox mb={3}>
                <ReportsLineChart
                  color="primary"
                  title="Не рекомендуемые товары"
                  description="Число товаров имеющие нарущения рекомендаций ВОЗ за последнюю неделю"
                  chart={notRecomendedChartData}
                />
              </MDBox>
            </Grid>
          </Grid>
        </MDBox>
      </MDBox>
    </DashboardLayout>
  );
}

export default Dashboard;
