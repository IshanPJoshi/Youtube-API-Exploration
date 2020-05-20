# Youtube-API-Exploration

## Preface
This started because I have a lot of songs in my Youtube playlist. 

## Issue 1
The videos in my playlist get deleted from time to time and I have no way of getting them back. 
The goal is to be able to document my music and be able to access and search songs much quicker.

## Solution
Using Youtube's API, I managed to get access to the videos in the playlist. I also learned and implemented
pagination (iterating through video pages cause Youtube
only lets you access 50 videos at a time). 

## Issue 2
My 3000+ video playlist is actually my liked playlist and is set private (Youtube makes all like playlists private and does not allow
to make them public). My friends wanted access to this list (cause I have pretty good taste in music). 

## Solution
Created a stack to essentially pop the videos from my private playlist and push them to a new public playlist. Is currently limited
by the Youtube API's limit of requests per day.

## Updates

- Scraped playlist data into a csv and converted to excel for easy access of videos via hyperlink.

- Created website for said videos, which can be accessed here: http://ishan-song-list.surge.sh/

## TODO

- Handle excel appending to top and error as a result of Youtube API limit

- Potentially convert excel data into an SQL Database for ease of updating and access
