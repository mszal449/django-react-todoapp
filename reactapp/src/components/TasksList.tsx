import React, { Component } from "react";
import { TaskContext } from "../providers/TaskProvider";
import { useContext, useEffect } from "react";

const TasksList = () => {
    const { tasks, fetchTasks, deleteTask } = useContext(TaskContext);

    useEffect(() => {
        const getTasks = async () => {
            try {
                await fetchTasks();
            } catch (error) {
                console.error("Error fetching tasks:", error);
            }
        };

        getTasks();
    }, []);


    return (
        <div className="task-list">
            {tasks && tasks.map(task => (
                <div className="list-element" key={task.id}>
                    <div>
                        {task.title}
                    </div>
                    <button onClick={()=> {
                        deleteTask(task.id)
                    }}>Delete</button>
                </div>
            ))}
        </div>
    );
};


export default TasksList;
