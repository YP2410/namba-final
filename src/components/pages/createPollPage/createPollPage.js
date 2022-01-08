import React, {useState} from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import "./createPollPage.css"
import {APIBase} from "../../../constAttributes";


const CreatePollPage = () => {
    //const {isAuthenticated} = useAppContext();
    //console.log(isAuthenticated);
    const [question, setQuestion] = useState("");
    const [option1, setoption1] = useState("");
    const [option2, setoption2] = useState("");
    const [option3, setoption3] = useState("");
    const [option4, setoption4] = useState("");
    const [multiple, setMultiple] = useState(false);

    function validateForm() {
    return question.length > 0 && option1.length > 0 && option2.length > 0;
  }

    function handleSubmit(event){
        event.preventDefault();
        //alert("Poll submitted!!")
        // init_poll: question, answers[]
        let answers = [option1, option2, option3, option4];
        //let data = {'question': question, 'answers': answers};
        fetch(APIBase + "/init_poll/" + question + "/" + answers +"/" + multiple, {
            method: 'POST',
            mode: "cors",
        })
            .then(res => res.json())
            .then(data => {
                console.log(data);
                if(data.result === true){
                    alert("submitted successfully")
                }
            })
            .catch(e => {
                console.log(e);
                alert("error has occurred");
            });

    }
    return(
        <div className={"createPollPage"}>
            <h1>Create Poll Page</h1>
            <Form onSubmit={handleSubmit}>
                <Form.Group size="lg" controlId="pollQuestion">
                    <Form.Label>Poll Question</Form.Label>
                    <Form.Control placeholder="Enter poll question (required)" value={question}
                                  as="textarea" rows="3"
                                  onChange={(e) => setQuestion(e.target.value)}/>
                </Form.Group>
                <Form.Group size="lg" controlId="pollOption1">
                    <Form.Control placeholder="Option 1 (required)" value={option1}
                                  onChange={(e) => setoption1(e.target.value)}/>
                </Form.Group>
                <Form.Group size="lg" controlId="pollOption2">
                    <Form.Control placeholder="Option 2 (required)" value={option2}
                                  onChange={(e) => setoption2(e.target.value)}/>
                </Form.Group>
                <Form.Group size="lg" controlId="pollOption3">
                    <Form.Control placeholder="Option 3 (optional)" value={option3}
                                  onChange={(e) => setoption3(e.target.value)}/>
                </Form.Group>
                <Form.Group size="lg" controlId="pollOption4">
                    <Form.Control placeholder="Option 4 (optional)" value={option4}
                                  onChange={(e) => setoption4(e.target.value)}/>
                </Form.Group>
                <Form.Group size="lg" controlId="pollOption4">
                    <Form.Check label="multiple choice" checked={multiple} onChange={e => setMultiple(e.target.checked)}/>
                </Form.Group>
                <Button className="custom-btn" type="submit" block size="lg" disabled={!validateForm()} > Submit Poll</Button>
            </Form>
        </div>
    )
}

export default CreatePollPage;