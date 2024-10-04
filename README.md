# The Aim
To convert data from safety data sheets (pdfs) into machine readable JSON format. 


# The Solution (?)
I analysed the steps to be taken in order to perform a task like this and came up with following approach: 

First, we use the pymupdf library in order to extract the raw text.

Then we preprocess the text and eliminate any unwanted stuff like headers, footers etc. + categorize the important stuff by using spaCy/Regex. Both are different in their approach: spaCy is an NLP library that uses ML models to process text in a more contexual sense, while Regex uses pattern matching to find specific sequences of data,  so I guess it's better for static patterns of data. 

pymupdf seems to have an inbuilt function for extracting tabular data.
However, I was unable to do this due to enviroment problems.
