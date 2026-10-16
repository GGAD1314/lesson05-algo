"""
独立研究任务②：sys.setrecursionlimit 实验
验证合并排序 10 万元素是否会撞递归上限
对应实践指南五第十三节独立研究②
"""

import sys
import os
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from merge_sort import merge_sort, reset_depth, get_max_depth


def experiment_recursion_limit():
    """测试 10 万元素合并排序的递归深度"""
    print("=" * 60)
    print("独立研究②：sys.setrecursionlimit 与合并排序递归上限")
    print("=" * 60)

    # 查看当前递归上限
    current_limit = sys.getrecursionlimit()
    print(f"当前 Python 默认递归上限: {current_limit}")

    # 生成 10 万元素随机数组
    n = 100000
    arr = [random.randint(0, 1000000) for _ in range(n)]
    print(f"\n生成 {n} 个随机元素的数组")

    # 运行合并排序，观察最大递归深度
    reset_depth()
    try:
        result = merge_sort(arr)
        observed_depth = get_max_depth()
        print(f"合并排序成功完成！")
        print(f"实际达到的最大递归深度: {observed_depth}")
        print(f"log2({n}) ≈ {__import__('math').log2(n):.2f}")
        print(f"是否撞递归上限: {'否（深度远小于上限）' if observed_depth < current_limit else '是'}")
        print(f"排序结果正确: {all(result[i] <= result[i+1] for i in range(len(result)-1))}")
    except RecursionError:
        print("✗ 触发 RecursionError！合并排序 10 万元素撞了递归上限")
        print(f"递归上限需要至少 log2({n})+1 ≈ {int(__import__('math').log2(n)) + 2} 层")

    # 解释 sys.setrecursionlimit
    print("\n--- sys.setrecursionlimit 说明 ---")
    print("sys.setrecursionlimit(limit) 用于设置 Python 解释器允许的")
    print("最大递归深度。默认值为 1000，当递归调用超过此深度时会抛出")
    print("RecursionError。")
    print()
    print("合并排序的递归深度 = log2(n) + 1（每次对半切）：")
    print(f"  n=1000  → 深度 ≈ 11")
    print(f"  n=8000  → 深度 ≈ 14")
    print(f"  n=100000 → 深度 ≈ 18")
    print(f"  n=1000000 → 深度 ≈ 21")
    print("结论：合并排序 10 万元素只需要约 18 层递归，")
    print("远小于默认上限 1000，不会撞上限。")

    # 测试如果把递归上限设得很小会怎样
    print("\n--- 故意设置低递归上限测试 ---")
    original = sys.getrecursionlimit()
    sys.setrecursionlimit(50)  # 设到 50
    small_arr = [random.randint(0, 100000) for _ in range(100000)]
    reset_depth()
    try:
        merge_sort(small_arr)
        print(f"递归上限=50 时居然成功了（深度={get_max_depth()}）")
    except RecursionError:
        print(f"递归上限=50 时触发 RecursionError（深度={get_max_depth()}），"
              f"证实递归深度上限机制生效")
    finally:
        sys.setrecursionlimit(original)  # 恢复


if __name__ == '__main__':
    experiment_recursion_limit()
