"""
冒泡排序（Bubble Sort）—— O(n²) 的经典代表
对应实践指南五第八节
"""


def bubble_sort(nums):
    """冒泡排序：原地排序，返回排序后的数组

    原理：反复走数组，每遇到"前大后小"的相邻对就交换——
    每一轮把当前最大值"冒"到末尾。

    Args:
        nums: 待排序数组

    Returns:
        排序后的数组（原地修改后返回）
    """
    n = len(nums)
    for i in range(n - 1):              # 共 n-1 轮
        for j in range(n - 1 - i):      # 每轮比较相邻对
            if nums[j] > nums[j + 1]:   # 前大后小 → 交换
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
    return nums


if __name__ == '__main__':
    test = [8, 3, 5, 1, 9, 2]
    print(f"输入: {test}")
    result = bubble_sort(test[:])
    print(f"输出: {result}")
    print(f"排序正确: {result == [1, 2, 3, 5, 8, 9]}")
