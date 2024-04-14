import React, { forwardRef } from 'react';
import PropTypes from 'prop-types';
import { Dialog, styled } from '@mui/material';

const MDDialogRoot = styled(Dialog)(({ theme, ownerState }) => {
  const { palette } = theme;
  const { bgColor } = ownerState;
  
  const greyColors = {
    "grey-100": palette.grey[100],
    "grey-200": palette.grey[200],
    "grey-300": palette.grey[300],
    "grey-400": palette.grey[400],
    "grey-500": palette.grey[500],
    "grey-600": palette.grey[600],
    "grey-700": palette.grey[700],
    "grey-800": palette.grey[800],
    "grey-900": palette.grey[900],
  };

  // В зависимости от темы и заданного фона, выбираем соответствующий цвет
  const backgroundColor = theme.palette.mode === 'dark'
    ? palette.white
    : palette.background.sidenav;

  return {
    '& .MuiDialog-paper': {
      backgroundColor,
      color: theme.palette.mode === 'dark' ? palette.common.white : palette.text.primary,
    },
  };
});

const MDDialog = forwardRef(({ bgColor = "grey-100", ...rest }, ref) => (
  <MDDialogRoot
    ref={ref}
    ownerState={{ bgColor }}
    {...rest}
  />
));

MDDialog.propTypes = {
  bgColor: PropTypes.oneOf([
    "grey-100",
    "grey-200",
    "grey-300",
    "grey-400",
    "grey-500",
    "grey-600",
    "grey-700",
    "grey-800",
    "grey-900",
  ]),
};

export default MDDialog;
