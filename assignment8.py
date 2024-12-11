from collections import defaultdict, deque
from typing import List

#1
class Solution1:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        # Build adjacency list and calculate in-degree for each vertex
        adj_list = defaultdict(list)
        in_degree = [0] * numCourses
        
        # Process prerequisites to build graph
        for course, prereq in prerequisites:
            adj_list[prereq].append(course)
            in_degree[course] += 1
        
        # Initialize queue with all courses having no prerequisites
        queue = deque()
        for course in range(numCourses):
            if in_degree[course] == 0:
                queue.append(course)
        
        # Process courses in topological order
        result = []
        while queue:
            current_course = queue.popleft()
            result.append(current_course)
            
            # Process all courses that depend on current course
            for next_course in adj_list[current_course]:
                in_degree[next_course] -= 1
                # If all prerequisites are satisfied, add to queue
                if in_degree[next_course] == 0:
                    queue.append(next_course)
        
        # Check if we've processed all courses
        # If not, there must be a cycle
        return result if len(result) == numCourses else []
    
#2
class Solution2:
    def divide(self, dividend: int, divisor: int) -> int:
        # Handle overflow cases for 32-bit integers
        MAX_INT = 2**31 - 1
        MIN_INT = -2**31
        
        # Special case for overflow
        if dividend == MIN_INT and divisor == -1:
            return MAX_INT
        
        # Get the sign of the quotient
        sign = -1 if (dividend < 0) ^ (divisor < 0) else 1
        
        # Convert to positive numbers
        dividend = abs(dividend)
        divisor = abs(divisor)
        
        quotient = 0
        current_dividend = dividend
        
        # Use bit manipulation for efficient division
        while current_dividend >= divisor:
            temp_divisor = divisor
            multiple = 1
            
            # Find the largest multiple of divisor that doesn't exceed current_dividend
            while (temp_divisor << 1) <= current_dividend and (temp_divisor << 1) > 0:
                temp_divisor <<= 1
                multiple <<= 1
            
            current_dividend -= temp_divisor
            quotient += multiple
        
        result = sign * quotient
        
        # Handle 32-bit integer bounds
        if result > MAX_INT:
            return MAX_INT
        if result < MIN_INT:
            return MIN_INT
            
        return result
from typing import List

#3
class Solution3:
    def coinChange(self, coins: List[int], amount: int) -> int:
        # Base case
        if amount == 0:
            return 0
        if not coins or amount < 0:
            return -1
            
        # Initialize dp array with amount + 1 (impossible value)
        # dp[i] represents the minimum number of coins needed to make amount i
        dp = [amount + 1] * (amount + 1)
        dp[0] = 0
        
        # Build up the dp array
        for i in range(1, amount + 1):
            # Try each coin
            for coin in coins:
                if coin <= i:
                    dp[i] = min(dp[i], dp[i - coin] + 1)
        
        # Return result, -1 if impossible
        return dp[amount] if dp[amount] != amount + 1 else -1

#4
from typing import List, Dict, Optional, Set
from datetime import datetime
import redis
from collections import defaultdict

class Comment:
    def __init__(self, comment_id: int, post_id: int, user_id: int, content: str):
        self.comment_id = comment_id
        self.post_id = post_id
        self.user_id = user_id
        self.content = content
        self.created_at = datetime.now()

class User:
    def __init__(self, user_id: int, username: str):
        self.user_id = user_id
        self.username = username
        self.followers: Set[int] = set()
        self.following: Set[int] = set()

class Post:
    def __init__(self, post_id: int, user_id: int, content: str):
        self.post_id = post_id
        self.user_id = user_id
        self.content = content
        self.created_at = datetime.now()
        self.likes = 0
        self.comments: List[Comment] = []

class SocialMediaPlatform:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.posts: Dict[int, Post] = {}
        self.news_feeds: Dict[int, List[int]] = defaultdict(list)
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.comment_counter = 0
        
    def create_post(self, user_id: int, content: str) -> Optional[Post]:
        """Create a new post and update followers' feeds"""
        if user_id not in self.users:
            return None
            
        post_id = len(self.posts) + 1
        post = Post(post_id, user_id, content)
        self.posts[post_id] = post
        
        # Update news feeds (fan-out on write)
        self._update_feeds(user_id, post_id)
        
        return post

    def add_comment(self, user_id: int, post_id: int, content: str) -> Optional[Comment]:
        """Add a comment to a post"""
        if user_id not in self.users or post_id not in self.posts:
            return None

        self.comment_counter += 1
        comment = Comment(self.comment_counter, post_id, user_id, content)
        self.posts[post_id].comments.append(comment)
        return comment
    
    def _update_feeds(self, user_id: int, post_id: int) -> None:
        """Update followers' feeds with new post"""
        # Get user's followers from cache or DB
        followers = self.users[user_id].followers
        
        # Update each follower's feed
        for follower_id in followers:
            feed_key = f"feed:{follower_id}"
            self.redis_client.lpush(feed_key, post_id)
            self.redis_client.ltrim(feed_key, 0, 999)  # Keep last 1000 posts
    
    def get_news_feed(self, user_id: int, page: int = 1, size: int = 20) -> List[Post]:
        """Get user's news feed with pagination"""
        if user_id not in self.users:
            return []
            
        feed_key = f"feed:{user_id}"
        start = (page - 1) * size
        end = start + size - 1
        
        # Get post IDs from Redis
        post_ids = self.redis_client.lrange(feed_key, start, end)
        
        # Fetch posts from cache/DB
        posts = []
        for post_id in post_ids:
            post = self.posts.get(int(post_id))
            if post:
                posts.append(post)
        
        return posts
    
    def follow_user(self, follower_id: int, following_id: int) -> bool:
        """Follow a user and update relationships"""
        if follower_id not in self.users or following_id not in self.users:
            return False
            
        self.users[follower_id].following.add(following_id)
        self.users[following_id].followers.add(follower_id)
        
        # Update follower's feed with recent posts
        self._backfill_feed(follower_id, following_id)
        return True
    
    def _backfill_feed(self, follower_id: int, following_id: int, limit: int = 100) -> None:
        """Backfill follower's feed with recent posts from newly followed user"""
        feed_key = f"feed:{follower_id}"
        recent_posts = [post_id for post_id, post in self.posts.items() 
                       if post.user_id == following_id][-limit:]
        
        for post_id in recent_posts:
            self.redis_client.lpush(feed_key, post_id)

    def like_post(self, user_id: int, post_id: int) -> bool:
        """Like a post and update counters"""
        if post_id not in self.posts or user_id not in self.users:
            return False
            
        like_key = f"post:{post_id}:likes"
        if not self.redis_client.sismember(like_key, user_id):
            self.redis_client.sadd(like_key, user_id)
            self.posts[post_id].likes += 1
        return True
