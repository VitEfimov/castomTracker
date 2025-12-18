import React, { useMemo } from 'react';
import { AgGridReact } from 'ag-grid-react'; // React Data Grid Component
import "ag-grid-community/styles/ag-grid.css"; // Mandatory CSS required by the grid
import "ag-grid-community/styles/ag-theme-quartz.css"; // Optional Theme applied to the grid

const Grid = ({ rowData }) => {
    // Column Definitions: Defines the columns to be displayed.
    const colDefs = useMemo(() => [
        { field: "hts_code", headerName: "HTS Code", filter: true },
        { field: "full_name", headerName: "Description", flex: 2, filter: true, wrapText: true, autoHeight: true },
        {
            headerName: "Duty Rate",
            valueGetter: (p) => p.data.duty?.rate || 'N/A',
            filter: true
        },
        {
            headerName: "Restrictions",
            autoHeight: true,
            cellRenderer: (p) => {
                const restrictions = p.data.restrictions || [];
                if (!restrictions.length) return "None";
                return (
                    <ul style={{ margin: 0, paddingLeft: '1.2rem' }}>
                        {restrictions.map((r, idx) => (
                            <li key={idx}><strong>{r.agency}</strong>: {r.description}</li>
                        ))}
                    </ul>
                );
            }
        },
        {
            field: "certifications",
            headerName: "Certifications",
            valueFormatter: (p) => Array.isArray(p.value) ? p.value.join(", ") : p.value,
            filter: true
        },
        { field: "score", headerName: "Match Score", hide: true, sort: 'desc' }
    ], []);

    const defaultColDef = useMemo(() => {
        return {
            flex: 1,
            minWidth: 100,
            filter: true,
            sortable: true,
            resizable: true,
        };
    }, []);

    return (
        <div
            className="ag-theme-quartz-dark" // applying the grid theme
            style={{ height: '100%', width: '100%' }} // the grid will fill the size of the parent container
        >
            <AgGridReact
                rowData={rowData}
                columnDefs={colDefs}
                defaultColDef={defaultColDef}
                pagination={true}
                paginationPageSize={20}
            />
        </div>
    );
}

export default Grid;
