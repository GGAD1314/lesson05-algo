"""
性能实验 benchmark.py
对比冒泡排序(O(n²))、合并排序(O(n log n))、Python 内置 sorted()(Timsort)
对应实践指南五第十节 + 自主实践任务②
"""

import timeit
import random
import sys
import os

# 确保能导入同目录下的模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bubble_sort import bubble_sort
from merge_sort import merge_sort


def make_array(n):
    """生成 n 个随机整数的数组"""
    return [random.randint(0, 100000) for _ in range(n)]


def make_reverse_array(n):
    """生成 n 个整数的逆序数组（从大到小）"""
    return [n - i for i in range(n)]


def benchmark():
    """运行性能对比实验"""
    sizes = [1000, 2000, 4000, 8000]
    repeat = 3

    print(f"{'n':>8} {'冒泡(s)':>10} {'合并(s)':>10} {'sorted(s)':>10} {'冒泡/合并':>10} {'冒泡/sorted':>12}")
    print("-" * 75)

    results = []
    for n in sizes:
        arr = make_array(n)

        # 冒泡排序（每次用副本，因为原地修改）
        t_bubble = timeit.timeit(lambda: bubble_sort(arr[:]), number=repeat) / repeat

        # 合并排序（每次用副本）
        t_merge = timeit.timeit(lambda: merge_sort(arr[:]), number=repeat) / repeat

        # Python 内置 sorted()（每次用副本）
        t_sorted = timeit.timeit(lambda: sorted(arr[:]), number=repeat) / repeat

        ratio_bm = t_bubble / t_merge if t_merge > 0 else float('inf')
        ratio_bs = t_bubble / t_sorted if t_sorted > 0 else float('inf')

        print(f"{n:>8} {t_bubble:>10.4f} {t_merge:>10.4f} {t_sorted:>10.4f} {ratio_bm:>10.1f} {ratio_bs:>12.1f}")
        results.append((n, t_bubble, t_merge, t_sorted))

    # 验证增长规律
    print("\n--- 增长规律验证 ---")
    for i in range(len(results) - 1):
        n1, b1, m1, s1 = results[i]
        n2, b2, m2, s2 = results[i + 1]
        if n2 == n1 * 2:
            bubble_ratio = b2 / b1 if b1 > 0 else 0
            merge_ratio = m2 / m1 if m1 > 0 else 0
            print(f"n: {n1} → {n2}（翻倍）")
            print(f"  冒泡耗时比: {bubble_ratio:.2f}（O(n²) 预期 ≈ 4.0）")
            print(f"  合并耗时比: {merge_ratio:.2f}（O(n log n) 预期 ≈ 2.x）")

    # 检查点 3：n=8000 时合并比冒泡快一个数量级以上
    n8000_bubble = results[-1][1]
    n8000_merge = results[-1][2]
    check3 = (n8000_bubble / n8000_merge) > 10
    print(f"\n检查点3(n=8000 合并比冒泡快10倍以上): {'通过' if check3 else '失败'} "
          f"(实际快 {n8000_bubble/n8000_merge:.1f} 倍)")

    return results


def benchmark_random_vs_reverse():
    """自主实践扩展：随机数组 vs 逆序数组，合并排序耗时对比

    验证：合并排序对随机数组和逆序数组耗时几乎不变
    原因（见指南 6.4）：怎么切都是对半，合并时比较次数与初始顺序无关
    """
    print("\n=== 随机数组 vs 逆序数组：合并排序耗时对比 ===")
    n = 8000
    repeat = 5

    arr_random = make_array(n)
    arr_reverse = make_reverse_array(n)

    t_random = timeit.timeit(lambda: merge_sort(arr_random[:]), number=repeat) / repeat
    t_reverse = timeit.timeit(lambda: merge_sort(arr_reverse[:]), number=repeat) / repeat

    print(f"n={n}, 重复 {repeat} 次取均值")
    print(f"随机数组:  {t_random:.4f}s")
    print(f"逆序数组:  {t_reverse:.4f}s")
    print(f"耗时比(逆序/随机): {t_reverse/t_random:.2f}")
    print("结论：合并排序对数据分布不敏感（怎么切都是对半，合并操作量与初始顺序无关）")


if __name__ == '__main__':
    print("=" * 75)
    print("性能实验：冒泡排序 vs 合并排序 vs 内置 sorted()")
    print("=" * 75)
    benchmark()
    benchmark_random_vs_reverse()
