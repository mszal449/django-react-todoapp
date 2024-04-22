import React from "react";
import TaskProvider from "./providers/TaskProvider";
import { useEffect } from "react";
import TasksList from "./components/TasksList";
import TaskForm from "./components/TaskForm";

interface ITask {
    title:string;
    description: string;
    done:boolean;
    fav:boolean
}

// First type: props type
// Second type: 
export default function App() {
    return (
      <div className="App">
        <TaskProvider>
          <h1 className="main-title">My tasks</h1>
          <TaskForm />
          <TasksList />

        </TaskProvider>
      </div>
    );
}
  