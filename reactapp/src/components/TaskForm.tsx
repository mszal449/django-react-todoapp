import { useState } from "react";
import useTask from "../providers/useTask"


export default function TaskForm() {
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [error, setError] = useState(false)
    const { addTask } = useTask();

    return (
        <div className="task-form"
        onSubmit={(e)=> {
            e.preventDefault();
            if(title.trim() === "" && description.trim() === "") {
                setError(true);
                return;
            }
            addTask(title, description);
            setTitle("");
            setDescription("");
            setError(false);
        }}>
            <form className="">
                <input
                    className="form-textfield" 
                    type="text"
                    placeholder="Title"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                />
                <input 
                    className="form-textfield" 
                    type="text"
                    placeholder="Description"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                />
                {error && <p className="error-message">Please provide title and description.</p>}
                <button className="submit-btn" type="submit">Submit</button>
            </form>
        </div>
    )
}