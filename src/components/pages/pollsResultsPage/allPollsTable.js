import React,{ useState, useEffect }from "react"
import { ReactTabulator } from 'react-tabulator';
import "tabulator-tables/dist/css/tabulator.min.css";
import {APIBase} from "../../../constAttributes";



export const AllPollsTable = () => {

    //const [data,setData] = useState([{id:1, name:"Dutchman", noOfRequest: 42}])
    const [data,setData] = useState([])

    function getData() {
        fetch(APIBase + "/all_polls_data",{method: 'GET', mode: "cors"})
            .then(res => res.json())
            .then(data => {
                console.log(data);
                let count = Object.keys(data).length;
                console.log(count);
                let lst = [];
                for (let i = 0; i < count; i++){
                    lst.push(data[i]);
                }
                console.log(lst);
                setData(lst);
                console.log(data)
            })
            .catch( (e) => {
                alert("error has occurred");
                console.log(e);
            })
    }

    useEffect(()=>{
      getData()
    },[])

    const options = {
    height: '100%',
    ajaxURL: 'http://example.com',
    ajaxProgressiveLoad: 'scroll',
    ajaxError: (error) => {
      console.log('ajaxError ', error);
    },
  };

    const columns=[
        /*{
            title:"name",
            field:"name",
        },
        {
            title:"Number of Request",
            field:"noOfRequest",
        }*/
        {
            title: "question",
            field: "question",
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