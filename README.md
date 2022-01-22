### Note: Genious has changed their Website so this currently does not work anymore 😔

## Fancy
![alt text](/fancy_header.jpg)
### Learn more [here](https://sidpremkumar.com/Fancy)

Fancÿ was a program born out of observing a pattern. I noticed that songs that required a lot of thought (either hidden meanings or references that were a bit obscure) often had a plethora of annotations on [Genius.com](https://genius.com). Conversely, I found that songs that I thought were simple and easy to understand tended to have little to no annotations. 

After a couple of weeks of verifying my hypothesis I decided it was time to automatize the laborious task of verifying the songs I loved on [Genius.com](https://genius.com). I wanted to create a way to rank and then compare songs that I came across. 

Enter Fancÿ; this program uses Genius’ API in order to look up the song in question. I then use BeautifulSoup to web-scrap the songs page. The algorithm assigns a value of 1 to lines in a song that have an annotation associated with it and a value of 0 otherwise. Furthermore, I wanted to develop a way to reduce the weight of repeated lyrics (i.e. the chorus). In order to do this, I constantly reduced the value of repeated lyrics by a half. This means that the first time the line was said it was given a value of 1, the second time a value of 0.5, the third time a value of 0.25 and so on. 

The score was then calculated by multiplying the value by the length of the line. This was then divided by the total length of the song (i.e. all the words in the song). This then results in a score between 1 and 0 that can be used to compare and rank songs against each other. 

This is clearly a very crude way of analyzing songs and is prone to a couple of issues; Firstly, it relies on user submissions to [Genius.com](https://genius.com), this then will give a low score to songs that have little user submissions which would be inaccurate. Furthermore, the algorithm does not judge the quality of annotations (something that is on the todo list). Judging the quality of the annotation either by length or content would result in a substantially better scoring system, but would make it hard to classify a perfect (i.e. a score of 1) song. 

