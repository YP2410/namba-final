import React,{ useState, useEffect }from "react"
import {reactFormatter, ReactTabulator} from 'react-tabulator';
import "tabulator-tables/dist/css/tabulator.min.css";
import {APIBase} from "../../../constAttributes";
import Tabulator from "tabulator-tables";
import {useAppContext} from "../../../lib/contextLib";
import {UsersPage} from "./usersPage";



export const AllVotesTable = () => {
    //const [data,setData] = useState([{id:1, name:"Dutchman", noOfRequest: 42}])
    const [data,setData] = useState([]);
    const {userData} = useAppContext();
    const columns=[

        {
            title: "poll_ID",
            field: "poll_ID",
        },
        {
            title: "question",
            field: "question",
        },
        {
            title: "answers",
            field: "answers",
        },
    ]



    function getData() {

        fetch(APIBase + "/specific_user_answers/" + userData.user_ID,{method: 'GET', mode: "cors"})
            .then(res => res.json())
            .then(data => {
                //console.log("reload");
                //console.log(data);
                let count = Object.keys(data).length;
                //console.log(count);
                let lst = [];
                for (let i = 0; i < count; i++){
                    lst.push(data[i]);
                }
                //console.log(lst);
                setData(lst);
                //console.log(data)
            })
            .catch( (e) => {
                alert("error has occurred");
                //console.log(e);
            })
    }

    function rowClicked(e, row){
        //alert(row.getData());
        //console.log(row.getData());
        //setUserData(row.getData());
        //console.log(row.getData());
    }


    useEffect(()=>{
        //console.log("use Effect is on");
        getData();
    },[])

    const options = {
        height: '100%',
        debugInvalidOptions: false,
        selectable: 1,
        layout: "fitColumns",
        pagination: "local",
        paginationSize: 5,
    };


    return(
        <div className="AllVotesTable">
            <ReactTabulator
                columns={columns}
                data={data} // here is the state of the table
                options={options}
                rowClick={(e,row) => rowClicked(e,row)}
            />
        </div>
    );
}