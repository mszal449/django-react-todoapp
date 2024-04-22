import { createContext } from "react";
import { ITask } from "../types/Task.type";
import { useState } from "react";
import axios from "axios";

export const TaskContext = createContext<{
    tasks: ITask[];
    fetchTasks: () => void;
    addTask: (title: string, description: string) => void;
    updateTask: (id: number, updatedTaskData: Partial<ITask>) => void;
    toggleFavorite: (id: number) => void;
    deleteTask: (id: number) => void;
}> ({
    tasks: [],
    fetchTasks: () => {},
    addTask: () => {},
    updateTask: () => {},
    toggleFavorite: () => {},
    deleteTask: () => {},
});

export default function TaskProvider({ children }: { children: React.ReactNode }) {
    const [tasks, setTasks] = useState<ITask[]>([]);

    async function fetchTasks() {
        try {
            const res = await axios.get("http://localhost:8000/api/tasks")
            setTasks(res.data.tasks)
        } catch (error) {
            console.error('Fetching tasks failed:', error);
        }
    } 


    async function addTask(title: string, description: string) {
        try {
            const res = await axios.post('http://localhost:8000/api/tasks/create', { title, description });
            await fetchTasks();
        } catch (error) {
            console.error('Adding task failed:', error);
        }
    }


    async function deleteTask(id: number) {
        try {
            await axios.delete(`http://localhost:8000/api/tasks/delete/${id}`);
            await fetchTasks();
        } catch (error) {
            console.error('Removing task failed:', error);
        }
    }


    async function updateTask(id: number, updatedTaskData: Partial<ITask>) {
        try {
            const res = await axios.put(`http://localhost:8000/api/tasks/update/${id}`, updatedTaskData);
            await fetchTasks();
        } catch (error) {
            console.error('Updating task failed:', error);
        }
    }

    async function toggleFavorite(id: number) {
        try {
            const res = await axios.put(`http://localhost:8000/api/tasks/update/${id}`, { fav: !tasks.find(task => task.id === id)?.fav });
            await fetchTasks();
        } catch (error) {
            console.error('Toggling favorite failed:', error);
        }
    }

    return (
        <TaskContext.Provider value={{ tasks, fetchTasks, addTask, deleteTask, updateTask, toggleFavorite}}>
          {children}
        </TaskContext.Provider>
    )


      
}