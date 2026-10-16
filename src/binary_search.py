"""
二分查找（Binary Search）—— 减治法的典型代表
对应实践指南五第七节
"""


def binary_search(rates, target):
    """在有序数组 rates 中找 target，返回下标，找不到返回 -1

    前提：rates 必须已按升序排好——不满足此前提，结果不可预测。

    Args:
        rates: 升序有序数组
        target: 要查找的目标值

    Returns:
        找到返回下标；找不到返回 -1
    """
    low, high = 0, len(rates) - 1
    count = 0                        # 记录比较次数
    while low <= high:
        count += 1
        mid = (low + high) // 2      # 中间档
        if rates[mid] == target:
            print(f"找到，位于下标 {mid}，共比较 {count} 次")
            return mid
        elif rates[mid] < target:    # 中间偏小 → 左半整体砍掉
            low = mid + 1
        else:                        # 中间偏大 → 右半整体砍掉
            high = mid - 1
    print(f"没找到，共比较 {count} 次")
    return -1


def binary_search_closest(rates, target):
    """在有序数组 rates 中找最接近 target 的值，返回 (下标, 值)

    用于"找月供最接近 5000 的利率"这类近似查找。
    前提：rates 必须已按升序排好。

    Args:
        rates: 升序有序数组
        target: 目标值

    Returns:
        (下标, 最接近的值)
    """
    low, high = 0, len(rates) - 1
    closest_idx = 0
    min_diff = abs(rates[0] - target)

    while low <= high:
        mid = (low + high) // 2
        diff = abs(rates[mid] - target)
        if diff < min_diff:
            min_diff = diff
            closest_idx = mid
        if rates[mid] == target:
            return mid, rates[mid]
        elif rates[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return closest_idx, rates[closest_idx]


def make_rate_table(n):
    """生成 n 档模拟利率表（升序），利率范围 0.00% ~ (n-1)*0.01%

    设计为步长 0.01%，保证常用利率（如 3.75%）恰好在表中。
    例如 n=1024 时，利率范围 0.00% ~ 10.23%，下标 375 = 3.75%。

    Args:
        n: 档位数

    Returns:
        升序排列的利率列表（单位：%）
    """
    return [round(i * 0.01, 2) for i in range(n)]


def make_rate_table_with_monthly_payment(n, loan=1000000, years=30):
    """生成 n 档利率表及对应月供（等额本息）

    年利率范围 1.0% ~ 10.0%，等间距分布。
    月供公式：M = P * r * (1+r)^n / ((1+r)^n - 1)
    其中 P=贷款本金，r=月利率，n=还款月数

    Args:
        n: 档位数
        loan: 贷款本金（元），默认 100 万
        years: 贷款年限，默认 30 年

    Returns:
        [(年利率%, 月利率, 月供), ...] 按年利率升序
    """
    import math
    table = []
    # 年利率 1.0% ~ 10.0%，等间距
    annual_rates = [round(1.0 + i * (9.0 / (n - 1)), 4) for i in range(n)]
    months = years * 12
    for annual in annual_rates:
        monthly_rate = annual / 100 / 12
        if monthly_rate == 0:
            payment = loan / months
        else:
            payment = loan * monthly_rate * (1 + monthly_rate) ** months / \
                      ((1 + monthly_rate) ** months - 1)
        table.append((annual, monthly_rate, round(payment, 2)))
    return table


if __name__ == '__main__':
    # Step 2 验收：1024 档利率表找 3.75%
    rates_1024 = make_rate_table(1024)
    target_rate = 3.75
    print(f"1024 档利率表中查找 {target_rate}%:")
    idx = binary_search(rates_1024, target_rate)
    if idx != -1:
        print(f"检查点2(≤10次): {'通过' if idx >= 0 else '失败'}")

    # 故意翻车实验：传入未排序数组
    print("\n--- 故意翻车实验：未排序数组 ---")
    unsorted = [5.0, 1.0, 3.0, 2.0, 4.0]
    print(f"未排序数组: {unsorted}")
    result = binary_search(unsorted, 3.0)
    print(f"查找 3.0 的结果下标: {result}（结果不可预测，验证前提的重要性）")

    # 自主实践任务：100 档利率表找月供最接近 5000 的利率
    print("\n--- 自主实践：100 档利率表找月供最接近 5000 的利率 ---")
    rate_table = make_rate_table_with_monthly_payment(100)
    payments = [row[2] for row in rate_table]
    annual_rates = [row[0] for row in rate_table]
    target_payment = 5000
    closest_idx, closest_payment = binary_search_closest(payments, target_payment)
    print(f"目标月供: {target_payment} 元")
    print(f"最接近月供: {closest_payment} 元")
    print(f"对应年利率: {annual_rates[closest_idx]}%")
    print(f"月供表下标: {closest_idx}")
