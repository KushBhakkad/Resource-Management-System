#include <bits/stdc++.h>
using namespace std;

struct Hospital {
    string name;
    int capacity_of_critical_patients = 35;
    int capacity_of_normal_patients = 65;
    int critical_patients;
    int normal_patients;
    int current_resources = 0;
};

struct Vendor {
    int normal_equipment_per_patient = 2;
    int critical_equipment_per_patient = 5;
};

int calculate_minimum_order(vector<Hospital>& hospitals, Vendor& vendor) {
    int total_normal_equipment = 0;
    int total_critical_equipment = 0;

    for (const auto& hospital : hospitals) {
        total_normal_equipment += hospital.normal_patients * vendor.normal_equipment_per_patient;
        total_critical_equipment += hospital.critical_patients * vendor.critical_equipment_per_patient;
    }

    int total_equipment_needed = total_normal_equipment + total_critical_equipment;
    int min_order_grosses = (total_equipment_needed + 143) / 144;

    return min_order_grosses * 144;
}

void calculate_all_paths(vector<vector<int>>& dist, vector<Hospital>& hospitals, vector<vector<int>>& all_paths, vector<int>& path_costs) {
    int n = dist.size();
    vector<int> path;
    vector<bool> visited(n, false);
    function<void(int, int, int)> dfs = [&](int u, int cost, int count) {
        path.push_back(u);
        if (count == n) {
            all_paths.push_back(path);
            path_costs.push_back(cost);
            path.pop_back();
            return;
        }
        visited[u] = true;
        for (int v = 0; v < n; ++v) {
            if (!visited[v] && dist[u][v] != -1) {
                dfs(v, cost + dist[u][v], count + 1);
            }
        }
        visited[u] = false;
        path.pop_back();
    };

    for (int i = 0; i < n; ++i) {
        dfs(i, 0, 1);
    }
}

void distribute_resources(vector<Hospital>& hospitals, int total_resources) {
    int remaining_resources = total_resources;
    vector<int> individual_needs(hospitals.size(), 0);

    for (int i = 0; i < hospitals.size(); ++i) {
        individual_needs[i] = (hospitals[i].normal_patients * 2) + (hospitals[i].critical_patients * 5);
    }

    for (int i = 0; i < hospitals.size(); ++i) {
        if (remaining_resources >= individual_needs[i]) {
            remaining_resources -= individual_needs[i];
            cout << "Hospital " << hospitals[i].name << " received its required resources." << endl;
        } else {
            cout << "Hospital " << hospitals[i].name << " received partial resources." << endl;
            individual_needs[i] -= remaining_resources;
            remaining_resources = 0;
            break;
        }
    }

    if (remaining_resources > 0) {
        vector<int> surplus(hospitals.size(), 0);
        for (int i = 0; i < hospitals.size(); ++i) {
            surplus[i] = remaining_resources / hospitals.size() + (i < remaining_resources % hospitals.size() ? 1 : 0);
        }

        for (int i = 0; i < hospitals.size(); ++i) {
            hospitals[i].capacity_of_normal_patients += surplus[i];
            hospitals[i].capacity_of_critical_patients += surplus[i];
            cout << "Hospital " << hospitals[i].name << " received a surplus of " << surplus[i] << " resources." << endl;
        }
    }
}

bool check_resources_needed(const vector<Hospital>& hospitals) {
    for (const auto& hospital : hospitals) {
        int total_needed = (hospital.normal_patients * 2) + (hospital.critical_patients * 5);
        if (total_needed > (hospital.capacity_of_normal_patients + hospital.capacity_of_critical_patients)) {
            return true;
        }
    }
    return false;
}

void update_patient_counts(vector<Hospital>& hospitals) {
    for (auto& hospital : hospitals) {
        int discharged_critical, discharged_normal;
        int new_critical, new_normal;

        cout << "Enter the number of critical patients discharged from " << hospital.name << ": ";
        cin >> discharged_critical;
        cout << "Enter the number of new critical patients admitted to " << hospital.name << ": ";
        cin >> new_critical;

        cout << "Enter the number of normal patients discharged from " << hospital.name << ": ";
        cin >> discharged_normal;
        cout << "Enter the number of new normal patients admitted to " << hospital.name << ": ";
        cin >> new_normal;

        hospital.critical_patients = max(0, hospital.critical_patients - discharged_critical + new_critical);
        hospital.normal_patients = max(0, hospital.normal_patients - discharged_normal + new_normal);
    }
}

int main() {
    int no_of_hospitals;
    cout << "Enter total number of hospitals: ";
    cin >> no_of_hospitals;
    cout << endl;

    cout << "NOTE: Each Hospital has a capacity of 35 critical and 65 normal patients." << endl << endl;

    Vendor vendor;
    vector<Hospital> hospitals(no_of_hospitals);
    vector<vector<int>> distance_graph(no_of_hospitals, vector<int>(no_of_hospitals, -1));

    for (int i = 0; i < no_of_hospitals; i++) {
        cout << endl << "   Enter name of hospital " << i + 1 << ": ";
        cin >> hospitals[i].name;
        do {
            cout << "   Enter the number of critical patients in " << hospitals[i].name << ": ";
            cin >> hospitals[i].critical_patients;
        } while (hospitals[i].critical_patients > hospitals[i].capacity_of_critical_patients || hospitals[i].critical_patients < 0);
        do {
            cout << "   Enter the number of normal patients in " << hospitals[i].name << ": ";
            cin >> hospitals[i].normal_patients;
        } while (hospitals[i].normal_patients > hospitals[i].capacity_of_normal_patients || hospitals[i].normal_patients < 0);
    }

    cout << endl << "Enter the distances between hospitals (enter -1 if there's no direct path): " << endl;
    for (int i = 0; i < no_of_hospitals; ++i) {
        for (int j = 0; j < no_of_hospitals; ++j) {
            if (i != j) {
                int dist;
                cout << "   Distance from " << hospitals[i].name << " to " << hospitals[j].name << ": ";
                cin >> dist;
                if (dist != -1) {
                    distance_graph[i][j] = dist;
                }
            }
        }
        cout << endl;
    }

    while (true) {
        vector<vector<int>> all_paths;
        vector<int> path_costs;
        calculate_all_paths(distance_graph, hospitals, all_paths, path_costs);

        cout << endl << "All possible paths and their costs:" << endl;
        for (int i = 0; i < all_paths.size(); ++i) {
            cout << "   Path: ";
            for (int j : all_paths[i]) {
                cout << hospitals[j].name << " -> ";
            }
            cout << "Cost: " << path_costs[i] << endl;
        }

        int min_cost = *min_element(path_costs.begin(), path_costs.end());
        vector<vector<int>> min_cost_paths;
        vector<int> min_cost_path_indices;

        for (int i = 0; i < path_costs.size(); ++i) {
            if (path_costs[i] == min_cost) {
                min_cost_paths.push_back(all_paths[i]);
                min_cost_path_indices.push_back(i);
            }
        }

        cout << endl << "Minimum cost paths:" << endl;
        for (const auto& path : min_cost_paths) {
            cout << "   Path: ";
            for (int j : path) {
                cout << hospitals[j].name << " -> ";
            }
            cout << "Cost: " << min_cost << endl;
        }

        int total_resources = calculate_minimum_order(hospitals, vendor);
        cout << "Total equipment needed (in units): " << total_resources << endl;

        vector<Hospital> hospitals_needing_resources;
        for (const auto& hospital : hospitals) {
            if (check_resources_needed({hospital})) {
                hospitals_needing_resources.push_back(hospital);
            }
        }

        if (!hospitals_needing_resources.empty()) {
            distribute_resources(hospitals_needing_resources, total_resources);
        }

        update_patient_counts(hospitals);

        if (!check_resources_needed(hospitals)) {
            cout << "All hospitals have sufficient resources." << endl;
            break;
        }
    }

    cout << "Program terminated." << endl;
    return 0;
}
