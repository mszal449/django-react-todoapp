import { useContext } from "react";
import { TaskContext } from "./TaskProvider";

export default function useTask() {
    const context = useContext(TaskContext);
    if (!context) {
        throw new Error("bad provider");
      }
      return context;
}
