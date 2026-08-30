# Task-03: Leetcode
## Problem 1: 1672. Richest Customer Wealth
We are given a 2D integer grid of people and the money they have in a bank.
Each element of the grid represents an array of all the money a person has in each of their bank accounts.
So the approach I used to solve this was to iterate through each of the elements, calculating the total wealth each person had in all accounts combined and keeping track of which person had the highest wealth encountered so far.
```cpp
class Solution {
public:
    int maximumWealth(vector<vector<int>>& accounts) {
        // Variable to track the highest wealth encountered
        int highestWealth = 0;

        for (int i = 0; i < accounts.size(); ++i)
        {
            // For each person calculates their wealth from all bank accounts
            int wealth = 0;
            for (int j = 0; j < accounts[i].size(); ++j)
            {
                wealth += accounts[i][j];
            }

            // If the encountered wealth is the highest so far, track it with the variable created earlier
            if (wealth > highestWealth)
                highestWealth = wealth;
        }

        return highestWealth;
    }
};
```

## Problem 2: 1732. Find the Highest Altitude
We are given an integer array which contains the gain in altitude from one point to the next on a road trip.
We are tasked to find the highest altitude point.
It is mentioned that the altitude of the first point is 0 so therefore by adding all the elements before a given element in the array we can find the altitude at the point
```cpp
class Solution {
public:
    int largestAltitude(vector<int>& gain) {
        int highest = 0;
        
        for (int i = 0; i < gain.size(); ++i)
        {
            int height = 0;
            int j = i;

            // Iterates through all previous points to calculate the altitude of the current point
            while (j >= 0)
            {
                height += gain[j];
                --j;
            }

            // Here it checks if the altitude of the current point is the highest encountered so far. If so,  track it
            if (height > highest)
                highest = height;
        }

        return highest;
    }
};
```

## Problem 3: 27. Remove Element
Here we are given an array of integers and another integer of which all ocurrences in the array should be removed.
The approach used here is simple, traverse the array and remove the current element if it equals the target value
```cpp
class Solution {
public:
    int removeElement(vector<int>& nums, int val) {
      for (int i = 0; i < nums.size(); ++i)
      {
        if (nums[i] == val)
        {
            // If the current element is the target then remove it and decrement the index counter as to not go out of bounds
            nums.erase(nums.begin() + i);
            --i;
        }
      }

      return nums.size();
    }
};
```

## Problem 4: 49. Group Anagrams
So here we have to group anagrams together. Since they're anagrams, they have the same length and if sorted would be the same.
To group anagrams, we maintain a hash map of strings to arrays and strings with the same sorted version would be anagrams and hence come under the same key.
```cpp
class Solution {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        unordered_map<string, vector<string>> charset{};
        vector<vector<string>> result{};

        for (auto& s : strs)
        {
            // Makes a copy of the original string as sort modifies the original string
            string copy = s;
            sort(s.begin(), s.end());
            if (charset.contains(s))
                charset[s].push_back(copy);
            else
                charset[s] = {copy};
        }

        // Collects all anagram groups into a final result vector
        for (const auto& pair : charset)
        {
            result.push_back(pair.second);
        }

        return result;
    }
};
```

## Problem 5: Product of Array except Self
This one was tricky and took a while for the logic to set in. But essentially what you're doing is keeping track of the product of each the elements before and storing it in an array.
```cpp
class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        vector<int> result(nums.size());

        int product{1};

        // Move forward in the array to find product of elements before nums[i]
        for (int i = 0; i < nums.size(); ++i)
        {
            // Product at this moment contains the product of all previous elements, so store that in an array before updating product with the current element.
            result[i] = product;
            product *= nums[i];
        }
        product = 1;

        // Move backward in the array to find product of elements after nums[i]
        for (int i = nums.size() - 1; i >= 0; --i)
        {
            // result[i] contains the product of elements before nums[i], multiply that with product which contains the product of elements after nums[i]
            result[i] *= product;
            product *= nums[i];
        }

        return result;
    }
};
```
