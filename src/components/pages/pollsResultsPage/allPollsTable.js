import React,{ useState, useEffect }from "react"
import { ReactTabulator } from 'react-tabulator';
import "tabulator-tables/dist/css/tabulator.min.css";




export const AllPollsTable = () => {

    const [data,setData] = useState([{id:1, name:"Dutchman", noOfRequest: 42}])

    function getData() {
    }

    const options = {
    height: '100%',
    ajaxURL: 'http://example.com',
    ajaxProgressiveLoad: 'scroll',
    ajaxError: (error) => {
      console.log('ajaxError ', error);
    },
  };

    const columns=[
        {
            title:"name",
            field:"name",
        },
        {
            title:"Number of Request",
            field:"noOfRequest",
        }
    ]

    return(
        <div className = "AllPollsTable">
            <ReactTabulator
        columns={columns}
        layout="fitColumns"
        data={data} // here is the state of the table
        options={options}
        />
        </div>
    );
}