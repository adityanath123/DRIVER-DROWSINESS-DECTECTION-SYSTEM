import random

def quiz_game():
    print("\nWelcome to the Python Quiz Game!")
    
    # List of questions, options, and answers
    quiz_data = [
        {"question": "What is the output of '2 ** 3' in Python?", "options": ["A) 8", "B) 6", "C) 9", "D) Error"], "answer": "A"},
        {"question": "Which data type is immutable in Python?", "options": ["A) List", "B) Tuple", "C) Dictionary", "D) Set"], "answer": "B"},
        {"question": "What keyword is used to define a function in Python?", "options": ["A) loop", "B) define", "C) def", "D) function"], "answer": "C"},
        {"question": "Which loop executes at least once before checking the condition?", "options": ["A) for loop", "B) while loop", "C) if-else", "D) do-while loop"], "answer": "D"},
        {"question": "What is the correct way to access a dictionary value?", "options": ["A) dict[key]", "B) dict.value", "C) dict->key", "D) dict.get"], "answer": "A"}
    ]
    
    random.shuffle(quiz_data)  # Shuffle questions for randomness
    score = 0
    
    for i, data in enumerate(quiz_data):
        print(f"\nQ{i+1}: {data['question']}")
        for option in data['options']:
            print(option)
        
        answer = input("Your answer (A/B/C/D): ").upper()
        if answer == data['answer']:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Wrong! The correct answer was: {data['answer']}")
    
    print(f"\nGame Over! You scored {score}/{len(quiz_data)}.")
    if score == len(quiz_data):
        print("🎉 Excellent! You got all correct!")
    elif score >= len(quiz_data) // 2:
        print("😊 Good job! Keep practicing.")
    else:
        print("📚 Try again and improve!")



quiz_game()  
