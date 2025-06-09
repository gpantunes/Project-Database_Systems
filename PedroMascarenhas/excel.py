import csv

test_params = {
    "Test 1": {"Warehouses": 5, "VUs": 5, "Duration": 5, "Ramp Up": 2, "Iterations": 10_000_000},
    "Test 2": {"Warehouses": 5, "VUs": 20, "Duration": 5, "Ramp Up": 2, "Iterations": 10_000_000},
    "Test 3": {"Warehouses": 10, "VUs": 20, "Duration": 5, "Ramp Up": 2, "Iterations": 10_000_000},
    "Test 4": {"Warehouses": 100, "VUs": 20, "Duration": 5, "Ramp Up": 2, "Iterations": 10_000_000}
}

results = {
    "Baseline": {
        "Test 1": [
            {"TPM": 198034, "NOPM": 86006, "JobId": "683F0C44E30F03E293438333"},
            {"TPM": 227845, "NOPM": 98889, "JobId": "683F0FE5C9B403E253438333"},
            {"TPM": 250041, "NOPM": 108618, "JobId": "683F1947A48203E283339373"},
            {"TPM": 222149, "NOPM": 96655, "JobId": "683F1C5B7A0103E253636313"},
            {"TPM": 207192, "NOPM": 90071, "JobId": "683F224A33DD03E213537333"},
            {"TPM": 221852, "NOPM": 95847, "JobId": ""},
        ],
        "Test 2": [
            {"TPM": 181238, "NOPM": 78615, "JobId": "683F2772165A03E253630303"},
            {"TPM": 216061, "NOPM": 93551, "JobId": "683F2AA98D6803E283235383"},
            {"TPM": 342125, "NOPM": 148720, "JobId": "683F30C4A44903E273938373"},
            {"TPM": 287786, "NOPM": 124718, "JobId": "683F32ECED5D03E263032393"},
            {"TPM": 287786, "NOPM": 124718, "JobId": "683F32ECED5D03E263032393"},
            {"TPM": 256802, "NOPM": 111651, "JobId": ""},
        ],
        "Test 3": [
            {"TPM": 228038, "NOPM": 99258, "JobId": "683F35F9BF3F03E243638393"},
            {"TPM": 239537, "NOPM": 104267, "JobId": "683F381F6DE603E233837303"},
            {"TPM": 277919, "NOPM": 120750, "JobId": "683F3AF1B50803E283536383"},
            {"TPM": 261872, "NOPM": 113927, "JobId": "68471ECDC2F403E253931303"},
            {"TPM": 242175, "NOPM": 105307, "JobId": "684720D4F85A03E283636333 "},
            {"TPM": 249908, "NOPM": 108701, "JobId": ""},
        ],
        "Test 4": [
            {"TPM": 129464, "NOPM": 56397, "JobId": "684342E8E0BA03E293235333"},
            {"TPM": 141175, "NOPM": 61333, "JobId": "684345AF883F03E253636363"},
            {"TPM": 112907, "NOPM": 49060, "JobId": "684348A24A5C03E253837383"},
            {"TPM": 143751, "NOPM": 62626, "JobId": "68434DF073B503E293637313"},
            {"TPM": 142468, "NOPM": 61955, "JobId": "684350A611B703E243433343"},
            {"TPM": 133953, "NOPM": 58274, "JobId": ""},
        ],

    },
    "Resources 1": {
        "Test 1": [
            {"TPM": 270447, "NOPM": 117450, "JobId": "684428E3F88303E223935323"},
            {"TPM": 269893, "NOPM": 117074, "JobId": "68442ACE1D5D03E283335383"},
            {"TPM": 288199, "NOPM": 125280, "JobId": "68442CB941B403E223032363"},
            {"TPM": 285778, "NOPM": 124005, "JobId": "68442EA5674403E233132333"},
            {"TPM": 286366, "NOPM": 124641, "JobId": "684430918C4403E213739313"},
            {"TPM": 280136, "NOPM": 121690, "JobId": ""},
        ],
        "Test 2": [
            {"TPM": 493017, "NOPM": 214041, "JobId": "68435A70E70703E213733353"},
            {"TPM": 401783, "NOPM": 174646, "JobId": "68435C4D3D6C03E243539313"},
            {"TPM": 469702, "NOPM": 204371, "JobId": "68435E291F6303E253037323"},
            {"TPM": 478894, "NOPM": 208216, "JobId": "6843FA3324D403E273138333"},
            {"TPM": 468511, "NOPM": 203616, "JobId": "6843FC264E4B03E203930303"},
            {"TPM": 462381, "NOPM": 200978, "JobId": ""},
        ]
    },
    "WriteAheadLog": {
        "Test 2": [
            {"TPM": 598019, "NOPM": 260032, "JobId": "68448882F72E03E233130393"},
            {"TPM": 517658, "NOPM": 224590, "JobId": "68448CA36D8A03E203336393"},
            {"TPM": 594534, "NOPM": 258654, "JobId": "684495529A4603E233037303"},
            {"TPM": 469691, "NOPM": 204344, "JobId": "6844974CC80803E203739303"},
            {"TPM": 561607, "NOPM": 244322, "JobId": "68449943F39403E273330333"},
            {"TPM": 548701, "NOPM": 238788, "JobId": ""},
        ]
    },
    "Final": {
        "Test 1": [
            {"TPM": 336333, "NOPM": 146127, "JobId": "6846DB6796CC03E213937393"},
            {"TPM": 345679, "NOPM": 150087, "JobId": "6846DD53BBEB03E283336373"},
            {"TPM": 328743, "NOPM": 142831, "JobId": "6846DF3FE19503E233532323"},
            {"TPM": 339024, "NOPM": 146926, "JobId": "6846E12C77C903E233432333"},
            {"TPM": 358392, "NOPM": 155869, "JobId": "6846E3192D3203E223730303"},
            {"TPM": 341234, "NOPM": 148368, "JobId": ""}
          ],
          "Test 2": [
            {"TPM": 528657, "NOPM": 230033, "JobId": "6844B21FC4B603E283839393"},
            {"TPM": 604513, "NOPM": 262917, "JobId": "6844B02496AB03E233830303"},
            {"TPM": 623815, "NOPM": 271011, "JobId": "6844B416F0F803E253933313"},
            {"TPM": 566122, "NOPM": 246325, "JobId": "6844B6111EF103E213630393"},
            {"TPM": 567733, "NOPM": 246404, "JobId": "6844B815525603E203337333"},
            {"TPM": 578568, "NOPM": 251738, "JobId": ""}
          ],
          "Test 3": [
            {"TPM": 568284, "NOPM": 246974, "JobId": "6846F990913903E273239363"},
            {"TPM": 561700, "NOPM": 243940, "JobId": "6846E9CA2A6603E253431333"},
            {"TPM": 598285, "NOPM": 260089, "JobId": "6846EBCE5D6503E253033353"},
            {"TPM": 555189, "NOPM": 241496, "JobId": "6846EDD0901B03E203334373"},
            {"TPM": 569799, "NOPM": 247617, "JobId": "6846EFD3C33503E293839323"},
            {"TPM": 570651, "NOPM": 248823, "JobId": ""}
          ],
        "Test 4": [
            {"TPM": 219140, "NOPM": 95167, "JobId": "68471846DEE203E253831323"},
            {"TPM": 188341, "NOPM": 82078, "JobId": "684710C867A403E223934313"},
            {"TPM": 222056, "NOPM": 96485, "JobId": "6847019256BB03E253431343"},
            {"TPM": 215382, "NOPM": 93615, "JobId": "684704E3510A03E253634373"},
            {"TPM": 229305, "NOPM": 99909, "JobId": "68470BDA77A803E223637373"},
            {"TPM": 214844, "NOPM": 93450, "JobId": ""},
        ],

    },
}

with open("benchmark_results_detailed.csv", mode="w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Category", "Test ID", "Run", "JobId", "Warehouses", "VUs", "Duration", "Ramp Up", "Iterations", "TPM", "NOPM"])

    for category, tests in results.items():
        for test_id, runs in tests.items():
            params = test_params[test_id]
            for i, run in enumerate(runs, start=1):
                if i == 6:
                    writer.writerow([
                        category,
                        test_id,
                        f"Average from test {test_id}",
                        run["JobId"],
                        params["Warehouses"],
                        params["VUs"],
                        params["Duration"],
                        params["Ramp Up"],
                        params["Iterations"],
                        run["TPM"],
                        run["NOPM"]
                    ])
                else:
                    writer.writerow([
                        category,
                        test_id,
                        f"Run {i}",
                        run["JobId"],
                        params["Warehouses"],
                        params["VUs"],
                        params["Duration"],
                        params["Ramp Up"],
                        params["Iterations"],
                        run["TPM"],
                        run["NOPM"]
                    ])
