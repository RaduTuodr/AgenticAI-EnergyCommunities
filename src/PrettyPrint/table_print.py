def table_print(results: list[(str, dict)]):
    print("==== Scenario Comparison ====")
    header = f"{'Metric':<30} |" + "".join(f" {col_name:<15} |" for col_name, _ in results)
    print(header)
    print("-" * len(header))

    for k in results[0][1].keys():
        print(f"{k:<30} |" + "".join([f" {result[k]:<15.2f} |" for _, result in results]))
