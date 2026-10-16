"""
合并排序（Merge Sort）—— 分治法的完整样板
对应实践指南五第六节
"""

# 全局变量：记录递归过程中达到的最大深度
max_depth = 0


def merge_sort(nums, depth=0):
    """合并排序：分治三步的完整样板

    Args:
        nums: 待排序数组
        depth: 当前递归深度（用于观察递归树深度，0 表示根节点）

    Returns:
        排序后的新数组（不修改原数组）
    """
    global max_depth
    # 更新最大深度
    if depth > max_depth:
        max_depth = depth

    # 基准情形：长度 0 或 1 的数组天然有序
    if len(nums) <= 1:
        return nums

    # ---- 分解（Divide）：从中间切成两半 ----
    mid = len(nums) // 2
    left, right = nums[:mid], nums[mid:]

    # ---- 解决（Conquer）：递归排序两个小段 ----
    left_sorted = merge_sort(left, depth + 1)
    right_sorted = merge_sort(right, depth + 1)

    # ---- 合并（Combine）：两个有序段拼成一个有序段 ----
    return merge(left_sorted, right_sorted)


def merge(a, b):
    """双指针合并两个有序数组

    Args:
        a: 有序数组 a
        b: 有序数组 b

    Returns:
        合并后的有序数组
    """
    result, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:              # 取较小者入结果
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    result.extend(a[i:])              # 残段必有序，直接接上
    result.extend(b[j:])
    return result


def get_max_depth():
    """返回上一次 merge_sort 调用达到的最大递归深度"""
    return max_depth


def reset_depth():
    """重置最大深度计数器"""
    global max_depth
    max_depth = 0


def is_sorted(arr):
    """检查数组是否升序有序"""
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


if __name__ == '__main__':
    # Step 1 验收：对 [8, 3, 5, 1, 9, 2] 排序
    test = [8, 3, 5, 1, 9, 2]
    result = merge_sort(test)
    print(f"输入: {test}")
    print(f"输出: {result}")
    print(f"检查点1: {'通过' if result == [1, 2, 3, 5, 8, 9] else '失败'}")

    # 递归深度观察：8000 元素
    import random
    import math
    reset_depth()
    big = [random.randint(0, 100000) for _ in range(8000)]
    sorted_big = merge_sort(big)
    observed_depth = get_max_depth()
    expected = math.log2(8000)
    print(f"\n8000 元素排序后有序: {is_sorted(sorted_big)}")
    print(f"递归树最大深度: {observed_depth}")
    print(f"log2(8000) ≈ {expected:.2f}")
    print(f"检查点(深度≈13): {'通过' if abs(observed_depth - 13) <= 1 else '失败'}")
