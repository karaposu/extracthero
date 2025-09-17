i want to create benchmark 

results collumsn should be like this

framework, methodology, model name, model config,  run count, doc length, avg line retain ratio, Line Retain STD, avg elapsed time, avg cost, avg input cost, avg output cost, 

so it results should look like : 

filterhero, extractive, gpt-4.1-mini, -, 5,  538,  ....


here are the combinations 

extractive, subtractive 

gpt-4o, gpt-4.1-mini, gpt-4.1, gpt-5-mini, gpt-5-mini, gpt-5, 

run count 5


doc length  538 (2.md ) , 980 (1.md)



create benchmark.py which runs all of these combinations with and saves the results as csv file