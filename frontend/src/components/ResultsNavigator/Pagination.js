import React from "react";
import PropTypes from "prop-types";
import Pagination from '@mui/material/Pagination';
import PaginationItem from '@mui/material/PaginationItem';

const CustomPagination = ({ currentPage, totalPages, paginate }) => {
  const handlePageChange = (event, page) => {
    paginate(page);
  };

  return (
    <Pagination
      count={totalPages}
      page={currentPage}
      onChange={handlePageChange}
      renderItem={(item) => (
        <PaginationItem
          {...item}
          disabled={item.page === currentPage}
        />
      )}
    />
  );
};

export default CustomPagination;
