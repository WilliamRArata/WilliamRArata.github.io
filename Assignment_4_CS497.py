#1
class MinHeap:
    def __init__(self):
        self.heap = []

    def parent(self, i):
        return (i - 1) // 2

    def left_child(self, i):
        return 2 * i + 1

    def right_child(self, i):
        return 2 * i + 2

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def push(self, item):
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        min_item = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return min_item

    def _sift_up(self, i):
        parent = self.parent(i)
        if i > 0 and self.heap[i][0] < self.heap[parent][0]:
            self.swap(i, parent)
            self._sift_up(parent)

    def _sift_down(self, i):
        min_index = i
        left = self.left_child(i)
        right = self.right_child(i)
        if left < len(self.heap) and self.heap[left][0] < self.heap[min_index][0]:
            min_index = left
        if right < len(self.heap) and self.heap[right][0] < self.heap[min_index][0]:
            min_index = right
        if i != min_index:
            self.swap(i, min_index)
            self._sift_down(min_index)

def topKFrequent(nums, k):
    # Count the frequency of each element
    count = {}
    for num in nums:
        count[num] = count.get(num, 0) + 1
    
    # Use a min heap to keep the k most frequent elements
    heap = MinHeap()
    for num, freq in count.items():
        if len(heap.heap) < k:
            heap.push((freq, num))
        elif freq > heap.heap[0][0]:
            heap.pop()
            heap.push((freq, num))
    
    # Extract the numbers from the heap
    return [num for freq, num in heap.heap]

#2
def findClosestElements(arr, k, x):
    # Binary search to find the closest element to x
    left, right = 0, len(arr) - 1
    while left < right:
        mid = (left + right) // 2
        if arr[mid] < x:
            left = mid + 1
        else:
            right = mid
    
    # Initialize two pointers
    left = right - 1
    right = left + 1
    
    # Expand the window to find k closest elements
    while k > 0:
        if left < 0:
            right += 1
        elif right >= len(arr):
            left -= 1
        elif x - arr[left] <= arr[right] - x:
            left -= 1
        else:
            right += 1
        k -= 1
    
    # Return the subarray
    return arr[left+1:right]

#3
class MinHeap:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.heap = [0] * capacity

    def parent(self, i):
        return (i - 1) // 2

    def left_child(self, i):
        return 2 * i + 1

    def right_child(self, i):
        return 2 * i + 2

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def push(self, value):
        if self.size == self.capacity:
            if value > self.heap[0]:
                self.heap[0] = value
                self._sift_down(0)
        else:
            self.heap[self.size] = value
            self.size += 1
            self._sift_up(self.size - 1)

    def _sift_up(self, i):
        while i > 0 and self.heap[self.parent(i)] > self.heap[i]:
            self.swap(i, self.parent(i))
            i = self.parent(i)

    def _sift_down(self, i):
        min_index = i
        left = self.left_child(i)
        if left < self.size and self.heap[left] < self.heap[min_index]:
            min_index = left
        right = self.right_child(i)
        if right < self.size and self.heap[right] < self.heap[min_index]:
            min_index = right
        if i != min_index:
            self.swap(i, min_index)
            self._sift_down(min_index)

class TopKIterator:
    def __init__(self, heap):
        self.data = sorted(heap.heap[:heap.size], reverse=True)
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.data):
            result = self.data[self.index]
            self.index += 1
            return result
        raise StopIteration

def peekTopK(arr, k):
    min_heap = MinHeap(k)
    queue = [0]  # Start with the root

    while queue and min_heap.size < k:
        index = queue.pop(0)
        
        if index >= len(arr):
            continue
        
        min_heap.push(arr[index])
        
        # Add children to the queue
        left_child = 2 * index + 1
        right_child = 2 * index + 2
        queue.append(left_child)
        queue.append(right_child)

    return TopKIterator(min_heap)



#4
def shortestSubarray(nums, k):
    n = len(nums)
    current_sum = 0
    left = 0
    min_length = float('inf')
    
    for right in range(n):
        current_sum += nums[right]
        
        while current_sum >= k:
            min_length = min(min_length, right - left + 1)
            current_sum -= nums[left]
            left += 1
    
    return min_length if min_length != float('inf') else -1


#5
def kthSmallestFraction(arr, k):
    n = len(arr)
    
    def count_smaller_fractions(mid):
        count = 0
        j = 1
        for i in range(n - 1):
            while j < n and arr[i] > mid * arr[j]:
                j += 1
            count += n - j
        return count
    
    left, right = 0, 1
    while right - left > 1e-9:
        mid = (left + right) / 2
        if count_smaller_fractions(mid) < k:
            left = mid
        else:
            right = mid
    
    # Find the exact fraction
    for i in range(n - 1, 0, -1):
        j = n - 1
        while j > i and arr[i-1] / arr[j] > left:
            j -= 1
        if j > i and arr[i-1] / arr[j] == left:
            return [arr[i-1], arr[j]]