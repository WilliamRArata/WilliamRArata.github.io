#1) Two Sum
#Input: nums = [2,7,11,15], target = 9
#Output: [0,1]
#Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
    #Creating a hash table that stores which index the number is stored

#Time complexity:O(n) Space Complexity: O(n)

def twoSum(self, nums: List[int], target: int) -> List[int]:
    """For this solution I used a hash table"""
    numToIndex = {}
    #Going through the arr
    for i in range(len(nums)):
        #Calculate the complement that would add to target
        complement = target - nums[i]
        #Check if complement is in hash table
        if complement in numToIndex:
            return numToIndex[complement], i
        #Add number to hash table
        numToIndex[nums[i]] = i



#2) Find First and Last Position of Element in Sorted Array.
#Input: nums = [5,7,7,8,8,10], target = 8
#Output: [3,4]

#Complexity: O(n) Space complexity: O(1)

def searchRange(self, nums: List[int], target: int) -> List[int]:
    """For this solution I used Linear Search"""
    #initialize first and last variables, set them to -1
    first, last = -1, -1
    #iterate through the arr
    for i in range(len(nums)):
        #set first to target
        if nums[i] == target:
            if first == -1:
                    first = i
            #last will constantly be updated until it stops at actual last position of target
            last = i
    return [first, last]



#3) Median of Two Sorted Arrays
#Input: nums1 = [1,3], nums2 = [2]
#Output: 2.00000
#Explanation: merged array = [1,2,3] and median is 2.

#Time Complexity:O(logm/logn) Space Complexity: O(1)

def findMedianSortedArrays(self, nums1, nums2):
    #concatenate the arrays
    merged = nums1 + nums2
    #sort from largest to smallest
    merged.sort()
    #get length of array
    total = len(merged)
    #if length is an odd number, then return middle number
    if total % 2 == 1:
        return float(merged[total // 2])
    #else return average of middle 2
    else:
        middle1 = merged[total // 2 - 1]
        middle2 = merged[total // 2]
        return (float(middle1) + float(middle2)) / 2.0



#4) Remove Nth Node From End of List
#Input: head = [1], n = 1
#Output: []


# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

#Time complexity:O(n) Space complexity:O(1)

class RemoveNthFromEnd:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        temp = head
        c = 0
        #count how many nodes there are
        while temp is not None:
            #go to the next node
            temp = temp.next
            #add 1 to c
            c += 1
        #if c = nth node return the node
        if c==n:
            head = head.next
            return head

        temp = head
        #traverse through nodes
        for i in range(c-n-1):
            temp = temp.next
        
        temp.next = temp.next.next
        return head




#5) Merge k Sorted Lists
#Input: lists = [[1,4,5],[1,3,4],[2,6]]
#Output: [1,1,2,3,4,4,5,6]
#Explanation: The linked-lists are:
#[
 # 1->4->5,
 # 1->3->4,
 # 2->6
#]
#merging them into one sorted list:
#1->1->2->3->4->4->5->6

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

#Time complexity: O(NlogK) Space:O(logK)

class MergeKSortedLists:
    def merge(self, left: ListNode, right: ListNode) -> ListNode:
        """Takes 2 pointers to linked lists as input and merges them sorted"""
        #create dummy node initiated to -1
        dummy = ListNode(-1)
        temp = dummy
        #compare to first node and left and right linked lists, append temp to smaller linked list
        while left and right:
            if left.val < right.val:
                temp.next = left
                temp = temp.next
                left = left.next
            else:
                temp.next = right
                temp = temp.next
                right = right.next
        #continue until empty
        while left:
            temp.next = left
            temp = temp.next
            left = left.next
        while right:
            temp.next = right
            temp = temp.next
            right = right.next
        return dummy.next
    
    def mergeSort(self, lists: List[ListNode], start: int, end: int) -> ListNode:
        """takes vector of linked list, a starting index, and an ending index"""    
        #if the starting index is equal to end, return the linked list at start index
        if start == end:
            return lists[start]
        #figure out mid index and call merge sort recursively on left and right
        mid = start + (end - start) // 2
        left = self.mergeSort(lists, start, mid)
        right = self.mergeSort(lists, mid + 1, end)
        #merge the 2 sorted lists
        return self.merge(left, right)
    
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        """takes vector of linked list as input and returns single sorted linkked list"""
        #if input vector is empty return null ptr
        if not lists:
            return None
        #call mergesort function on entire input vector
        return self.mergeSort(lists, 0, len(lists) - 1)
