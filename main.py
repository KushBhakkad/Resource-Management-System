import tkinter as tk
from tkinter import messagebox

class Hospital:
    def __init__(self, name, normal_patients, critical_patients):
        self.name = name
        self.critical_patients = critical_patients
        self.normal_patients = normal_patients

class Vendor:
    def __init__(self):
        self.normal_equipment_per_patient = 2
        self.critical_equipment_per_patient = 5

def calculate_minimum_order(hospitals, vendor):
    total_normal_equipment = sum(h.normal_patients * vendor.normal_equipment_per_patient for h in hospitals)
    total_critical_equipment = sum(h.critical_patients * vendor.critical_equipment_per_patient for h in hospitals)
    total_equipment_needed = total_normal_equipment + total_critical_equipment
    min_order_grosses = (total_equipment_needed + 143) // 144
    return min_order_grosses * 144

def calculate_all_paths(distances, hospitals):
    n = len(hospitals)
    all_paths = []
    path_costs = []
    path = []
    visited = [False] * n

    def dfs(u, cost, count):
        path.append(u)
        if count == n:  # Once all hospitals have been visited
            all_paths.append(list(path))  # Add the current path to the list of paths
            path_costs.append(cost)  # Record the cost of this path
            path.pop()  # Backtrack
            return
        visited[u] = True
        for v in range(n):
            if not visited[v] and distances[u][v] != -1:  # Check for valid path
                dfs(v, cost + distances[u][v], count + 1)  # Recursive DFS call
        visited[u] = False
        path.pop()

    for i in range(n):  # Start DFS from every hospital
        dfs(i, 0, 1)

    return all_paths, path_costs

def calculate_paths_and_display():
    all_paths, path_costs = calculate_all_paths(distances, hospitals)

    if not all_paths:
        distance_display.insert(tk.END,"No valid paths found between the hospitals. Please check the distance inputs.\n")
        return

    distance_display.insert(tk.END, "\nAll possible paths and their costs:\n")
    for i in range(len(all_paths)):
        path_str = " -> ".join([hospitals[j].name for j in all_paths[i]])
        distance_display.insert(tk.END, f"   Path: {path_str} | Cost: {path_costs[i]} km\n")

    min_cost = min(path_costs)
    min_cost_paths = [all_paths[i] for i in range(len(path_costs)) if path_costs[i] == min_cost]

    distance_display.insert(tk.END, "\nMinimum cost paths:\n")
    for path in min_cost_paths:
        path_str = " -> ".join([hospitals[j].name for j in path])
        distance_display.insert(tk.END, f"   Path: {path_str} | Cost: {min_cost} km\n")


def calculate_shortest_path():
    all_paths, path_costs = calculate_all_paths(distances, hospitals)
    if not path_costs:
        return []

    min_cost = min(path_costs)
    min_cost_paths = [all_paths[i] for i in range(len(path_costs)) if path_costs[i] == min_cost]
    return min_cost_paths

def distribute_resources(hospitals, total_resources, distances):
    shortest_paths = calculate_shortest_path()

    remaining_resources = total_resources
    individual_needs = [(hospital.normal_patients * 2) + (hospital.critical_patients * 5) for hospital in hospitals]

    sorted_hospitals = sorted(range(len(hospitals)), key=lambda i: shortest_paths[0].index(i))

    for i in sorted_hospitals:
        hospital = hospitals[i]
        if remaining_resources >= individual_needs[i]:
            remaining_resources -= individual_needs[i]
            resources_output.insert(tk.END, f"Hospital {hospital.name} received its required {individual_needs[i]} resources.\n")
        else:
            resources_output.insert(tk.END, f"Hospital {hospital.name} received partial resources.\n")
            individual_needs[i] -= remaining_resources
            remaining_resources = 0
            break

    if remaining_resources > 0:
        surplus = [remaining_resources // len(hospitals) + (1 if i < remaining_resources % len(hospitals) else 0) for i
                   in range(len(hospitals))]
        for i, hospital in enumerate(hospitals):
            resources_output.insert(tk.END, f"Hospital {hospital.name} received a surplus of {surplus[i]} resources.\n")

def add_distance():
    try:
        from_hospital = int(from_hospital_entry.get()) - 1
        to_hospital = int(to_hospital_entry.get()) - 1
        distance = int(distance_entry.get())

        if 0 <= from_hospital < len(hospitals) and 0 <= to_hospital < len(hospitals):
            # Update distance matrix
            distances[from_hospital][to_hospital] = distance
            distances[to_hospital][from_hospital] = distance
            # Display the entered distance
            distance_display.insert(tk.END, f"Distance from {hospitals[from_hospital].name} to {hospitals[to_hospital].name} is {distance} km.\n")
        else:
            messagebox.showerror("Invalid Input", "Invalid hospital number.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid distance values.")


def submit_data():
    try:
        hospital_name = hospital_name_entry.get()
        normal_patients = int(normal_patients_entry.get())
        critical_patients = int(critical_patients_entry.get())
        new_hospital = Hospital(hospital_name, normal_patients, critical_patients)
        hospitals.append(new_hospital)
        update_hospitals_list()
        hospital_name_entry.delete(0, tk.END)
        normal_patients_entry.delete(0, tk.END)
        critical_patients_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for patients.")

def update_data():
    try:
        hospital_name = hospital_name_entry.get()
        normal_patients = int(normal_patients_entry.get())
        critical_patients = int(critical_patients_entry.get())

        # Find the hospital to update
        for hospital in hospitals:
            if hospital.name == hospital_name:  # Check for matching hospital name
                hospital.normal_patients = normal_patients  # Update normal patients
                hospital.critical_patients = critical_patients  # Update critical patients
                break  # Exit the loop after updating

        update_hospitals_list()  # Refresh the displayed list of hospitals
        hospital_name_entry.delete(0, tk.END)
        normal_patients_entry.delete(0, tk.END)
        critical_patients_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for patients.")

def update_hospitals_list():
    hospitals_listbox.delete(0, tk.END)
    for hospital in hospitals:
        hospitals_listbox.insert(tk.END, f"Name: {hospital.name}, Critical: {hospital.critical_patients}, Normal: {hospital.normal_patients}")

def calculate_resources():
    total_resources = calculate_minimum_order(hospitals, vendor)
    result_label.config(text=f"Total resources needed: {total_resources}")
    distribute_resources(hospitals, total_resources, distances)

root = tk.Tk()
root.title("Hospital Resource Management")
root.geometry("480x500")

hospitals = []
vendor = Vendor()
distances = [[-1] * 10 for _ in range(10)]  # Initialize distance matrix for up to 10 hospitals

canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

scrollable_frame = tk.Frame(canvas)
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

hospital_name_label = tk.Label(scrollable_frame, text="Hospital Name:")
hospital_name_label.grid(row=0, column=0, padx=10, pady=10)
hospital_name_entry = tk.Entry(scrollable_frame)
hospital_name_entry.grid(row=0, column=1, padx=10, pady=10)

normal_patients_label = tk.Label(scrollable_frame, text="Normal Patients:")
normal_patients_label.grid(row=1, column=0, padx=10, pady=10)
normal_patients_entry = tk.Entry(scrollable_frame)
normal_patients_entry.grid(row=1, column=1, padx=10, pady=10)

critical_patients_label = tk.Label(scrollable_frame, text="Critical Patients:")
critical_patients_label.grid(row=2, column=0, padx=10, pady=10)
critical_patients_entry = tk.Entry(scrollable_frame)
critical_patients_entry.grid(row=2, column=1, padx=10, pady=10)

submit_button = tk.Button(scrollable_frame, text="Add Hospital", command=submit_data)
submit_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

submit_button = tk.Button(scrollable_frame, text="Update Hospital", command=update_data)
submit_button.grid(row=3, column=1, columnspan=2, padx=10, pady=10)

hospitals_listbox = tk.Listbox(scrollable_frame, width=50)
hospitals_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

from_hospital_label = tk.Label(scrollable_frame, text="From Hospital (number):")
from_hospital_label.grid(row=5, column=0, padx=10, pady=10)
from_hospital_entry = tk.Entry(scrollable_frame)
from_hospital_entry.grid(row=5, column=1, padx=10, pady=10)

to_hospital_label = tk.Label(scrollable_frame, text="To Hospital (number):")
to_hospital_label.grid(row=6, column=0, padx=10, pady=10)
to_hospital_entry = tk.Entry(scrollable_frame)
to_hospital_entry.grid(row=6, column=1, padx=10, pady=10)

distance_label = tk.Label(scrollable_frame, text="Distance (km):")
distance_label.grid(row=7, column=0, padx=10, pady=10)
distance_entry = tk.Entry(scrollable_frame)
distance_entry.grid(row=7, column=1, padx=10, pady=10)

add_distance_button = tk.Button(scrollable_frame, text="Add Distance", command=add_distance)
add_distance_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

distance_display_frame = tk.Frame(scrollable_frame)
distance_display_frame.grid(row=9, column=0, columnspan=2, padx=10, pady=10)
distance_display_scrollbar = tk.Scrollbar(distance_display_frame)
distance_display_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

distance_display = tk.Text(distance_display_frame, height=15, width=50, yscrollcommand=distance_display_scrollbar.set)
distance_display.pack(side=tk.LEFT)
distance_display_scrollbar.config(command=distance_display.yview)

find_shortest_distance_button = tk.Button(scrollable_frame, text="Find Shortest Distance", command=calculate_paths_and_display)
find_shortest_distance_button.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

result_label = tk.Label(scrollable_frame, text="Total resources needed:")
result_label.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

calculate_button = tk.Button(scrollable_frame, text="Calculate Resources", command=calculate_resources)
calculate_button.grid(row=12, column=0, columnspan=2, padx=10, pady=10)

resources_output = tk.Text(scrollable_frame, height=10, width=50)
resources_output.grid(row=13, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()