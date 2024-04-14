import Dashboard from "layouts/dashboard";
import History from "layouts/history";
import Cameras from "layouts/cameras";
import Feedback from "layouts/feedback";
import Icon from "@mui/material/Icon";
import ReviewsRoundedIcon from '@mui/icons-material/ReviewsRounded';

const routes = [
  {
    type: "collapse",
    name: "Панель управления",
    key: "dashboard",
    icon: <Icon fontSize="small">dashboard</Icon>,
    route: "/dashboard",
    component: <Dashboard />,
  },
  {
    type: "collapse",
    name: "История",
    key: "history",
    icon: <Icon fontSize="small">history</Icon>,
    route: "/history",
    component: <History />,
  },
  {
    type: "collapse",
    name: "Загрузка",
    key: "camera",
    icon: <Icon fontSize="small">camera</Icon>,
    route: "/cameras",
    component: <Cameras />,
  },
  {
    type: "collapse",
    name: "Отзывы",
    key: "feedback",
    icon: <ReviewsRoundedIcon/>,
    route: "/feedback",
    component: <Feedback />,
  },
];

export default routes;
