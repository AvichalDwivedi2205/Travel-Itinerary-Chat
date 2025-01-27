# Prompt Structure
Firstly I got the basic trip details from the person which includes the following
The place he wants to visit
Number Of people He is traveling with
The dates he is traveling for 
The budget he has which has 5 criteria rangingg from low to high.
After this I asked the user for other prompts in a chat based manner to make it look more interactive
The first question was What was the purpose of the trip so that we can know why the user wants to go to a trip. Is it for enjoying with friends or for family retreat or something else
The next question was what activities he would be interested in doing there? this tells us about the activities he wants to do at that place and the travel plan will be designed like that
The next 2 question asks about the person's dietary preferences and any allergies he might have so that we can suggest whatever diet he is most compfortable with.
The next question asks about the eprson's walking tolerance so that the travel could be designed like that
The next three questions asks about where he wants his accomodation to be, what type of accomodation the user prefers and is there any facility that he wants.

# Final Prompt Structure
Finally I put in the last propmt taking in all the input and give it to gemini.
I ask gemini to seperate the day in 3 intervals of morning, afternoon and evening, make dietary plans as per regulations set by the user, Make transportation options depending on the walking tolerance of the person, make cost estimates depending on the budget and finally give them local insider tips and some gems that te=hey would not want to miss.
I also ask it to group nearby attractions to save time. Along with that I asked it to keep time in between for meals and add give safety tips. Finally I asked to give answer in english as there was some errors which generated answer in some other language.