def format_dicts_as_table(data_list):
    if not data_list:
        return "No data to display."
    columns = list(data_list[0].keys())
    table_head = f""
    separator = f"{'=' * 5}|"
    for item in columns:
        table_head += f" {item:^20}|"
        separator += f"{'='*21:^20}|"

    print("  #  |" + table_head)
    print(separator)

    for number, data_dict in enumerate(data_list, start=1):
        print_line = f"{number:^5}|"
        for k, v in data_dict.items():
            while len(v) > 20:
                print(f"{' ':5}|{' ':21}| {v[:19]} |{' ':21}|")
                v = v[19:]
            v = "-" if not v else v
            print_line += f" {v:^20}|"
        print(print_line)
        print("-" * len(print_line))
