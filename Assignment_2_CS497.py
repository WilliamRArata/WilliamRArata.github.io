def majorityElement(nums):
    #initialize variables majority and counter
    majority = None
    count = 0
    #loop through each number in array
    for num in nums:
        #set current number to majority if there is no other majority
        if count == 0:
            majority = num
        #if majority is met again, then increase its count
        if num == majority:
            count += 1
        else: 
            count = -1
    
    return majority

def findKthLargest(nums, k):
    #using the quickselect algorithm, find the kth largest number
    def quickSelect(l, r):
        #choose the last element as the pivot
        pivot, p = nums[r], l
        #partition the array so that all elements are on the left of p
        for i in range(l, r):
            if nums[i] <= pivot:
                #move smaller elements to the left
                nums[p], nums[i] = nums[i], nums[p] #switch elements to move the smaller one to the left
                p += 1 #increase pivot point
        #place pivot in final correct position
        nums[p], nums[r] = nums[r], nums[p]
        
        if k < len(nums) - p:
            return quickSelect(p + 1, r)
        elif k > len(nums) - p:
            return quickSelect(l, p - 1)
        else:
            return nums[p]
    
    return quickSelect(0, len(nums) - 1)

def maximumGap(nums):
    #base case
    if len(nums) < 2:
        return 0
    
    # Find min and max values
    min_val, max_val = min(nums), max(nums)
    
    # Compute bucket size and number of buckets needed
    bucket_size = max(1, (max_val - min_val) // (len(nums) - 1))
    #each bucket is an empty list, _ is used as a dummy temp variable for values in the range
    buckets = [[] for _ in range((max_val - min_val) // bucket_size + 1)]
    
    # Distribute numbers into buckets
    for num in nums:
        index = (num - min_val) // bucket_size
        buckets[index].append(num)
    
    # Find maximum gap
    max_gap = 0
    prev_max = min_val
    for bucket in buckets:
        #empty bucket case
        if not bucket:
            continue
        #min and max of current bucket
        curr_min, curr_max = min(bucket), max(bucket)
        #update max gap
        max_gap = max(max_gap, curr_min - prev_max)
        prev_max = curr_max
    
    return max_gap

def removeDuplicateLetters(s):
    stack = []
    #set to track characters already added to stack
    seen = set()
    #dictionary to track last occurence for each character
    last_occurrence = {c: i for i, c in enumerate(s)}
    
    #iterate over the string
    for i, c in enumerate(s):
        #if character is not considered already
        if c not in seen:
            #if stack is not empty, if c < last character in stack (stack[-1]), and if there is another occurence of the character later on
            while stack and c < stack[-1] and i < last_occurrence[stack[-1]]:
                #pop last character and remove from seen
                seen.remove(stack.pop())
            #add curr character to stack and mark it as seen    
            stack.append(c)
            seen.add(c)
    #return final string
    return ''.join(stack)

def shortestSubarray(nums, k):
    n = len(nums)
    #initialize prefix sum array with 0 at beginning
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + nums[i]
    
    #initialize minimum length to infinity
    min_length = float('inf')
    index_queue = []
    
    #iterate through prefix sum array
    for i, curr_sum in enumerate(prefix_sum):
        #compare curr_sum to front of queue to update min_length
        while index_queue and curr_sum - prefix_sum[index_queue[0]] >= k:
            min_length = min(min_length, i - index_queue.pop(0))
        #remove indices from back of queue if prefix sum > currsum
        while index_queue and prefix_sum[index_queue[-1]] >= curr_sum:
            index_queue.pop()
        #add curr index to back of queue
        index_queue.append(i)
    
    return min_length if min_length != float('inf') else -1


